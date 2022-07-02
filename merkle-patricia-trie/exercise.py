import rlp
from codecs import encode, decode
from ethereum import trie, utils, db

## EX1
print("Exercice 1 ... \n")

# initialize empty trie
state = trie.Trie(db.EphemDB())

# add one entry
key = utils.to_string("\x01\x01\x02")
state.update(key, rlp.encode(["hello"]))
print("Root hash: ", encode(state.root_hash, "hex"))

k, v = state.root_node
print("Root node: ", [k, v])
print("HP encoded key, in hex:", encode(k, "hex"))
print(
    "- Note the final 6 nibbles are the key we used, 010102, while the first two give us the HP encoding."
)
# The first nibble tells us that this is a terminator node (since it would be 10 in binary,
# so the second least significant bit is on),
# and since the key was even length (least significant bit is 0), we add a second 0 nibble.


primaryRoot = encode(state.root_hash, "hex")

## EX2 - A
input("\n\nExercice 2 - A... \n")

# initialize trie from previous hash; add new entry with same key.
state = trie.Trie(state.db, decode(primaryRoot, "hex"))
print("- we initialize a trie that starts with the previous hash")
print("Root hash: ", encode(state.root_hash, "hex"))
print("Root node: ", state.root_node)

print("\n")

state.update(key, rlp.encode(["hellothere"]))
print("- we add an entry with the same key we already used but a different value")
print("Root hash: ", encode(state.root_hash, "hex"))
print("Root node: ", state.root_node)
# we now have two tries, addressed in the database by their respective hashes, though they each have the same key


## EX2 - B
input("\n\nExercice 2 - B... \n")

state = trie.Trie(state.db, decode(primaryRoot, "hex"))
print(
    "- Now, let’s add an entry that use’s the same key but with a different final nibble"
)
key = utils.to_string("\x01\x01\x03")

state.update(key, rlp.encode(["hellothere"]))
print("Root hash:", encode(state.root_hash, "hex"))
k, v = state.root_node

print("Root node: " + str([k, v]))
print(
    f"- Ext. node? {state._get_node_type(state.root_node) == trie.NODE_TYPE_EXTENSION}\n"
)

print("HP encoded key, in hex:", encode(k, "hex"))


common_prefix_key, node_hash = state.root_node
print("Node hash : ", state._decode_to_node(node_hash))
print(
    "- this is a branch node with 17 entries, entires 2 and 3 contain non empty node (our two keys 010102 and 010103)"
)
print(
    f"- Branch node? {state._get_node_type(state._decode_to_node(node_hash)) == trie.NODE_TYPE_BRANCH}"
)


## EX2 - C
input("\n\nExercice 2 - C... \n")

state = trie.Trie(state.db, decode(primaryRoot, "hex"))

print("Root hash: ", encode(state.root_hash, "hex"))
print("Root node: ", state.root_node)

print("\n")
print(
    "- Let’s do it again but with a key equal to the first few nibbles of our original ke"
)
key = utils.to_string("\x01\x01")
state.update(key, rlp.encode(["hellothere"]))

print("Root hash:", encode(state.root_hash, "hex"))
print("Root node:", state.root_node)
print("new Branch node: ", state._decode_to_node(state.root_node[1]))


## EX2 - D
input("\n\nExercice 2 - D... \n")

state = trie.Trie(state.db, decode(primaryRoot, "hex"))

print("Root hash: ", encode(state.root_hash, "hex"))
print("Root node: ", state.root_node)

print("\n")

key = utils.to_string("\x01\x01\x02\x57")
state.update(key, rlp.encode(["hellothere"]))

print("Root hash:", encode(state.root_hash, "hex"))
print("Root node:", state.root_node)
print("Branch node: ", state._decode_to_node(state.root_node[1]))


## EX3
input("\n\nExercice 3 ... \n")

state = trie.Trie(state.db, decode(primaryRoot, "hex"))

print("Root hash: ", encode(state.root_hash, "hex"))
print("Root node: ", state.root_node)

print("\n")

key = utils.to_string("\x01\x01\x02\x55")
state.update(key, rlp.encode(["hellothere"]))

print("Root hash:", encode(state.root_hash, "hex"))
print("Root node:", state.root_node)
print("Branch node: ", state._decode_to_node(state.root_node[1]))

print("\n")

key = utils.to_string("\x01\x01\x02\x57")
state.update(key, rlp.encode(["jimbojones"]))

print("Root hash:", encode(state.root_hash, "hex"))
print("Root node:", state.root_node)

branch_node = state._decode_to_node(state.root_node[1])
print("Branch node: ", branch_node)

print("\n")

# Looking at hash in the previous branch node
next_hash = branch_node[5]

print("Hash stored in branch node: ", encode(next_hash, "hex"))
print("Branch node it points to: ", state._decode_to_node(next_hash))


## EX4

input("\n\nExercice 4 ... \n")

# initialize trie from previous hash; add new [key, value] where key has common prefix
state = trie.Trie(
    state.db,
    decode("b5e187f15f1a250e51a78561e29ccfc0a7f48e06d19ce02f98dd61159e81f71d", "hex"),
)
print("Using root hash from EX2 - B ...")
print(rlp.decode(state.get("\x01\x01\x02")))
print(rlp.decode(state.get("\x01\x01\x03")))


print("\n")
state = trie.Trie(
    state.db,
    decode("fcb2e3098029e816b04d99d7e1bba22d7b77336f9fe8604f2adfb04bcf04a727", "hex"),
)
print("Using root hash from EX3 ...")

print(rlp.decode(state.get("\x01\x01\x02")))
print(rlp.decode(state.get("\x01\x01\x02\x55")))
print(rlp.decode(state.get("\x01\x01\x02\x57")))
