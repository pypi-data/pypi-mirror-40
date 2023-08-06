#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# Problem !! => LaTeXで表組みするのはとても難しそうにみえる、要検討
def process_mtr(insertion_list):
    # Syntax: `<mtr> <mtd></ mtd> ...  </ mtr>`
    if not insertion_list:
        print('error occered: mathml tag `mtd` not found.')
    else:
        mtd_lump = ''.join([x + ' &' for x in insertion_list])
        mtr = mtd_lump[:-1] + '\\\\'  # 末尾の`&` を削除し、改行として「\\」を挿入

    return mtr
