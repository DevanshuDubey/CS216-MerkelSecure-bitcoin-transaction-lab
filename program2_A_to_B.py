from bitcoinrpc.authproxy import AuthServiceProxy
import json

rpc_user = "pratyush"
rpc_password = "pratyush"

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/labwallet")

# load addresses
with open("addresses.json") as f:
    data = json.load(f)

A = data["A"]
B = data["B"]

print("Address A:", A)
print("Address B:", B)

# find UTXO for A
utxos = rpc.listunspent()

utxo_A = None
for u in utxos:
    if u["address"] == A:
        utxo_A = u
        break

print("\nUTXO for A:", utxo_A)

# create raw transaction
inputs = [{
    "txid": utxo_A["txid"],
    "vout": utxo_A["vout"]
}]

outputs = {
    B: 0.5,
    A: 0.4999,
}

raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction A -> B:")
print(raw_tx)

# decode raw transaction
decoded = rpc.decoderawtransaction(raw_tx)

print("\nDecoded Transaction:")
print(decoded)

print("\nLocking Script (scriptPubKey):")
print(decoded["vout"][0]["scriptPubKey"])

# sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

print("\nSigned Transaction:", signed_tx)

# broadcast
txid_AB = rpc.sendrawtransaction(signed_tx["hex"])

print("\nTXID A -> B:", txid_AB)

# mine block to confirm
miner = rpc.getnewaddress()
rpc.generatetoaddress(1, miner)

# save txid for program 3
with open("txid_AB.txt", "w") as f:
    f.write(txid_AB)

print("\nTXID saved for next program")