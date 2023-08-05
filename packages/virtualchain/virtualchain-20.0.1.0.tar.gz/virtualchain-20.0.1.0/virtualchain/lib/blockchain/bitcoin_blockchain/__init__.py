#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    along with Virtualchain.  If not, see <http://www.gnu.org/licenses/>.
"""

from .keys import BitcoinPublicKey, BitcoinPrivateKey, hex_hash160_to_address, btc_script_hex_to_address, version_byte, btc_is_multisig_script, \
        btc_make_payment_script, btc_make_data_script, btc_address_reencode, btc_is_p2sh_script, btc_is_p2sh_address, MAX_DATA_LEN

from .fees import get_tx_fee_per_byte, get_tx_fee, tx_estimate_signature_len

from .multisig import *
from .authproxy import *

from .spv import SPVClient
from .blocks import BlockchainDownloader, get_bitcoin_blockchain_height
from .bits import *
