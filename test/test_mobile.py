# -*- coding: UTF-8 -*-
#/**
# * Software Name : pycrate
# * Version : 0.4
# *
# * Copyright 2016. Benoit Michau. ANSSI.
# *
# * This library is free software; you can redistribute it and/or
# * modify it under the terms of the GNU Lesser General Public
# * License as published by the Free Software Foundation; either
# * version 2.1 of the License, or (at your option) any later version.
# *
# * This library is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# * Lesser General Public License for more details.
# *
# * You should have received a copy of the GNU Lesser General Public
# * License along with this library; if not, write to the Free Software
# * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# * MA 02110-1301  USA
# *
# *--------------------------------------------------------
# * File Name : test/test_mobile.py
# * Created : 2016-04-28
# * Authors : Benoit Michau 
# *--------------------------------------------------------
#*/

from timeit import timeit

#from pycrate_core.elt           import Element
#Element._SAFE_STAT = False
#Element._SAFE_DYN  = False

from pycrate_mobile.GSMTAP      import *
from pycrate_mobile.NAS         import *
from pycrate_mobile.SIGTRAN     import *
from pycrate_mobile.SCCP        import *

from pycrate_core.elt           import _with_json


# uplink messages
nas_pdu_mo = tuple(map(unhexlify, (
    # CS domain
    '05080200f11040005705f44c6a94c033035758a6', # MM LU Request
    '052401035758a605f4345b7129c2', # MM CM Service Request
    '0514a3c729e021042a92f637', # MM Auth Response
    '034504066004020005815e068160000000001502010040080402600400021f00', # CC Setup
    '8381', # CC Alert
    '834804066004020005811502010040080402600400021f00', # CC Call Confirmed
    '83c7', # CC Connect
    '03cf', # CC Connect Ack
    '036502e090', # CC Disconnect
    '032d', # CC Release
    '03aa', # CC Release Complete
    '8904', # SMS CP-ACK
    '890106020141020000', # SMS RP-ACK
    '19011c00020007913386094000f01001840a816000000000000004d4f29c0e', # SMS SUBMIT
    '0b7b1c14a11202010002013b300a04010f0405a3986c36027f0100', # SS Register
    '0bfa12a210020180300b02013c300604010f040131', # SS Facility
    '0baa', ## SS Release Complete
    # PS domain
    '080103e5e004010a0005f4fffa01f700f1104000100c0a53432b259ef989004000081705', # GMM Attach Request
    '0803', # GMM Attach Complete
    '08086002f8108003c81c1a53432b259ef9890040009dd9c633120080013a332c66240100026019e6e82017051805f4c2c85e9a3103e5e034320220005804e060c0401a05f4c3e0732f1b0602f8107500015d0100', # GMM RAU Request
    '081300224b1e647b290457a2f017', # GMM Auth Cipher Response
    '080a', # GMM RAU Complete
    '080c2605f4f1c8e8bf32022000', # GMM Service Request
    '8a49', # SM Modify PDP Ctxt Accept
    # EPS domain
    '17D2EBA20A020741020BF602F8107500E0C301732F04E060C04000240202D011D1271D8080211001000010810600000000830600000000000D00000A000010005C0A003103E5E0341302F810040511035758A65D0100C1', # EMM Attach Request
    '170d22f6f1030756080900000000000000', # EMM Ident Response
    '17450740e3040753083ec3a476f829b414', # EMM Auth Response
    '075e23093395684292874145f0', # EMM SMCompl
    '0202da2807066f72616e6765', # ESM Info Resp
    '074300035200c2', # EMM Attach Complete
    '0748610bf602f8108003c8c2e65e9a5804e060c0405202f810c4c25c0a00570220003103e5e0341302f810040511035758a65d0100c1', # EMM TAU Request
    'c7060500', # EMM Serv Request
    '074c6005f4c2e65e9a57022000', # EMM Ext Serv Request
    '074a', # EMM TAU Complete
    '07632009011d00010007913386094000f01101830a816000000000000005d4f29cae00', # EMM NAS transport + SMS CP-DATA
    '0745630bf602f8108003c8c2e65e9a' # EMM Detach Request MO
    )))

# downlink messages
nas_pdu_mt = tuple(map(unhexlify, (
    # CS domain
    '051201f6e3c095753f23a9194291c86395f4782010a322f1689dc5000030dcb7d5eaafafe3', # MM Auth Request
    '0521', # MM CM Service Accept
    '050202f8100404', # MM LU Accept
    '83011e02e2a0', # CC Alert
    '8302', # CC Call Proceeding
    '83071e02e281', # CC Connect
    '030f', # CC Connect Ack
    '832502e090', # CC Disconnect
    '830302e2a0', # CC Progress
    '832d0802e090', # CC Release
    '032a0802e090', # CC Release Complete
    '03050401a05c0811833306000000f0', # CC Setup
    '090123010107913386094000f00017040b913306000000f000007101911172758004d4f29c0e', # SMS DELIVER
    '0904', # SMS CP-ACK
    '9901020302', # SMS RP-ACK
    '8b3a97a1819402018002013c30818b04010f048185c13a28867bc5602d180c0d8329866ff7fcdd6e17403a500c3d83b561b5b9c2181ed3ebf202885d06c164af584ca118a2dfe9797a3e2feb413a45ac472cd3c36936685e4fdbd3a0f1db3d7f2b64bde6db0d2acfe1e1715931ebc58e6fd00a1486c3cbecf96bda9c82d26cb60b14a381d4f239885c86d7d37350751a7c0dc3ee30390c92e58a', # SS Facility
    '8b3a9fa1819c02018102013c30819304010f04818dc4023d9c6683c86590fd4d979741f37ada9e068ddfeef91b047fd7e5209d22d60bc2e165f65c21eb4d9bd357b33955cc7a4937bd2c7797e9a0f65b9c669715b45e959e66a7e7653dc8fea6cbcba0b7d92c2f83c6ef76bb0c2abb414679d83d2e83c865783d3d07b14fc5bafc0d2f2b5aad96e25907e914b05ef3ed0695e7f0f0b8ac68b55a0a5c4f5aa6bfeb72', # SS Facility
    # PS domain
    '0802095e0102f8100405011805f4ffc856602a012c3801e0', # GMM Attach Accept
    '08120000211f12d433eac66f821ce2dfaf54c2c43b802810ac537cb6940c00006a1ec8ee4e0c7c8e', # GMM Auth Cipher Request
    '08214308804f79d87d2e838c4508804f79d87d2e838c4771019190727480490101', # GMM Information
    '081503', # GMM Ident Request
    '0809805e02f8100404011805f4d4cbf2852a012c320220003801e0', # GMM RAU Accept
    '0a4804030e1c921f7396d2fe7343ffff006400340101', # SM Modify PDP Ctxt Request
    # EPS domain
    '075501', # EMM Ident Request
    '075206905ADA1E7DA557ADA1E72650E21EE5E3104BFB73F6B4558000B1903AB88A27237F', # EMM Auth Request
    '37E8A14BCF00075D220605E060C04070C1', # EMM SMCmd
    '27807D6AA1016B8354', # EMM encrypted
    '0202d9', # ESM Info Req
    '07614308004f79d87d2e838c4508004f79d87d2e838c4771019190616180490101', # EMM Info
    '07420249062302f810c4c000725202c101081a066f72616e6765066d6e63303031066d6363323038046770727305010a7456415d010030101c911f7396fefe734bffff00fa00fa003203843401005e06fefedddd1010272780000d04c0a80a6e80210a0300000a8106c0a80a6e80210a0400000a83060000000000100205dc500bf602f8108003c8c2e65e9a1302f81004055949640103f05e0106', # EMM Attach Accept
    '0749015a4954062202f810c4a0570220001302f81004045949640103f05e0106', # EMM TAU Accept
    '0762028904', # EMM NAS transport + SMS CP-ACK
    '0746' # EMM Detach Accept
    )))

# SIGTRAN messages
sigtran_pdu = tuple(map(unhexlify, (
    '01000701000000d4000600080000000c011500080000000101020018000200008002000800000001800300080000000101160008000000010101000800000001011300080000000101140008000000010013000800000001011700080000000c010b0072626a4804000000106c62a16002010102012e3058840791198996909949820791198996000033044411330a8189961083993100a73ee8329bfd6681e8e8f41c949e83d4f5391d1406b1dfee73590ea297e774d03d4d4783e2f534bd0c0a83cce53be8fe9693e7a0b41b94a60300000000',
    '01000101000000740210006a0000012d000001360302000a0100003502020604c336018e0f4b001340470000060003400100000f40060062f2570001003a40080062f25700010001001040151405081162f25700013005f412f000003303301821004f40033500000056400562f2570001000000'
    )))

# SCCP messages
sccp_pdu = tuple(map(unhexlify, (
    '09810305090242c804430a00981e651c480206f7490213b86c12a1100201020201183008800107a403800101', # SCCP Camel (wireshark)
    '090103070904430a00980242c81464124902ec0f6c0ca10a02010402011604028490',
    '090003050902420e04434324077ee27cc70461060390e874e972cf0101d102092ff26995033940018805011890002789048d2ad4fe8107394001011c30009f6204000000009f7b020c719f21021004840a0100210b403480000102820201049f5d090000210a33135009279f50090200210a33135009279f82170124bf82180c9f8215037d7b1f9f8219010f', # SCCP ANSI TCAP (wireshark)
    '090003050702c20102c20105018e560400', # SCCP SCMG (cloudshark)
    '090003070b04435604010443430a0105018e430a00'
    )))


def test_nas_mo(nas_pdu=nas_pdu_mo):
    for pdu in nas_pdu:
        m, e = parse_NAS_MO(pdu)
        assert( e == 0 )
        v = m.get_val()
        m.reautomate()
        assert( m.get_val() == v )
        m.set_val(v)
        assert( m.to_bytes() == pdu )
        #
        if _with_json:
            t = m.to_json()
            m.from_json(t)
            assert( m.get_val() == v )


def test_nas_mt(nas_pdu=nas_pdu_mt):
    for pdu in nas_pdu:
        m, e = parse_NAS_MT(pdu)
        assert( e == 0 )
        v = m.get_val()
        m.reautomate()
        assert( m.get_val() == v )
        m.set_val(v)
        assert( m.to_bytes() == pdu )
        #
        if _with_json:
            t = m.to_json()
            m.from_json(t)
            assert( m.get_val() == v )


def test_sigtran(sigtran_pdu=sigtran_pdu):
    for pdu in sigtran_pdu:
        S = SIGTRAN()
        S.from_bytes(pdu)
        v = S.get_val()
        S.reautomate()
        assert( S.get_val() == v )
        S.__init__()
        S.set_val(v)
        assert( S.to_bytes() == pdu )
        #
        if _with_json:
            t = S.to_json()
            S.from_json(t)
            assert( S.get_val() == v )


def test_sccp(sccp_pdu=sccp_pdu):
    for pdu in sccp_pdu:
        m, e = parse_SCCP(pdu)
        assert( e == 0 )
        v = m.get_val()
        m.reautomate()
        assert( m.get_val() == v )
        m.set_val(v)
        assert( m.to_bytes() == pdu)
        #
        if _with_json:
            t = m.to_json()
            m.from_json(t)
            assert( m.get_val() == v )


def test_perf_mobile():
    
    print('[+] NAS MO decoding and re-encoding')
    Ta = timeit(test_nas_mo, number=14)
    print('test_nas_mo: {0:.4f}'.format(Ta))
    
    print('[+] NAS MT decoding and re-encoding')
    Tb = timeit(test_nas_mt, number=24)
    print('test_nas_mt: {0:.4f}'.format(Tb))
    
    print('[+] SIGTRAN decoding and re-encoding')
    Tc = timeit(test_sigtran, number=300)
    print('test_sigtran: {0:.4f}'.format(Tc))
    
    print('[+] SCCP decoding and re-encoding')
    Td = timeit(test_sccp, number=100)
    print('test_sccp: {0:.4f}'.format(Td))
    
    print('[+] test_mobile total time: {0:.4f}'.format(Ta+Tb+Tc+Td))


if __name__ == '__main__':
    test_perf_mobile()

