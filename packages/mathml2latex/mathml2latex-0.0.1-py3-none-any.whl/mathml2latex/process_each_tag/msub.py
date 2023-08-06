#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_msub(child_list, insertion_list):
    # Syntax: `<msub> base subscript </msub>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        if len(insertion_list) == 2:
            # Both base and subscript are `Parent like` block
            msub = r'{}_{{{}}}'.format(insertion_list[0], insertion_list[1])
        else:
            # `msub` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # subscript is `parent like` block, but base is not.
                base = ''.join(child_list)
                msub = r'{}_{{{}}}'.format(base, insertion_list[0])
            # `msub` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            else:
                # base is `parent like` block, but subscript is not.
                subscript = ''.join(child_list)
                msub = r'{}_{{{}}}'.format(insertion_list[0], subscript)
    # 親タグ要素の塊がない場合
    else:
        # Both base and subscript are NOT `parent like` block
        base, subscript = child_list[0], child_list[1]
        msub = r'{}_{{{}}}'.format(base, subscript)

    return msub
