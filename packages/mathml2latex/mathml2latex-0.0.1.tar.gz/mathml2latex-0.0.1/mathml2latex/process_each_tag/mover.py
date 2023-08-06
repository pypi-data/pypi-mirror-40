#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# Problem !! => LaTeX形式で表記するときに、数式装飾記号が複雑すぎる………
# cf. http://www.latex-cmd.com/equation/accent.html
def process_mover(child_list, insertion_list):
    # Syntax: `<mover> base overscript </mover>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        if len(insertion_list) == 2:
            # Both base and overscript are `Parent like` block
            mover = r'\mover {{{}}}^{{{}}}'.format(insertion_list[0], insertion_list[1])
        else:
            # `mover` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # overscript is `parent like` block, but base is not.
                base = ''.join(child_list)
                mover = r'\mover {{{}}}^{{{}}}'.format(base, insertion_list[0])
            # `mover` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            else:
                # base is `parent like` block, but overscript is not.
                overscript = ''.join(child_list)
                mover = r'\mover {{{}}}^{{{}}}'.format(insertion_list[0], overscript)
    # 親タグ要素の塊がない場合
    else:
        # Both base and overscript are NOT `parent like` block
        base, overscript = child_list[0], child_list[1]
        mover = r'\mover {{{}}}^{{{}}}'.format(base, overscript)

    return mover
