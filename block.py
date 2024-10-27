from transaction import *

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.merkle_root = self.compute_merkle_root()
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.nonce}{self.merkle_root}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=4):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

    @staticmethod
    def hash_transaction(transaction):
        return hashlib.sha256(transaction.to_string().encode()).hexdigest()

    def compute_merkle_root(self):
        if not self.transactions:
            return "0"

        transaction_hashes = [self.hash_transaction(tx) for tx in self.transactions]

        while len(transaction_hashes) > 1:
            temp_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                if i + 1 < len(transaction_hashes):
                    combined_hash = transaction_hashes[i] + transaction_hashes[i + 1]
                else:
                    combined_hash = transaction_hashes[i] + transaction_hashes[i]
                temp_hashes.append(hashlib.sha256(combined_hash.encode()).hexdigest())
            transaction_hashes = temp_hashes

        return transaction_hashes[0]