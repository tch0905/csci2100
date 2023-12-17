from HashTable import *
# Create a HashTable instance
hash_table = HashTable([], 10000, 10)

# Insert blocks into the hash table
hash_table.insert({"start_address": 0, "size": 20})  # Insert a block starting at address 0 with size 20
hash_table.insert({"start_address": 30, "size": 10})  # Insert a block starting at address 30 with size 10

# Query the hash table
print(hash_table.query(5))  # Output: True (address 5 falls within the first block)
print(hash_table.query(25))  # Output: False (address 25 does not fall within any allocated block)

# Delete a block from the hash table
hash_table.delete({"start_address": 0, "size": 10})  # Delete the first block

# Query the hash table after deletion
print(hash_table.query(5))  # Output: False (the first block was deleted)
print(hash_table.query(35))  # Output: True (address 35 falls within the remaining block)