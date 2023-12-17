from typing import List


class HashTable:
    def __init__(self, values: List[object], memory_size: int, block_size: int) -> None:
        # Calculate the maximum address based on memory size and block size
        self.max_address = memory_size // block_size

        # Initialize the hash tables and the shared database
        self.size_block_table = {}  # Hash table indexed on size of blocks
        self.allocated_block_table = {}  # Hash table indexed on starting address of allocated blocks
        self.database = {}  # Shared database to store memory blocks

        # Populate hash tables and database with initial set of memory-block allocations and releases
        for value in values:
            self.insert(value)

    def delete(self, value: object) -> bool:
        # Delete an existing value from the hash tables and the shared database
        delete_block = value
        delete_block_starting_address = value["starting_address"]
        delete_block_size = value['size']
        target_block = self.query(value)
        if not target_block:
            return False

        starting_address = target_block["starting_address"]
        size = target_block['size']
        ending_address = starting_address + size

        self.database.pop(starting_address)
        self.allocated_block_table.pop(starting_address)

        if starting_address < delete_block_starting_address:
            left_block_size = delete_block_starting_address - starting_address
            left_block = {'starting_address': starting_address, 'size': left_block_size}
            self.insert(left_block)

        if ending_address > delete_block_starting_address + delete_block_size:
            right_block_starting_address = delete_block_starting_address + delete_block_size
            right_block_size = ending_address - right_block_starting_address
            right_block = {'starting_address': right_block_starting_address, 'size': right_block_size}
            self.insert(right_block)
        self.delete(value)
        return True



    def insert(self, value: object):
        # Insert a new value into the hash tables and the shared database
        starting_address, size = value['starting_address'], value['size']

        # Check if the starting address is within the valid range
        if starting_address < 0 or starting_address >= self.max_address:
            raise ValueError("Invalid starting address.")

        # Check if the memory block overlaps with any existing allocated blocks
        for allocated_starting_address, allocated_size in self.allocated_block_table.items():
            allocated_end_address = allocated_starting_address + allocated_size - 1
            if starting_address <= allocated_end_address and starting_address + size - 1 >= allocated_starting_address:
                raise ValueError("Memory block overlaps with an existing allocated block.")

        # Add the memory block to the allocated_block_table
        self.allocated_block_table[starting_address] = size

        # Remove the memory block from the free_block_table if it was previously marked as free
        if starting_address in self.free_block_table:
            del self.free_block_table[starting_address]

        # Add the memory block to the size_block_table
        if size in self.size_block_table:
            self.size_block_table[size].append(starting_address)
        else:
            self.size_block_table[size] = [starting_address]

        # Add the memory block to the database
        self.database[starting_address] = value

    def query(self, key: object) -> bool:
        # Query by key in the hash tables and the shared database
        starting_address = key["starting_address"]
        size = key["size"]

        # Check if the specified block is in the allocated_block_table
        if starting_address in self.allocated_block_table and self.allocated_block_table[starting_address] == size:
            return True

        # Find the memory block that contains the desired key
        for target_starting_address, size in self.allocated_block_table.items():
            if target_starting_address + size > starting_address
        return False