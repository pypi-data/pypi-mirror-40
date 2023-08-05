#!/usr/bin/python
"""
    Parts of this source file are derived from code from Electrum
    (https://github.com/spesmilo/electrum), as of December 9, 2015.

    These parts are (c) 2015 by Thomas Voegtlin.  All changes are
    subject to the following copyright.
"""
"""
    Virtualchain
    ~~~~~
    copyright: (c) 2014-2015 by Halfmoon Labs, Inc.
    copyright: (c) 2016 by Blockstack.org

    This file is part of Virtualchain

    Virtualchain is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Virtualchain is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Virtualchain. If not, see <http://www.gnu.org/licenses/>.
"""


import socket
import os
import sys
import time
import logging

import protocoin
import protocoin.exceptions
from protocoin.clients import *
from protocoin.serializers import *
from protocoin.fields import *
from protocoin.exceptions import *

from keys import version_byte as VERSION_BYTE

import bits

from ....lib import hashing

DEBUG = True

try:
    from ....lib.config import get_logger
except:
    def get_logger(name=None):
        """
        Get virtualchain's logger
        """

        level = logging.CRITICAL
        if DEBUG:
            logging.disable(logging.NOTSET)
            level = logging.DEBUG

        if name is None:
            name = "<unknown>"
            level = logging.CRITICAL

        log = logging.getLogger(name=name)
        log.setLevel( level )
        console = logging.StreamHandler()
        console.setLevel( level )
        log_format = ('[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d] (' + str(os.getpid()) + ') %(message)s' if DEBUG else '%(message)s')
        formatter = logging.Formatter( log_format )
        console.setFormatter(formatter)
        log.propagate = False

        if len(log.handlers) > 0:
            for i in xrange(0, len(log.handlers)):
                log.handlers.pop(0)
        
        log.addHandler(console)
        return log


log = get_logger("virtualchain-bitcoin-spv")

BLOCK_HEADER_SIZE = 81

GENESIS_BLOCK_HASH = None
GENESIS_BLOCK_MERKLE_ROOT = None
USE_MAINNET = False
USE_TESTNET = False

GENESIS_BLOCK_HASH_MAINNET = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
GENESIS_BLOCK_MERKLE_ROOT_MAINNET = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"

GENESIS_BLOCK_HASH_TESTNET = "0f9188f13cb7b2c71f2a335e3a4fc328bf5beb436012afca590b1a11466e2206"
GENESIS_BLOCK_MERKLE_ROOT_TESTNET = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"

if VERSION_BYTE == 0:
    # mainnet
    log.debug("Using mainnet")
    USE_MAINNET = True
    GENESIS_BLOCK_HASH = GENESIS_BLOCK_HASH_MAINNET
    GENESIS_BLOCK_MERKLE_ROOT = GENESIS_BLOCK_MERKLE_ROOT_MAINNET

elif VERSION_BYTE == 111:
    # testnet
    log.debug("Using testnet/regtest")
    USE_TESTNET = True
    GENESIS_BLOCK_HASH = GENESIS_BLOCK_HASH_TESTNET
    GENESIS_BLOCK_MERKLE_ROOT = GENESIS_BLOCK_HASH_TESTNET
else:
    raise Exception("Unknown version byte %s" % VERSION_BYTE)

BLOCK_DIFFICULTY_CHUNK_SIZE = 2016
BLOCK_DIFFICULTY_INTERVAL = 14*24*60*60  # two weeks, in seconds


class BlockHash(SerializableMessage):
    """
    Block hash to request
    """
    def __init__(self):
        self.block_hash = None 

    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, "%064x" % self.block_hash)


class GetHeaders(SerializableMessage):
    """
    getheaders message
    """
    command = "getheaders"

    def __init__(self):
        self.version = PROTOCOL_VERSION
        self.block_hashes = []
        self.hash_stop = 0

    def add_block_hash( self, block_hash ):
        """
        Append up to 2000 block hashes for which to get headers.
        """
        if len(self.block_hashes) > 2000:
            raise Exception("A getheaders request cannot have over 2000 block hashes")

        hash_num = int("0x" + block_hash, 16)
        
        bh = BlockHash()
        bh.block_hash = hash_num

        self.block_hashes.append( bh )
        self.hash_stop = hash_num

    def num_block_hashes( self ):
        """
        Get the number of block headers to request
        """
        return len(self.block_hashes)

    def __repr__(self):
        return "<%s block_hashes=[%s]>" % (self.__class__.__name__, ",".join([str(h) for h in self.block_hashes]))


class BlockHashSerializer( Serializer ):
    """
    Serialization class for a BlockHash
    """
    model_class = BlockHash
    block_hash = Hash()


class GetHeadersSerializer( Serializer ):
    """
    Serialization class for a GetHeaders
    """
    model_class = GetHeaders
    version = UInt32LEField()
    block_hashes = ListField(BlockHashSerializer)
    hash_stop = Hash()


# monkey-patch
protocoin.serializers.MESSAGE_MAPPING['getheaders'] = GetHeadersSerializer


class BlockHeaderClient( BitcoinBasicClient ):
    """
    Client to fetch and store block headers.
    """

    coin = None

    def __init__(self, socket, headers_path, first_block_hash, last_block_id ):

        if VERSION_BYTE == 0:
            self.coin = "bitcoin"
        else:
            self.coin = "bitcoin_testnet"

        super(BlockHeaderClient, self).__init__(socket)
        self.path = headers_path
        self.last_block_id = last_block_id
        self.finished = False
        self.verack = False
        self.first_block_hash = first_block_hash

    
    def loop_exit( self ):
        """
        Stop the loop
        """
        self.finished = True
        self.close_stream()


    def run( self ):
        """
        Interact with the blockchain peer,
        until we get a socket error or we
        exit the loop explicitly.
        Return True on success
        Raise on error
        """

        self.handshake()

        try:
            self.loop()
        except socket.error, se:
            if self.finished:
                return True
            else:
                raise


    def hash_to_string( self, hash_int ):
        return "%064x" % hash_int 


    def handle_headers( self, message_header, block_headers_message ):
        """
        Handle a 'headers' message.
        NOTE: we request headers in order, so we will expect to receive them in order here.
        Verify that we do so.
        """
        log.debug("handle headers (%s)" % len(block_headers_message.headers))

        block_headers = block_headers_message.headers

        serializer = BlockHeaderSerializer()

        # verify that the local header chain connects to this sequence
        current_height = SPVClient.height( self.path )
        if current_height is None:
            assert USE_TESTNET
            current_height = -1

        assert (current_height >= 0 and USE_MAINNET) or USE_TESTNET, "Invalid height %s" % current_height
    
        last_header = None

        if current_height >= 0:
            last_header = SPVClient.read_header( self.path, current_height )
            log.debug("Receive %s headers (%s to %s)" % (len(block_headers), current_height, current_height + len(block_headers)))

        else:
            # first testnet header
            log.debug("Receive %s testnet headers (%s to %s)" % (len(block_headers), current_height + 1, current_height + len(block_headers)))
            last_header = {
                "version": block_headers[0].version,
                "prev_block_hash": "%064x" % block_headers[0].prev_block,
                "merkle_root": "%064x" % block_headers[0].merkle_root,
                "timestamp": block_headers[0].timestamp,
                "bits": block_headers[0].bits,
                "nonce": block_headers[0].nonce,
                "hash": block_headers[0].calculate_hash()
            }

        if (USE_MAINNET or (USE_TESTNET and current_height >= 0)) and last_header['hash'] != self.hash_to_string(block_headers[0].prev_block):
            raise Exception("Received discontinuous block header at height %s: hash '%s' (expected '%s')" % \
                    (current_height,
                    self.hash_to_string(block_headers[0].prev_block),
                    last_header['hash'] ))

        header_start = 1
        if USE_TESTNET and current_height < 0:
            # save initial header
            header_start = 0

        # verify that this sequence of headers constitutes a hash chain 
        for i in xrange(header_start, len(block_headers)):
            prev_block_hash = self.hash_to_string(block_headers[i].prev_block)
            if i > 0 and prev_block_hash != block_headers[i-1].calculate_hash():
                raise Exception("Block '%s' is not continuous with block '%s'" % \
                        prev_block_hash,
                        block_headers[i-1].calculate_hash())

        if current_height < 0:
            # save the first header 
            if not os.path.exists(self.path):
                with open(self.path, "wb") as f:
                    block_header_serializer = BlockHeaderSerializer()
                    bin_data = block_header_serializer.serialize( block_headers[0] )
                    f.write( bin_data )

            # got all headers, including the first
            current_height = 0

        # insert into to local headers database
        next_block_id = current_height + 1
        for block_header in block_headers:
            with open(self.path, "rb+") as f:

                # omit tx count 
                block_header.txns_count = 0
                bin_data = serializer.serialize( block_header )

                if len(bin_data) != BLOCK_HEADER_SIZE:
                    raise Exception("Block %s (%s) has %s-byte header" % (next_block_id, block_header.calculate_hash(), len(bin_data)))

                # NOTE: the fact that we use seek + write ensures that we can:
                # * restart synchronizing at any point
                # * allow multiple processes to work on the chain safely (even if they're duplicating effort)
                f.seek( BLOCK_HEADER_SIZE * next_block_id, os.SEEK_SET )
                f.write( bin_data )

                if SPVClient.height( self.path ) >= self.last_block_id - 1:
                    break

                next_block_id += 1
            
        current_block_id = SPVClient.height( self.path )
        if current_block_id >= self.last_block_id - 1:
            # got all headers
            self.loop_exit()
            return

        prev_block_header = SPVClient.read_header( self.path, current_block_id )
        prev_block_hash = prev_block_header['hash']
        self.send_getheaders( prev_block_hash )

    
    def send_getheaders( self, prev_block_hash ):
        """
        Request block headers from a particular block hash.
        Will receive up to 2000 blocks, starting with the block *after*
        the given block hash (prev_block_hash)
        """

        getheaders = GetHeaders()

        getheaders.add_block_hash( prev_block_hash )

        log.debug("send getheaders")
        self.send_message( getheaders )


    def handshake(self):
        """
        This method will implement the handshake of the
        Bitcoin protocol. It will send the Version message,
        and block until it receives a VerAck
        """
        log.debug("handshake (version %s)" % PROTOCOL_VERSION)
        version = Version()
        version.services = 0    # can't send blocks
        log.debug("send Version")
        self.send_message(version)


    def handle_version(self, message_header, message):
        """
        This method will handle the Version message and
        will send a VerAck message when it receives the
        Version message.

        :param message_header: The Version message header
        :param message: The Version message
        """
        log.debug("handle version")
        verack = VerAck()
        log.debug("send VerAck")
        self.send_message(verack)
        self.verack = True

        # begin!
        self.send_getheaders( self.first_block_hash )


    def handle_ping(self, message_header, message):
        """
        This method will handle the Ping message and then
        will answer every Ping message with a Pong message
        using the nonce received.

        :param message_header: The header of the Ping message
        :param message: The Ping message
        """
        log.debug("handle ping")
        pong = Pong()
        pong.nonce = message.nonce
        log.debug("send pong")
        self.send_message(pong)


class SPVClient(object):
    """
    Simplified Payment Verification client.
    Accesses locally-stored headers obtained by BlockHeaderClient
    to verify and synchronize them with the blockchain.
    """

    def __init__(self, path):
        SPVClient.init( path )


    @classmethod
    def init(cls, path):
        """
        Set up an SPV client.
        If the locally-stored headers do not exist, then 
        create a stub headers file with the genesis block information.
        """
        if not os.path.exists( path ):

            block_header_serializer = BlockHeaderSerializer()
            genesis_block_header = BlockHeader()

            if USE_MAINNET:
                # we know the mainnet block header
                # but we don't know the testnet/regtest block header
                genesis_block_header.version = 1
                genesis_block_header.prev_block = 0
                genesis_block_header.merkle_root = int(GENESIS_BLOCK_MERKLE_ROOT, 16 )
                genesis_block_header.timestamp = 1231006505
                genesis_block_header.bits = int( "1d00ffff", 16 )
                genesis_block_header.nonce = 2083236893
                genesis_block_header.txns_count = 0

                with open(path, "wb") as f:
                    bin_data = block_header_serializer.serialize( genesis_block_header )
                    f.write( bin_data )
            

    @classmethod
    def height(cls, path):
        """
        Get the locally-stored block height
        """
        if os.path.exists( path ):
            sb = os.stat( path )
            h = (sb.st_size / BLOCK_HEADER_SIZE) - 1
            return h
        else:
            return None


    @classmethod
    def read_header_at( cls, f):
        """
        Given an open file-like object, read a block header
        from it and return it as a dict containing:
        * version (int)
        * prev_block_hash (hex str)
        * merkle_root (hex str)
        * timestamp (int)
        * bits (int)
        * nonce (ini)
        * hash (hex str)
        """
        header_parser = BlockHeaderSerializer()
        hdr = header_parser.deserialize( f )
        h = {}
        h['version'] = hdr.version
        h['prev_block_hash'] = "%064x" % hdr.prev_block
        h['merkle_root'] = "%064x" % hdr.merkle_root
        h['timestamp'] = hdr.timestamp
        h['bits'] = hdr.bits
        h['nonce'] = hdr.nonce
        h['hash'] = hdr.calculate_hash()
        return h


    @classmethod
    def load_header_chain( cls, chain_path ):
        """
        Load the header chain from disk.
        Each chain element will be a dictionary with:
        * 
        """

        header_parser = BlockHeaderSerializer()
        chain = []
        height = 0
        with open(chain_path, "rb") as f:

            h = SPVClient.read_header_at( f )
            h['block_height'] = height 

            height += 1
            chain.append(h)

        return chain


    @classmethod
    def read_header(cls, headers_path, block_height, allow_none=False):
        """
        Get a block header at a particular height from disk.
        Return the header if found
        Return None if not.
        """
        if os.path.exists(headers_path):
    
            header_parser = BlockHeaderSerializer()
            sb = os.stat( headers_path )
            if sb.st_size < BLOCK_HEADER_SIZE * block_height:
                # beyond EOF 
                if allow_none:
                    return None 
                else:
                    raise Exception('EOF on block headers')

            with open( headers_path, "rb" ) as f:
                f.seek( block_height * BLOCK_HEADER_SIZE, os.SEEK_SET )
                hdr = SPVClient.read_header_at( f )

            return hdr
        else:
            if allow_none:
                return None
            else:
                raise Exception('No such file or directory: {}'.format(headers_path))


    @classmethod
    def get_target(cls, path, index, chain=None):
        """
        Calculate the target difficulty at a particular difficulty interval (index).
        Return (bits, target) on success
        """
        if chain is None:
            chain = []  # Do not use mutables as default values!

        max_target = 0x00000000FFFF0000000000000000000000000000000000000000000000000000
        if index == 0:
            return 0x1d00ffff, max_target

        first = SPVClient.read_header( path, (index-1)*BLOCK_DIFFICULTY_CHUNK_SIZE)
        last = SPVClient.read_header( path, index*BLOCK_DIFFICULTY_CHUNK_SIZE - 1, allow_none=True)
        if last is None:
            for h in chain:
                if h.get('block_height') == index*BLOCK_DIFFICULTY_CHUNK_SIZE - 1:
                    last = h

        nActualTimespan = last.get('timestamp') - first.get('timestamp')
        nTargetTimespan = BLOCK_DIFFICULTY_INTERVAL
        nActualTimespan = max(nActualTimespan, nTargetTimespan/4)
        nActualTimespan = min(nActualTimespan, nTargetTimespan*4)

        bits = last.get('bits')
        # convert to bignum
        MM = 256*256*256
        a = bits%MM
        if a < 0x8000:
            a *= 256
        target = (a) * pow(2, 8 * (bits/MM - 3))

        # new target
        new_target = min( max_target, (target * nActualTimespan)/nTargetTimespan )

        # convert it to bits
        c = ("%064X"%new_target)[2:]
        i = 31
        while c[0:2]=="00":
            c = c[2:]
            i -= 1

        c = int('0x'+c[0:6],16)
        if c >= 0x800000:
            c /= 256
            i += 1

        new_bits = c + MM * i
        return new_bits, new_target

   
    @classmethod 
    def block_header_verify( cls, headers_path, block_id, block_hash, block_header ):
        """
        Given the block's numeric ID, its hash, and the bitcoind-returned block_data,
        use the SPV header chain to verify the block's integrity.

        block_header must be a dict with the following structure:
        * version: protocol version (int)
        * prevhash: previous block hash (hex str)
        * merkleroot: block Merkle root (hex str)
        * timestamp: UNIX time stamp (int)
        * bits: difficulty bits (hex str)
        * nonce: PoW nonce (int)
        * hash: block hash (hex str)
        (i.e. the format that the reference bitcoind returns via JSON RPC)

        Return True on success
        Return False on error
        """
        prev_header = cls.read_header( headers_path, block_id - 1 )
        prev_hash = prev_header['hash']
        return bits.block_header_verify( block_header, prev_hash, block_hash )


    @classmethod 
    def block_verify( cls, verified_block_header, block_txids ):
        """
        Given the block's verified header structure (see block_header_verify) and
        its list of transaction IDs (as hex strings), verify that the transaction IDs are legit.

        Return True on success
        Return False on error.
        """

        block_data = {
            'merkleroot': verified_block_header['merkleroot'],
            'tx': block_txids
        }

        return bits.block_verify( block_data )


    @classmethod 
    def tx_hash( cls, tx ):
        """
        Calculate the hash of a transction structure given by bitcoind
        """
        tx_hex = bits.btc_bitcoind_tx_serialize( tx )
        tx_hash = hashing.bin_double_sha256(tx_hex.decode('hex'))[::-1].encode('hex')
        return tx_hash


    @classmethod
    def tx_verify( cls, verified_block_txids, tx ):
        """
        Given the block's verified block txids, verify that a transaction is legit.
        @tx must be a dict with the following fields:
        * locktime: int
        * version: int
        * vin: list of dicts with:
           * vout: int,
           * hash: hex str
           * sequence: int (optional)
           * scriptSig: dict with:
              * hex: hex str
        * vout: list of dicts with:
           * value: float
           * scriptPubKey: dict with:
              * hex: hex str
        """
        tx_hash = cls.tx_hash( tx )
        return tx_hash in verified_block_txids


    @classmethod 
    def tx_index( cls, verified_block_txids, verified_tx ):
        """
        Given a block's verified block txids and a verified transaction, 
        find out where it is in the list of txids (i.e. what's its index)?
        """
        tx_hash = cls.tx_hash( verified_tx )
        return verified_block_txids.index( tx_hash )


    @classmethod 
    def block_header_index( cls, path, block_header ):
        """
        Given a block's serialized header, go and find out what its
        block ID is (if it is present at all).

        Return the >= 0 index on success
        Return -1 if not found.

        NOTE: this is slow
        """
        with open( path, "rb" ) as f:
            chain_raw = f.read()

        for blk in xrange(0, len(chain_raw) / (BLOCK_HEADER_SIZE)):
            if chain_raw[blk * BLOCK_HEADER_SIZE : blk * BLOCK_HEADER_SIZE + BLOCK_HEADER_SIZE] == block_header:
                return blk

        return -1


    @classmethod
    def verify_header_chain(cls, path, chain=None):
        """
        Verify that a given chain of block headers
        has sufficient proof of work.
        """
        if chain is None:
            chain = SPVClient.load_header_chain( path )

        prev_header = chain[0]
        
        for i in xrange(1, len(chain)):
            header = chain[i]
            height = header.get('block_height')
            prev_hash = prev_header.get('hash')
            if prev_hash != header.get('prev_block_hash'):
                log.error("prev hash mismatch: %s vs %s" % (prev_hash, header.get('prev_block_hash')))
                return False

            bits, target = SPVClient.get_target( path, height/BLOCK_DIFFICULTY_CHUNK_SIZE, chain)
            if bits != header.get('bits'):
                log.error("bits mismatch: %s vs %s" % (bits, header.get('bits')))
                return False

            _hash = header.get('hash')
            if int('0x'+_hash, 16) > target:
                log.error("insufficient proof of work: %s vs target %s" % (int('0x'+_hash, 16), target))
                return False

            prev_header = header

        return True


    @classmethod
    def sync_header_chain(cls, path, bitcoind_server, last_block_id ):
        """
        Synchronize our local block headers up to the last block ID given.
        @last_block_id is *inclusive*
        @bitcoind_server is host:port or just host
        """
        current_block_id = SPVClient.height( path )
        if current_block_id is None:
            assert USE_TESTNET
            current_block_id = -1

        assert (current_block_id >= 0 and USE_MAINNET) or USE_TESTNET

        if current_block_id < last_block_id:
          
            if USE_MAINNET:
                log.debug("Synchronize %s to %s" % (current_block_id, last_block_id))
            else:
                log.debug("Synchronize testnet %s to %s" % (current_block_id + 1, last_block_id ))

            # need to sync
            if current_block_id >= 0:
                prev_block_header = SPVClient.read_header( path, current_block_id )
                prev_block_hash = prev_block_header['hash']

            else:
                # can only happen when in testnet
                prev_block_hash = GENESIS_BLOCK_HASH_TESTNET

            # connect 
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # timeout (10 min)
            sock.settimeout(600)

            bitcoind_port = 8333
            if ":" in bitcoind_server:
                p = bitcoind_server.split(":")
                bitcoind_server = p[0]
                bitcoind_port = int(p[1])

            log.debug("connect to %s:%s" % (bitcoind_server, bitcoind_port))
            sock.connect( (bitcoind_server, bitcoind_port) )

            client = BlockHeaderClient( sock, path, prev_block_hash, last_block_id )

            # get headers
            client.run()

            # verify headers
            if SPVClient.height(path) < last_block_id:
                raise Exception("Did not receive all headers up to %s (only got %s)" % (last_block_id, SPVClient.height(path)))

            # defensive: make sure it's *exactly* that many blocks 

            rc = SPVClient.verify_header_chain( path )
            if not rc:
                raise Exception("Failed to verify headers (stored in '%s')" % path)

        log.debug("synced headers from %s to %s in %s" % (current_block_id, last_block_id, path))
        return True


if __name__ == "__main__":
    # test synchonize headers 
    try:
        bitcoind_server = sys.argv[1]
        headers_path = sys.argv[2]
        height = int(sys.argv[3])
    except:
        print >> sys.stderr, "Usage: %s bitcoind_server headers_path blockchain_height" % sys.argv[0]
        sys.exit(0)

    log.setLevel(logging.DEBUG)
    SPVClient.init( headers_path )
    rc = SPVClient.sync_header_chain( headers_path, bitcoind_server, height )
    if rc:
        print "Headers are up to date with %s and seem to have sufficient proof-of-work" % height
