#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from codecs import open
from os import path

version_code = '0.0.01'  # あとから変更する際はこの数字を変える

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()  # long_descriptionとしてあとから読み込む
    requires = [
        "beautifulsoup4>=4.6.3",
        "lxml>=4.2.5"
    ]

setup(
    name='mathml2latex',
    version=version_code,
    description='Convert MathML to LaTeX format',
    long_description=long_description,  # README.mdをそのまま読み込む
    long_description_content_type="text/markdown",
    url='https://github.com/KiaismAgre/mathml2latex',
    author='KiaismAgre',
    author_email='KUBOKAWA.Takara@nims.go.jp',
    license='MIT',  # ライセンス周りの指定は要検討
    # 実際に動かす時に依存関係にあるライブラリをinstallしてくれる
    install_requires=requires,
    keywords='mathml2latex mathml latex convert xml',
    packages=[
        "mathml2latex",
        "mathml2latex.process_each_tag"
    ],
    # 今回コマンドを作ったのでconsole_scriptsを記述している
    entry_points={
        "console_scripts": [
            "mathml2latex = mathml2latex.mathml:process_mathml",
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
