#! /usr/bin/env python3
# -*- coding:utf-8 -*-


#  <mfenced open="{" close="}" separators=";;,">  => 属性から区切り記号を取ってくる必要あり
def process_mfenced(descendant, insertion_list):
    determine_list = [x.string for x in list(descendant.children)]
    temp_list = []
    i = 0
    for x_string in determine_list:
        if x_string is None:
            temp_list.append(insertion_list[i])
            i += 1
        else:
            temp_list.append(x_string)
    mfenced = ''.join(temp_list)
    return mfenced
