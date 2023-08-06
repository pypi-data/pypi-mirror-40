#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# Problem !! => LaTeX形式で表記するときに、数式装飾記号が複雑すぎる………
# cf. http://www.latex-cmd.com/equation/accent.html
def process_munder(child_list, insertion_list):
    # Syntax: `<munder> base underscript </munder>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        if len(insertion_list) == 2:
            # Both base and underscript are `Parent like` block
            munder = r'\munder {{{}}}_{{{}}}'.format(insertion_list[0], insertion_list[1])
        else:
            # `munder` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # underscript is `parent like` block, but base is not.
                base = ''.join(child_list)
                munder = r'\munder {{{}}}_{{{}}}'.format(base, insertion_list[0])
            # `munder` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            else:
                # base is `parent like` block, but underscript is not.
                underscript = ''.join(child_list)
                munder = r'\munder {{{}}}_{{{}}}'.format(insertion_list[0], underscript)
    # 親タグ要素の塊がない場合
    else:
        # Both base and underscript are NOT `parent like` block
        base, underscript = child_list[0], child_list[1]
        munder = r'\munder {{{}}}_{{{}}}'.format(base, underscript)

    return munder
