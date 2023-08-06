#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import sys

from bs4.element import NavigableString

from mathml2latex.parts_pickup import select_insert_list
from mathml2latex.parts_pickup import select_true_chidren

from mathml2latex.process_each_tag.math import process_math
from mathml2latex.process_each_tag.mrow import process_mrow
from mathml2latex.process_each_tag.msub import process_msub
from mathml2latex.process_each_tag.msup import process_msup
from mathml2latex.process_each_tag.msubsup import process_msubsup
from mathml2latex.process_each_tag.mfrac import process_mfrac
from mathml2latex.process_each_tag.mroot import process_mroot
from mathml2latex.process_each_tag.msqrt import process_msqrt  # mrootと同じでいいのか確認（メモ：2019/01/08）
# froprocess_mprescripts
from mathml2latex.process_each_tag.mpadded import process_mpadded
from mathml2latex.process_each_tag.mphantom import process_mphantom
from mathml2latex.process_each_tag.mmultiscripts import process_mmultiscripts
from mathml2latex.process_each_tag.munder import process_munder
from mathml2latex.process_each_tag.mover import process_mover
from mathml2latex.process_each_tag.munderover import process_munderover
from mathml2latex.process_each_tag.mtd import process_mtd
from mathml2latex.process_each_tag.mtr import process_mtr
from mathml2latex.process_each_tag.mtable import process_mtable
from mathml2latex.process_each_tag import process_mfenced
from mathml2latex.process_each_tag.mspace import process_mspace



pattern = {}
pattern['math'] = re.compile('math$')
pattern['mrow'] = re.compile('mrow$')
pattern['msub'] = re.compile('msub$')
pattern['msup'] = re.compile('msup$')
pattern['msubsup'] = re.compile('msubsup$')
pattern['mfrac'] = re.compile('mfrac$')
pattern['mroot'] = re.compile('mroot$')
pattern['msqrt'] = re.compile('msqrt$')
pattern['mprescripts'] = re.compile('mprescripts$')
pattern['mpadded'] = re.compile('mpadded$')
pattern['mphantom'] = re.compile('mphantom$')
pattern['mmultiscripts'] = re.compile('mmultiscripts$')
pattern['munder'] = re.compile('munder$')
pattern['mover'] = re.compile('mover$')
pattern['munderover'] = re.compile('munderover$')
pattern['mtd'] = re.compile('mtd$')
pattern['mtr'] = re.compile('mtr$')
pattern['mtable'] = re.compile('mtable$')
pattern['mfenced'] = re.compile('mfenced$')
pattern['mspace'] = re.compile('mspace$')
pattern['none'] = re.compile('none$')


# These objects are all tags that may become parent tags.
def process_mathml(soup):

    insertion_dict = {}

    insertion_dict['math'] = []
    insertion_dict['mrow'] = []
    insertion_dict['mfrac'] = []
    insertion_dict['mroot'] = []
    insertion_dict['msub'] = []
    insertion_dict['msup'] = []
    insertion_dict['msubsup'] = []
    insertion_dict['mpadded'] = []
    insertion_dict['mphantom'] = []
    insertion_dict['munder'] = []
    insertion_dict['mover'] = []
    insertion_dict['munderover'] = []
    insertion_dict['mtd'] = []
    insertion_dict['mtr'] = []
    insertion_dict['mtable'] = []
    insertion_dict['mmultiscripts'] = []
    insertion_dict['mspace'] = []
    insertion_dict['none'] = ['']

    stack_list = []

    for descendant in list(soup.parent.descendants)[::-1]:  # `parent`で`math`も含めた`descendants`を得る

        if isinstance(descendant, NavigableString):
            # print('this element is NOT tag.')
            continue
        else:
            end_point = pattern['math'].match(descendant.name)
            if not end_point:
                tagname = descendant.name
                string = descendant.string

                # 子タグのとき, `.string`はstr型(Noneにはならない)
                if string:
                    stack_list.append(string)
                # 親タグのとき, `.string`はNoneになる
                else:
                    # あとから考えるべきこと: 各process内での蒸発してしまうchild_listの要素の扱い, hoge, fuga
                    insertion_list = select_insert_list(descendant, insertion_dict)
                    child_list = select_true_chidren(descendant, stack_list)
                    stack_list = []  # re: initialize

                    if pattern['mspace'].match(tagname):
                        # Synatax: None
                        insertion_dict['mspace'].append(process_mspace(descendant))
                    elif pattern['mfrac'].match(tagname):
                        # Syntax: `<mfrac> numerator denominator </mfrac>`
                        insertion_dict['mfrac'].append(process_mfrac(child_list, insertion_list))
                    elif pattern['mroot'].match(tagname):
                        # Syntax: `<mroot> base index </mroot>.`
                        insertion_dict['mroot'].append(process_mroot(child_list, insertion_list))
                    elif pattern['msqrt'].match(tagname):
                        # Syntax: `<msqrt> base </msqrt>`
                        insertion_dict['msqrt'].append(process_msqrt(child_list, insertion_list))
                    elif pattern['mrow'].match(tagname):
                        insertion_dict['mrow'].append(process_mrow(descendant, child_list, insertion_list))
                    elif pattern['msub'].match(tagname):
                        # Syntax: `<msub> base subscript </msub>`
                        insertion_dict['msub'].append(process_msub(child_list, insertion_list))
                    elif pattern['msup'].match(tagname):
                        # Syntax: `<msup> base superscript </msup>`
                        insertion_dict['msup'].append(process_msup(child_list, insertion_list))
                    elif pattern['msubsup'].match(tagname):
                        # Syntax: `<msubsup> base subscript superscript </msubsup>`
                        insertion_dict['msubsup'].append(process_msubsup(descendant, child_list, insertion_list))
                    elif pattern['mpadded'].match(tagname):
                        # Syntax: None → 形を視覚的に整えるためだけのもの
                        insertion_dict['mpadded'].append(process_mpadded(child_list, insertion_list))
                    elif pattern['mphantom'].match(tagname):
                        # Syntax: None → 形を視覚的に整えるためだけのもの
                        insertion_dict['mphantom'].append(process_mphantom(child_list, insertion_list))
                    elif pattern['none'].match(tagname):
                        # `<none />` は `mmultiscripts`の中でしか出現しない
                        # `mmultiscripts` の中で同時に処理してもらう
                        pass
                    elif pattern['mmultiscripts'].match(tagname):
                        # Syntax: `<mmultiscripts> base (subscript superscript)* [ <mprescripts/> \
                        #          (presubscript presuperscript)* ] </mmultiscripts>`
                        insertion_dict['mmultiscripts'].append(process_mmultiscripts(descendant, insertion_list))
                    elif pattern['mprescripts'].match(tagname):
                        # Syntax: None → mmultiscripts の内部で処理
                        pass
                    elif pattern['munder'].match(tagname):
                        # Synatax: `<munder> base underscript </munder>`
                        insertion_dict['munder'].append(process_munder(child_list, insertion_list))
                    elif pattern['mover'].match(tagname):
                        # Syntax: `<mover> base overscript </mover>`
                        insertion_dict['mover'].append(process_mover(child_list, insertion_list))
                    elif pattern['munderover'].match(tagname):
                        # Syntax: `<munderover> base underscript overscript </ munderover>`
                        insertion_dict['mover'].append(process_munderover(descendant, child_list, insertion_list))
                    elif pattern['mtd'].match(tagname):
                        # Syntax: `<mtd> <mi|mn|mo|mparent> content </ mi|mn|mo|mparent> </ mtd>`
                        insertion_dict['mtd'].append(process_mtd(child_list, insertion_list))
                    elif pattern['mtr'].match(tagname):
                        # Syntax: `<mtr> <mtd></ mtd> ...  </ mtr>`
                        insertion_dict['mtr'].append(process_mtr(insertion_list))
                    elif pattern['mtable'].match(tagname):
                        # Syntax: `<mtable><mtr> <mtd>hogehoge</mtd> .. </ mtr> ... ... </ mtable>`
                        insertion_dict['mtable'].append(process_mtable(insertion_list))
                    elif pattern['mfenced'].match(tagname):
                        # Syntax: `<mfenced><mn|mi|mo|mparent></ mn|mi|mo|mparent> ... </ mfenced>  </mfenced> `
                        insertion_dict['mfenced'].append(process_mfenced(descendant, insertion_list))
                    else:
                        print(descendant, '\n')
                        print('Unknown Tag appeared!! terminate the program.\n')
                        print('New tag name is ; ', descendant.name)
                        sys.exit()  # debug

            # ##### if endpoint: ##### #
            else:
                insertion_list = select_insert_list(descendant, insertion_dict)
                insertion_dict['math'].append(process_math(descendant, insertion_list))
                mathml_list = insertion_dict['math']
                print('MathML list is : ', mathml_list)  # debug
                # print(soup.prettify())  # debug
                mathml_str_block = ''.join(mathml_list)

                return mathml_str_block  # in Production environment (type: string)
