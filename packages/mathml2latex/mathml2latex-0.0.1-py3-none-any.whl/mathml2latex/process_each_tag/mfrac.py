#! /usr/bin/env python3
# -*- coding:utf-8 -*-


def process_mfrac(child_list, insertion_list):
    # Syntax: `<mfrac> numerator denominator </mfrac>`
    # 親タグ要素の塊がある場合
    if insertion_list:
        if len(insertion_list) == 2:
            # Both numerator and denominator are `Parent like` block
            mfrac = r'\frac {{{}}} {{{}}}'.format(insertion_list[0], insertion_list[1])
        else:
            # `mfrac` の直下が子タグ要素だった場合、`child_list` は要素を持つはず
            if child_list:
                # denominator is `parent like` block, but numerator is not.
                numerator = ''.join(child_list)
                mfrac = r'\frac {{{}}} {{{}}}'.format(numerator, insertion_list[0])
            # `mfrac` の直下が`parent like`な要素だった場合、`child_list` は要素を持たない
            else:
                # numerator is `parent like` block, but denominator is not.
                denominator = ''.join(child_list)
                mfrac = r'\frac {{{}}} {{{}}}'.format(insertion_list[0], denominator)
    # 親タグ要素の塊がない場合
    else:
        # Both numerator and denominator are NOT `parent like` block
        numerator, denominator = child_list[0], child_list[1]
        mfrac = r'\frac {{{}}} {{{}}}'.format(numerator, denominator)

    return mfrac
