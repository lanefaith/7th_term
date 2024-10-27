from block import *

class Blockchain:
    def __init__(self, block_size=2):
        self.chain = []
        self.pending_transactions = []
        self.block_size = block_size
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block()
        self.chain.append(genesis_block)

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.pending_transactions.append(transaction)
            if len(self.pending_transactions) >= self.block_size:
                self.create_block_from_pending_transactions()
        else:
            print("Invalid transaction. Must be of type Transaction.")

    def create_block_from_pending_transactions(self):
        if not self.pending_transactions:
            print("No transactions to add.")
            return

        last_block = self.chain[-1]
        new_block = Block(len(self.chain), self.pending_transactions[:self.block_size], last_block.hash)
        new_block.mine_block()
        self.chain.append(new_block)
        self.pending_transactions = self.pending_transactions[self.block_size:]

    def display_chain(self):
        chain_data = ""
        for block in self.chain:
            chain_data += f"Block {block.index}:\n"
            chain_data += f"  Timestamp: {time.ctime(block.timestamp)}\n"
            chain_data += f"  Transactions: {[tx.to_string() for tx in block.transactions]}\n"
            chain_data += f"  Merkle Root: {block.merkle_root}\n"
            chain_data += f"  Nonce: {block.nonce}\n"
            chain_data += f"  Hash: {block.hash}\n"
            chain_data += f"  Previous Hash: {block.previous_hash}\n"
            chain_data += "-" * 30 + "\n"
        return chain_data

    def mine_chain(self, difficulty=4):
        if len(self.chain) == 0:
            print("Chain is empty.")
            return

        for i in range(1, len(self.chain)):
            self.chain[i].mine_block(difficulty)
            self.update_chain_hashes(i)

    def mine_single_block(self, index, difficulty=4):
        if index < len(self.chain):
            block = self.chain[index]
            block.mine_block(difficulty)
            self.update_chain_hashes(index)

    def update_chain_hashes(self, start_index):
        for i in range(start_index, len(self.chain)):
            if i > 0:
                self.chain[i].previous_hash = self.chain[i - 1].hash
            self.chain[i].hash = self.chain[i].compute_hash()