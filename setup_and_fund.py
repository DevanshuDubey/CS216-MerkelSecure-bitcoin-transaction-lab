from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

RPC_USER = "pratyush"
RPC_PASS = "pratyush"
RPC_PORT = 18443
WALLET_NAME = "lab_wallet"
rpc_url = f"http://{RPC_USER}:{RPC_PASS}@127.0.0.1:{RPC_PORT}"

def setup():
    rpc = AuthServiceProxy(rpc_url)
    print("Connecting to bitcoind...")

    try:
        loaded_wallets = rpc.listwallets()
        
        if WALLET_NAME in loaded_wallets:
            print(f"Wallet '{WALLET_NAME}' is already loaded in memory.")
        else:
            try:
                print(f"Attempting to load wallet '{WALLET_NAME}' from disk...")
                rpc.loadwallet(WALLET_NAME)
                print(f"Wallet '{WALLET_NAME}' loaded successfully.")
            except JSONRPCException as e:
                if "does not exist" in str(e) or "not found" in str(e):
                    print(f"Wallet '{WALLET_NAME}' not found. Creating a new one...")
                    rpc.createwallet(WALLET_NAME)
                    print(f"Wallet '{WALLET_NAME}' created.")
                else:
                    raise e
    except JSONRPCException as e:
        raise Exception(f"Wallet setup failed: {e}")

    wallet_rpc_url = f"{rpc_url}/wallet/{WALLET_NAME}"
    rpc_wallet = AuthServiceProxy(wallet_rpc_url)

    print("Mining 101 blocks to mature the coinbase reward (this takes a moment)...")
    miner_address = rpc_wallet.getnewaddress("miner", "bech32")
    rpc_wallet.generatetoaddress(101, miner_address)
    
    balance = rpc_wallet.getbalance()
    print(f"\nSetup complete! Current Wallet Balance: {balance} BTC")

if __name__ == "__main__":
    setup()