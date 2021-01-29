#!/usr/bin/env python
import copy
import json
import sys


def del_dic(data, keys):
    if len(keys) == 1:
        if keys[0] in data:
            del data[keys[0]]
            return

    else:
        temp_key = keys.pop(0)
        if temp_key in data:
            temp_data = data.pop(temp_key)
            del_dic(temp_data, keys)
            data[temp_key] = temp_data


def del_dic_main(dic_data, del_list):
    for key in del_list:
        key_list = key.split(".")
        if len(key_list) > 1:
            del_dic(dic_data, key_list)
    return dic_data


if __name__ == "__main__":
    new_dic = []
    json_file = open(sys.argv[1], 'r')
    test_data = json.load(json_file)
    print(test_data)
    with open(sys.argv[2], 'r') as del_lists:
        del_lists = [s.strip() for s in del_lists.readlines()]
        print(del_lists)

    # for i in test_data:
        # print(f"before: {i}")
        # new_i = del_dic_main(i, del_lists)

        # print(f"after: {new_i}")
        # new_dic.append(new_i)
        # new_dic.append(del_dic_main(i, del_lists))

    test_data = del_dic_main(test_data, del_lists)
    with open(sys.argv[1], mode='w') as f:
        f.write(json.dumps(test_data, indent=4))
