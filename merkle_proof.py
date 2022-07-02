from utils import *
import math
from node import Node


def merkle_proof(tx, merkle_tree) -> list:
    """Given a tx and a Merkle tree object, retrieve its list of tx's and
    parse through it to arrive at the minimum amount of information required
    to arrive at the correct block header. This does not include the tx
    itself.

    Return this data as a list; remember that order matters!
    """
    merkel_proof: list = []
    transactions: list = merkle_tree.leaves
    if len(transactions) < 2:
        return merkel_proof

    while len(transactions) > 2:
        tx_index = transactions.index(tx)
        half_size = int(len(transactions) / 2)
        # tx on left size
        if tx_index < half_size:
            top_hash = concat_and_hash_list(transactions[half_size:])
            transactions = transactions[:half_size]  # keep left half of the tree
            direction = "r"
        # tx on right size
        else:
            top_hash = concat_and_hash_list(transactions[:half_size])
            transactions = transactions[half_size:]  # keep right half of the tree
            direction = "l"
        # add hash
        merkel_proof.append(Node(direction, top_hash))

    # add sibling hash
    tx_index = transactions.index(tx)
    if tx_index == 0:
        merkel_proof.append(Node("r", transactions[1]))
    else:
        merkel_proof.append(Node("l", transactions[0]))

    return merkel_proof


def verify_proof(tx, merkle_proof):
    """Given a Merkle proof - constructed via `merkle_proof(...)` - verify
    that the correct block header can be retrieved by properly hashing the tx
    along with every other piece of data in the proof in the correct order
    """
    current_hash = tx
    while len(merkle_proof):
        next_hash = merkle_proof.pop()
        if next_hash.direction == "l":
            current_hash = concat_and_hash_list([next_hash.tx, current_hash])
        else:
            current_hash = concat_and_hash_list([current_hash, next_hash.tx])

    return current_hash
