#! /usr/bin/env python3
# -*- coding:utf-8 -*-


# insert_list: descendantが任意の親タグであったとき、そのsyntaxをリストにしたもの
# 入れ子構造となる部分（親タグがsyntaxに含まれている場合）だけを判定
def select_insert_list(descendant, insertion_dict):
    """
    return: list object (list of element to insert that parent)
    """
    # 大前提: 突っ込む必要があるタグの中にある値は、insertion_dictの中に格納されているはずである
    # していること: 任意のタグにおける入れ子構造の検出
    # していないこと: 最終的に返すリスト内の値がどのようなものであるのか検証すること
    #     # => 挿入したい値の型検証(inspection)は、各`process_m-hogehoge`でやってもらうべき
    # 思案したポイント:
    # `.siblings` の役割を果たす `.parent.children` を使う => 重複タグがないかどうかの分岐を作る必要がある
    # 未解決問題: insertion_dictが保持する値が初期化したくないリストなので、メモリが大量に必要になるかもしれない

    # decendant が入れ子構造の外側にあり、keyの上書きを考慮する必要がある場合
    nested_name_list = [x.name for x in list(descendant.children) if x.children and x.string == None]
    selected_list = []

    if not nested_name_list:
        # 入れ子構造がない場合 <= 挿入すべき親要素がない
        return selected_list
    else:  # 入れ子構造がある場合
        # 重複している要素そのものと、そのインデックスのペアを取り出してリストにする
        # インデックスは、insertion_list内のどの要素にアクセスすればよいのかを特定する
        # 参照：https://bit.ly/2u3ft8o
        confirm_list = [[key, nested_name_list.count(key)] for key in set(nested_name_list)
                        if nested_name_list.count(key) > 1]
        # 上記のペアが存在しない場合(要素の重複がない場合)
        if not confirm_list:  # ex. `confirm_list = []`
            # insertion_dict[key]に一番新しく`append`された要素を取ってくる
            selected_list = [insertion_dict[key][-1] for key in nested_name_list]
        else:
            print('Confirm_list is: ', confirm_list)  # debug
            # 上記のペアが存在する場合(入れ子構造かつ同じ階層に重複あり)
            index = {}  # あとでインデックス代わりに使う辞書オブジェクト
            for key in nested_name_list:
                index[key] = 1
                print('Insertion_dict[`{}`] is : '.format(key), insertion_dict[key])  # debug

            for tagname in nested_name_list:

                try:
                    selected_list.append(insertion_dict[tagname][-index[tagname]])
                    index[tagname] += 1
                except IndexError:  # `<none />` が含まれるときに起こる
                    selected_list += insertion_dict[tagname][-1]

        # confirm_listの中身の有無に依らず、selected_listを返す
        return selected_list


# 親タグの塊に実際の子タグ以外の子タグ(親タグと同じ階層にある子タグ)が含まれてしまう問題の解決
def select_true_chidren(descendant, stack_list):
    # 子タグ要素のうち、親タグ要素になっているものを探す
    # そのために、`.string`を使って検出しようとしている(親タグ要素 => `None object` になるはず)
    temp_list = [x.string for x in list(descendant.children)]
    i = 0
    # 先頭が親タグ要素であれば、`descendant`の直下に親タグの入れ子構造があることになり、
    # 親タグを検出するたびにchild_listは初期化されているはずだから、`stack_list`はそのまま返す
    if not temp_list:  # ==> if not None: と同じ意味
        stack_list = stack_list[::-1][:i]
    else:
        # `temp_list` の大きさはそのまま`descendant`の子タグの数と同値である
        i = len(temp_list)
        stack_list = stack_list[::-1][:i]
    # print('stack list is ', stack_list)

    return stack_list
