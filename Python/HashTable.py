from typing import List


class HashTable:
    def __init__(self, values: List[object], memory_size: int, block_size: int) -> None:
        # Calculate the maximum address based on memory size and block size
        self.max_address = memory_size // block_size
        self.allocated_block_table = {}  # Hash table indexed on starting address of allocated blocks
        self.database = {0:self.max_address}  # Shared database to store memory blocks
        self.free_block = {0:self.max_address}
        for val in values:
            self.insert(val,block_size)

    def insert(self, value: dict):
        start_address = value.get('start_address')
        size = value.get('size')

        # Step 1: Check if the start address and size are valid
        if start_address is None or size is None:
            raise ValueError("Invalid start address or size")
        if start_address < 0 or start_address >= self.max_address:
            raise ValueError("Invalid start address")
        if size <= 0:
            raise ValueError("Invalid size")

        # Step 2: Check if the start address is already in the allocated block table
        if start_address in self.allocated_block_table:
            raise ValueError("Start address already allocated")

        # Step 3: Update the allocated block table
        end_address = start_address + size
        self.allocated_block_table[start_address] = end_address

        # Step 4: Update the database by splitting existing blocks
        new_block = [start_address, end_address]
        for block_start, block_end in list(self.database.items()):
            if block_start < new_block[1] and block_end > new_block[0]:
                # Split the existing block into two separate blocks
                if block_start < new_block[0]:
                    self.database[block_start] = new_block[0]
                if block_end > new_block[1]:
                    self.database[new_block[1]] = block_end

        # Step 5: Update the free block table by removing or splitting blocks
        for block_start, block_end in list(self.free_block.items()):
            if block_start < new_block[1] and block_end > new_block[0]:
                # Remove the block from the free block table
                del self.free_block[block_start]

                # Split the existing block into two separate blocks
                if block_start < new_block[0]:
                    self.free_block[block_start] = new_block[0]
                if block_end > new_block[1]:
                    self.free_block[new_block[1]] = block_end



    def delete(self, value: object) -> bool:
        # the value should be a dict which contain the start_address and size
        # if consider
        #     # before insert [8,10]
        #        the allocated_block_table is [4,16] the database is [0,4],[4,16],[16,memory_size // block_size], the free_block is [0,4],[16,memory_size // block_size]
        # after delete [8,10]
        # the allocated_block_table is [4,8], [10,16] the database is [0,4],[4,8],8,10], [10,16],[16,memory_size // block_size], the free_block is [0,4],[8,10],[16,memory_size // block_size]
        #     # we need consider that the allocated_block_table, database,free_block  is not overlap
        #     # Note:　u need to update allocated_block_table,database, free_block
        start_address = value["start_address"]
        end_address = start_address+ value["size"]
        target = self.query(start_address)
        target2  =  self.query(start_address)
        if target != target2:
            self.delete({"start_address": target["start_address"]+target["size"], "size":value["size"]-target["size"]})
        # del self.query((start_address))
        pass

    def query(self, key: int) -> bool:
        keys = sorted(self.allocated_block_table.keys())  # Sort the keys in ascending order

        if key < keys[0]:  # Key is smaller than the smallest key
            return False

        left = 0
        right = len(keys) - 1

        while left < right:
            mid = (left + right) // 2  # Calculate the middle index

            if keys[mid] <= key < keys[mid + 1]:  # Key is between the current and next key
                return True
            elif keys[mid] <= key:  # Key is in the right half
                left = mid + 1
            else:  # Key is in the left half
                right = mid

        return False  # Key not found

    # def insert(self, value: object):
    #     # the value should be a dict which contain the start_address and size
    #     # if consider the address is init, the database is [0, memory_size // block_size]
    #     # value = {start_address = 4, size = 12}
    #     # that mean insert[4,16]
    #     # before insert [4,16]
    #     # the allocated_block_table is Empty
    #     # the database is [0,memory_size // block_size],
    #     # the free_block is [0,memory_size // block_size],
    #     # after insert [4,16]
    #     # the allocated_block_table is [4,16]
    #     # the database is [0,4],[4,16],[16,memory_size // block_size],
    #     # the free_block is [0,4],[16,memory_size // block_size]
    #     # we need consider that the allocated_block_table is not overlap
    #     # Note:　u need to update allocated_block_table,database, free_block
    #     pass
