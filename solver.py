import sys
from typing import List
import re


class FormatError(SyntaxError):
    def __init__(self, message):
        super().__init__(message)


class SumList(list):
    def __init__(self, lst=None):
        super().__init__([] if lst is None else lst)

    def __repr__(self):
        return 'SumList' + super().__repr__()


class SousList(list):
    def __init__(self, lst=None):
        super().__init__([] if lst is None else lst)

    def __repr__(self):
        return 'SousList' + super().__repr__()


class MulList(list):
    def __init__(self, lst=None):
        super().__init__([] if lst is None else lst)

    def __repr__(self):
        return 'MulList' + super().__repr__()


class DivList(list):
    def __init__(self, lst=None):
        super().__init__([] if lst is None else lst)

    def __repr__(self):
        return 'DivList' + super().__repr__()


class ExpList(list):
    def __init__(self, lst=None):
        super().__init__([] if lst is None else lst)

    def __repr__(self):
        return 'ExpList' + super().__repr__()


def content_validate(equation):
    if not re.match(r'^[0-9\[\]\(\) /+\-*^]+$', equation):
        raise FormatError('Illegal(s) character(s)')
    if equation.count('(') != equation.count(')') or equation.count('[') != equation.count(']'):
        raise FormatError('Not all brackets have been closed')
    return 'Valid'


def symbol_cut(lst, symbol, symbol_class):
    for i, el in enumerate(lst):
        if isinstance(el, list):
            lst[i] = symbol_cut(el, symbol, symbol_class)
        elif el.count(symbol) > 0:
            lst[i] = symbol_class(el.split(symbol))
    return lst


def sub_equation_filler(lst, sub_equations):
    for i, el in enumerate(lst):
        if isinstance(el, list):
            lst[i] = sub_equation_filler(el, sub_equations)
        for j, sub_equation in enumerate(sub_equations):
            if lst[i] == '{' + str(j) + '}':
                lst[i] = cut(sub_equation)
    return lst


# (3/2)+7-2*4+((2-7)/4) -> [[[[3, '/', 2], '+', 7], '-', [2, '*', 4]], '+', [[2, '-', 7], '/', 4]]
def cut(equation):
    sub_equations = []
    current_equation = ''
    bracket_count = 0
    for char in equation:
        if char in {')', ']'}:
            bracket_count -= 1
            if bracket_count < 0:
                raise FormatError('Closing brackets without opening brackets')
            if bracket_count == 0:
                sub_equations[-1] = sub_equations[-1][1:]
        else:
            if char in {'(', '['}:
                bracket_count += 1
                if bracket_count == 1:
                    sub_equations.append('')
                    current_equation += '{' + str(len(sub_equations)-1) + '}'

        if bracket_count > 0:
            sub_equations[-1] += char
        else:
            if char not in [')', ']']:
                current_equation += char

    symbols = [
        ('+', SumList),
        ('-', SousList),
        ('*', MulList),
        ('/', DivList),
        ('^', ExpList)
    ]

    division = current_equation

    for symbol, symbol_class in symbols:
        if isinstance(division, str):
            if symbol in division:
                division = symbol_class(division.split(symbol))
        else:
            division = symbol_cut(division, symbol, symbol_class)

    if isinstance(division, str):
        division = SumList(division.split('+'))

    division = sub_equation_filler(division, sub_equations)

    return division


def solve_sum(equation):
    res = 0.
    for el in equation:
        if isinstance(el, list):
            res += solve(el)
        else:
            res += float(el)
    return res


def solve_sous(equation):
    res = None
    for el in equation:
        fct = None
        if isinstance(el, list):
            fct = solve
        else:
            fct = float

        if res is None:
            res = fct(el)
        else:
            res -= fct(el)
    return res


def solve_mul(equation):
    res = 1
    for el in equation:
        if isinstance(el, list):
            res *= solve(el)
        else:
            res *= float(el)
    return res


def solve_div(equation):
    res = None
    for el in equation:
        fct = None
        if isinstance(el, list):
            fct = solve
        else:
            fct = float

        if res is None:
            res = fct(el)
        else:
            res /= fct(el)
    return res


def solve_exp(equation):
    res = None
    for el in equation:
        fct = None
        if isinstance(el, list):
            fct = solve
        else:
            fct = float

        if res is None:
            res = fct(el)
        else:
            res = res ** fct(el)
    return res


def solve(equation):
    if isinstance(equation, SumList):
        return solve_sum(equation)
    if isinstance(equation, SousList):
        return solve_sous(equation)
    if isinstance(equation, MulList):
        return solve_mul(equation)
    if isinstance(equation, DivList):
        return solve_div(equation)
    if isinstance(equation, ExpList):
        return solve_exp(equation)


def main(args: List[str]) -> None:
    content_validate(args[0])
    cutted = cut(args[0])
    print(solve(cutted))


if __name__ == '__main__':
    main(sys.argv[1:])
