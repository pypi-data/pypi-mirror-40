#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_msup(child_list, insertion_list):
    # Syntax: `<msup> base superscript </msup>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        if len(insertion_list) == 2:
            # Both base and superscript are `Parent like` block
            msup = r'{}^{{{}}}'.format(insertion_list[0], insertion_list[1])
        else:
            # `msup` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # superscript is `parent like` block, but base is not.
                base = ''.join(child_list)
                msup = r'{}^{{{}}}'.format(base, insertion_list[0])
            # `msup` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            else:
                # base is `parent like` block, but superscript is not.
                superscript = ''.join(child_list)
                msup = r'{}^{{{}}}'.format(insertion_list[0], superscript)
    # 親タグ要素の塊がない場合
    else:
        # Both base and superscript are NOT `parent like` block
        base, superscript = child_list[0], child_list[1]
        msup = r'{}^{{{}}}'.format(base, superscript)

    return msup
