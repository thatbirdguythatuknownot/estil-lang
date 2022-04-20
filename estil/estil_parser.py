from re import A
from estil_constant_parser import parser as cparser
from estil_lexer import *
from estil_node_types import *

class ParserError(SyntaxError):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col=0):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
    def __repr__(self):
        return f"ParserError({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        return f"\x1b[38;2;220;0;0mERROR (Parser):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}^"
    def __bool__(self):
        return False

class ParserErrorWithStart(ParserError):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col, msg2, line2, text2, col2):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
        self.msg2 = msg2
        self.line2 = line2
        self.text2 = text2
        self.col2 = col2
    def __repr__(self):
        return f"ParserErrorWithStart({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r}, {self.msg2!r}, {self.line2!r}, {self.text2!r}, {self.col2!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        linen2 = f"{self.line2:03d}"
        return f"\x1b[38;2;220;0;0mERROR (Parser):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}^\n{self.msg2}\n{linen2}  | {self.text2}\n{len(linen2) * ' '}   {' ' * self.col2}^"

class ParserErrorWithTildeAndCaret(ParserError):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col, tildenum, caretnum):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
        self.tildenum = tildenum
        self.caretnum = caretnum
    def __repr__(self):
        return f"ParserErrorWithTildeAndCaret({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r}, {self.tildenum!r}, {self.caretnum!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        return f"\x1b[38;2;220;0;0mERROR (Parser):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}{'~' * self.tildenum}{'^' * self.caretnum}"

class ParserWarning(SyntaxWarning):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col=0):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
    def __repr__(self):
        return f"ParserWarning({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        return f"\x1b[38;2;220;205;0mWARNING (Parser):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}^"
    def __bool__(self):
        return True

class Parser:
    __module__ = 'builtins'
    def __init__(self, source, start_index=0):
        self.source = source
        self.stream = lexer(source)
        self.index = start_index
        self.stack = []

def token_name(tok):
    tokt = tok[0]
    if tokt is T_IDENT:
        return f"identifier '{tok[1]}'"
    elif tokt is T_INT:
        return f"integer ({tok!s})"
    elif tokt is T_DEC:
        return f"decimal ({tok!s})"
    elif tokt is T_STRING:
        if tok[6]:
            return "char"
        else:
            return "string"
    elif tokt is T_WSPACE:
        return "non-newline whitespace"
    elif tokt is T_LINEBREAK:
        return "line break"
    elif tokt is T_EOF:
        return "EOF"
    else:
        return f"symbol {tok[1]}"

def valid_name(tok):
    return tok.value[1] not in {'in'}

def skip_space(parser):
    while (tokt := peek(parser)[0]) is not T_EOF and tokt is T_WSPACE:
        advance(parser)

def skip_linebreak(parser):
    while (tokt := peek(parser)[0]) is not T_EOF and tokt is T_LINEBREAK:
        advance(parser)

def skip_whitespace(parser):
    while (tokt := peek(parser)[0]) is not T_EOF and (tokt is T_WSPACE or tokt is T_LINEBREAK):
        advance(parser)

def skip_whitespace_get_index(parser):
    while (tokt := peek(parser)[0]) is not T_EOF and (tokt is T_WSPACE or tokt is T_LINEBREAK):
        advance(parser)
    return parser.index

def advance(parser, n=1):
    _tmp_advance = parser.stream[parser.index]
    parser.index += n
    return _tmp_advance

def sadvance(parser, n=1):
    skip_space()
    return advance(parser, n)

def ladvance(parser, n=1):
    skip_linebreak()
    return advance(parser, n)

def wadvance(parser, n=1):
    skip_whitespace(parser)
    return advance(parser, n)

def peek(parser, n=1):
    return parser.stream[parser.index + (n - 1)]

def speek(parser, n=1):
    skip_space(parser)
    return peek(parser, n)

def lpeek(parser, n=1):
    skip_linebreak(parser)
    return peek(parser, n)

def wpeek(parser, n=1):
    skip_whitespace(parser)
    return peek(parser, n)

def check(parser, toktype):
    if peek(parser)[0] is toktype:
        return advance(parser)
    return None

def scheck(parser, toktype):
    if speek(parser)[0] is toktype:
        return advance(parser)
    return None

def lcheck(parser, toktype):
    if lpeek(parser)[0] is toktype:
        return advance(parser)
    return None

def wcheck(parser, toktype):
    if wpeek(parser)[0] is toktype:
        return advance(parser)
    return None

def init_node(node_type, *args, start_pos, **kwargs):
    node = node_type(*args, **kwargs)
    node.start_pos = start_pos
    return node

def cleanup(parser):
    parser.index = parser.stack.pop()

def slice_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = expression_rule(parser, indentlevel)
    if not wcheck(parser, T_COLON):
        parser.stack.pop()
        return a
    b = expression_rule(parser, indentlevel)
    if wcheck(parser, T_COLON):
        c = expression_rule(parser, indentlevel)
    else:
        c = None
    return AST_Slice(a, b, c, start_pos=parser.stack.pop())

def slices_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = slice_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    else:
        a = [a]
        append = a.append
        _tmp_a = None
        while wcheck(parser, T_COMMA) and (_tmp_a := slice_rule(parser, indentlevel)):
            append(_tmp_a)
        if not _tmp_a and _tmp_a is not None:
            parser.stack.pop()
            return _tmp_a
        if len(a) == 1:
            return a[0]
        return AST_Tuple(a, frozen=True, without_parens=True, start_pos=parser.stack.pop())

def arg_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = check(parser, T_IDENT)
    if a and not wcheck(parser, T_COLON) or not check(parser, T_EQUAL):
        parser.index = parser.stack[-1]
        a = None
    elif not a and a is not None:
        cleanup(parser)
        return a
    b = expression_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    return AST_Arg(a, b, start_pos=parser.stack.pop())

def args_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = arg_rule(parser, indentlevel)
    if not wcheck(parser, T_COMMA):
        parser.stack.pop()
        if not a and a is None:
            return a
        return [a] if a else []
    else:
        a = [a]
        append = a.append
        _tmp_a = arg_rule(parser, indentlevel)
        while wcheck(parser, T_COMMA):
            if not _tmp_a and _tmp_a is not None:
                return _tmp_a
            append(_tmp_a)
            _tmp_a = arg_rule(parser, indentlevel)
        parser.stack.pop()
        if _tmp_a:
            append(_tmp_a)
        elif _tmp_a is not None:
            return _tmp_a
        return a

def param_rule(parser, indentlevel=0, do_default=True):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = type_spec_rule(parser, indentlevel)
    b = wcheck(parser, T_IDENT)
    if not b and a and len(a.value) == 1:
        b = a.value[0]
        a = None
    if not do_default:
        return AST_Param(a, b, None, start_pos=parser.stack.pop())
    late_bound = None
    if b:
        idx = parser.index
        if wcheck(parser, T_COLON) and check(parser, T_EQUAL):
            late_bound = False
        else:
            parser.index = idx
            if wcheck(parser, T_EQUAL) and check(parser, T_GT):
                late_bound = True
            else:
                parser.index = idx
                return AST_Param(a, b, None, start_pos=parser.stack.pop())
    else:
        cleanup(parser)
        return b
    c = expression_rule(parser, indentlevel)
    print(c)
    if not c:
        cleanup(parser)
        return c
    return AST_Param(a, b, c, start_pos=parser.stack.pop())

def params_rule(parser, indentlevel=0, do_default=True):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = param_rule(parser, indentlevel, do_default=do_default)
    if not a:
        parser.stack.pop()
        return a
    else:
        a = [a]
        append = a.append
        _tmp_a = None
        while wcheck(parser, T_COMMA) and (_tmp_a := param_rule(parser, indentlevel, do_default=do_default)):
            append(_tmp_a)
        parser.stack.pop()
        if not _tmp_a and _tmp_a is not None:
            return _tmp_a
        return a

def capture_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = name_expr_rule(parser, indentlevel)
    parser.stack.pop()
    return a

def block_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = statement_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    else:
        a = [a]
        append = a.append
        _tmp_a = statement_rule(parser, indentlevel)
        while _tmp_a:
            append(_tmp_a)
            _tmp_a = statement_rule(parser, indentlevel)
        parser.stack.pop()
        if _tmp_a is not None:
            return _tmp_a
        return a

def attr_access_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = check(parser, T_IDENT)
    if not a or not wcheck(parser, T_DOT):
        cleanup(parser)
        return None
    b = [a]
    append = b.append
    _tmp_b = check(parser, T_IDENT)
    while _tmp_b:
        append(_tmp_b)
        if not wcheck(parser, T_DOT):
            break
        _tmp_b = check(parser, T_IDENT)
    else:
        cleanup(parser)
        return None
    parser.stack.pop()
    return b

def variations_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LPAREN):
        parser.stack.pop()
        return None
    if wcheck(parser, T_COLON):
        a = wcheck(parser, T_INT)
        if a and (a[2] or a[3]):
            cleanup(parser)
            return None
        if not wcheck(parser, T_COLON) or not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        return AST_ScopeNum(a, start_pos=parser.stack.pop())
    elif wcheck(parser, T_PIPE):
        a = wcheck(parser, T_IDENT)
        if not wcheck(parser, T_PIPE) or not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        return AST_ScopeName(a, start_pos=parser.stack.pop())
    cleanup(parser)
    return None

def name_expr_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = check(parser, T_IDENT)
    if not a:
        parser.stack.pop()
        return None
    b = variations_rule(parser, indentlevel)
    if not b and b is not None:
        parser.stack.pop()
        return b
    return AST_Name(a, b, start_pos=parser.stack.pop())

def type_spec_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = check(parser, T_IDENT)
    if not A:
        cleanup(parser)
        return a
    else:
        a = [a]
        if wcheck(parser, T_PIPE):
            append = a.append
            _tmp_a = check(parser, T_IDENT)
            while _tmp_a:
                append(_tmp_a)
                if not wcheck(parser, T_PIPE):
                    break
                _tmp_a = check(parser, T_IDENT)
            else:
                cleanup(parser)
                return None
        return AST_TypeSpec(a, start_pos=parser.stack.pop())

def target_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if (_tmp_strong := wcheck(parser, T_IDENT)):
        if _tmp_strong[1] == "strong":
            strong = True
        else:
            strong = False
            parser.index -= 1
    else:
        strong = False
    a = type_spec_rule(parser, indentlevel)
    if strong and not a or not a and a is not None:
        cleanup(parser)
        return a
    b = name_expr_rule(parser, indentlevel)
    if not (b and valid_name(b)):
        if a and len(a.value) == 1:
            parser.index = parser.stack[-1]
            b = name_expr_rule(parser, indentlevel)
            if b:
                parser.stack.pop()
                return (strong, None, b)
        cleanup(parser)
        return b
    parser.stack.pop()
    return (strong, a, b)

def targets_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = target_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    else:
        a = [a]
        if wcheck(parser, T_COMMA):
            append = a.append
            _tmp_a = target_rule(parser, indentlevel)
            while _tmp_a:
                append(_tmp_a)
                if not wcheck(parser, T_COMMA):
                    break
                _tmp_a = target_rule(parser, indentlevel)
            if not _tmp_a and _tmp_a is not None:
                cleanup(parser)
                return _tmp_a
        return AST_Targets(a, start_pos=parser.stack.pop())

# MISCELLANEOUS RULES END

def dict_comp_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACE):
        parser.stack.pop()
        return None
    frozen = not not check(parser, T_COLON)
    a = expressions_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    b = expressions_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    c = targets_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    if not wcheck(parser, T_TILDEGT) and (not (tok := check(parser, T_IDENT)) or not tok[1] == "in"):
        cleanup(parser)
        return None
    d = expression_rule(parser, indentlevel)
    if not d:
        cleanup(parser)
        return d
    else:
        d = [d]
        if wcheck(parser, T_COMMA):
            append = d.append
            _tmp_d = expression_rule(parser, indentlevel)
            while _tmp_d:
                append(_tmp_d)
                if not wcheck(parser, T_COMMA):
                    break
                _tmp_d = expression_rule(parser, indentlevel)
            if not _tmp_d and _tmp_d is not None:
                parser.stack.pop()
                return _tmp_d
    if wcheck(parser, T_COLON):
        e = expression_rule(parser, indentlevel)
        if not e:
            cleanup(parser)
            return e
        else:
            e = [e]
            if wcheck(parser, T_COMMA):
                append = e.append
                _tmp_e = expression_rule(parser, indentlevel)
                while _tmp_e:
                    append(_tmp_e)
                    if not wcheck(parser, T_COMMA):
                        break
                    _tmp_e = expression_rule(parser, indentlevel)
                if not _tmp_e and _tmp_e is not None:
                    parser.stack.pop()
                    return _tmp_e
    else:
        e = None
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_DictComp(a, b, c, d, e, frozen=frozen, start_pos=parser.stack.pop())

def set_comp_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACE):
        parser.stack.pop()
        return None
    frozen = not not check(parser, T_COLON)
    a = expressions_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    b = targets_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    if not wcheck(parser, T_TILDEGT) and (not (tok := check(parser, T_IDENT)) or not tok[1] == "in"):
        cleanup(parser)
        return None
    c = expression_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    else:
        c = [c]
        if wcheck(parser, T_COMMA):
            append = c.append
            _tmp_c = expression_rule(parser, indentlevel)
            while _tmp_c:
                append(_tmp_c)
                if not wcheck(parser, T_COMMA):
                    break
                _tmp_c = expression_rule(parser, indentlevel)
            if not _tmp_c and _tmp_c is not None:
                cleanup(parser)
                return _tmp_c
    if wcheck(parser, T_COLON):
        d = expression_rule(parser, indentlevel)
        if not d:
            cleanup(parser)
            return d
        else:
            d = [d]
            if wcheck(parser, T_COMMA):
                append = d.append
                _tmp_d = expression_rule(parser, indentlevel)
                while _tmp_d:
                    append(_tmp_d)
                    if not wcheck(parser, T_COMMA):
                        break
                    _tmp_d = expression_rule(parser, indentlevel)
                if not _tmp_d and _tmp_d is not None:
                    cleanup(parser)
                    return _tmp_d
    else:
        d = None
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_SetComp(a, b, c, d, frozen=frozen, start_pos=parser.stack.pop())

def list_comp_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACKET):
        parser.stack.pop()
        return None
    frozen = not not check(parser, T_COLON)
    a = expressions_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    b = targets_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    print(b)
    if not wcheck(parser, T_TILDEGT) and (not (tok := check(parser, T_IDENT)) or not tok[1] == "in"):
        cleanup(parser)
        return None
    c = expression_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    else:
        c = [c]
        if wcheck(parser, T_COMMA):
            append = c.append
            _tmp_c = expression_rule(parser, indentlevel)
            while _tmp_c:
                append(_tmp_c)
                if not wcheck(parser, T_COMMA):
                    break
                _tmp_c = expression_rule(parser, indentlevel)
            if not _tmp_c and _tmp_c is not None:
                parser.stack.pop()
                return _tmp_c
    if wcheck(parser, T_COLON):
        d = expression_rule(parser, indentlevel)
        if not d:
            cleanup(parser)
            return d
        else:
            d = [d]
            if wcheck(parser, T_COMMA):
                append = d.append
                _tmp_d = expression_rule(parser, indentlevel)
                while _tmp_d:
                    append(_tmp_d)
                    if not wcheck(parser, T_COMMA):
                        break
                    _tmp_d = expression_rule(parser, indentlevel)
                if not _tmp_d and _tmp_d is not None:
                    parser.stack.pop()
                    return _tmp_d
    else:
        d = None
    if not wcheck(parser, T_RBRACKET):
        cleanup(parser)
        return None
    return AST_ListComp(a, b, c, d, frozen=frozen, start_pos=parser.stack.pop())

def tuple_comp_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LPAREN):
        parser.stack.pop()
        return None
    frozen = not check(parser, T_COLON)
    a = expressions_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    b = targets_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    if not wcheck(parser, T_TILDEGT) and (not (tok := check(parser, T_IDENT)) or not tok[1] == "in"):
        cleanup(parser)
        return None
    c = expression_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    else:
        c = [c]
        if wcheck(parser, T_COMMA):
            append = c.append
            _tmp_c = expression_rule(parser, indentlevel)
            while _tmp_c:
                append(_tmp_c)
                if not wcheck(parser, T_COMMA):
                    break
                _tmp_c = expression_rule(parser, indentlevel)
            if not _tmp_c and _tmp_c is not None:
                parser.stack.pop()
                return _tmp_c
    if wcheck(parser, T_COLON):
        d = expression_rule(parser, indentlevel)
        if not d:
            cleanup(parser)
            return d
        else:
            d = [d]
            if wcheck(parser, T_COMMA):
                append = d.append
                _tmp_d = expression_rule(parser, indentlevel)
                while _tmp_d:
                    append(_tmp_d)
                    if not wcheck(parser, T_COMMA):
                        break
                    _tmp_d = expression_rule(parser, indentlevel)
                if not _tmp_d and _tmp_d is not None:
                    parser.stack.pop()
                    return _tmp_d
    else:
        d = None
    if not wcheck(parser, T_RPAREN):
        cleanup(parser)
        return None
    return AST_TupleComp(a, b, c, d, frozen=frozen, start_pos=parser.stack.pop())

def dict_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACE):
        parser.stack.pop()
        return None
    frozen = not not check(parser, T_COLON)
    a = []
    append = a.append
    b = expression_rule(parser, indentlevel)
    if b:
        if not wcheck(parser, T_COLON):
            cleanup(parser)
            return None
        c = expression_rule(parser, indentlevel)
        if not c:
            cleanup(parser)
            return c
        append((b, c))
        while wcheck(parser, T_COMMA) and (b := expression_rule(parser, indentlevel)):
            if not wcheck(parser, T_COLON):
                cleanup(parser)
                return None
            c = expression_rule(parser, indentlevel)
            if not c:
                cleanup(parser)
                return c
            append((b, c))
        if not b and b is not None:
            parser.stack.pop()
            return b
    elif b is not None:
        parser.stack.pop()
        return b
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_Dict(a, frozen=frozen, start_pos=parser.stack.pop())

def set_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACE):
        parser.stack.pop()
        return None
    frozen = not not check(parser, T_COLON)
    a = []
    b = expression_rule(parser, indentlevel)
    if not b:
        if b is not None:
            cleanup(parser)
            return b
        if not wcheck(parser, T_COMMA):
            cleanup(parser)
            return None
    else:
        append = a.append
        append(b)
        while wcheck(parser, T_COMMA) and (b := expression_rule(parser, indentlevel)):
            append(b)
        if not b and b is not None:
            parser.stack.pop()
            return b
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_Set(a, frozen=frozen, start_pos=parser.stack.pop())

def list_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACKET):
        parser.stack.pop()
        return None
    frozen = not not check(parser, T_COLON)
    a = []
    append = a.append
    b = expression_rule(parser, indentlevel)
    if b:
        append(b)
        while wcheck(parser, T_COMMA) and (b := expression_rule(parser, indentlevel)):
            append(b)
        if not b and b is not None:
            parser.stack.pop()
            return b
    elif b is not None:
        parser.stack.pop()
        return b
    if not wcheck(parser, T_RBRACKET):
        cleanup(parser)
        return None
    return AST_List(a, frozen=frozen, start_pos=parser.stack.pop())

def tuple_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LPAREN):
        parser.stack.pop()
        return None
    frozen = not check(parser, T_COLON)
    a = []
    append = a.append
    b = expression_rule(parser, indentlevel)
    if b:
        append(b)
        while (tok := wcheck(parser, T_COMMA)) and (b := expression_rule(parser, indentlevel)):
            append(b)
        if not b and b is not None:
            parser.stack.pop()
            return b
        if not tok and frozen and len(a) == 1:
            cleanup(parser)
            return None
    elif b is not None:
        parser.stack.pop()
        return b
    if not wcheck(parser, T_RPAREN):
        cleanup(parser)
        return None
    return AST_Tuple(a, frozen=frozen, start_pos=parser.stack.pop())

# data types and comprehensions end

def genexpr_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = expressions_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    b = targets_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    if not wcheck(parser, T_TILDEGT) and (not (tok := wcheck(parser, T_IDENT)) or not tok[1] == "in"):
        cleanup(parser)
        return None
    c = expression_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    else:
        c = [c]
        if wcheck(parser, T_COMMA):
            append = c.append
            _tmp_c = expression_rule(parser, indentlevel)
            while _tmp_c:
                append(_tmp_c)
                if not wcheck(parser, T_COMMA):
                    break
                _tmp_c = expression_rule(parser, indentlevel)
            if not _tmp_c and _tmp_c is not None:
                parser.stack.pop()
                return _tmp_c
    if wcheck(parser, T_COLON):
        d = expression_rule(parser, indentlevel)
        if not d:
            cleanup(parser)
            return d
        else:
            d = [d]
            if wcheck(parser, T_COMMA):
                append = d.append
                _tmp_d = expression_rule(parser, indentlevel)
                while _tmp_d:
                    append(_tmp_d)
                    if not wcheck(parser, T_COMMA):
                        break
                    _tmp_d = expression_rule(parser, indentlevel)
                if not _tmp_d and _tmp_d is not None:
                    parser.stack.pop()
                    return _tmp_d
    else:
        d = None
    return AST_GenComp(a, b, c, d, start_pos=parser.stack.pop())

def convenient_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not check(parser, T_PIPE):
        parser.stack.pop()
        return None
    a = params_rule(parser, indentlevel, do_default=False)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_PIPE):
        cleanup(parser)
        return None
    b = expression_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    return AST_Lambda([], None, a, AST_Block([b], start_pos=b.start_pos), is_simple=True, start_pos=parser.stack.pop())

def atom_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if (tok := wcheck(parser, T_IDENT)):
        if tok[1] in {"null", "nil"}:
            return AST_Constant(None, start_pos=parser.stack.pop())
        elif tok[1] == "NAN":
            return AST_NameWithDefault("NAN", default=float('nan'), start_pos=parser.stack.pop())
        elif tok[1] == "INF":
            return AST_NameWithDefault("INF", default=float('inf'), start_pos=parser.stack.pop())
        elif tok[1] == "true":
            return AST_Constant(True, start_pos=parser.stack.pop())
        elif tok[1] == "T":
            return AST_NameWithDefault("T", default=True, start_pos=parser.stack.pop())
        elif tok[1] == "false":
            return AST_Constant(False, start_pos=parser.stack.pop())
        elif tok[1] == "F":
            return AST_NameWithDefault("F", default=False, start_pos=parser.stack.pop())
        else:
            parser.index -= 1
            parser.stack.pop()
            return name_expr_rule(parser, indentlevel)
    elif check(parser, T_CMAT):
        return AST_Modifier(start_pos=parser.stack.pop())
    elif (tok := (check(parser, T_INT) or check(parser, T_DEC))):
        start = tok[-2]
        end = tok[-1]
        lines = parser.source.split('\n')
        lineno = parser.source[:start].count('\n') + 1
        colno = len(parser.source[:start].split('\n')[-1])
        node = cparser(tok, lines[lineno-1], lineno, colno, lines[parser.source[:end].count('\n')])
        if not node:
            cleanup(parser)
            return node
        node.start_pos = parser.stack.pop()
        return node
    elif (tok := check(parser, T_STRING)):
        start = tok[-2]
        end = tok[-1]
        lines = parser.source.split('\n')
        lineno = parser.source[:start].count('\n') + 1
        colno = len(parser.source[:start].split('\n')[-1])
        node = cparser(tok, lines[lineno-1], lineno, colno, lines[parser.source[:end].count('\n')])
        if not node:
            cleanup(parser)
            return node
        node.start_pos = parser.index-1
        a = [node]
        append = a.append
        while (tok := wcheck(parser, T_STRING)):
            start = tok[-2]
            end = tok[-1]
            lines = parser.source.split('\n')
            lineno = parser.source[:start].count('\n') + 1
            colno = len(parser.source[:start].split('\n')[-1])
            node = cparser(tok, lines[lineno-1], lineno, colno, lines[parser.source[:end].count('\n')])
            if not node:
                cleanup(parser)
                return node
            node.start_pos = parser.index-1
            append(node)
        return AST_Strings(a, start_pos=parser.stack.pop())
    elif (toktype := peek(parser)[0]) is T_LPAREN:
        a = tuple_rule(parser, indentlevel) or tuple_comp_rule(parser, indentlevel)
        parser.stack.pop()
        if not a:
            if a is not None:
                return a
            else:
                advance(parser)
                a = expression_rule(parser, indentlevel)
                if not a:
                    return a
                if not wcheck(parser, T_RPAREN):
                    return None
                return a
        else:
            return a
    elif toktype is T_LBRACKET:
        parser.stack.pop()
        return list_rule(parser, indentlevel) or list_comp_rule(parser, indentlevel)
    elif toktype is T_LBRACE:
        parser.stack.pop()
        return set_rule(parser, indentlevel) or dict_rule(parser, indentlevel) or set_comp_rule(parser, indentlevel) or dict_comp_rule(parser, indentlevel) or block_raw_rule(parser, indentlevel)
    elif toktype is T_PIPE:
        parser.stack.pop()
        return convenient_rule(parser, indentlevel)
    cleanup(parser)
    return None

def safe_navigation_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = atom_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_QMARK):
        parser.stack.pop()
        return a
    return AST_UnaryOp(Safe, a, precedence=27, start_pos=parser.stack.pop())

def primary_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    primary_array = []
    primary_append = primary_array.append
    a = safe_navigation_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    op = None
    _tmp_primary = None
    oldidx = parser.index
    if wcheck(parser, T_DOT):
        _tmp_primary = wcheck(parser, T_IDENT)
        if not _tmp_primary:
            cleanup(parser)
            return None
        op = AttrP
    elif check(parser, T_LBRACKET):
        _tmp_primary = slices_rule(parser, indentlevel)
        if not _tmp_primary:
            cleanup(parser)
            return _tmp_primary
        if not wcheck(parser, T_RBRACKET):
            cleanup(parser)
            return None
        op = SubscrP
    elif check(parser, T_LPAREN):
        _tmp_primary = genexpr_rule(parser, indentlevel)
        if _tmp_primary:
            _tmp_primary = [AST_Arg(None, _tmp_primary, start_pos=_tmp_primary.start_pos)]
        else:
            _tmp_primary = args_rule(parser, indentlevel)
        if not _tmp_primary and _tmp_primary is not None:
            cleanup(parser)
            return _tmp_primary
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        op = CallP
    else:
        parser.stack.pop()
        parser.index = oldidx
        return a
    primary_append((op, _tmp_primary))
    while True:
        if wcheck(parser, T_DOT):
            _tmp_primary = wcheck(parser, T_IDENT)
            if not _tmp_primary:
                cleanup(parser)
                return None
            op = AttrP
        elif check(parser, T_LBRACKET):
            _tmp_primary = slices_rule(parser, indentlevel)
            if not _tmp_primary:
                cleanup(parser)
                return _tmp_primary
            if not wcheck(parser, T_RBRACKET):
                cleanup(parser)
                return None
            op = SubscrP
        elif check(parser, T_LPAREN):
            _tmp_primary = genexpr_rule(parser, indentlevel)
            if _tmp_primary:
                _tmp_primary = [AST_Arg(None, _tmp_primary, start_pos=_tmp_primary.start_pos)]
            else:
                _tmp_primary = args_rule(parser, indentlevel)
            if not _tmp_primary and _tmp_primary is not None:
                cleanup(parser)
                return _tmp_primary
            if not wcheck(parser, T_RPAREN):
                cleanup(parser)
                return None
            op = CallP
        else:
            break
        primary_append((op, _tmp_primary))
    return AST_Primary(a, primary_array, start_pos=parser.stack.pop())

def reference_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_AMP):
        a = reference_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(Ref, a, precedence=25, start_pos=parser.stack.pop())
    elif wcheck(parser, T_STAR):
        a = reference_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(Deref, a, precedence=25, start_pos=parser.stack.pop())
    cleanup(parser)
    return primary_rule(parser, indentlevel)

def cast_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_LT):
        a = type_spec_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            if a is None:
                return reference_rule(parser, indentlevel)
            else:
                return a
        if not wcheck(parser, T_GT):
            cleanup(parser)
            return reference_rule(parser, indentlevel)
        b = reference_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            if b is None:
                return reference_rule(parser, indentlevel)
            else:
                return b
        return AST_Cast(a, b, start_pos=parser.stack.pop())
    cleanup(parser)
    return reference_rule(parser, indentlevel)

def range_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = cast_rule(parser, indentlevel)
    if not a and a is not None:
        cleanup(parser)
        return a
    oldidx = parser.index
    end_exclusive = False
    frozen = False
    if wcheck(parser, T_MINUSGT):
        end_exclusive = True
    elif wcheck(parser, T_COLONGT):
        end_exclusive = True
        frozen = True
    elif wcheck(parser, T_COLONDOT):
        frozen = True
    elif not wcheck(parser, T_DBLDOT):
        parser.index = oldidx
        parser.stack.pop()
        return a
    b = cast_rule(parser, indentlevel)
    if not b and b is not None:
        cleanup(parser)
        return b
    return AST_Range(a, b, end_exclusive=end_exclusive, frozen=frozen, start_pos=parser.stack.pop())

def length_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_TAG):
        a = length_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(Len, a, precedence=22, start_pos=parser.stack.pop())
    cleanup(parser)
    return range_rule(parser, indentlevel)

def factorial_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = length_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while wcheck(parser, T_EXCLMARK):
        res = AST_UnaryOp(Fact, res, precedence=21, start_pos=pos)
    parser.stack.pop()
    return res

def hypop_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = factorial_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if wpeek(parser)[0] is T_LBRACE and peek(parser, 2)[0] is T_PIPE:
        b = expression_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        if not (wcheck(parser, T_PIPE) and check(parser, T_RBRACE)):
            cleanup(parser)
            return None
        c = factor_rule(parser, indentlevel)
        if not c:
            cleanup(parser)
            return c
        return AST_TernOp(THyp, a, b, c, precedence=20, start_pos=parser.stack.pop())
    elif check(parser, T_CARET):
        b = factor_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        return AST_BinOp(a, Pow, b, precedence=20, start_pos=parser.stack.pop())
    parser.stack.pop()
    return a

def factor_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_MINUS):
        a = factor_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(USub, a, precedence=19, start_pos=parser.stack.pop())
    elif check(parser, T_PLUS):
        a = factor_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(UAdd, a, precedence=19, start_pos=parser.stack.pop())
    elif check(parser, T_TILDE):
        a = factor_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(Invert, a, precedence=19, start_pos=parser.stack.pop())
    cleanup(parser)
    return hypop_rule(parser, indentlevel)

def operator_inversion_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_EXCLMARK):
        a = operator_inversion_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        return AST_UnaryOp(Not, a, precedence=18, start_pos=parser.stack.pop())
    cleanup(parser)
    return factor_rule(parser, indentlevel)

def term_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = operator_inversion_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_STAR):
            op = Mul
        elif check(parser, T_DBLSLASH):
            op = FDiv
        elif check(parser, T_SLASH):
            op = Div
        elif check(parser, T_PERCENT):
            op = Mod
        elif check(parser, T_DBLBACKSLASH):
            op = CDiv
        else:
            break
        b = operator_inversion_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=17, start_pos=pos)
    parser.stack.pop()
    return res

def common_shift_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = term_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_DBLLT):
            op = BLS
        elif check(parser, T_DBLGT):
            op = BRS
        elif peek(parser)[0] is T_LT and peek(parser, 2)[0] is T_GT:
            advance(parser, 2)
            op = BLR
        elif peek(parser)[0] is T_GT and peek(parser, 2)[0] is T_LT:
            advance(parser, 2)
            op = BRR
        else:
            break
        b = term_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=16, start_pos=pos)
    parser.stack.pop()
    return res

def arith_shift_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = common_shift_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_TRPLLT):
            op = ALS
        elif check(parser, T_TRPLGT):
            op = ARS
        else:
            break
        b = common_shift_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=15, start_pos=pos)
    parser.stack.pop()
    return res

def bitwise_and_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = arith_shift_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_AMP):
            op = BAnd
        elif check(parser, T_TILDEAMP):
            op = BNAnd
        else:
            break
        b = arith_shift_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=14, start_pos=pos)
    parser.stack.pop()
    return res

def bitwise_xor_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = bitwise_and_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_DOLLAR):
            op = BXor
        elif check(parser, T_TILDEDOLLAR):
            op = BNXor
        else:
            break
        b = bitwise_and_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=13, start_pos=pos)
    parser.stack.pop()
    return res

def bitwise_or_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = bitwise_xor_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_PIPE):
            op = BOr
        elif check(parser, T_TILDEPIPE):
            op = BNOr
        else:
            break
        b = bitwise_xor_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=12, start_pos=pos)
    parser.stack.pop()
    return res

def sum_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = bitwise_or_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while True:
        op = None
        if wcheck(parser, T_PLUS):
            op = Add
        elif check(parser, T_MINUS):
            op = Sub
        else:
            break
        b = bitwise_or_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, op, b, precedence=11, start_pos=pos)
    parser.stack.pop()
    return res

def composition_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = sum_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    res = a
    while wcheck(parser, T_CMAT):
        b = sum_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, Comp, b, precedence=10, start_pos=pos)
    parser.stack.pop()
    return res

def threeway_comparison_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not check(parser, T_LTEQUALGT):
        cleanup(parser)
        return None
    a = composition_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    parser.stack.pop()
    return (RichCmp, a)

def common_comparison_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    op = None
    if wcheck(parser, T_DBLEQUAL):
        op = Eq
    elif check(parser, T_EXCLMARKEQUAL):
        op = NotEq
    elif check(parser, T_LT):
        op = LT
    elif check(parser, T_GT):
        op = GT
    elif check(parser, T_LTEQUAL):
        op = LTE
    elif check(parser, T_GTEQUAL):
        op = GTE
    else:
        cleanup(parser)
        return None
    a = composition_rule(parser, indentlevel)
    if not a:
        return a
    parser.stack.pop()
    return (op, a)

def exact_comparison_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    op = None
    if (tok := wcheck(parser, T_IDENT)):
        if tok[1] == "is":
            op = Is
        elif tok[1] == "nis":
            op = IsNot
        else:
            cleanup(parser)
            return None
    elif check(parser, T_TAGEQUAL):
        op = Is
    elif check(parser, T_TAGEXCLMARK):
        op = IsNot
    else:
        cleanup(parser)
        return None
    a = composition_rule(parser, indentlevel)
    if not a:
        return a
    parser.stack.pop()
    return (op, a)

def membership_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    op = None
    if (tok := wcheck(parser, T_IDENT)):
        if tok[1] == "in":
            op = In
        elif tok[1] == "nin":
            op = NotIn
        else:
            cleanup(parser)
            return None
    elif check(parser, T_TILDEGT):
        op = In
    elif check(parser, T_TILDEEXCLMARK):
        op = NotIn
    else:
        cleanup(parser)
        return None
    a = composition_rule(parser, indentlevel)
    if not a:
        return a
    parser.stack.pop()
    return (op, a)

def comparison_rule(parser, indentlevel=0):
    return membership_rule(parser, indentlevel) or exact_comparison_rule(parser, indentlevel) or common_comparison_rule(parser, indentlevel) or threeway_comparison_rule(parser, indentlevel)

def comparisons_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = composition_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    b = []
    append = b.append
    while (_tmp_b := comparison_rule(parser, indentlevel)):
        append(_tmp_b)
    if not _tmp_b and _tmp_b is not None:
        cleanup(parser)
        return None
    if not b:
        parser.stack.pop()
        return a
    return AST_Compare(a, b, start_pos=parser.stack.pop())

def conjunction_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = comparisons_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = []
    append = b.append
    while True:
        op = None
        idx = parser.index
        if (tok := wcheck(parser, T_IDENT)):
            if tok[1] == "and":
                op = LAnd
            elif tok[1] == "nand":
                op = LNAnd
            else:
                parser.index = idx
                parser.stack.pop()
                return a
        elif check(parser, T_DBLAMP):
            op = LAnd
        elif check(parser, T_EXCLMARK) and check(parser, T_DBLAMP):
            op = LNAnd
        else:
            break
        c = comparisons_rule(parser, indentlevel)
        if not c:
            cleanup(parser)
            return c
        append((op, c))
    if not b:
        parser.index = idx
        parser.stack.pop()
        return a
    return AST_BoolOp(a, And, b, precedence=8, start_pos=parser.stack.pop())

def keyword_inversion_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not (tok := check(parser, T_IDENT)) or not tok[1] == "not":
        cleanup(parser)
        return conjunction_rule(parser, indentlevel)
    a = conjunction_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_UnaryOp(Not, a, precedence=7, start_pos=parser.stack.pop())

def excl_disjunction_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = keyword_inversion_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = []
    append = b.append
    while True:
        op = None
        idx = parser.index
        if (tok := wcheck(parser, T_IDENT)):
            if tok[1] == "xor":
                op = LOr
            elif tok[1] == "nxor":
                op = LNOr
            else:
                parser.index = idx
                parser.stack.pop()
                return a
        elif check(parser, T_DBLDOLLAR):
            op = LXor
        elif check(parser, T_EXCLMARK) and check(parser, T_DBLDOLLAR):
            op = LNXor
        else:
            break
        c = keyword_inversion_rule(parser, indentlevel)
        if not c:
            cleanup(parser)
            return c
        append((op, c))
    if not b:
        parser.index = idx
        parser.stack.pop()
        return a
    return AST_BoolOp(a, Xor, b, precedence=6, start_pos=parser.stack.pop())

def disjunction_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = excl_disjunction_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = []
    append = b.append
    while True:
        op = None
        idx = parser.index
        if (tok := wcheck(parser, T_IDENT)):
            if tok[1] == "or":
                op = LOr
            elif tok[1] == "nor":
                op = LNOr
            else:
                parser.index = idx
                parser.stack.pop()
                return a
        elif check(parser, T_DBLPIPE):
            op = LOr
        elif check(parser, T_EXCLMARK) and check(parser, T_DBLPIPE):
            op = LNOr
        else:
            break
        c = excl_disjunction_rule(parser, indentlevel)
        if not c:
            cleanup(parser)
            return c
        append((op, c))
    if not b:
        parser.index = idx
        parser.stack.pop()
        return a
    return AST_BoolOp(a, Or, b, precedence=5, start_pos=parser.stack.pop())

def coalesce_rule(parser, indentlevel=0):
    parser.stack.append(pos := skip_whitespace_get_index(parser))
    a = disjunction_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    res = a
    while wcheck(parser, T_DBLQMARK):
        b = disjunction_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        res = AST_BinOp(res, Clsc, b, precedence=4, start_pos=pos)
    parser.stack.pop()
    return res

def ternary_expr_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = coalesce_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_QMARK):
        parser.stack.pop()
        return a
    b = ternary_expr_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    c = ternary_expr_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    return AST_TernOp(TTern, a, b, c, precedence=3, start_pos=parser.stack.pop())

def choose_expr_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = ternary_expr_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    op = None
    if wcheck(parser, T_EQUALLT):
        op = Also
    elif wcheck(parser, T_EQUALGT):
        op = Then
    else:
        parser.stack.pop()
        return a
    b = choose_expr_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    return AST_BinOp(a, op, b, precedence=2, start_pos=parser.stack.pop())

def augmented_assignment_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = targets_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    b = None
    op = None
    third = None
    if wcheck(parser, T_DOTEQUAL):
        b = check(parser, T_IDENT)
        op = Attr
    elif ((start_idx := parser.index), check(parser, T_LBRACKET) and check(parser, T_EQUAL))[1]:
        b = slices_rule(parser, indentlevel)
        if not wcheck(parser, T_RBRACKET):
            cleanup(parser)
            return None
        op = Subscr
    elif check(parser, T_LPAREN) and check(parser, T_EQUAL):
        b = args_rule(parser, indentlevel)
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        op = Call
    elif check(parser, T_LBRACE):
        third = expression_rule(parser, indentlevel)
        if not third:
            cleanup(parser)
            return third
        if not wcheck(parser, T_RBRACE):
            cleanup(parser)
            return None
        if not wcheck(parser, T_EQUAL):
            cleanup(parser)
            return None
        b = expressions_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        op = Hyp
    elif ((check(parser, T_CARETEQUAL) and (op := Pow))
          or (check(parser, T_STAREQUAL) and (op := Mul))
          or (check(parser, T_DBLSLASHEQUAL) and (op := FDiv))
          or (check(parser, T_SLASHEQUAL) and (op := Div))
          or (check(parser, T_PERCENTEQUAL) and (op := Mod))
          or (check(parser, T_DBLBACKSLASHEQUAL) and (op := CDiv))
          or (check(parser, T_DBLLTEQUAL) and (op := BLS))
          or (check(parser, T_DBLGTEQUAL) and (op := BRS))
          or (check(parser, T_LTGTEQUAL) and (op := BLR))
          or (check(parser, T_GTLTEQUAL) and (op := BRR))
          or (check(parser, T_TRPLLTEQUAL) and (op := ALS))
          or (check(parser, T_TRPLGTEQUAL) and (op := ARS))
          or (check(parser, T_AMPEQUAL) and (op := BAnd))
          or (check(parser, T_TILDEAMPEQUAL) and (op := BNAnd))
          or (check(parser, T_DOLLAREQUAL) and (op := BXor))
          or (check(parser, T_TILDEDOLLAREQUAL) and (op := BNXor))
          or (check(parser, T_PIPEEQUAL) and (op := BOr))
          or (check(parser, T_TILDEPIPEEQUAL) and (op := BNOr))
          or (check(parser, T_PLUSEQUAL) and (op := Add))
          or (check(parser, T_MINUSEQUAL) and (op := Sub))
          or (check(parser, T_CMATEQUAL) and (op := Comp))
          or (check(parser, T_EXCLMARK) and check(parser, T_DBLAMPEQUAL) and (op := BinNAnd))
              or setattr(parser, 'index', start_idx)
          or (check(parser, T_EXCLMARK) and check(parser, T_DBLDOLLAREQUAL) and (op := BinNXor))
              or setattr(parser, 'index', start_idx)
          or (check(parser, T_EXCLMARK) and (check(parser, T_DBLPIPEEQUAL) or check(parser, T_QMARKCOLONEQUAL)) and (op := BinNOr))
              or setattr(parser, 'index', start_idx)
          or (check(parser, T_DBLAMPEQUAL) and (op := BinAnd))
          or (check(parser, T_DBLDOLLAREQUAL) and (op := BinXor))
          or ((check(parser, T_DBLPIPEEQUAL) or check(parser, T_QMARKCOLONEQUAL)) and (op := BinOr))
          or (check(parser, T_DBLQMARKEQUAL) and (op := Clsc))
          or (check(parser, T_QMARKEQUAL) and (op := TAnd))):
        b = expressions_rule(parser, indentlevel)
    else:
        cleanup(parser)
        return None
    if not b:
        cleanup(parser)
        return b
    return AST_AugAssignment(a, op, b, third, start_pos=parser.stack.pop())

def assignment_expr_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = targets_rule(parser, indentlevel)
    if not a:
        parser.stack.pop()
        return a
    if not wcheck(parser, T_EQUAL):
        cleanup(parser)
        return augmented_assignment_rule(parser, indentlevel)
    b = expressions_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    return AST_Assignment(a, b, start_pos=parser.stack.pop())

def unpack_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    op = None
    if check(parser, T_CMAT):
        op = SeqUnpack
    elif check(parser, T_DOLLAR):
        op = MapUnpack
    else:
        parser.index = parser.stack.pop()
        return assignment_expr_rule(parser, indentlevel) or choose_expr_rule(parser, indentlevel)
    a = assignment_expr_rule(parser, indentlevel) or choose_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_UnaryOp(op, a, precedence=0, start_pos=parser.stack.pop())

def lambda_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = []
    if check(parser, T_LBRACKET):
        if (_tmp_a := capture_rule(parser, indentlevel)):
            a = [_tmp_a]
            append = a.append
            while wcheck(parser, T_SEMICOLON):
                _tmp_a = capture_rule(parser, indentlevel)
                if not _tmp_a:
                    if _tmp_a is not None:
                        cleanup(parser)
                        return _tmp_a
                    break
                append(_tmp_a)
        elif _tmp_a is not None:
            cleanup(parser)
            return _tmp_a
        if not wcheck(parser, T_RBRACKET):
            cleanup(parser)
            return None
    b = []
    can_reparse = False
    if wcheck(parser, T_LPAREN):
        oldidx = parser.index
        append = b.append
        while (_tmp_b := type_spec_rule(parser, indentlevel)):
            append(_tmp_b)
            if not wcheck(parser, T_COMMA):
                break
        if not b and b is not None:
            cleanup(parser)
            return b
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        can_reparse = all([len(x.value) == 1 for x in b])
    else:
        b = type_spec_rule(parser, indentlevel)
        if not b and b is not None:
            cleanup(parser)
            return b
        elif b:
            b = [b]
    if not wcheck(parser, T_LPAREN):
        if can_reparse:
            parser.index = oldidx
            b.clear()
        else:
            cleanup(parser)
            return None
    c = params_rule(parser, indentlevel)
    if not c and c is not None:
        cleanup(parser)
        return c
    if not wcheck(parser, T_RPAREN):
        cleanup(parser)
        return None
    if not wcheck(parser, T_COLON):
        cleanup(parser)
        return None
    d = block_raw_rule(parser, indentlevel+1, True) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
    if not d:
        cleanup(parser)
        return d
    return AST_Lambda(a, b, c, d, is_simple=False, start_pos=parser.stack.pop())

def expression_rule(parser, indentlevel=0):
    return lambda_rule(parser, indentlevel) or unpack_rule(parser, indentlevel)

def expressions_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = expression_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_COMMA):
        parser.stack.pop()
        return a
    a = [a]
    append = a.append
    while (_tmp_a := expression_rule(parser, indentlevel)):
        append(_tmp_a)
        if not wcheck(parser, T_COMMA):
            break
    if not _tmp_a and _tmp_a is not None:
        cleanup(parser)
        return _tmp_a
    return AST_Tuple(a, frozen=True, without_parens=True, start_pos=parser.stack.pop())

# EXPRESSIONS END

def incl_valid_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = check(parser, T_IDENT) or attr_access_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = None
    if wcheck(parser, T_LBRACKET):
        b = wcheck(parser, T_STRING) or check(parser, T_STAR)
        if not b:
            cleanup(parser)
            return None
        b = b[1]
        if not wcheck(parser, T_RBRACKET):
            cleanup(parser)
            return None
        return AST_AttrIncl(a, b, start_pos=parser.stack.pop())
    elif wcheck(parser, T_DOT):
        b = wcheck(parser, T_STAR)
        if not b:
            cleanup(parser)
            return None
        b = b[1]
        return AST_AttrIncl(a + [b], start_pos=parser.stack.pop())
    else:
        return AST_AttrIncl(a, start_pos=parser.stack.pop())

def incl_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'incl'):
        cleanup(parser)
        return None
    a = []
    append = a.append
    b = incl_valid_rule(parser, indentlevel)
    if b:
        idx = parser.index
        if wcheck(parser, T_EQUAL) and wcheck(parser, T_LPAREN):
            c = targets_rule(parser, indentlevel)
            if not c:
                cleanup(parser)
                return c
            if not wcheck(parser, T_RPAREN):
                cleanup(parser)
                return None
        else:
            parser.index = idx
            c = None
        append((b, c))
        while wcheck(parser, T_COMMA) and (b := incl_valid_rule(parser, indentlevel)):
            idx = parser.index
            if wcheck(parser, T_EQUAL) and wcheck(parser, T_LPAREN):
                c = targets_rule(parser, indentlevel)
                if not c:
                    cleanup(parser)
                    return c
                if not wcheck(parser, T_RPAREN):
                    cleanup(parser)
                    return None
            else:
                parser.index = idx
                c = None
            append((b, c))
        if not b and b is not None:
            cleanup(parser)
            return b
        return AST_InclStmt(a, start_pos=parser.stack.pop())
    else:
        cleanup(parser)
        return None

def use_valid_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = attr_access_rule(parser, indentlevel)
    can_standalone = False
    if a:
        can_standalone = True
    elif a is not None:
        cleanup(parser)
        return a
    else:
        a = check(parser, T_IDENT)
        if not a:
            cleanup(parser)
            return a
    b = None
    if wcheck(parser, T_LBRACKET):
        b = wcheck(parser, T_STRING) or check(parser, T_STAR)
        if not b:
            cleanup(parser)
            return None
        b = b[1]
        if not wcheck(parser, T_RBRACKET):
            cleanup(parser)
            return None
        return AST_SubscrUse(a, b, start_pos=parser.stack.pop())
    elif can_standalone:
        return AST_AttrUse(a, start_pos=parser.stack.pop())
    cleanup(parser)
    return None

def use_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'use'):
        cleanup(parser)
        return None
    a = []
    append = a.append
    b = use_valid_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    idx = parser.index
    if wcheck(parser, T_EQUAL) and wcheck(parser, T_LPAREN):
        c = targets_rule(parser, indentlevel)
        if not c:
            cleanup(parser)
            return c
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
    elif isinstance(b, list):
        parser.index = idx
        c = None
    else:
        cleanup(parser)
        return None
    append((b, c))
    while wcheck(parser, T_COMMA) and (b := use_valid_rule(parser, indentlevel)):
        if wcheck(parser, T_EQUAL) and wcheck(parser, T_LPAREN):
            c = targets_rule(parser, indentlevel)
            if not c:
                cleanup(parser)
                return c
            if not wcheck(parser, T_RPAREN):
                cleanup(parser)
                return None
        elif isinstance(b, list):
            parser.index = idx
            c = None
        else:
            cleanup(parser)
            return None
        append((b, c))
    if not b and b is not None:
        cleanup(parser)
        return b
    return AST_UseStmt(a, start_pos=parser.stack.pop())

def dcl_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = wpeek(parser)
    if a and a[0] == T_IDENT and a[1] == 'dcl':
        advance(parser)
        a = None
    else:
        a = type_spec_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
    b = []
    append = b.append
    c = name_expr_rule(parser, indentlevel)
    if not c:
        cleanup(parser)
        return c
    append(c)
    while wcheck(parser, T_COMMA) and (c := name_expr_rule(parser, indentlevel)):
        append(c)
    if not c:
        cleanup(parser)
        return c
    return AST_DclStmt(a, b, start_pos=parser.stack.pop())

def del_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'del'):
        cleanup(parser)
        return None
    a = []
    append = a.append
    b = name_expr_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    append(b)
    while wcheck(parser, T_COMMA):
        b = name_expr_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
        append(b)
    return AST_DelStmt(a, start_pos=parser.stack.pop())

def label_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wpeek(parser))[0] is T_IDENT and tok == 'label' and advance(parser)
            or tok[0] is T_COLON and advance(parser) and check(parser, T_COLON)):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_LabelStmt(a, start_pos=parser.stack.pop())

def goto_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'goto'):
        a = name_expr_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        if not wcheck(parser, T_COLON) and check(parser, T_COLON):
            cleanup(parser)
            return None
    else:
        a = name_expr_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
    return AST_GotoStmt(a, start_pos=parser.stack.pop())

def break_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'break'):
        cleanup(parser)
        return None
    a = variations_rule(parser, indentlevel)
    if not a and a is not None:
        cleanup(parser)
        return a
    return AST_BreakStmt(a, start_pos=parser.stack.pop())

def cont_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'cont'):
        cleanup(parser)
        return None
    a = variations_rule(parser, indentlevel)
    if not a and a is not None:
        cleanup(parser)
        return a
    return AST_ContStmt(a, start_pos=parser.stack.pop())

def ret_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'ret'):
        cleanup(parser)
        return None
    a = variations_rule(parser, indentlevel)
    if not a and a is not None:
        cleanup(parser)
        return a
    b = expressions_rule(parser, indentlevel)
    if not b and b is not None:
        cleanup(parser)
        return b
    return AST_RetStmt(a, b, implicit=False, start_pos=parser.stack.pop())

def enum_dcl_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'enum'):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_EnumDcl(a, start_pos=parser.stack.pop())

def union_dcl_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'union'):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_UnionDcl(a, start_pos=parser.stack.pop())

def struct_dcl_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'struct'):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_StructDcl(a, start_pos=parser.stack.pop())

def func_dcl_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_LPAREN):
        a = type_spec_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        a = [a]
        append = a.append
        _tmp_a = None
        while wcheck(parser, T_COMMA) and (_tmp_a := type_spec_rule(parser, indentlevel)):
            append(_tmp_a)
        if not _tmp_a and _tmp_a is not None:
            cleanup(parser)
            return _tmp_a
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
    elif (tok := peek(parser))[0] is T_IDENT and tok == 'dcl':
        advance(parser)
        a = None
    elif (a := type_spec_rule(parser, indentlevel)):
        a = [a]
    else:
        cleanup(parser)
        return a
    b = name_expr_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    if not wcheck(parser, T_LPAREN):
        cleanup(parser)
        return None
    c = params_rule(parser, indentlevel)
    if not c and c is not None:
        cleanup(parser)
        return c
    if not wcheck(parser, T_RPAREN):
        cleanup(parser)
        return None
    return AST_FuncDcl(a, b, c, start_pos=parser.stack.pop())

# SIMPLE STATEMENTS END

def block_raw_rule(parser, indentlevel=0, is_func=False):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not wcheck(parser, T_LBRACE):
        cleanup(parser)
        return None
    a = block_rule(parser, indentlevel)
    if not a and a is not None:
        cleanup(parser)
        return a
    elif not a:
        a = []
    if is_func:
        if a:
            last_stmt = a[-1]
            if isinstance(last_stmt, AST_Expr):
                a[-1] = AST_RetStmt(None, last_stmt.value, implicit=True, start_pos=last_stmt.start_pos)
            elif not isinstance(last_stmt, AST_RetStmt):
                a.append(AST_RetStmt(None, None, implicit=True))
        else:
            a.append(AST_RetStmt(None, None, implicit=True))
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    res = AST_Block(a, indentlevel=indentlevel, start_pos=parser.stack.pop())
    return res

def enum_field_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = check(parser, T_IDENT)
    if not a:
        cleanup(parser)
        return None
    if wcheck(parser, T_EQUAL):
        b = expression_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
    else:
        b = None
    return AST_EnumField(a, b, start_pos=parser.stack.pop())

def enum_def_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'enum'):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_LBRACE):
        cleanup(parser)
        return None
    b = []
    append = b.append
    _tmp_b = enum_field_rule(parser, indentlevel)
    if _tmp_b:
        append(_tmp_b)
        while wcheck(parser, T_COMMA) and (_tmp_b := enum_field_rule(parser, indentlevel)):
            append(_tmp_b)
        if not _tmp_b and _tmp_b is not None:
            cleanup(parser)
            return _tmp_b
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_EnumDef(a, b, start_pos=parser.stack.pop())

def field_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = type_spec_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = wcheck(parser, T_IDENT)
    if not b:
        cleanup(parser)
        return None
    if not wcheck(parser, T_SEMICOLON):
        cleanup(parser)
        return None
    return AST_Field(a, b, start_pos=parser.stack.pop())

def union_def_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'union'):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_LBRACE):
        cleanup(parser)
        return None
    b = []
    append = b.append
    _tmp_b = field_rule(parser, indentlevel)
    if _tmp_b:
        append(_tmp_b)
        while wcheck(parser, T_COMMA) and (_tmp_b := field_rule(parser, indentlevel)):
            append(_tmp_b)
        if not _tmp_b and _tmp_b is not None:
            cleanup(parser)
            return _tmp_b
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_UnionDef(a, b, start_pos=parser.stack.pop())

def struct_def_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'struct'):
        cleanup(parser)
        return None
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_LBRACE):
        cleanup(parser)
        return None
    b = []
    append = b.append
    _tmp_b = field_rule(parser, indentlevel)
    if _tmp_b:
        append(_tmp_b)
        while wcheck(parser, T_COMMA) and (_tmp_b := field_rule(parser, indentlevel)):
            append(_tmp_b)
        if not _tmp_b and _tmp_b is not None:
            cleanup(parser)
            return _tmp_b
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_StructDef(a, b, start_pos=parser.stack.pop())

def switch_cases_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'case'):
        cleanup(parser)
        return None
    a = expression_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    idx = parser.index
    if (tok := wcheck(parser, T_IDENT)) and tok[1] == 'as':
        b = targets_rule(parser, indentlevel)
        if not b:
            cleanup(parser)
            return b
    else:
        parser.index = idx
        b = None
    c = []
    append = c.append
    while (tok := wpeek(parser))[0] is T_IDENT and tok[1] == 'if' and advance(parser):
        d = expression_rule(parser, indentlevel)
        if not d:
            cleanup(parser)
            return d
        append(d)
    d = block_raw_rule(parser, indentlevel+1)
    if not d:
        cleanup(parser)
        return d
    return AST_SwitchCaseStmt(a, b, c, d, start_pos=parser.stack.pop())

def switch_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'switch'):
        cleanup(parser)
        return None
    a = expression_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_LBRACE):
        cleanup(parser)
        return None
    b = []
    append = b.append
    _tmp_b = switch_cases_rule(parser, indentlevel)
    if _tmp_b:
        append(_tmp_b)
        while (_tmp_b := switch_cases_rule(parser, indentlevel)):
            append(_tmp_b)
        if not _tmp_b and _tmp_b is not None:
            cleanup(parser)
            return _tmp_b
    if not wcheck(parser, T_RBRACE):
        cleanup(parser)
        return None
    return AST_SwitchStmt(a, b, start_pos=parser.stack.pop())

def if_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'if'):
        cleanup(parser)
        return None
    a = expression_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = block_raw_rule(parser, indentlevel+1)
    if not b:
        cleanup(parser)
        return b
    c = [(a, b)]
    append = c.append
    while (tok := wpeek(parser))[0] is T_IDENT and tok[1] == 'elif' and advance(parser):
        d = expression_rule(parser, indentlevel)
        if not d:
            cleanup(parser)
            return d
        e = block_raw_rule(parser, indentlevel+1)
        if not e:
            cleanup(parser)
            return e
        append((d, e))
    if (tok := wpeek(parser))[0] is T_IDENT and tok[1] == 'else':
        advance(parser)
        f = block_raw_rule(parser, indentlevel+1)
        if not f:
            cleanup(parser)
            return f
        append((True, f))
    return AST_IfStmt(c, start_pos=parser.stack.pop())

def func_def_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if wcheck(parser, T_LBRACKET):
        e = []
        _tmp_e = capture_rule(parser, indentlevel)
        if _tmp_e:
            append = e.append
            append(_tmp_e)
            while wcheck(parser, T_SEMICOLON) and (_tmp_e := capture_rule(parser, indentlevel)):
                append(_tmp_e)
            if not _tmp_e and _tmp_e is not None:
                cleanup(parser)
                return _tmp_e
        elif _tmp_e is not None:
            cleanup(parser)
            return _tmp_e
        if not wcheck(parser, T_RBRACKET):
            cleanup(parser)
            return None
    else:
        e = []
    if wcheck(parser, T_LPAREN):
        a = []
        append = a.append
        _tmp_a = type_spec_rule(parser, indentlevel)
        if not _tmp_a:
            cleanup(parser)
            return _tmp_a
        append(_tmp_a)
        while wcheck(parser, T_COMMA) and (_tmp_a := type_spec_rule(parser, indentlevel)):
            append(_tmp_a)
        if not _tmp_a and _tmp_a is not None:
            cleanup(parser)
            return _tmp_a
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        can_reparse = 0
    else:
        idx = parser.index
        a = type_spec_rule(parser, indentlevel)
        if not a:
            cleanup(parser)
            return a
        can_reparse = len(a.value) == 1
        a = [a]
    b = wcheck(parser, T_IDENT)
    if not b:
        if can_reparse:
            parser.index = idx
            a = None
            b = wcheck(parser, T_IDENT)
        else:
            cleanup(parser)
            return None
    is_op = False
    if b[1] == 'op':
        tok = wpeek(parser)
        toktype = tok[0]
        if toktype is T_LPAREN:
            advance(parser)
            if not wcheck(parser, T_RPAREN):
                advance(parser, -1)
            else:
                is_op = True
                b = '()'
        elif toktype is T_LBRACKET:
            advance(parser)
            if not wcheck(parser, T_RBRACKET):
                cleanup(parser)
                return None
            is_op = False
            b = '[]'
        elif 0 <= toktype < T_IDENT and toktype not in {82, 83}:
            is_op = True
            advance(parser)
            b = tok[1]
    if not wcheck(parser, T_LPAREN):
        cleanup(parser)
        return None
    c = params_rule(parser, indentlevel)
    if not c and c is not None:
        cleanup(parser)
        return c
    if not wcheck(parser, T_RPAREN):
        cleanup(parser)
        return None
    if not is_op:
        b, c = [b], [c]
        append1 = b.append
        append2 = c.append
        broke = 0
        while (d := wcheck(parser, T_IDENT)):
            if not wcheck(parser, T_LPAREN):
                broke = 1
                break
            e = params_rule(parser, indentlevel)
            if not e and e is not None:
                cleanup(parser)
                return e
            if not wcheck(parser, T_RPAREN):
                cleanup(parser)
                return None
            append1(d)
            append2(e)
        if broke:
            append1(d)
    d = None if is_op else variations_rule(parser, indentlevel)
    if not d and d is not None:
        cleanup(parser)
        return d
    f = block_raw_rule(parser, indentlevel+1, True) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
    if not f:
        cleanup(parser)
        return f
    return AST_FuncDef(a, b, c, e, f, d, is_op=is_op, start_pos=parser.stack.pop())

def for_loop_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not ((tok := wcheck(parser, T_IDENT)) and tok[1] == 'for'):
        cleanup(parser)
        return None
    if wcheck(parser, T_LPAREN):
        a = statement_rule(parser, indentlevel)
        if not a and a is not None:
            cleanup(parser)
            return a
        if not wcheck(parser, T_COLON):
            cleanup(parser)
            return None
        b = expression_rule(parser, indentlevel)
        if not b and b is not None:
            cleanup(parser)
            return b
        if not wcheck(parser, T_COLON):
            cleanup(parser)
            return None
        c = statement_rule(parser, indentlevel)
        if not c and c is not None:
            cleanup(parser)
            return c
        if not wcheck(parser, T_RPAREN):
            cleanup(parser)
            return None
        d = block_raw_rule(parser, indentlevel+1) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
        if not d:
            cleanup(parser)
            return d
        return AST_CForStmt(a, b, c, d, start_pos=parser.stack.pop())
    idx = parser.index
    a = expression_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    b = block_raw_rule(parser, indentlevel+1) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
    if not b:
        parser.index = idx
        a = targets_rule(parser, indentlevel)
        print(a)
        if not a:
            cleanup(parser)
            return a
        if (tok := wpeek(parser))[0] is T_IDENT and tok[1] == 'in':
            advance(parser)
        elif not check(parser, T_TILDEGT):
            cleanup(parser)
            return None
        print(parser.stream[parser.index:parser.index+5])
        b = expression_rule(parser, indentlevel)
        print(parser.stream[parser.index:parser.index+5], expression_rule(parser, indentlevel))
        if not b:
            cleanup(parser)
            return b
        c = block_raw_rule(parser, indentlevel+1) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
        print(c)
        if not c:
            cleanup(parser)
            return c
        return AST_ForStmt(a, b, c, start_pos=parser.stack.pop())
    return AST_SimpleForStmt(a, b, start_pos=parser.stack.pop())

def while_loop_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    print(parser.stack)
    do_first = False
    if (tok := wcheck(parser, T_IDENT)):
        if tok[1] == 'while':
            a = expression_rule(parser, indentlevel)
            if not a:
                cleanup(parser)
                return a
            b = block_raw_rule(parser, indentlevel+1) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
            if not b:
                cleanup(parser)
                return b
        elif tok[1] == 'do':
            b = block_raw_rule(parser, indentlevel+1)
            if not b:
                cleanup(parser)
                return b
            if not (tok := wcheck(parser, T_IDENT)) or tok[1] != 'while':
                cleanup(parser)
                return None
            if not wcheck(parser, T_LPAREN):
                cleanup(parser)
                return None
            a = expression_rule(parser, indentlevel)
            if not a:
                cleanup(parser)
                return a
            if not wcheck(parser, T_RPAREN):
                cleanup(parser)
                return None
            do_first = True
        else:
            cleanup(parser)
            return None
    elif peek(parser)[0] is T_LBRACE:
        b = block_raw_rule(parser, indentlevel+1)
        if not b:
            cleanup(parser)
            return b
        if (tok := wcheck(parser, T_IDENT)) and tok[1] == 'while':
            if not wcheck(parser, T_LPAREN):
                cleanup(parser)
                return None
            a = expression_rule(parser, indentlevel)
            if not a:
                cleanup(parser)
                return a
            if not wcheck(parser, T_RPAREN):
                cleanup(parser)
                return None
            do_first = True
        else:
            cleanup(parser)
            return None
    print(parser.stack)
    return AST_WhileStmt(a, b, do_first=do_first, start_pos=parser.stack.pop())

def loop_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if not (tok := wcheck(parser, T_IDENT)) or tok[1] != 'loop':
        cleanup(parser)
        return None
    a = block_raw_rule(parser, indentlevel+1) or (wcheck(parser, T_SEMICOLON) and AST_Block([], start_pos=parser.index-1))
    if not a:
        cleanup(parser)
        return a
    return AST_RawLoopStmt(a, start_pos=parser.stack.pop())

# BLOCK STATEMENTS END

def assignment_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = name_expr_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    if not wcheck(parser, T_EQUAL):
        cleanup(parser)
        return None
    b = block_stmt_rule(parser, indentlevel)
    if not b:
        cleanup(parser)
        return b
    return AST_LabeledBlock(a, b, start_pos=parser.stack.pop())

def simple_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if (toktype := (tok := peek(parser))[0]) is T_IDENT:
        tokstring = tok[1]
        if tokstring == "struct":
            parser.stack.pop()
            return struct_dcl_rule(parser, indentlevel)
        elif tokstring == "union":
            parser.stack.pop()
            return union_dcl_rule(parser, indentlevel)
        elif tokstring == "enum":
            parser.stack.pop()
            return enum_dcl_rule(parser, indentlevel)
        elif tokstring == "ret":
            parser.stack.pop()
            return ret_stmt_rule(parser, indentlevel)
        elif tokstring == "cont":
            parser.stack.pop()
            return cont_stmt_rule(parser, indentlevel)
        elif tokstring == "break":
            parser.stack.pop()
            return break_stmt_rule(parser, indentlevel)
        elif tokstring == "label":
            parser.stack.pop()
            return label_stmt_rule(parser, indentlevel)
        elif tokstring == "del":
            parser.stack.pop()
            return del_stmt_rule(parser, indentlevel)
        elif tokstring == "use":
            parser.stack.pop()
            return use_stmt_rule(parser, indentlevel)
        elif tokstring == "incl":
            parser.stack.pop()
            return incl_stmt_rule(parser, indentlevel)
        elif tokstring == "dcl":
            parser.stack.pop()
            return dcl_stmt_rule(parser, indentlevel) or func_dcl_rule(parser, indentlevel)
        elif tokstring == "goto":
            parser.stack.pop()
            return goto_stmt_rule(parser, indentlevel)
        else:
            a = expression_rule(parser, indentlevel)
            if not a and a is not None:
                cleanup(parser)
                return a
            elif a:
                return AST_Expr(a, start_pos=parser.stack.pop())
            parser.stack.pop()
            return dcl_stmt_rule(parser, indentlevel) or func_dcl_rule(parser, indentlevel) or goto_stmt_rule(parser, indentlevel)
    elif toktype is T_COLON and peek(parser, 2)[0] is T_COLON:
        parser.stack.pop()
        a = label_stmt_rule(parser, indentlevel)
        if a or not a and a is not None:
            parser.stack.pop()
            return a
    elif toktype is T_LPAREN:
        a = func_dcl_rule(parser, indentlevel)
        if a or not a and a is not None:
            parser.stack.pop()
            return a
    a = expressions_rule(parser, indentlevel)
    if not a:
        cleanup(parser)
        return a
    return AST_Expr(a, start_pos=parser.stack.pop())

def block_stmt_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    if (toktype := (tok := peek(parser))[0]) is T_IDENT:
        tokstring = tok[1]
        if tokstring == "loop":
            parser.stack.pop()
            return loop_stmt_rule(parser, indentlevel)
        elif tokstring == "while":
            parser.stack.pop()
            return while_loop_rule(parser, indentlevel)
        elif tokstring == "for":
            parser.stack.pop()
            return for_loop_rule(parser, indentlevel)
        elif tokstring == "if":
            parser.stack.pop()
            return if_stmt_rule(parser, indentlevel)
        elif tokstring == "switch":
            parser.stack.pop()
            return switch_stmt_rule(parser, indentlevel)
        elif tokstring == "struct":
            parser.stack.pop()
            return struct_def_rule(parser, indentlevel)
        elif tokstring == "union":
            parser.stack.pop()
            return union_def_rule(parser, indentlevel)
        elif tokstring == "enum":
            parser.stack.pop()
            return enum_def_rule(parser, indentlevel)
        else:
            parser.stack.pop()
            return func_def_rule(parser, indentlevel)
    elif toktype is T_LPAREN or toktype is T_LBRACKET:
        parser.stack.pop()
        return func_def_rule(parser, indentlevel)
    parser.stack.pop()
    return None

def statement_rule(parser, indentlevel=0):
    a = assignment_stmt_rule(parser, indentlevel) or block_stmt_rule(parser, indentlevel) or simple_stmt_rule(parser, indentlevel)
    b = wcheck(parser, T_SEMICOLON)
    return a or b

# PRIMARY STATEMENTS END

def eval_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    try:
        a = expressions_rule(parser, indentlevel)
        if not a and a is not None:
            cleanup(parser)
            return a
    except IndexError:
        splitted = parser.source.split('\n')
        line = len(splitted)
        text = splitted[-1]
        col = len(text)
        parser.stack.pop()
        return ParserWarning("EOF token does not exist at supposed end of eval rule", line, text, col)
    else:
        if not wcheck(parser, T_EOF):
            splitted = parser.source[:parser.stream[parser.index][-2]].split('\n')
            line = len(splitted)
            text = parser.source.split('\n')[line-1]
            col = len(splitted[-1])
            parser.stack.pop()
            return ParserErrorWithTildeAndCaret(f"EOF expected at supposed end of eval rule, instead got unexpected {token_name(parser.stream[parser.index])}",
                                                line, text, col, 0, len(str(parser.stream[parser.index])))
    return AST_Eval(a, start_pos=parser.stack.pop())

def exec_rule(parser, indentlevel=0):
    parser.stack.append(skip_whitespace_get_index(parser))
    a = []
    append = a.append
    try:
        _tmp_a = statement_rule(parser, indentlevel)
        if _tmp_a:
            append(_tmp_a)
            while (_tmp_a := statement_rule(parser, indentlevel)):
                append(_tmp_a)
        if not _tmp_a and _tmp_a is not None:
            cleanup(parser)
            return _tmp_a
    except IndexError:
        splitted = parser.source.split('\n')
        line = len(splitted)
        text = splitted[-1]
        col = len(text)
        parser.stack.pop()
        return ParserWarning("EOF token does not exist at supposed end of exec rule", line, text, col)
    else:
        if not wcheck(parser, T_EOF):
            splitted = parser.source[:parser.stream[parser.index][-2]].split('\n')
            line = len(splitted)
            text = parser.source.split('\n')[line-1]
            col = len(splitted[-1])
            parser.stack.pop()
            return ParserErrorWithTildeAndCaret(f"EOF expected at supposed end of exec rule, instead got unexpected {token_name(parser.stream[parser.index])}",
                                                line, text, col, 0, len(str(parser.stream[parser.index])))
    return AST_Exec(a, start_pos=parser.stack.pop())

# START RULES END

def parser(source, start="exec"):
    parse_object = Parser(source)
    if not isinstance(parse_object.stream, list):
        return parse_object.stream
    return globals()[f"{start}_rule"](parse_object, 0)
