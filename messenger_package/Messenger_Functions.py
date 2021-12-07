#!/usr/bin/env python3

import random
import time


def get_random_n_digit_int(n):
    random.seed(time.time_ns())
    multiple = int("1" + ("0" * (n-1)))
    return int(round(((random.random()) * multiple), 0))


def get_time():
    return time.strftime("%m/%d/%Y at %H:%M:%S", time.localtime())


def get_str_all_val_x(dict, x):
    ret_string = ', '.join(str(val) for val in get_list_of_dict_idx_x(dict, x))
    return f"Connected users: {ret_string}"


def get_key_by_dict_val_x(dict, client_id, x):
    # get_client_by_client_id(self, client_id)
    for key, value in dict.items():
        if value[x] == client_id:
            return key
    return None


def get_list_of_dict_idx_x(dict, x):
    # takes dict (like self.client_dict) returns values (like username) list
    x_list = []
    for val in list(dict.values()):
        x_list.append(val[x])
    return x_list


def get_dict_value_x_by_value_y(dict, user_value, x, y):
    #  example: get client_id by username
    #   get_dict_value_x_by_value_y(self.client_dict, username, 0, 1)
    for key, value in dict.items():
        if value[y] == user_value:
            return value[x]
    return None
