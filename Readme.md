# CS216: Bitcoin Transaction Lab – Python Implementation

## Team Members
*   **Devanshu Dubey** (240001024)
*   **Pratyush Gupta** (240001054)
*   **Abhinav Patel** (240001004)
*   **Abhay Lodhi** (240001003)

---

## Project Overview
This project implements the workflow for the **CS216 Bitcoin Transaction Lab**. It demonstrates the creation, signing, and broadcasting of transactions using two different Bitcoin address formats:
1.  **Legacy (P2PKH):** Standard Bitcoin addresses.
2.  **SegWit (P2SH-P2WPKH):** Modern, fee-efficient addresses that use Segregated Witness data.

The implementation interacts with a local `bitcoind` node in **regtest mode** using JSON-RPC via the `python-bitcoinrpc` library.

---

## Features
*   **Automated Setup:** Creates a local wallet and mines 101 blocks to provide spendable funds.
*   **UTXO Management:** Automatically identifies and spends specific Unspent Transaction Outputs (UTXOs).
*   **Raw Transaction Construction:** Manually builds transaction inputs and outputs using `createrawtransaction`.
*   **Script Analysis:** Decodes transactions to analyze `scriptPubKey`, `scriptSig`, and `txinwitness` structures.
*   **Size Comparison:** Outputs performance metrics (Size, vSize, Weight) to demonstrate SegWit efficiency.

---

## Project Structure
*   `setup_and_fund.py`: Initializes the environment, creates the `lab_wallet`, and mines blocks.
*   `part1.py`: Executes the A → B → C transaction chain using **Legacy** addresses.
*   `part2.py`: Executes the A' → B' → C' transaction chain using **SegWit** addresses.
*   `Bitcoin_Transaction_Lab_Report.pdf`: The detailed technical report containing script analysis and debugger screenshots.

---

## Prerequisites
*   **Bitcoin Core:** `bitcoind` installed and configured for regtest.
*   **Python 3.10+**
*   **Dependencies:**
    ```bash
    pip install python-bitcoinrpc
    ```

---

## How to Run

### 1. Start Bitcoin Daemon
Ensure your `bitcoin.conf` has the correct `rpcuser` and `rpcpassword`. Start the node:
```bash
bitcoind -regtest -daemon
```

### 2. Setup the Environment
Run the setup script to create the wallet and generate initial BTC:
```bash
python setup_and_fund.py
```

### 3. Execute Legacy Transactions (Part 1)
```bash
python part1.py
```

### 4. Execute SegWit Transactions (Part 2)
```bash
python part2.py
```

---


### Logic Verification (btcdeb)
As documented in the attached report, we used the `btcdeb` (Bitcoin Debugger) to step through the stack execution for both transaction types. 
*   **In Part 1**, we verified the `OP_DUP` and `OP_HASH160` logic.
*   **In Part 2**, we successfully validated the P2SH wrapper hash, resulting in a `TRUE (01)` stack state.

### SegWit Efficiency
Our implementation confirms the benefits of Segregated Witness. By moving signature data to the witness field, we achieved a significant reduction in virtual size (**vSize**):
*   **Legacy Transaction:** ~191 vbytes
*   **SegWit Transaction:** ~134 vbytes

This reduction directly translates to lower miner fees and increased network throughput.

---

