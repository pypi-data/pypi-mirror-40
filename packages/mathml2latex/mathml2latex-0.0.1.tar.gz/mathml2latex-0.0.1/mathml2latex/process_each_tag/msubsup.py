#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_msubsup(descendant, child_list, insertion_list):
    # Syntax: `<msubsup> base subscript superscript </msubsup>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        length = len(insertion_list)
        if length == 3:
            # Both base and superscript are `Parent like` block
            msubsup = r'{}_{{{}}}^{{{}}}'.format(insertion_list[0], insertion_list[1], insertion_list[2])
        elif length == 2:
            determine_list = [x.string for x in list(descendant.children)]
            if child_list:
                # subscript & superscript is `parent like` block, but base is not.
                base = ''.join(child_list)
                msubsup = r'{}_{{{}}}^{{{}}}'.format(base, insertion_list[0], insertion_list[1])

            # `msubsup` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            elif determine_list[1] == None:
                # base & superscript are `parent like` block, but subscript is not.
                child_list = [x for x in determine_list if x is not None]
                subscript = ''.join(child_list)
                msubsup = r'{}_{{{}}}^{{{}}}'.format(insertion_list[0], subscript, insertion_list[1])
            else:
                # base & subscript are `parent like` block, but superscript is not.
                child_list = [x for x in determine_list if x is not None]
                superscript = ''.join(child_list)
                msubsup = r'{}_{{{}}}^{{{}}}'.format(insertion_list[0], insertion_list[1], superscript)
        else:
            determine_list = [x.string for x in list(descendant.children)]
            # `msubsup` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # superscript is `parent like` block, but base is not.
                base, subscript = child_list[0], child_list[1]
                msubsup = r'{}_{{{}}}^{{{}}}'.format(base, subscript, insertion_list[0])
            # `msubsup` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            elif determine_list[1] == None:
                # base is `parent like` block, but superscript is not.
                child_list = [x for x in determine_list if x is not None]
                base, superscript = child_list[0], child_list[1]
                msubsup = r'{}_{{{}}}^{{{}}}'.format(base, insertion_list[0], superscript)
            else:
                # base is `parent like` block, but superscript is not.
                child_list = [x for x in determine_list if x is not None]
                subscript, superscript = child_list[0], child_list[1]
                msubsup = r'{}_{{{}}}^{{{}}}'.format(insertion_list[0], subscript, superscript)
    # 親タグ要素の塊がない場合
    else:
        # Both base and superscript are NOT `parent like` block
        base, subscript, superscript = child_list[0], child_list[1], child_list[2]
        msubsup = r'{}_{{{}}}^{{{}}}'.format(base, subscript, superscript)

    return msubsup
