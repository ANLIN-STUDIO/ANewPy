def para_checker(para_single_rule: any, paras: list[str], *args_rule_paras):
    def wrapper(func):
        def __(*args, **kwargs):
            for i in paras:
                func_para = func.__code__.co_varnames[:func.__code__.co_argcount]
                if i in func_para:
                    idx = func_para.index(i)
                    # kwargs check
                    if i in kwargs.keys():
                        if args_rule_paras:
                            para_single_rule(kwargs[i], i, args_rule_paras)
                        else:
                            para_single_rule(kwargs[i], i)
                            # positional check
                    elif args.__len__() - 1 >= idx:
                        if args_rule_paras:
                            para_single_rule(args[idx], i, args_rule_paras)
                        else:
                            para_single_rule(args[idx], i)
                    # default para check
                    else:
                        pos = idx - func_para.__len__()
                        if func.__defaults__.__len__() >= pos:
                            if args_rule_paras:
                                para_single_rule(func.__defaults__[pos], i, args_rule_paras)
                            else:
                                para_single_rule(func.__defaults__[pos], i)
            return func(*args, **kwargs)

        return __

    return wrapper


def paras_checker(**kwparas):
    def wrapper(func):
        def __(*args, **kwargs):
            paras = kwparas.keys()
            for para in paras:
                value = kwparas[para]
                if isinstance(value, list | tuple):
                    value: list | tuple
                    para_single_rule = value.pop(0)
                    args_rule_paras = value
                else:
                    para_single_rule = value
                    args_rule_paras = False
                func_para = func.__code__.co_varnames[:func.__code__.co_argcount]
                if para in func_para:
                    idx = func_para.index(para)
                    # kwargs check
                    if para in kwargs.keys():
                        if args_rule_paras:
                            para_single_rule(kwargs[para], para, args_rule_paras)
                        else:
                            para_single_rule(kwargs[para], para)
                            # positional check
                    elif args.__len__() - 1 >= idx:
                        if args_rule_paras:
                            para_single_rule(args[idx], para, args_rule_paras)
                        else:
                            para_single_rule(args[idx], para)
                    # default para check
                    else:
                        pos = idx - func_para.__len__()
                        if func.__defaults__.__len__() >= pos:
                            if args_rule_paras:
                                para_single_rule(func.__defaults__[pos], para, args_rule_paras)
                            else:
                                para_single_rule(func.__defaults__[pos], para)
            return func(*args, **kwargs)

        return __

    return wrapper


def if_value_in_range(test_int: int, range_: str):
    """"∞", "infinity" or "i" all indicate positive infinity.
    Add "-" before them to indicate negative infinity.
    "(" and ")" means not to take this value; "[" and "]" means to take this value.
    Closed loop formed between brackets.
    Separate two values with ", "(comma+space) or ","(comma).

    "∞"、"infinity"或"i"都表示正无穷大。
    在它们前面加上"-"表示负无穷大。
    "("和")"表示不取此值；"["和"]"表示取此值。
    括号之间形成闭环。
    用", "（逗号+空格）或","（逗号）分隔两个值。

    · For example:
    > @para_checker(Rule.value_range, ['a'], '(i, 0]')
    > def test(a: int):
    >   print(a)
    · 当 a 大于等于 0 时不报错
    """
    range_ = range_.replace('infinity', '∞').replace('i', '∞').replace(', ', ',')
    try:
        if '(' in range_:
            the_max = (False, range_[1:].split(',')[0])
        elif '[' in range_:
            the_max = (True, range_[1:].split(',')[0])
        else:
            assert False
        if ')' in range_:
            the_min = (False, range_[:-1].split(',')[1])
        elif ']' in range_:
            the_min = (True, range_[:-1].split(',')[1])
        else:
            assert False
        if the_max[1] != '∞':
            int(the_max[1])
        if the_min[1] == '∞':
            the_min = (the_min[0], '-∞')
        if the_min[1] != '-∞':
            int(the_min[1])
        assert isinstance(test_int, int)
    except Exception as e:
        assert False, \
            f'Incorrect parameter structure passed in ({e})'
    if not (the_max[1] == '∞' or the_min[1] == '-∞'):
        assert (the_max[1] == the_min[1] and the_max[0] and the_min[0]) or (the_max[1] > the_min[1]), \
            'The maximum value should be greater than the minimum value'
    if the_max[1] == '∞':
        if the_min[1] != '-∞':
            if the_min[0]:
                if not test_int >= int(the_min[1]):
                    return False
            else:
                if not test_int > int(the_min[1]):
                    return False
    elif the_min[1] == '-∞':
        if the_max[1] != '∞':
            if the_max[0]:
                if not int(the_max[1]) >= test_int:
                    return False
            else:
                if not int(the_max[1]) > test_int:
                    return False
    else:
        if the_max[0]:
            if the_min[0]:
                if not int(the_max[1]) >= test_int >= int(the_min[1]):
                    return False
            else:
                if not int(the_max[1]) >= test_int > int(the_min[1]):
                    return False
        else:
            if the_min[0]:
                if not int(the_max[1]) > test_int >= int(the_min[1]):
                    return False
            else:
                if not int(the_max[1]) > test_int > int(the_min[1]):
                    return False
    return True


class Rule(object):
    @staticmethod
    def __positional_arguments(name: str, args: tuple, expected_quantity: int):
        assert len(args) == expected_quantity, \
            f'Rule.{name}() takes {expected_quantity} positional arguments but {len(args)} were given'
        if len(args) == 0:
            return None
        elif len(args) == 1:
            return args[0]
        elif len(args) > 1:
            return args

    @staticmethod
    def __notNone(x, i, *args):
        Rule.__positional_arguments('notNone', args, 0)
        assert x is not None, \
            f'\"{i}\" should not take None'

    notNone = __notNone

    @staticmethod
    def __notTure(x, i, RelativeAndAbsolute):
        """:RelativeAndAbsolute:
        "True" is absolute True
        "False" is relative True"""
        Rule.__positional_arguments('notTure', RelativeAndAbsolute, 1)
        if bool(RelativeAndAbsolute[0]):
            assert x is not True, \
                f'\"{i}\" should not take Ture'
        else:
            assert not x, \
                f'\"{i}\" should not take Ture'

    notTrue = __notTure

    @staticmethod
    def __notFalse(x, i, RelativeAndAbsolute):
        """:RelativeAndAbsolute:
        "True" is absolute False
        "False" is relative False"""
        Rule.__positional_arguments('notTure', RelativeAndAbsolute, 1)
        if bool(RelativeAndAbsolute[0]):
            assert x is not False, \
                f'\"{i}\" should not take False'
        else:
            assert x, \
                f'\"{i}\" should not take False'

    notFalse = __notFalse

    @staticmethod
    def __value_range(x, i, range_: tuple[str]):
        """"∞", "infinity" or "i" all indicate positive infinity.
        Add "-" before them to indicate negative infinity.
        "(" and ")" means not to take this value; "[" and "]" means to take this value.
        Closed loop formed between brackets.
        Separate two values with ", "(comma+space) or ","(comma).

        "∞"、"infinity"或"i"都表示正无穷大。
        在它们前面加上"-"表示负无穷大。
        "("和")"表示不取此值；"["和"]"表示取此值。
        括号之间形成闭环。
        用", "（逗号+空格）或","（逗号）分隔两个值。

        · For example:
        > @para_checker(Rule.value_range, ['a'], '(i, 0]')
        > def test(a: int):
        >     print(a)
        · 当 a 大于等于 0 时不报错
        """
        range_ = Rule.__positional_arguments('value_range', range_, 1) \
            .replace('infinity', '∞') \
            .replace('i', '∞') \
            .replace(', ', ',')
        try:
            if '(' in range_:
                the_max = (False, range_[1:].split(',')[0])
            elif '[' in range_:
                the_max = (True, range_[1:].split(',')[0])
            else:
                assert False
            if ')' in range_:
                the_min = (False, range_[:-1].split(',')[1])
            elif ']' in range_:
                the_min = (True, range_[:-1].split(',')[1])
            else:
                assert False
            if the_max[1] != '∞':
                int(the_max[1])
            if the_min[1] == '∞':
                the_min = (the_min[0], '-∞')
                range_ = f"{range_[:-1].split(',')[0]},-∞)"
            if the_min[1] != '-∞':
                int(the_min[1])
            assert isinstance(x, int)
        except Exception as e:
            assert False, \
                f'Incorrect parameter structure passed in ({e})'
        if not (the_max[1] == '∞' or the_min[1] == '-∞'):
            assert (the_max[1] == the_min[1] and the_max[0] and the_min[0]) or (the_max[1] > the_min[1]), \
                'The maximum value should be greater than the minimum value'
        if the_max[1] == '∞':
            range_ = range_.replace('[', '(')
        if the_min[1] == '-∞':
            range_ = range_.replace(']', ')')
        error = f'\"{i}\" should be in the range {range_}'
        if the_max[1] == '∞':
            if the_min[1] != '-∞':
                if the_min[0]:
                    assert x >= int(the_min[1]), \
                        error
                else:
                    assert x > int(the_min[1]), \
                        error
        elif the_min[1] == '-∞':
            if the_max[1] != '∞':
                if the_max[0]:
                    assert int(the_max[1]) >= x, \
                        error
                else:
                    assert int(the_max[1]) > x, \
                        error
        else:
            if the_max[0]:
                if the_min[0]:
                    assert int(the_max[1]) >= x >= int(the_min[1]), \
                        error
                else:
                    assert int(the_max[1]) >= x > int(the_min[1]), \
                        error
            else:
                if the_min[0]:
                    assert int(the_max[1]) > x >= int(the_min[1]), \
                        error
                else:
                    assert int(the_max[1]) > x > int(the_min[1]), \
                        error

    value_range = __value_range

    @staticmethod
    def __list_structure(x, i, structure: tuple[list[type] | tuple[type]]):
        """
        not only "list", but also "tuple"
        The passed in parameters must be in the format you specify.
        One more element, one less element and change a kind of element all cannot pass.
        """
        structure = Rule.__positional_arguments('list_structure', structure, 1)
        assert isinstance(x, list | tuple), \
            f'\"{i}\" must be a list or tuple'
        assert len(x) == len(structure), \
            f'The length of \"{i}\" must be the same as that of \"structure\"({structure})'
        for each_type in range(len(structure)):
            assert isinstance(x[each_type], structure[each_type]), \
                f"The {each_type + 1}-th element, \"{i}\"({x[each_type]}: {type(x[each_type])}) is different from \"structure\"{structure[each_type]}"

    list_structure = __list_structure
