from blockchain import *

class BlockchainApp:
    def __init__(self, root):
        self.blockchain = Blockchain()

        self.root = root
        self.root.title("Blockchain App")
        self.root.geometry("800x600")

        self.label = tk.Label(root, text="Blockchain Demo", font=("Arial", 16))
        self.label.pack(pady=10)

        self.display_button = tk.Button(root, text="Display Blockchain", command=self.display_chain)
        self.display_button.pack(pady=5)

        self.add_transaction_button = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_button.pack(pady=5)

        self.mine_button = tk.Button(root, text="Mine Blockchain", command=self.mine_blockchain)
        self.mine_button.pack(pady=5)

        self.mine_single_block_button = tk.Button(root, text="Mine Specific Block", command=self.mine_single_block)
        self.mine_single_block_button.pack(pady=5)

        self.canvas = tk.Canvas(root)
        self.scrollbar = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    def display_chain(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for block in self.blockchain.chain:
            block_frame = tk.Frame(self.scrollable_frame, borderwidth=2, relief="groove", padx=15, pady=15)
            block_frame.pack(side=tk.LEFT, padx=10, pady=10)

            block_label = tk.Label(block_frame, text=f"Block {block.index}", font=("Arial", 14, "bold"))
            block_label.pack(pady=5)

            timestamp_label = tk.Label(block_frame, text=f"Timestamp: {time.ctime(block.timestamp)}",
                                       font=("Arial", 12))
            timestamp_label.pack(pady=5)

            if block.index > 0:
                transaction_list = tk.Text(block_frame, height=5, width=60, padx=5, pady=5)
                for tx in block.transactions:
                    amount_display = tx.amount if isinstance(tx.amount, int) else int(tx.amount)
                    transaction_list.insert(tk.END,f"{tx.sender}->{tx.recipient}: {amount_display}\n")
                transaction_list.config(state=tk.DISABLED)
                transaction_list.pack(pady=5)

                for tx_index, tx in enumerate(block.transactions):
                    transaction_frame = tk.Frame(block_frame)
                    transaction_frame.pack(pady=5)

                    transaction_label = tk.Label(transaction_frame, text=f"T{tx_index + 1}:", padx=5)
                    transaction_label.pack(side=tk.LEFT)

                    transaction_entry = tk.Entry(transaction_frame, width=40)
                    transaction_entry.insert(0, "format: sender:recipient:amount")
                    transaction_entry.pack(side=tk.LEFT)

                    save_button = tk.Button(transaction_frame, text="Save", command=lambda b=block, i=tx_index, e=transaction_entry: self.save_transaction(b, i, e))
                    save_button.pack(side=tk.LEFT)

            merkle_label = tk.Label(block_frame, text=f"Merkle Root: {block.merkle_root}", font=("Arial", 12))
            merkle_label.pack(pady=5)

            nonce_label = tk.Label(block_frame, text=f"Nonce: {block.nonce}", font=("Arial", 12))
            nonce_label.pack(pady=5)

            hash_label = tk.Label(block_frame, text=f"Hash: {block.hash}", font=("Arial", 12))
            hash_label.pack(pady=5)

            previous_hash_label = tk.Label(block_frame, text=f"Previous Hash: {block.previous_hash}", font=("Arial", 12))
            previous_hash_label.pack(pady=5)

    def save_transaction(self, block, tx_index, entry):
        new_transaction_string = entry.get()
        try:
            sender, recipient, amount = new_transaction_string.split(":")
            amount = float(amount.split()[0])

            amount_display = amount if isinstance(amount, int) else int(amount)
            new_transaction = Transaction(sender=sender, recipient=recipient, amount=amount_display)

            block.transactions[tx_index] = new_transaction

            block.merkle_root = block.compute_merkle_root()
            block.hash = block.compute_hash()

            self.blockchain.update_chain_hashes(block.index + 1)

            self.display_chain()
        except ValueError:
            print("Invalid transaction format. Please use 'sender:recipient:amount' format.")
            messagebox.showerror("Error", "Invalid transaction format. Please use 'sender:recipient:amount' format.")

    def add_transaction(self):
        sender = simpledialog.askstring("Input", "Enter sender's name:")
        recipient = simpledialog.askstring("Input", "Enter recipient's name:")
        amount = simpledialog.askinteger("Input", "Enter amount:")
        transaction = Transaction(sender=sender, recipient=recipient, amount=amount)
        self.blockchain.add_transaction(transaction)

    def mine_blockchain(self):
        self.blockchain.mine_chain()
        self.display_chain()

    def mine_single_block(self):
        block_index = int(simpledialog.askinteger("Input", "Enter block index to mine:"))
        self.blockchain.mine_single_block(block_index)
        self.display_chain()