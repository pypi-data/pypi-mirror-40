#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_msqrt(child_list, insertion_list):
    # Syntax: `<msqrt> base index </msqrt>.`
    # 親タグ要素の塊がある場合
    if insertion_list:
        if len(insertion_list) == 2:
            # Both base and index are `Parent like` block
            msqrt = r'\sqrt [{{{}}}] {{{{}}}}'.format(insertion_list[0], insertion_list[1])
        else:
            # `msqrt` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # index is `parent like` block, but base is not.
                base = ''.join(child_list)
                msqrt = r'\sqrt [{{{}}}] {{{}}}'.format(base, insertion_list[0])
            # `msqrt` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            else:
                # base is `parent like` block, but index is not.
                index = ''.join(child_list)
                msqrt = r'\sqrt [{{{}}}] {{{}}}'.format(insertion_list[0], index)
    # 親タグ要素の塊がない場合
    else:
        # Both base and index are NOT `parent like` block
        base, index = child_list[0], child_list[1]
        msqrt = r'\sqrt [{{{}}}] {{{}}}'.format(base, index)

    return msqrt
