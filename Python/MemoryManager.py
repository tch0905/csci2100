from typing import List
from HashTable import HashTable
from MemoryOperation import MemoryOperation, MemoryOperationType


class MemoryStrategy:
    FIRST_FIT = 1
    BEST_FIT = 2
    WORST_FIT = 3


class MemoryManager:
    def __init__(self, strategy: MemoryStrategy) -> None:
        self.strategy = strategy
        self.table = HashTable([],4*2**32,32)  # Hash table indexed on starting address of allocated blocks

    def request(self, op: MemoryOperation) -> int:
        if self.is_valid_op(op):
            if op.op_type == MemoryOperationType.REQUEST:
                size = op.size
                starting_address = op.addr

                if starting_address is None:
                    # Allocate memory block based on the current strategy
                    if self.strategy == MemoryStrategy.FIRST_FIT:
                        allocated_address = self.first_fit(size)
                    elif self.strategy == MemoryStrategy.BEST_FIT:
                        allocated_address = self.best_fit(size)
                    elif self.strategy == MemoryStrategy.WORST_FIT:
                        allocated_address = self.worst_fit(size)
                    else:
                        raise ValueError("Invalid memory strategy.")

                    if allocated_address != -1:
                        # Update hash tables for allocated block
                        self.table.insert({'starting_address': allocated_address, 'size': size})
                        return allocated_address

                else:
                    # Check if the specified address is available
                    if self.is_address_available(starting_address, size):
                        # Update hash tables for allocated block
                        self.table.insert({'starting_address': starting_address, 'size': size})
                        return starting_address

        return -1

    def release(self, op: MemoryOperation) -> bool:
        if self.is_valid_op(op):
            if op.op_type == MemoryOperationType.RELEASE:
                starting_address = op.addr

                if self.table.query(starting_address):
                    # Get size of the released block
                    size = self.table.query(starting_address)['size']

                    # Update hash tables for released block
                    self.table.delete({'starting_address': starting_address, 'size': op.size})
                    # self.table.insert({'starting_address': starting_address, 'size': size})

                    # Perform coalescing of adjacent free blocks

                    return True

        return False

    def is_valid_op(self, op: MemoryOperation) -> bool:
        if op.op_type == MemoryOperationType.REQUEST:
            if op.size > 0:
                if op.addr is None or op.addr >= 0:
                    return True
        elif op.op_type == MemoryOperationType.RELEASE:
            if op.addr is not None and op.addr >= 0:
                return True
        return False

    def is_address_available(self, starting_address: int, size: int) -> bool:
        # Check if the specified address is available for allocation
        if self.table.query(starting_address):
            return False

        # Check if the specified address overlaps with any allocated blocks
        for allocated_starting_address, allocated_size in self.table.database.items():
            allocated_end_address = allocated_starting_address + allocated_size["size"] - 1
            if starting_address <= allocated_end_address and starting_address + size - 1 >= allocated_starting_address:
                return False

        return True

    def first_fit(self, size: int) -> int:
        # Find the first free block that can accommodate the requested size
        for starting_address, block_size in self.free_block_table.database.items():
            if block_size >= size:
                return starting_address
        return -1

    def best_fit(self, size: int) -> int:
        # Find the smallest free block that can accommodate the requested size
        best_fit_address = -1
        best_fit_size = float('inf')

        for starting_address, block_size in self.free_block_table.items():
            if block_size >= size and block_size < best_fit_size:
                best_fit_address = starting_address
                best_fit_size = block_size

        return best_fit_address

    def worst_fit(self, size: int) -> int:
        # Find the largest free block that can accommodate the requested size
        worst_fit_address = -1
        worst_fit_size = -1

        for starting_address, block_size in self.free_block_table.items():
            if block_size >= size and block_size > worst_fit_size:
                worst_fit_address = starting_address
                worst_fit_size = block_size

        return worst_fit_address

