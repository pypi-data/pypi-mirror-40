#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re


def process_mmultiscripts(descendant, insertion_list):
    # Syntax: `<mmultiscripts>base postsubscript postsuperscript
    # <mprescripts /> presubscript presuperscript </mmultiscripts>`

    # ただし、任意の要素が`<none />`に置き換わることもある

    child_list = [x for x in list(descendant.children) if x.name]  # if文を付けないと余計な改行コードとかが混ざる
    prescript_list = []
    postscript_list = child_list
    pre_insertion_list = []
    post_insertion_list = insertion_list

    temp_list = []
    index = 0
    p = 0

    # `mmultiscripts`内に`mprescripts`があるかどうかの判定
    for x in child_list:

        if x.name == 'mprescripts':
            prescript_list = child_list[index:]
            postscript_list = child_list[:index]
            break
        elif x.children and x.string == None:
            p += 1
            pre_insertion_list = insertion_list[p:]
            post_insertion_list = insertion_list[:p]
        else:
            index += 1
            continue

    i = 0
    j = 0

    #  まず、`prescripts`以下のタグから処理していく
    for x in prescript_list:
        if x.name == 'none':  # <none /> タグのとき
            x_string = 'nnnn'
        elif x.name == 'mprescripts':
            x_string = 'mprescripts'
        else:
            x_string = x.string

        # xが`parent like`な要素ではないとき
        if x_string:
            if i == 0:
                base = '{}'
                temp_list.append(base)  # `mprescripts`のstring値は None になる
            elif i % 2:  # 余りを求める（0, 1のどちらかになる）
                # 奇数なら1になるので次を実行
                presubscript = '_{{{}}}'.format(x_string)
                temp_list.append(presubscript)
            else:
                # 偶数なら0になるので次を実行
                presuperscript = '^{{{}}}'.format(x_string)
                temp_list.append(presuperscript)
                pass
        else:  # `parent like`な要素があるとき
            if i == 0:
                base = '{{{}}}'.format(pre_insertion_list[j])
                temp_list.append(base)
            elif i % 2:
                presubscript = '_{{{}}}'.format(pre_insertion_list[j])
                temp_list.append(presubscript)
            else:
                presuperscript = '^{{{}}}'.format(pre_insertion_list[j])
                temp_list.append(presuperscript)
            j += 1
            pass
        i += 1

    k = 0
    m = 0

    for x in postscript_list:
        if x.name == 'none':  # <none /> タグのとき
            x_string = 'nnnn'
        else:
            x_string = x.string

        if x_string:
            if k == 0:
                base = '{{{}}}'.format(x_string)
                temp_list.append(base)
            elif k % 2:  # 偶数なら0になるのでスキップ　奇数なら1になるので次の行を実行
                postsubscript = '_{{{}}}'.format(x_string)
                temp_list.append(postsubscript)
            else:
                postsuperscript = '^{{{}}}'.format(x_string)
                temp_list.append(postsuperscript)
        else:
            if k == 0:
                base = '{{{}}}'.format(pre_insertion_list[m])
                temp_list.append(base)
            elif k % 2:  # 偶数なら0になるのでスキップ　奇数なら1になるので次の行を実行
                postsubscript = '_{{{}}}'.format(post_insertion_list[m])
                temp_list.append(postsubscript)
            else:
                postsuperscript = '^{{{}}}'.format(post_insertion_list[m])
                temp_list.append(postsuperscript)
            m += 1
            pass
        k += 1

    mmultiscripts = re.sub('nnnn', '', ''.join(temp_list))

    return mmultiscripts
