from bitcoinrpc.authproxy import AuthServiceProxy
import json

rpc_user = "pratyush"
rpc_password = "pratyush"

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/labwallet")

# load addresses
with open("addresses.json") as f:
    data = json.load(f)

B = data["B"]
C = data["C"]

print("Address B:", B)
print("Address C:", C)

# find UTXO belonging to B
utxos = rpc.listunspent()

utxo_B = None
for u in utxos:
    if u["address"] == B:
        utxo_B = u
        break

print("\nUTXO for B:", utxo_B)

# create raw transaction
inputs = [{
    "txid": utxo_B["txid"],
    "vout": utxo_B["vout"]
}]

outputs = {
    C: 0.3,
    B : 0.1999,
}

raw_tx = rpc.createrawtransaction(inputs, outputs)

print("\nRaw Transaction B -> C:")
print(raw_tx)

# decode raw transaction
decoded = rpc.decoderawtransaction(raw_tx)

print("\nDecoded Transaction:")
print(decoded)

# sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)

# broadcast
txid_BC = rpc.sendrawtransaction(signed_tx["hex"])

print("\nTXID B -> C:", txid_BC)

# decode final transaction
final_tx = rpc.getrawtransaction(txid_BC, True)

print("\nUnlocking Script (ScriptSig):")
print(final_tx["vin"][0]["scriptSig"])