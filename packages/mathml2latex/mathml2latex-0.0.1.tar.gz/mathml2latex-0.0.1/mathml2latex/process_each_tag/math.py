#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_math(descendant, insertion_list):
    child_list = [x for x in list(descendant.children) if x.name]
    temp_list = []
    i = 0
    for x in child_list:
        x_string = x.string
        if x_string:
            temp_list.append(x_string)
        else:
            temp_list.append(insertion_list[i])
            i += 1
        continue
    math = ''.join(temp_list)
    return math
