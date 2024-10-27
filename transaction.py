import hashlib
import time
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_string(self):
        return f"{self.sender}->{self.recipient}: {self.amount}"