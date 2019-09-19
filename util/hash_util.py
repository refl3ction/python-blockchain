import hashlib
import json


# Exports only the functions below, not hashlib or json
__all__ = ['hash_string', 'hash_block']


def hash_string(string):
    return hashlib.sha256(string).hexdigest()


def hash_block(block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block to be hashed.
    """
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict()
                                      for tx in hashable_block['transactions']]
    return hash_string(json.dumps(hashable_block, sort_keys=True).encode())
