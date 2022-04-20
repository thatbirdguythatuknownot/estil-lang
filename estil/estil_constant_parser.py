from estil_node_types import (AST_Int, AST_Dec, AST_String, AST_JoinedString,
                              AST_ByteString, AST_JoinedByteString, AST_Formatted)
from estil_lexer import _newlines as newlines, lexer, T_INT, T_DEC, T_STRING
from decimal import Decimal, getcontext
from os import system
system('')

class ConstantParserError(SyntaxError):
    __module__ = 'builtins'
    def __init__(self, msg, text='', line=-1, scol=-1, caret_length=0, adv=False):
        self.msg = msg
        self.text = text
        self.scol = scol
        self.line = line
        self.caret_length = caret_length
        self.advanced = adv
    def __repr__(self):
        return f"ConstantParserError({self.msg!r}, {self.text!r}, {self.line!r}, {self.scol!r}, {self.caret_length!r}, {self.advanced!r})"
    def __str__(self):
        if self.advanced:
            linen = f"{self.line:03d}"
            return f"\x1b[38;2;220;0;0mERROR (Constant Parser):{self.line}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}   {' ' * self.scol}{'^' * self.caret_length}"
        return f"\x1b[38;2;0;220;0mconstant parser error:{self.line}:{self.scol}:\x1b[0m {self.msg}"
    def __bool__(self):
        return False

class ConstantParserErrorWithStart(SyntaxError):
    __module__ = 'builtins'
    def __init__(self, msg, text='', line=-1, scol=-1, caret_length=0, msg2=None, text2='', line2=-1, scol2=-1, caret_length2=0):
        self.msg = msg
        self.text = text
        self.scol = scol
        self.line = line
        self.caret_length = caret_length
        self.msg2 = msg2
        self.text2 = text2
        self.scol2 = scol2
        self.line2 = line2
        self.caret_length2 = caret_length2
    def __repr__(self):
        return f"ConstantParserErrorWithStart({self.msg!r}, {self.text!r}, {self.line!r}, {self.scol!r}, {self.caret_length!r}, {self.msg2!r}, {self.text2!r}, {self.line2!r}, {self.scol2!r}, {self.caret_length2!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        linen2 = f"{self.line2:03d}"
        return (f"\x1b[38;2;220;0;0mERROR (Constant Parser):{self.line}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.scol}{'^' * self.caret_length}\n"
                f"{self.msg2}\n{linen2}  | {self.text2}\n{len(linen2) * ' '}    {' ' * self.scol2}{'^' * self.caret_length2}")
    def __bool__(self):
        return False

class ConstantParserWarning(SyntaxWarning):
    __module__ = 'builtins'
    def __init__(self, msg, text='', line=-1, scol=-1, caret_length=0, adv=False):
        self.msg = msg
        self.text = text
        self.scol = scol
        self.line = line
        self.caret_length = caret_length
        self.advanced = adv
    def __repr__(self):
        return f"ConstantParserWarning({self.msg!r}, {self.text!r}, {self.line!r}, {self.scol!r}, {self.caret_length!r}, {self.advanced!r})"
    def __str__(self):
        if self.advanced:
            linen = f"{self.line:03d}"
            return f"\x1b[38;2;220;205;0mWARNING (Constant Parser):{self.line}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}   {' ' * self.scol}{'^' * self.caret_length}"
        return f"\x1b[38;2;0;220;205mconstant parser warning:\x1b[0m {self.msg}"
    def __bool__(self):
        return False

class ConstantParserWarningWithStart(SyntaxWarning):
    __module__ = 'builtins'
    def __init__(self, msg, text='', line=-1, scol=-1, caret_length=0, msg2=None, text2='', line2=-1, scol2=-1, caret_length2=0):
        self.msg = msg
        self.text = text
        self.scol = scol
        self.line = line
        self.caret_length = caret_length
        self.msg2 = msg2
        self.text2 = text2
        self.scol2 = scol2
        self.line2 = line2
        self.caret_length2 = caret_length2
    def __repr__(self):
        return f"ConstantParserWarningWithStart({self.msg!r}, {self.text!r}, {self.line!r}, {self.scol!r}, {self.caret_length!r}, {self.msg2!r}, {self.text2!r}, {self.line2!r}, {self.scol2!r}, {self.caret_length2!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        linen2 = f"{self.line2:03d}"
        return (f"\x1b[38;2;220;205;0mWARNING (Constant Parser):{self.line}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.scol}{'^' * self.caret_length}\n"
                f"{self.msg2}\n{linen2}  | {self.text2}\n{len(linen2) * ' '}    {' ' * self.scol2}{'^' * self.caret_length2}")


div2 = {'0': .0, '1': .5}
div8 = {'0': .0, '1': .125, '2': .25, '3': .375, '4': .5, '5': .625, '6': .75, '7': .875}
div16 = {'0': .0, '1': .0625, '2': .125, '3': .1875, '4': .25, '5': .3125, '6': .375, '7': .4375,
         '8': .5, '9': .5625, 'a': .625, 'b': .6875, 'c': .75, 'd': .8125, 'e': .875, 'f': .9375}
hexdigits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15,
                             'a':10, 'b':11, 'c':12, 'd':13, 'e':14, 'f':15}
octdigits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7}

def parser(x, linetext="<nil>", lineno=-1, curcol=-1, lastlinetext="<nil>"):
    """
    Parse an Estil constant.
    """
    orig_linetext = linetext
    orig_lineno = lineno
    orig_curcol = curcol
    LNT_HEX = 0
    LNT_BIN = 1
    LNT_OCT = 2
    LNT_DEC = 3
    LT_INT = T_INT
    LT_DEC = T_DEC
    LT_STRING = T_STRING
    DEC_2 = Decimal("2")
    DEC_8 = Decimal("8")
    DEC_10 = Decimal("10")
    if (tok_type := x[0]) not in {LT_INT, LT_DEC, LT_STRING}:
        return ConstantParserError(f"Unexpected token type {x[0]}", linetext, lineno, curcol)
    if tok_type is LT_INT:
        if x[4] is LNT_HEX:
            res = int(x[1], 16) << x[2]
        elif x[4] is LNT_BIN:
            res = int(x[1], 2) << x[2]
        elif x[4] is LNT_OCT:
            res = int(x[1], 8) << x[2]
        else:
            res = int(x[1]) * 10 ** x[2]
        if (specifier := x[3]):
            if specifier == 'b':
                res &= 255
            elif specifier == 's':
                res &= 65535
            elif specifier == 'd':
                res &= 4294967295
            elif specifier == 'l':
                res &= 18446744073709551615
        res = AST_Int(res)
        res.start_pos = x[5]
        return res
    elif tok_type is LT_DEC:
        if (specifier := x[3]):
            if specifier == 's':
                getcontext().prec = 4 # approximate unofficial decimal16
            elif specifier == 'f':
                getcontext().prec = 8 # IEEE 754 decimal32/binary32
            elif specifier == 'd':
                getcontext().prec = 16 # IEEE 754 decimal64/binary64
            elif specifier == 'l':
                getcontext().prec = 34 # IEEE 754 decimal128/binary128
        if x[4] is LNT_HEX:
            int_part, float_part = x[1].split('.')
            if not specifier:
                getcontext().prec = (len(int_part) + len(float_part)) * 4 + abs(x[2])*2 + 1
            if float_part:
                last_digit, *float_part = float_part[::-1]
                num = Decimal(div16[last_digit])
                if float_part:
                    for i in float_part:
                        num = hexdigits[i]+num/16
                    num /= 16
            else:
                num = Decimal('.0')
            res = (int(int_part or '0', 16) + num) * DEC_2**x[2]
        elif x[4] is LNT_BIN:
            int_part, float_part = x[1].split('.')
            if not specifier:
                getcontext().prec = len(int_part) + len(float_part) + abs(x[2]) + 1
            if float_part:
                num = Decimal(div2[float_part[0]])
                for i, v in enumerate(float_part):
                    if v != '0':
                        num += Decimal(v) * DEC_2**(-i - 1)
            else:
                num = Decimal('.0')
            res = (int(int_part or '0', 2) + num) * DEC_2**x[2]
        elif x[4] is LNT_OCT:
            int_part, float_part = x[1].split('.')
            if not specifier:
                getcontext().prec = (len(int_part) + len(float_part)) * 2 + abs(x[2]) + 1
            if float_part:
                num = 0
                for i, v in enumerate(float_part):
                    num += Decimal(v) * DEC_8**(-i - 1)
            else:
                num = Decimal('.0')
            res = (int(int_part or '0', 8) + num) * DEC_2**x[2]
        else:
            length = len(x[1])-1
            if not specifier:
                getcontext().prec = len(x[1])-1 + abs(x[2]) + 1
            res = Decimal(x[1]) * DEC_10**x[2]
        res = AST_Dec(res)
        res.start_pos = x[5]
        return res
    else:
        _, string, f, a, u, b, c, _, _ = x
        onenewl_splitted = string.replace('\v', '\n').replace('\f', '\n').replace('\r', '\n').replace('\x85', '\n').replace('\u2028', '\n').replace('\u2029', '\n').replace('\u240a', '\n').replace('\u240b', '\n').replace('\u240c', '\n').replace('\u240d', '\n').replace('\u2424', '\n').split('\n')
        last_index = len(onenewl_splitted) - 1
        new_string = ''
        len_string = len(string)
        i = 0
        startcol = curcol
        while i < len_string:
            x = string[i]
            start_err = i
            if x == '\\':
                if (i := i + 1) < len_string:
                    x = string[i]
                    if x == 'U':
                        start = i = i + 1
                        if i < len_string and string[i] in hexdigits:
                            if (i := i + 1) < len_string and string[i] in hexdigits:
                                if (i := i + 1) < len_string and string[i] in hexdigits:
                                    if (i := i + 1) < len_string and string[i] in hexdigits:
                                        if (i := i + 1) < len_string and string[i] in hexdigits:
                                            if (i := i + 1) < len_string and string[i] in hexdigits:
                                                i += 1
                            val = int(string[start:i], 16)
                            if a and val > 127:
                                return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\U escape sequence",
                                                                    linetext, lineno, startcol, i - start_err,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            elif u and val < 128:
                                return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\U escape sequence",
                                                                    linetext, lineno, startcol, i - start_err,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            new_string += chr(val)
                            startcol += i - start_err - 1
                        else:
                            if u:
                                return ConstantParserErrorWithStart("Non-ASCII string literal cannot have ASCII characters",
                                                                    linetext, lineno, startcol, 2,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            new_string += '\\U'
                            startcol += 2
                    elif x == 'u':
                        start = i = i + 1
                        if i < len_string and string[i] in hexdigits:
                            if (i := i + 1) < len_string and string[i] in hexdigits:
                                if (i := i + 1) < len_string and string[i] in hexdigits:
                                    if (i := i + 1) < len_string and string[i] in hexdigits:
                                        i += 1
                            val = int(string[start:i], 16)
                            if a and val > 127:
                                return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\u escape sequence",
                                                                    linetext, lineno, startcol, i - start_err,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            elif u and val < 128:
                                return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\u escape sequence",
                                                                    linetext, lineno, startcol, i - start_err,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            new_string += chr(val)
                            startcol += i - start_err - 1
                        else:
                            if u:
                                return ConstantParserErrorWithStart("Non-ASCII string literal cannot have ASCII characters",
                                                                    linetext, lineno, startcol, 2,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            new_string += '\\u'
                            startcol += 2
                    elif x == 'x':
                        start = i = i + 1
                        if i < len_string and string[i] in hexdigits:
                            if (i := i + 1) < len_string and string[i] in hexdigits:
                                i += 1
                            val = int(string[start:i], 16)
                            if a and val > 127:
                                return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\x escape sequence",
                                                                    linetext, lineno, startcol, i - start_err,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            elif u and val < 128:
                                return ConstantParserErrorWithStart("Non-ASCII string literal contains an ASCII character by \\x escape sequence",
                                                                    linetext, lineno, startcol, i - start_err,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            new_string += chr(val)
                            startcol += i - start_err + 1
                        else:
                            if a:
                                return ConstantParserErrorWithStart("ASCII string literal cannot have \\x (\\x85)",
                                                                    linetext, lineno, startcol, 2,
                                                                    "note: string started here",
                                                                    orig_linetext, orig_lineno, orig_curcol - 1, 1)
                            new_string += '\x85'
                            startcol += 2
                    elif x == 'b':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\b (\\x08)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\b'
                    elif x == '"':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\\" (\\x22)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '"'
                    elif x == "'":
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\' (\\x27)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += "'"
                    elif x == '\\':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\\\ (\\x5c)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\\'
                    elif x == 'e':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\e (\\x1b)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\x1b'
                    elif x == 'p':
                        i += 1
                        if a:
                            return ConstantParserErrorWithStart("ASCII string literal cannot have \\p (\\u2029)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\u2029'
                    elif x == 'l':
                        i += 1
                        if a:
                            return ConstantParserErrorWithStart("ASCII string literal cannot have \\l (\\u2028)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\u2028'
                    elif x == 'v':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\v (\\x0b)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\v'
                    elif x == 'f':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\f (\\x0c)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\f'
                    elif x == 't':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\t (\\x09)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\t'
                    elif x == 'r':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\r (\\x0d)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\r'
                    elif x == 'n':
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have \\n (\\x0a)",
                                                                linetext, lineno, startcol, 2,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\n'
                    elif x in newlines:
                        i += 1
                        startcol += 1
                        if a and x > '\x7f':
                            return ConstantParserErrorWithStart("ASCII string literal cannot have a non-ASCII newline character",
                                                                linetext, lineno, startcol, 1,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        elif u and x < '\x80':
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have an ASCII newline character",
                                                                linetext, lineno, startcol, 1,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        lineno += 1
                        linetext = lastlinetext if (lno := lineno - orig_lineno) == last_index else onenewl_splitted[lno]
                        curcol = 0
                        startcol = -1
                    elif x in octdigits:
                        start = i
                        if (i := i + 1) < len_string and string[i] in octdigits:
                            if (i := i + 1) < len_string and string[i] in octdigits:
                                i += 1
                        val = int(string[start:i], 8)
                        if a and val > 127:
                            return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\U escape sequence",
                                                                linetext, lineno, startcol, i - start_err,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        elif u and val < 128:
                            return ConstantParserErrorWithStart("ASCII string literal contains a non-ASCII character by \\U escape sequence",
                                                                linetext, lineno, startcol, i - start_err,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        new_string += chr(val)
                        startcol += i - start_err - 1
                    else:
                        i += 1
                        if u:
                            return ConstantParserErrorWithStart("Non-ASCII string literal cannot have a backslash character (\\x5c)",
                                                                linetext, lineno, startcol, 1,
                                                                "note: string started here",
                                                                orig_linetext, orig_lineno, orig_curcol - 1, 1)
                        startcol += 1
                        new_string += '\\'
                        new_string += x
                else:
                    if u:
                        return ConstantParserErrorWithStart("Non-ASCII string literal cannot have a backslash character (\\x5c)",
                                                            linetext, lineno, startcol, 1,
                                                            "note: string started here",
                                                            orig_linetext, orig_lineno, orig_curcol - 1, 1)
                    new_string += '\\'
                startcol += 1
            else:
                i += 1
                if a and x > '\x7f':
                    return ConstantParserErrorWithStart("ASCII string literal cannot have a non-ASCII character",
                                                        linetext, lineno, startcol, 1,
                                                        "note: string started here",
                                                        orig_linetext, orig_lineno, orig_curcol - 1, 1)
                elif u and x < '\x80':
                    return ConstantParserErrorWithStart("Non-ASCII string literal cannot have an ASCII character",
                                                        linetext, lineno, startcol, 1,
                                                        "note: string started here",
                                                        orig_linetext, orig_lineno, orig_curcol - 1, 1)
                if x in newlines:
                    lineno += 1
                    linetext = lastlinetext if (lno := lineno - orig_lineno) == last_index else onenewl_splitted[lno]
                    curcol = 0
                    startcol = 0
                else:
                    startcol += 1
                new_string += x
        string = new_string
        if f:
            i = 0
            len_string = len(string)
            linetext, lineno, curcol = orig_linetext, orig_lineno, (startcol := orig_curcol)
            values = []
            new_value = values.append
            end_brace = 0
            while i < len_string:
                x = string[i]
                if x == '\\':
                    i += 1
                    startcol += 1
                    if i < len_string:
                        x = string[i]
                        if x == '{':
                            new_string += '{'
                            i += 1
                            startcol += 1
                        elif x == '}':
                            new_string += '}'
                            i += 1
                            startcol += 1
                    else:
                        new_string += '\\'
                elif x == '{':
                    start_err = i
                    balance = 1
                    start_brace = i = i + 1
                    start_linetext = linetext
                    start_lineno = lineno
                    start_startcol = startcol
                    start_start_err = start_err
                    end_start_err = -1
                    while i < len_string and balance:
                        x = string[i]
                        if x == '{':
                            balance += 1
                        elif x == '}':
                            balance -= 1
                        elif x == '\\':
                            i += 1
                        elif x in newlines:
                            lineno += 1
                            linetext = lastlinetext if (lno := lineno - orig_lineno) == last_index else onenewl_splitted[lno]
                            curcol = startcol = 0
                            if start_err == start_start_err:
                                end_start_err = i
                            start_err = i
                        i += 1
                    if balance:
                        return ConstantParserErrorWithStart(f"Unbalanced braces (still need {balance} more closing brace{'s' if balance != 1 else ''}) in f-string",
                                                            linetext, lineno, startcol, i - start_err,
                                                            "note: started brace here",
                                                            start_linetext, start_lineno, start_startcol, 1)
                    if (before_brace := string[end_brace:start_brace - 1]):
                        node = AST_Formatted(before_brace, None, 1)
                        node.start_pos = end_brace
                        new_value(node)
                    inbrace = string[start_brace:i - 1]
                    split_inbrace = inbrace.split(';', 1)
                    if any(split_inbrace):
                        if len(split_inbrace) == 2:
                            expr, specifier = split_inbrace
                            specifier = specifier or None
                        else:
                            expr = split_inbrace[0]
                            specifier = None
                        node = AST_Formatted(expr, specifier)
                        node.start_pos = start_brace
                        new_value(node)
                    else:
                        print(ConstantParserWarningWithStart(f"Empty f-string expression",
                                                             linetext, lineno, startcol, i - start_err,
                                                             "note: started string here",
                                                             orig_linetext, orig_lineno, orig_curcol - 1, 1))
                    end_brace = i
                    startcol += i - start_err
                elif x == '}':
                    print(ConstantParserWarningWithStart(f"Unexpected closing brace in f-string",
                                                         linetext, lineno, startcol, 1,
                                                         "note: started string here",
                                                         orig_linetext, orig_lineno, orig_curcol - 1, 1))
                    new_string += '}'
                    i += 1
                    startcol += 1
                else:
                    new_string += x
                    i += 1
                    startcol += 1
            if end_brace < len_string:
                node = AST_Formatted(string[end_brace:], None, 1)
                node.start_pos = end_brace
                new_value(node)
            if b:
                retval = AST_JoinedByteString(values)
            else:
                retval = AST_JoinedString(values)
            retval.start_pos = orig_curcol
            return retval
        if b:
            retval = AST_ByteString(string)
        else:
            retval = AST_String(string)
        retval.start_pos = orig_curcol
        return retval

if 0:
    parser(lexer(content := '0x1.p5')[0], content, 1, 0, content)
    parser(lexer(content := '0x2.3p-1')[0], content, 1, 0, content)
    parser(lexer(content := '0x.')[0], content, 1, 0, content)
    parser(lexer(content := '0b.0111001')[0], content, 1, 0, content)
    parser(lexer(content := '0x1p8')[0], content, 1, 0, content)
    parser(lexer(content := '1.e+38')[0], content, 1, 0, content)
    parser(lexer(content := '1e+23')[0], content, 1, 0, content)
    parser(lexer(content := '1e-11')[0], content, 1, 0, content)
    print(parser(lexer(content := r"a'\U10ffff\u0030'")[0], content, 1, 2, content))
    print(parser(lexer(content := r"u'\U10ffff\u0030'")[0], content, 1, 2, content))
    print(parser(lexer(content := r"au'\U10ffff\u0030'")[0], content, 1, 3, content))
    parser(lexer(content := r"b'\U10ffff\ufeff 2'")[0], content, 1, 2, content)
    parser(lexer(content := "b'a + b = \\\nc'")[0], content, 1, 2, "c'")
    print(parser(lexer(content := r"a'\p25 + 3'")[0], content, 1, 2, content))
    print(parser(lexer(content := r"a'25\n + 3\p55'")[0], content, 1, 2, content))
    print(parser(lexer(content := r"u'\n25 + 3'")[0], content, 1, 2, content))
    print(parser(lexer(content := r"u'\p\n'")[0], content, 1, 2, content))
    print(parser(lexer(content := "u'\\\n'")[0], "u'\\", 1, 2, "'"))
    print(parser(lexer(content := "a'\\\nabc\p'")[0], "a'\\", 1, 2, "abc\p'"))
    print(parser(lexer(content := "f'{{1 + 2 + 3;take L}\nlol {2+2}'")[0], "f'{{1 + 2 + 3;take L}", 1, 2, "lol {2+2}'"))
    print(parser(lexer(content := "f'{}lol'")[0], "f'{}lol'", 1, 2, "f'{}lol'"))
    print(parser(lexer(r"a'\xff + 2'")[0], r"a'\xff + 2'", 1, 2, r"a'\xff + 2'"))
