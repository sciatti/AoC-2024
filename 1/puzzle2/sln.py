# gather input
input_list_1 = []
input_list_2 = []

list_1_dict = {}
list_2_dict = {}

def insert_func(dict_item, key):
    if key not in dict_item:
        dict_item[key] = 1
    else:
        dict_item[key] += 1

with open("input.txt", "r", encoding="utf-8") as input_file_handler:
    for line in input_file_handler.readlines():
        x, y = line.split()
        input_1, input_2 = int(x), int(y)
        input_list_1.append(input_1)
        input_list_2.append(input_2)
        insert_func(list_1_dict, input_1)
        insert_func(list_2_dict, input_2)

input_size = len(input_list_1)

print(f"Input sizes, List 1: {len(input_list_1)} List 2: {len(input_list_2)}")

if len(input_list_1) != len(input_list_2):
    print("error, input lists size mismatch")
    exit(1)

sim_score = 0
for key in list_1_dict:
    if key in list_2_dict:
        sim_score += key * list_2_dict[key]

print(sim_score)
