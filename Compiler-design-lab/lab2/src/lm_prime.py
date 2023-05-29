# -*- coding = utf-8 -*-
# @Time : 2023/5/29 4:42 PM
# @Author : Jingbo Su
# @File : lm_prime.py
# @Software : PyCharm

"""
E -> E+T | E-T | T
T -> T*F | T/F | F
F -> (E) | i
"""

left_most_prime_phrase = {
    'i': 'F',
    'F': 'E',
    'T': 'E',
    '(E)': 'F',
    'F+F': 'E',
    'F-F': 'E',
    'F*F': 'E',
    'F/F': 'E',
}
