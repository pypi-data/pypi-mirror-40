#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_mphantom(descendant, insertion_list):
    # そもそもどこでPhantomなんて使うのか？利用方法がわからない
    determine_list = [x.string for x in list(descendant.children)]
    temp_list = []
    i = 0
    for x_string in determine_list:
        if x_string is None:
            temp_list.append(insertion_list[i])
            i += 1
        else:
            temp_list.append(x_string)
    mphantom = ''.join(temp_list)
    return mphantom
