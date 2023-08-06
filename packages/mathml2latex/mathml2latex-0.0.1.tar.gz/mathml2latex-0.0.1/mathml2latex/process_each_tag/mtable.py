#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# Problem !! => LaTeXで表組みするのはとても難しそうにみえる、要検討
def process_mtable(insertion_list):
    # Syntax: `<mtable><mtr> <mtd>hogehoge</mtd> .. </ mtr> ... ... </ mtable>`
    if not insertion_list:
        mtable = 'error occered: mathml tag `mtr` not found.'
        print(mtable)
    else:
        column_assignment = 'c' * len(insertion_list)  # centering の「C」=> 他にも指定方法あり
        mtr_lump = ''.join([x + '\n' for x in insertion_list])
        table_content = mtr_lump[:-4]  # 末尾の「\n」と「\\」を削除する
        mtable = '\\begin{{table}}[htb] \n \\begin{{tabular}}{{{}}} \n  '.format(column_assignment) \
                 + '{} \n \end{{tabular}} \n\end{{table}}'.format(table_content)

    return mtable
