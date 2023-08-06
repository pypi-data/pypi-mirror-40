#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_mtd(child_list, insertion_list):
    # Syntax: `<mtd> <mi|mn|mo|`mparent`> content </ mi|mn|mo|`mparent`> </ mtd>`
    # 親タグ要素の塊がある場合

    if insertion_list:
        mtd = ''.join(insertion_list)
    else:
        # There is NO `parent like` block, is only child elements.
        mtd = ''.join(child_list)

    return mtd
