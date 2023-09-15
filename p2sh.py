# Imports
import util
from test_framework.address import program_to_witness, script_to_p2sh, script_to_p2sh_hash
from test_framework.key import generate_key_pair, generate_bip340_key_pair, generate_schnorr_nonce
from test_framework.messages import CTxInWitness, sha256
from test_framework.musig import aggregate_musig_signatures, aggregate_schnorr_nonces, generate_musig_key, sign_musig
from test_framework.script import *

OP_dict = {
    1: OP_1,
    2: OP_2,
    3: OP_3,
    4: OP_4,
    5: OP_5,
    6: OP_6,
    7: OP_7,
    8: OP_8,
    9: OP_9,
    10: OP_10,
    11: OP_11,
    12: OP_12,
    13: OP_13,
    14: OP_14,
    15: OP_15,
    16: OP_16
}

def p2sh(logger=False):
    
    try:
        n = int(input("Please enter N: "))
        m = int(input("Please enter M: "))
        if m > 16 or n > 16 or m <= 0 or n <= 0 or m > n:
            raise Exception("Invalid M and N")
    except Exception as e:
        raise Exception("Invalid M and N")

    try:
        privkeys = list()
        pubkeys = list()

        for _ in range(n):
            _privkey, _pubkey = generate_key_pair()
            privkeys.append(_privkey)
            pubkeys.append(_pubkey)

        print(f"\nFollowing are the generated {n} public and private keys.", end='\n\n')
        for idx, pk, privk in zip([i + 1 for i in range(n)], pubkeys, privkeys):
            print(f"Public Key {idx}: {pk}")
            print(f"Private Key {idx}: {privk}")
            #TODO: get_bytes function have bip=True as default argument which return 32 bytes
            #TODO: Specifying bip=False in get_bytes return 33 bytes size (1 byte + 32 bytes key)
            #TODO: Check ECPub key class, get_bytes implementation at line number 316
            print(f"Size of Public Key {idx} is: {len(pk.get_bytes())} bytes", end='\n\n')

        
        # Create the spending script
        redeem_script = [CScriptOp(OP_dict[m])]
        for idx in range(n):
            redeem_script.append(pubkeys[idx].get_bytes(bip340=False))
        redeem_script.append(OP_dict[n])
        redeem_script.append(OP_CHECKMULTISIG)

        redeem_script = CScript(redeem_script)
        #TODO: ScriptPubKey Hex

        # 20-byte hash value of the redeem script
        p2sh_address = script_to_p2sh(redeem_script)
        p2sh_address_hash = script_to_p2sh_hash(redeem_script)
        # print(f"P2SH address: {p2sh_address} ")
        # print(f"Size of the p2sh_address hash is {len(p2sh_address_hash)} bytes", end='\n\n')
        # print(f"Size of the p2sh_address is {len(bytearray(p2sh_address.encode()))} bytes", end='\n\n')
        logger.warning(f"P2SH address: {p2sh_address} ")
        logger.warning(f"Size of the p2sh_address hash is {len(p2sh_address_hash)} bytes")
        logger.warning(f"Size of the p2sh_address is {len(bytearray(p2sh_address.encode()))} bytes")
        print("\n\n")

        # Setup test node
        test = util.TestWrapper()
        test.setup()
        node = test.nodes[0]

        # Generate coins and create an output
        tx = node.generate_and_send_coins(p2sh_address)
        tx_information = node.decoderawtransaction(tx.serialize().hex())
        # print(f"Transaction Id: {tx_information['txid']}")
        logger.warning(f"Transaction Id: {tx_information['txid']}")
        print(f"Transaction size: {tx_information['size']}")
        print(f"Transaction vsize: {tx_information['vsize']}")
        print(f"Transaction Weight: {tx_information['weight']}")
        print(f"Transaction sent to: {p2sh_address}")

        print("\n\n #######  Spending Transaction  #######   \n\n")
        # Create a spending transaction
        spending_tx = test.create_spending_transaction(tx.hash)
        sighash = LegacySignatureHash(script=redeem_script,
                        txTo=spending_tx,
                        inIdx=0,
                        hashtype=SIGHASH_ALL)

        print("Please specify the order in which you would like to apply the M private keys.")
        print("Application will prompt for M times. Each time, pass the key number out of [1, 2, ... M] and press Enter.", end='\n\n')
        priority_order = list()
        correct = True
        for i in range(m):
            order = int(input(f"Please enter private Key number {i + 1}: "))
            if order > n or (order - 1) in priority_order or order <= 0:
                correct = False
                continue
            priority_order.append(order - 1)

        if len(priority_order) != m or not correct:
            raise Exception("Incorrect or duplicate key added")
        priority_order.sort()
        
        sigs = [privkeys[i].sign_ecdsa(sighash[0]) + chr(SIGHASH_ALL).encode('latin-1') for i in priority_order]

        scriptSig = [OP_0]
        for sig in sigs:
            scriptSig.append(sig)
        scriptSig.append(redeem_script)
        spending_tx.vin[0].scriptSig = CScript(scriptSig)

        tx_information = node.decoderawtransaction(spending_tx.serialize().hex())
        # print(f"Spending Transaction Id: {tx_information['txid']}")
        logger.warning(f"Spending Transaction Id: {tx_information['txid']}")
        print(f"Spending Transaction size: {tx_information['size']}")
        print(f"Spending Transaction vsize: {tx_information['vsize']}")
        print(f"Spending Transaction Weight: {tx_information['weight']}", end='\n\n')

        # Test mempool acceptance
        test_status = node.test_transaction(spending_tx)
        # print(f"Spending Transaction acceptance status is {test_status}", end='\n\n')
        logger.warning(f"Spending Transaction acceptance status is {test_status}")
        print("")

    except Exception as e:
        raise(e)
    finally:
        test.shutdown()