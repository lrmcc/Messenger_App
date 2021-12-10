import random
import time


def get_random_n_digit_int(n):
    random.seed(time.time_ns())
    multiple = int("1" + ("0" * (n-1)))
    return int(round(((random.random()) * multiple), 0))


def get_time():
    return time.strftime("%m/%d/%Y at %H:%M:%S", time.localtime())


def get_str_all_val_x(dict, x):
    # takes a dictionary where each key has an array for value
    # returns list of all values at index x
    ret_string = ', '.join(str(val) for val in get_list_of_dict_idx_x(dict, x))
    return f"Connected users: {ret_string}"


def get_key_by_dict_val_x(dict, val, x):
    # takes dictionary and a val, returns key for matching value at index x
    for key, value in dict.items():
        if value[x] == val:
            return key
    return None


def get_list_of_dict_idx_x(dict, x):
    # takes dictionary returns list of all values at index x
    x_list = []
    for val in list(dict.values()):
        x_list.append(val[x])
    return x_list


def get_dict_value_x_by_value_y(dict, val, x, y):
    # takes dictionary and a val, when value at index y matches val, returns value at index x 
    for key, value in dict.items():
        if value[y] == val:
            return value[x]
    return None
