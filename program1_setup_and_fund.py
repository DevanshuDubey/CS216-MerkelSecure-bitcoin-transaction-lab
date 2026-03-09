from bitcoinrpc.authproxy import AuthServiceProxy
import json

rpc_user = "pratyush"
rpc_password = "pratyush"

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443")

# create/load wallet
try:
    rpc.createwallet("labwallet")
except:
    pass

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/labwallet")

print("Connected to Bitcoin node")

# generate legacy addresses
A = rpc.getnewaddress("", "legacy")
B = rpc.getnewaddress("", "legacy")
C = rpc.getnewaddress("", "legacy")

print("\nAddress A:", A)
print("Address B:", B)
print("Address C:", C)

# mine blocks
miner = rpc.getnewaddress()
rpc.generatetoaddress(101, miner)

# fund A
txid = rpc.sendtoaddress(A, 1)

print("\nFunding TXID:", txid)

rpc.generatetoaddress(1, miner)

# save addresses for next programs
data = {
    "A": A,
    "B": B,
    "C": C
}

with open("addresses.json", "w") as f:
    json.dump(data, f)

print("\nAddresses saved to addresses.json")