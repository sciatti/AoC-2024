from dataclasses import dataclass, field
from queue import PriorityQueue

# declare prioirty queue dataclass structure
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    index: int=field(compare=False)

# gather input
input_list_1 = []
input_list_2 = []

with open("input.txt", "r", encoding="utf-8") as input_file_handler:
    for line in input_file_handler.readlines():
        input_1, input_2 = line.split()
        input_list_1.append(int(input_1))
        input_list_2.append(int(input_2))

input_size = len(input_list_1)

print(f"Input sizes, List 1: {len(input_list_1)} List 2: {len(input_list_2)}")

if len(input_list_1) != len(input_list_2):
    print("error, input lists size mismatch")
    exit(1)

list_1_queue = PriorityQueue(input_size)
list_2_queue = PriorityQueue(input_size)

for index in range(input_size):
    list_1_queue.put(PrioritizedItem(priority=input_list_1[index], index=index))
    list_2_queue.put(PrioritizedItem(priority=input_list_2[index], index=index))

diff = 0
for _ in range(input_size):
    diff += abs(list_1_queue.get().priority - list_2_queue.get().priority)

print(diff)
