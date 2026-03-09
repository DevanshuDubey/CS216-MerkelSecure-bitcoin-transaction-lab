import json
from decimal import Decimal
from bitcoinrpc.authproxy import AuthServiceProxy

# --- CONFIGURATION ---
RPC_USER = "pratyush"          
RPC_PASS = "pratyush"      
RPC_PORT = 18443
WALLET_NAME = "lab_wallet"
rpc_url = f"http://{RPC_USER}:{RPC_PASS}@127.0.0.1:{RPC_PORT}/wallet/{WALLET_NAME}"

FEE = Decimal('0.0001')

def decimal_default(obj):
    """Helper to allow json.dumps to print Decimal objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_utxo(rpc, address):
    """Helper function to find an unspent output (UTXO) for a specific address."""
    unspent = rpc.listunspent(1, 9999999, [address])
    if not unspent:
        raise Exception(f"No UTXO found for address {address}")
    return unspent[0]

def run_part2():
    rpc = AuthServiceProxy(rpc_url)
    print("========== PART 2: SEGWIT (P2SH-P2WPKH) ==========\n")

    # 1. Generate SegWit Addresses
    addr_A = rpc.getnewaddress("Label_A_Segwit", "p2sh-segwit")
    addr_B = rpc.getnewaddress("Label_B_Segwit", "p2sh-segwit")
    addr_C = rpc.getnewaddress("Label_C_Segwit", "p2sh-segwit")
    print(f"Address A': {addr_A}\nAddress B': {addr_B}\nAddress C': {addr_C}\n")

    # 2. Fund Address A'
    print("Funding Address A'...")
    rpc.sendtoaddress(addr_A, 5.0)
    rpc.generatetoaddress(1, rpc.getnewaddress()) # Mine 1 block to confirm

    # 3. Create Transaction A' -> B'
    print("Creating Raw Transaction A' -> B'...")
    utxo_A = get_utxo(rpc, addr_A)
    
    # Send exact UTXO amount minus a tiny fee
    send_amount_AB = utxo_A["amount"] - FEE
    inputs_AB = [{"txid": utxo_A["txid"], "vout": utxo_A["vout"]}]
    outputs_AB = {addr_B: send_amount_AB}
    raw_tx_AB = rpc.createrawtransaction(inputs_AB, outputs_AB)

    # Decode and extract challenge script (scriptPubKey) for B'
    decoded_raw_AB = rpc.decoderawtransaction(raw_tx_AB)
    print("\n--- Decoded Raw TX (A' -> B') ---")
    print(json.dumps(decoded_raw_AB["vout"], indent=2, default=decimal_default))

    # Sign and Broadcast A' -> B'
    signed_tx_AB = rpc.signrawtransactionwithwallet(raw_tx_AB)
    txid_AB = rpc.sendrawtransaction(signed_tx_AB["hex"])
    print(f"\nBroadcasted A' -> B'. TXID: {txid_AB}")
    rpc.generatetoaddress(1, rpc.getnewaddress()) # Mine 1 block to confirm

    # 4. Create Transaction B' -> C' using B's UTXO
    print("\nExtracting UTXO for Address B'...")
    utxo_B = get_utxo(rpc, addr_B)
    print(f"Found UTXO for B'! TXID: {utxo_B['txid']}, VOUT: {utxo_B['vout']}")

    print("Creating Raw Transaction B' -> C'...")
    # Send exact UTXO amount minus another tiny fee
    send_amount_BC = utxo_B["amount"] - FEE
    inputs_BC = [{"txid": utxo_B["txid"], "vout": utxo_B["vout"]}]
    outputs_BC = {addr_C: send_amount_BC}
    raw_tx_BC = rpc.createrawtransaction(inputs_BC, outputs_BC)

    # Sign and Broadcast B' -> C'
    signed_tx_BC = rpc.signrawtransactionwithwallet(raw_tx_BC)
    txid_BC = rpc.sendrawtransaction(signed_tx_BC["hex"])
    print(f"Broadcasted B' -> C'. TXID: {txid_BC}")
    rpc.generatetoaddress(1, rpc.getnewaddress()) # Mine 1 block to confirm

    # 5. Decode signed TX B'->C' to analyze the response (Witness data)
    decoded_signed_BC = rpc.decoderawtransaction(signed_tx_BC["hex"])
    print("\n--- Decoded Signed TX (B' -> C') showing txinwitness ---")
    print(json.dumps(decoded_signed_BC["vin"], indent=2, default=decimal_default))
    
    # 6. Output size metrics for Report Comparison
    print("\n--- Size Comparison Metrics ---")
    print(f"Size:   {decoded_signed_BC['size']} bytes")
    print(f"vSize:  {decoded_signed_BC['vsize']} vbytes")
    print(f"Weight: {decoded_signed_BC['weight']}")

if __name__ == "__main__":
    run_part2()