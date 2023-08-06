#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# Problem !! => LaTeX形式で表記するときに、数式装飾記号が複雑すぎる………
# cf. http://www.latex-cmd.com/equation/accent.html
def process_munderover(descendant, child_list, insertion_list):
    # Syntax: `<munderover> base underscript overscript </ munderover>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        length = len(insertion_list)
        if length == 3:
            # Both base and overscript are `Parent like` block
            munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(insertion_list[0], insertion_list[1],
                                                                    insertion_list[2])
        elif length == 2:
            determine_list = [x.string for x in list(descendant.children)]
            if child_list:
                # underscript & overscript is `parent like` block, but base is not.
                base = ''.join(child_list)
                munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(base, insertion_list[0], insertion_list[1])
            # `munderover` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            elif determine_list[1] == None:
                # base & overscript are `parent like` block, but underscript is not.
                child_list = [x for x in determine_list if x is not None]
                underscript = ''.join(child_list)
                munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(insertion_list[0], underscript,
                                                                        insertion_list[1])
            else:
                # base & underscript are `parent like` block, but overscript is not.
                child_list = [x for x in determine_list if x is not None]
                overscript = ''.join(child_list)
                munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(insertion_list[0], insertion_list[1],
                                                                        overscript)
        else:
            determine_list = [x.string for x in list(descendant.children)]
            # `munderover` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # overscript is `parent like` block, but base is not.
                base, underscript = child_list[0], child_list[1]
                munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(base, underscript, insertion_list[0])
            # `munderover` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            elif determine_list[1] == None:
                # base is `parent like` block, but overscript is not.
                child_list = [x for x in determine_list if x is not None]
                base, overscript = child_list[0], child_list[1]
                munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(base, insertion_list[0], overscript)
            else:
                # base is `parent like` block, but overscript is not.
                child_list = [x for x in determine_list if x is not None]
                underscript, overscript = child_list[0], child_list[1]
                munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(insertion_list[0], underscript, overscript)
    # 親タグ要素の塊がない場合
    else:
        # Both base and overscript are NOT `parent like` block
        base, underscript, overscript = child_list[0], child_list[1], child_list[2]
        munderover = r'\munderover {{{}}}_{{{}}}^{{{}}}'.format(base, underscript, overscript)

    return munderover
