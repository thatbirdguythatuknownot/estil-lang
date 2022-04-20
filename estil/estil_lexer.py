from itertools import product, permutations
from functools import reduce
from operator import or_ as bor
from warnings import warn
from os import system
system('')

_whitespaces = {'\t', '\n', '\v', '\f', '\r', ' ', '\x85', '\xa0',
                '\xb7', '\u1680', '\u2000', '\u2001', '\u2002',
                '\u2003', '\u2004', '\u2005', '\u2006', '\u2007',
                '\u2008', '\u2009', '\u200a', '\u200c', '\u200d',
                '\u2028', '\u2029', '\u202f', '\u205f', '\u237d',
                '\u23ce', '\u2409', '\u240a', '\u240b', '\u240c',
                '\u240d', '\u2420', '\u2423', '\u2424', '\u3000'}
_newlines = {'\n', '\v', '\f', '\r', '\x85', '\u2028', '\u2029',
             '\u240a', '\u240b', '\u240c', '\u240d', '\u2424'}
_hex_digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'A', 'B', 'C', 'D', 'E', 'F',
              'a', 'b', 'c', 'd', 'e', 'f'}
_identifier_characters = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                          '_'}
_digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
_string_specifiers = set(map(lambda x: ''.join(set(''.join(x))), product([*'Cc', ''], [*'Rr', ''], [*'Bb', ''], [*'Ff', ''], [*'Uu', ''], [*'Aa', ''])))
_escapables = {'n', 'r', 't', 'f', 'v', 'l', 'p', 'e', 'x', '\\', "'", '"', 'b'}
_number_specifiers = [{'b', 's', 'd', 'l'}, {'s', 'f', 'd', 'l'}]
_octal_digits = {'0', '1', '2', '3', '4', '5', '6', '7'}
_specifier_digits = [{'0', '1', '_'}, _hex_digits | {'_'}, _octal_digits | {'_'}]

T_LPAREN = 0                ; S_LPAREN = "("
T_RPAREN = 1                ; S_RPAREN = ")"
T_LBRACKET = 2              ; S_LBRACKET = "["
T_RBRACKET = 3              ; S_RBRACKET = "]"
T_LBRACE = 4                ; S_LBRACE = "{"
T_RBRACE = 5                ; S_RBRACE = "}"
T_COMMA = 6                 ; S_COMMA = ","
T_COLON = 7                 ; S_COLON = ":"
T_SEMICOLON = 8             ; S_SEMICOLON = ";"
T_DOT = 9                   ; S_DOT = "."
T_QMARK = 10                ; S_QMARK = "?"
T_AMP = 11                  ; S_AMP = "&"
T_STAR = 12                 ; S_STAR = "*"
T_TAG = 13                  ; S_TAG = "#"
T_EXCLMARK = 14             ; S_EXCLMARK = "!"
T_CARET = 15                ; S_CARET = "^"
T_MINUS = 16                ; S_MINUS = "-"
T_PLUS = 17                 ; S_PLUS = "+"
T_TILDE = 18                ; S_TILDE = "~"
T_DBLSLASH = 19             ; S_DBLSLASH = "//"
T_SLASH = 20                ; S_SLASH = "/"
T_PERCENT = 21              ; S_PERCENT = "%"
T_BACKSLASH = 22            ; S_BACKSLASH = "\\"
T_DBLBACKSLASH = 23         ; S_DBLBACKSLASH = "\\\\"
T_DBLLT = 24                ; S_DBLLT = "<<"
T_DBLGT = 25                ; S_DBLGT = ">>"
T_TRPLLT = 28               ; S_TRPLLT = "<<<"
T_TRPLGT = 29               ; S_TRPLGT = ">>>"
T_TILDEAMP = 30             ; S_TILDEAMP = "~&"
T_DOLLAR = 31               ; S_DOLLAR = "$"
T_TILDEDOLLAR = 32          ; S_TILDEDOLLAR = "~$"
T_PIPE = 33                 ; S_PIPE = "|"
T_TILDEPIPE = 34            ; S_TILDEPIPE = "~|"
T_GRAVE = 35                ; S_GRAVE = "`"
T_TILDEGT = 36              ; S_TILDEGT = "~>"
T_TILDEEXCLMARK = 37        ; S_TILDEEXCLMARK = "~!"
T_TAGEQUAL = 38             ; S_TAGEQUAL = "#="
T_TAGEXCLMARK = 39          ; S_TAGEXCLMARK = "#!"
T_DBLEQUAL = 40             ; S_DBLEQUAL = "=="
T_EXCLMARKEQUAL = 41        ; S_EXCLMARKEQUAL = "!="
T_LT = 42                   ; S_LT = "<"
T_GT = 43                   ; S_GT = ">"
T_LTEQUAL = 44              ; S_LTEQUAL = "<="
T_GTEQUAL = 45              ; S_GTEQUAL = ">="
T_LTEQUALGT = 46            ; S_LTEQUALGT = "<=>"
T_DBLAMP = 47               ; S_DBLAMP = "&&"
T_DBLDOLLAR = 48            ; S_DBLDOLLAR = "$$"
T_DBLPIPE = 49              ; S_DBLPIPE = "||"
T_QMARKCOLON = 50           ; S_QMARKCOLON = "?:"
T_DBLQMARK = 51             ; S_DBLQMARK = "??"
T_DOTEQUAL = 52             ; S_DOTEQUAL = ".="
T_CARETEQUAL = 53           ; S_CARETEQUAL = "^="
T_STAREQUAL = 54            ; S_STAREQUAL = "*="
T_DBLSLASHEQUAL = 55        ; S_DBLSLASHEQUAL = "//="
T_SLASHEQUAL = 56           ; S_SLASHEQUAL = "/="
T_PERCENTEQUAL = 57         ; S_PERCENTEQUAL = "%="
T_DBLBACKSLASHEQUAL = 58    ; S_DBLBACKSLASHEQUAL = "\\="
T_DBLLTEQUAL = 59           ; S_DBLLTEQUAL = "<<="
T_DBLGTEQUAL = 60           ; S_DBLGTEQUAL = ">>="
T_LTGTEQUAL = 61            ; S_LTGTEQUAL = "<>="
T_GTLTEQUAL = 62            ; S_GTLTEQUAL = "><="
T_TRPLLTEQUAL = 63          ; S_TRPLLTEQUAL = "<<<="
T_TRPLGTEQUAL = 64          ; S_TRPLGTEQUAL = ">>>="
T_AMPEQUAL = 65             ; S_AMPEQUAL = "&="
T_TILDEAMPEQUAL = 66        ; S_TILDEAMPEQUAL = "~&="
T_DOLLAREQUAL = 67          ; S_DOLLAREQUAL = "$="
T_TILDEDOLLAREQUAL = 68     ; S_TILDEDOLLAREQUAL = "~$="
T_PIPEEQUAL = 69            ; S_PIPEEQUAL = "|="
T_TILDEPIPEEQUAL = 70       ; S_TILDEPIPEEQUAL = "~|="
T_PLUSEQUAL = 71            ; S_PLUSEQUAL = "+="
T_MINUSEQUAL = 72           ; S_MINUSEQUAL = "-="
T_CMATEQUAL = 73           ; S_CMATEQUAL = "@="
T_DBLAMPEQUAL = 74          ; S_DBLAMPEQUAL = "&&="
T_DBLDOLLAREQUAL = 75       ; S_DBLDOLLAREQUAL = "$$="
T_DBLPIPEEQUAL = 76         ; S_DBLPIPEEQUAL = "||="
T_QMARKCOLONEQUAL = 77      ; S_QMARKCOLONEQUAL = "?:="
T_DBLQMARKEQUAL = 78        ; S_DBLQMARKEQUAL = "??="
T_QMARKEQUAL = 79           ; S_QMARKEQUAL = "?="
T_EQUAL = 80                ; S_EQUAL = "="
T_CMAT = 81                 ; S_CMAT = "@"
T_QUOTE = 82                ; S_QUOTE = "'"
T_DQUOTE = 83               ; S_DQUOTE = '"'
T_MINUSGT = 84              ; S_MINUSGT = "->"
T_COLONGT = 85              ; S_COLONGT = ":>"
T_DBLDOT = 86               ; S_DBLDOT = ".."
T_COLONDOT = 87             ; S_COLONDOT = ":."
T_EQUALLT = 88              ; S_EQUALLT = "=<"
T_EQUALGT = 89              ; S_EQUALGT = "=>"
T_IDENT = T_EQUALGT + 1
T_INT = T_IDENT + 1
T_DEC = T_INT + 1
T_STRING = T_DEC + 1
T_WSPACE = T_STRING + 1
T_LINEBREAK = T_WSPACE + 1
T_EOF = -1

class LexerError(SyntaxError):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col=0):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
    def __repr__(self):
        return f"LexerError({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        return f"\x1b[38;2;220;0;0mERROR (Lexer):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}^"
    def __bool__(self):
        return False

class LexerErrorWithStart(LexerError):
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
        return f"LexerErrorWithStart({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r}, {self.msg2!r}, {self.line2!r}, {self.text2!r}, {self.col2!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        linen2 = f"{self.line2:03d}"
        return f"\x1b[38;2;220;0;0mERROR (Lexer):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}^\n{self.msg2}\n{linen2}  | {self.text2}\n{len(linen2) * ' '}   {' ' * self.col2}^"

class LexerErrorWithTildeAndCaret(LexerError):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col, tildenum, caretnum):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
        self.tildenum = tildenum
        self.caretnum = caretnum
    def __repr__(self):
        return f"LexerErrorWithTildeAndCaret({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r}, {self.tildenum!r}, {self.caretnum!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        return f"\x1b[38;2;220;0;0mERROR (Lexer):{self.line}:{self.col}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}{'~' * self.tildenum}{'^' * self.caretnum}"

class LexerWarning(SyntaxWarning):
    __module__ = 'builtins'
    def __init__(self, msg, line, text, col=0):
        self.msg = msg
        self.line = line
        self.text = text
        self.col = col
    def __repr__(self):
        return f"LexerWarning({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        return f"\x1b[38;2;220;205;0mWARNING (Lexer):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}    {' ' * self.col}^"
    def __bool__(self):
        return True

class LexerWarningWithStart(LexerWarning):
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
        return f"LexerWarningWithStart({self.msg!r}, {self.line!r}, {self.text!r}, {self.col!r}, {self.msg2!r}, {self.line2!r}, {self.text2!r}, {self.col2!r})"
    def __str__(self):
        linen = f"{self.line:03d}"
        linen2 = f"{self.line2:03d}"
        return f"\x1b[38;2;220;205;0mWARNING (Lexer):{self.line}:{self.col+1}:\x1b[0m {self.msg}\n{linen}  | {self.text}\n{len(linen) * ' '}   {' ' * self.col}^\n{self.msg2}\n{linen2}  | {self.text2}\n{len(linen2) * ' '}   {' ' * self.col2}^"

number_prefixes = ['0b', '0x', '0o', '']

class Token:
    __module__ = 'builtins'
    def __init__(self, tok):
        self.tok = tok
    def __getitem__(self, i):
        return self.tok[i]
    def __repr__(self):
        return f"Token({self.tok!r})"
    def __str__(self):
        toktype = self.tok[0]
        if toktype is T_INT or toktype is T_DEC:
            numtype = self.tok[4]
            if numtype == 3:
                return f"{self.tok[1]}{self.tok[3]}"+(f"e{self.tok[2]!s}" if self.tok[2] else "")
            return f"{self.tok[3].join(number_prefixes[numtype])}{self.tok[1]}"+(f"p{self.tok[2]!s}" if self.tok[2] else "")
        elif toktype is T_STRING:
            f=self.tok[2] and 'f' or ''
            a=self.tok[3] and 'a' or ''
            u=self.tok[4] and 'u' or ''
            b=self.tok[5] and 'b' or ''
            c=self.tok[6] and 'c' or ''
            return f"{f}{a}{u}{b}{c}\"{self.tok[1]}\""
        else:
            return self.tok[1]

def _lexer(source: str) -> list:
    """
    Token generator for the estil language.
    """
    whitespaces = _whitespaces
    newlines = _newlines
    LT_LPAREN = T_LPAREN                        ; LS_LPAREN = S_LPAREN
    LT_RPAREN = T_RPAREN                        ; LS_RPAREN = S_RPAREN
    LT_LBRACKET = T_LBRACKET                    ; LS_LBRACKET = S_LBRACKET
    LT_RBRACKET = T_RBRACKET                    ; LS_RBRACKET = S_RBRACKET
    LT_LBRACE = T_LBRACE                        ; LS_LBRACE = S_LBRACE
    LT_RBRACE = T_RBRACE                        ; LS_RBRACE = S_RBRACE
    LT_COMMA = T_COMMA                          ; LS_COMMA = S_COMMA
    LT_COLON = T_COLON                          ; LS_COLON = S_COLON
    LT_SEMICOLON = T_SEMICOLON                  ; LS_SEMICOLON = S_SEMICOLON
    LT_DOT = T_DOT                              ; LS_DOT = S_DOT
    LT_QMARK = T_QMARK                          ; LS_QMARK = S_QMARK
    LT_AMP = T_AMP                              ; LS_AMP = S_AMP
    LT_STAR = T_STAR                            ; LS_STAR = S_STAR
    LT_TAG = T_TAG                              ; LS_TAG = S_TAG
    LT_EXCLMARK = T_EXCLMARK                    ; LS_EXCLMARK = S_EXCLMARK
    LT_CARET = T_CARET                          ; LS_CARET = S_CARET
    LT_MINUS = T_MINUS                          ; LS_MINUS = S_MINUS
    LT_PLUS = T_PLUS                            ; LS_PLUS = S_PLUS
    LT_TILDE = T_TILDE                          ; LS_TILDE = S_TILDE
    LT_DBLSLASH = T_DBLSLASH                    ; LS_DBLSLASH = S_DBLSLASH
    LT_SLASH = T_SLASH                          ; LS_SLASH = S_SLASH
    LT_PERCENT = T_PERCENT                      ; LS_PERCENT = S_PERCENT
    LT_BACKSLASH = T_BACKSLASH                  ; LS_BACKSLASH = S_BACKSLASH
    LT_DBLBACKSLASH = T_DBLBACKSLASH            ; LS_DBLBACKSLASH = S_DBLBACKSLASH
    LT_DBLLT = T_DBLLT                          ; LS_DBLLT = S_DBLLT
    LT_DBLGT = T_DBLGT                          ; LS_DBLGT = S_DBLGT
    LT_TRPLLT = T_TRPLLT                        ; LS_TRPLLT = S_TRPLLT
    LT_TRPLGT = T_TRPLGT                        ; LS_TRPLGT = S_TRPLGT
    LT_TILDEAMP = T_TILDEAMP                    ; LS_TILDEAMP = S_TILDEAMP
    LT_DOLLAR = T_DOLLAR                        ; LS_DOLLAR = S_DOLLAR
    LT_TILDEDOLLAR = T_TILDEDOLLAR              ; LS_TILDEDOLLAR = S_TILDEDOLLAR
    LT_PIPE = T_PIPE                            ; LS_PIPE = S_PIPE
    LT_TILDEPIPE = T_TILDEPIPE                  ; LS_TILDEPIPE = S_TILDEPIPE
    LT_GRAVE = T_GRAVE                          ; LS_GRAVE = S_GRAVE
    LT_TILDEGT = T_TILDEGT                      ; LS_TILDEGT = S_TILDEGT
    LT_TILDEEXCLMARK = T_TILDEEXCLMARK          ; LS_TILDEEXCLMARK = S_TILDEEXCLMARK
    LT_TAGEQUAL = T_TAGEQUAL                    ; LS_TAGEQUAL = S_TAGEQUAL
    LT_TAGEXCLMARK = T_TAGEXCLMARK              ; LS_TAGEXCLMARK = S_TAGEXCLMARK
    LT_DBLEQUAL = T_DBLEQUAL                    ; LS_DBLEQUAL = S_DBLEQUAL
    LT_EXCLMARKEQUAL = T_EXCLMARKEQUAL          ; LS_EXCLMARKEQUAL = S_EXCLMARKEQUAL
    LT_LT = T_LT                                ; LS_LT = S_LT
    LT_GT = T_GT                                ; LS_GT = S_GT
    LT_LTEQUAL = T_LTEQUAL                      ; LS_LTEQUAL = S_LTEQUAL
    LT_GTEQUAL = T_GTEQUAL                      ; LS_GTEQUAL = S_GTEQUAL
    LT_LTEQUALGT = T_LTEQUALGT                  ; LS_LTEQUALGT = S_LTEQUALGT
    LT_DBLAMP = T_DBLAMP                        ; LS_DBLAMP = S_DBLAMP
    LT_DBLDOLLAR = T_DBLDOLLAR                  ; LS_DBLDOLLAR = S_DBLDOLLAR
    LT_DBLPIPE = T_DBLPIPE                      ; LS_DBLPIPE = S_DBLPIPE
    LT_QMARKCOLON = T_QMARKCOLON                ; LS_QMARKCOLON = S_QMARKCOLON
    LT_DBLQMARK = T_DBLQMARK                    ; LS_DBLQMARK = S_DBLQMARK
    LT_DOTEQUAL = T_DOTEQUAL                    ; LS_DOTEQUAL = S_DOTEQUAL
    LT_CARETEQUAL = T_CARETEQUAL                ; LS_CARETEQUAL = S_CARETEQUAL
    LT_STAREQUAL = T_STAREQUAL                  ; LS_STAREQUAL = S_STAREQUAL
    LT_DBLSLASHEQUAL = T_DBLSLASHEQUAL          ; LS_DBLSLASHEQUAL = S_DBLSLASHEQUAL
    LT_SLASHEQUAL = T_SLASHEQUAL                ; LS_SLASHEQUAL = S_SLASHEQUAL
    LT_PERCENTEQUAL = T_PERCENTEQUAL            ; LS_PERCENTEQUAL = S_PERCENTEQUAL
    LT_DBLBACKSLASHEQUAL = T_DBLBACKSLASHEQUAL  ; LS_DBLBACKSLASHEQUAL = S_DBLBACKSLASHEQUAL
    LT_DBLLTEQUAL = T_DBLLTEQUAL                ; LS_DBLLTEQUAL = S_DBLLTEQUAL
    LT_DBLGTEQUAL = T_DBLGTEQUAL                ; LS_DBLGTEQUAL = S_DBLGTEQUAL
    LT_LTGTEQUAL = T_LTGTEQUAL                  ; LS_LTGTEQUAL = S_LTGTEQUAL
    LT_GTLTEQUAL = T_GTLTEQUAL                  ; LS_GTLTEQUAL = S_GTLTEQUAL
    LT_TRPLLTEQUAL = T_TRPLLTEQUAL              ; LS_TRPLLTEQUAL = S_TRPLLTEQUAL
    LT_TRPLGTEQUAL = T_TRPLGTEQUAL              ; LS_TRPLGTEQUAL = S_TRPLGTEQUAL
    LT_AMPEQUAL = T_AMPEQUAL                    ; LS_AMPEQUAL = S_AMPEQUAL
    LT_TILDEAMPEQUAL = T_TILDEAMPEQUAL          ; LS_TILDEAMPEQUAL = S_TILDEAMPEQUAL
    LT_DOLLAREQUAL = T_DOLLAREQUAL              ; LS_DOLLAREQUAL = S_DOLLAREQUAL
    LT_TILDEDOLLAREQUAL = T_TILDEDOLLAREQUAL    ; LS_TILDEDOLLAREQUAL = S_TILDEDOLLAREQUAL
    LT_PIPEEQUAL = T_PIPEEQUAL                  ; LS_PIPEEQUAL = S_PIPEEQUAL
    LT_TILDEPIPEEQUAL = T_TILDEPIPEEQUAL        ; LS_TILDEPIPEEQUAL = S_TILDEPIPEEQUAL
    LT_PLUSEQUAL = T_PLUSEQUAL                  ; LS_PLUSEQUAL = S_PLUSEQUAL
    LT_MINUSEQUAL = T_MINUSEQUAL                ; LS_MINUSEQUAL = S_MINUSEQUAL
    LT_CMATEQUAL = T_CMATEQUAL                ; LS_CMATEQUAL = S_CMATEQUAL
    LT_DBLAMPEQUAL = T_DBLAMPEQUAL              ; LS_DBLAMPEQUAL = S_DBLAMPEQUAL
    LT_DBLDOLLAREQUAL = T_DBLDOLLAREQUAL        ; LS_DBLDOLLAREQUAL = S_DBLDOLLAREQUAL
    LT_DBLPIPEEQUAL = T_DBLPIPEEQUAL            ; LS_DBLPIPEEQUAL = S_DBLPIPEEQUAL
    LT_QMARKCOLONEQUAL = T_QMARKCOLONEQUAL      ; LS_QMARKCOLONEQUAL = S_QMARKCOLONEQUAL
    LT_DBLQMARKEQUAL = T_DBLQMARKEQUAL          ; LS_DBLQMARKEQUAL = S_DBLQMARKEQUAL
    LT_QMARKEQUAL = T_QMARKEQUAL                ; LS_QMARKEQUAL = S_QMARKEQUAL
    LT_EQUAL = T_EQUAL                          ; LS_EQUAL = S_EQUAL
    LT_CMAT = T_CMAT                            ; LS_CMAT = S_CMAT
    LT_QUOTE = T_QUOTE                          ; LS_QUOTE = S_QUOTE
    LT_DQUOTE = T_DQUOTE                        ; LS_DQUOTE = S_DQUOTE
    LT_MINUSGT = T_MINUSGT                      ; LS_MINUSGT = S_MINUSGT
    LT_COLONGT = T_COLONGT                      ; LS_COLONGT = S_COLONGT
    LT_DBLDOT = T_DBLDOT                        ; LS_DBLDOT = S_DBLDOT
    LT_COLONDOT = T_COLONDOT                    ; LS_COLONDOT = S_COLONDOT
    LT_EQUALLT = T_EQUALLT                      ; LS_EQUALLT = S_EQUALLT
    LT_EQUALGT = T_EQUALGT                      ; LS_EQUALGT = S_EQUALGT
    LT_IDENT = T_IDENT
    LT_INT = T_INT
    LT_DEC = T_DEC
    LT_STRING = T_STRING
    LT_WSPACE = T_WSPACE
    LT_LINEBREAK = T_LINEBREAK
    LT_EOF = T_EOF
    break_or_space = (LT_WSPACE, LT_LINEBREAK)
    quotes = (LS_QUOTE, LS_DQUOTE)
    int_or_dec = (LT_INT, LT_DEC)
    hex_digits = _hex_digits
    identifier_characters = _identifier_characters
    digits = _digits
    ident_digits = identifier_characters | digits
    string_specifiers = _string_specifiers
    escapables = _escapables
    number_specifiers = _number_specifiers
    specifier_digits = _specifier_digits
    tokens = []
    _new_token = tokens.append
    def new_token(tok):
        _new_token(Token(tok))
    pop_token = tokens.pop
    len_source = len(source)
    modestr = ''
    string_specifier = ''
    onenewl_source = source.replace('\v', '\n').replace('\f', '\n').replace('\r', '\n').replace('\x85', '\n').replace('\u2028', '\n').replace('\u2029', '\n').replace('\u240a', '\n').replace('\u240b', '\n').replace('\u240c', '\n').replace('\u240d', '\n').replace('\u2424', '\n')
    i = 0
    bracket_stack = []
    _bracket_stack_append = bracket_stack.append
    def bracket_stack_append(x):
        if len(bracket_stack) > 298:
            return LexerError('brackets nested too deep (max: 300)', i)
        _bracket_stack_append(x)
    i = 0
    new_source = ''
    while i < len_source:
        if source[i] == '/':
            start_possible_comment = i = i + 1
            if i < len_source:
                if source[i] == ';':
                    i += 1
                    while i < len_source and source[i] not in newlines:
                        if source[i] == '\\':
                            i += 1
                        i += 1
                elif source[i] == ':':
                    i += 1
                    level_nested = 1
                    while (i < len_source and (source[i] != ':'
                            or i + 1 < len_source and source[i + 1] != '/'
                            or (level_nested := level_nested - 1))):
                        if source[i] == '\\':
                            i += 1
                        elif source[i] == '/' and source[i + 1] == ':':
                            i += 1
                            level_nested += 1
                        i += 1
                    i += 2
                    if i > len_source:
                        print(LexerWarningWithStart("Unterminated multiline comment",
                                                    (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l])+1,
                                                    "note: started here",
                                                    (l:=onenewl_source[:start_possible_comment].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_possible_comment].split('\n')[l])))
            else:
                new_source += '/'
        elif source[i] == '\\':
            if (i := i + 1) >= len_source or source[i] != '\\':
                if i < len_source:
                    if source[i] not in newlines:
                        return LexerError(f"Unexpected character {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'} after backslash", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]))
                    i += 1
                else:
                    print(LexerWarning("Unexpected end of file after backslash", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l])))
            elif source[i] == '\\':
                new_source += '\\\\'
                i += 1
        elif source[i] == '"':
            new_source += '"'
            while (i := i + 1) < len_source and source[i] != '"':
                if source[i] == '\\':
                    new_source += '\\'
                    i += 1
                new_source += source[i]
            if i < len_source:
                new_source += '"'
                i += 1
        elif source[i] == "'":
            new_source += "'"
            while (i := i + 1) < len_source and source[i] != "'":
                if source[i] == '\\':
                    new_source += '\\'
                    i += 1
                new_source += source[i]
            if i < len_source:
                new_source += "'"
                i += 1
        else:
            new_source += source[i]
            i += 1
    i = 0
    source = new_source
    len_source = len(source)
    while i < len_source:
        if source[i] in whitespaces:
            start = i
            tok_type = break_or_space[is_newline := source[i] in newlines]
            while (i := i + 1) < len_source and source[i] in whitespaces:
                if (_is_newline := source[i] in newlines) is not is_newline:
                    new_token((tok_type, source[start:i], start, i))
                    tok_type = break_or_space[is_newline := _is_newline]
                    start = i
            new_token((tok_type, source[start:i], start, i))
        elif source[i] == '(':
            new_token((LT_LPAREN, LS_LPAREN, i, (i := i + 1)))
            bracket_stack_append(('(', i))
        elif source[i] == ')':
            if not bracket_stack:
                return LexerError("Closing ) does not match any bracket", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]))
            elif bracket_stack[-1][0] != '(':
                j = bracket_stack[-1][1]
                return LexerErrorWithStart(f'Closing ) does not match {bracket_stack[-1][0]!s}',
                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                           "note: opening bracket here",
                                           (l:=onenewl_source[:j].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:j].split('\n')[l]))
            bracket_stack.pop()
            new_token((LT_RPAREN, LS_RPAREN, i, (i := i + 1)))
        elif source[i] == '[':
            new_token((LT_LBRACKET, LS_LBRACKET, i, (i := i + 1)))
            bracket_stack_append(('[', i))
        elif source[i] == ']':
            if not bracket_stack:
                return LexerError("Closing ] does not match any bracket", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]))
            elif bracket_stack[-1][0] != '[':
                j = bracket_stack[-1][1]
                return LexerErrorWithStart(f'Closing ] does not match {bracket_stack[-1][0]!s}',
                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                           "note: opening bracket here",
                                           (l:=onenewl_source[:j].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:j].split('\n')[l]))
            bracket_stack.pop()
            new_token((LT_RBRACKET, LS_RBRACKET, i, (i := i + 1)))
        elif source[i] == '{':
            new_token((LT_LBRACE, LS_LBRACE, i, (i := i + 1)))
            bracket_stack_append(('{', i))
        elif source[i] == '}':
            if not bracket_stack:
                return LexerError("Closing } does not match any bracket", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]))
            elif bracket_stack[-1][0] != '{':
                j = bracket_stack[-1][1]
                return LexerErrorWithStart(f'Closing }} does not match {bracket_stack[-1][0]!s}',
                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                           "note: opening bracket here",
                                           (l:=onenewl_source[:j].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:j].split('\n')[l]))
            bracket_stack.pop()
            new_token((LT_RBRACE, LS_RBRACE, i, (i := i + 1)))
        elif source[i] == ',':
            new_token((LT_COMMA, LS_COMMA, i, (i := i + 1)))
        elif source[i] == ':':
            if (i := i + 1) < len_source:
                if source[i] == '>':
                    new_token((LT_COLONGT, LS_COLONGT, i, (i := i + 1)))
                elif source[i] == '.':
                    new_token((LT_COLONDOT, LS_COLONDOT, i, (i := i + 1)))
                else:
                    new_token((LT_COLON, LS_COLON, i - 1, i))
            else:
                new_token((LT_COLON, LS_COLON, i - 1, i))
        elif source[i] == ';':
            new_token((LT_SEMICOLON, LS_SEMICOLON, i, (i := i + 1)))
        elif source[i] == '.' and (i + 1 >= len_source or source[i + 1] not in digits):
            if (i := i + 1) < len_source:
                if source[i] == '=':
                    new_token((LT_DOTEQUAL, LS_DOTEQUAL, i, (i := i + 1)))
                elif source[i] == '.':
                    new_token((LT_DBLDOT, LS_DBLDOT, i, (i := i + 1)))
                else:
                    new_token((LT_DOT, LS_DOT, i - 1, i))
            else:
                new_token((LT_DOT, LS_DOT, i - 1, i))
        elif source[i] == '?':
            if (i := i + 1) < len_source:
                if source[i] == ':':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_QMARKCOLONEQUAL, LS_QMARKCOLONEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_QMARKCOLON, LS_QMARKCOLON, i - 2, i))
                elif source[i] == '?':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_DBLQMARKEQUAL, LS_DBLQMARKEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_DBLQMARK, LS_DBLQMARK, i - 2, i))
                elif source[i] == '=':
                    new_token((LT_QMARKEQUAL, LS_QMARKEQUAL, i - 1, (i := i + 1)))
                else:
                    new_token((LT_QMARK, LS_QMARK, i - 1, i))
            else:
                new_token((LT_QMARK, LS_QMARK, i - 1, i))
        elif source[i] == '&':
            if (i := i + 1) < len_source:
                if source[i] == '&':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_DBLAMPEQUAL, LS_DBLAMPEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_DBLAMP, LS_DBLAMP, i - 2, i))
                elif source[i] == '=':
                    new_token((LT_AMPEQUAL, LS_AMPEQUAL, i - 1, (i := i + 1)))
                else:
                    new_token((LT_AMP, LS_AMP, i - 1, i))
            else:
                new_token((LT_AMP, LS_AMP, i - 1, i))
        elif source[i] == '*':
            if (i := i + 1) < len_source and source[i] == '=':
                new_token((LT_STAREQUAL, LS_STAREQUAL, i - 1, (i := i + 1)))
            else:
                new_token((LT_STAR, LS_STAR, i - 1, i))
        elif source[i] == '#':
            if (i := i + 1) < len_source:
                if source[i] == '=':
                    new_token((LT_TAGEQUAL, LS_TAGEQUAL, i - 1, (i := i + 1)))
                elif source[i] == '!':
                    new_token((LT_TAGEXCLMARK, LS_TAGEXCLMARK, i - 1, (i := i + 1)))
                else:
                    new_token((LT_TAG, LS_TAG, i - 1, i))
            else:
                new_token((LT_TAG, LS_TAG, i - 1, i))
        elif source[i] == '!':
            if (i := i + 1) < len_source and source[i] == '=':
                new_token((LT_EXCLMARKEQUAL, LS_EXCLMARKEQUAL, i - 1, (i := i + 1)))
            else:
                new_token((LT_EXCLMARK, LS_EXCLMARK, i - 1, i))
        elif source[i] == '^':
            if (i := i + 1) < len_source and source[i] == '=':
                new_token((LT_CARETEQUAL, LS_CARETEQUAL, i - 1, (i := i + 1)))
            else:
                new_token((LT_CARET, LS_CARET, i - 1, i))
        elif source[i] == '-':
            if (i := i + 1) < len_source:
                if source[i] == '=':
                    new_token((LT_MINUSEQUAL, LS_MINUSEQUAL, i - 1, (i := i + 1)))
                elif source[i] == '>':
                    new_token((LT_MINUSGT, LS_MINUSGT, i - 1, (i := i + 1)))
                else:
                    new_token((LT_MINUS, LS_MINUS, i - 1, i))
            else:
                new_token((LT_MINUS, LS_MINUS, i - 1, i))
        elif source[i] == '+':
            if (i := i + 1) < len_source and source[i] == '=':
                new_token((LT_PLUSEQUAL, LS_PLUSEQUAL, i - 1, (i := i + 1)))
            else:
                new_token((LT_PLUS, LS_PLUS, i - 1, i))
        elif source[i] == '~':
            if (i := i + 1) < len_source:
                if source[i] == '&':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_TILDEAMPEQUAL, LS_TILDEAMPEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_TILDEAMP, LS_TILDEAMP, i - 2, i))
                elif source[i] == '$':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_TILDEDOLLAREQUAL, LS_TILDEDOLLAREQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_TILDEDOLLAR, LS_TILDEDOLLAR, i - 2, i))
                elif source[i] == '|':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_TILDEPIPEEQUAL, LS_TILDEPIPEEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_TILDEPIPE, LS_TILDEPIPE, i - 2, i))
                elif source[i] == '>':
                    new_token((LT_TILDEGT, LS_TILDEGT, i - 1, (i := i + 1)))
                elif source[i] == '!':
                    new_token((LT_TILDEEXCLMARK, LS_TILDEEXCLMARK, i - 1, (i := i + 1)))
                else:
                    new_token((LT_TILDE, LS_TILDE, i - 1, i))
            else:
                new_token((LT_TILDE, LS_TILDE, i - 1, i))
        elif source[i] == '/':
            if (i := i + 1) < len_source:
                if source[i] == '/':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_DBLSLASHEQUAL, LS_DBLSLASHEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_DBLSLASH, LS_DBLSLASH, i - 2, i))
                elif source[i] == '=':
                    new_token((LT_SLASHEQUAL, LS_SLASHEQUAL, i - 1, (i := i + 1)))
                else:
                    new_token((LT_SLASH, LS_SLASH, i - 1, i))
        elif source[i] == '%':
            if (i := i + 1) < len_source and source[i] == '=':
                new_token((LT_PERCENTEQUAL, LS_PERCENTEQUAL, i - 1, (i := i + 1)))
            else:
                new_token((LT_PERCENT, LS_PERCENT, i - 1, i))
        elif source[i] == '\\':
            if (i := i + 2) < len_source and source[i] == '=':
                new_token((LT_DBLBACKSLASHEQUAL, LS_DBLBACKSLASHEQUAL, i - 2, (i := i + 1)))
            else:
                new_token((LT_DBLBACKSLASH, LS_DBLBACKSLASH, i - 2, i))
        elif source[i] == '<':
            if (i := i + 1) < len_source:
                if source[i] == '<':
                    if (i := i + 1) < len_source:
                        if source[i] == '<':
                            if (i := i + 1) < len_source and source[i] == '=':
                                new_token((LT_TRPLLTEQUAL, LS_TRPLLTEQUAL, i - 3, (i := i + 1)))
                            else:
                                new_token((LT_TRPLLT, LS_TRPLLT, i - 3, i))
                        elif source[i] == '=':
                            new_token((LT_DBLLTEQUAL, LS_DBLLTEQUAL, i - 2, (i := i + 1)))
                        else:
                            new_token((LT_DBLLT, LS_DBLLT, i - 2, i))
                    else:
                        new_token((LT_DBLLT, LS_DBLLT, i - 2, i))
                elif source[i] == '>' and i + 1 < len_source and source[i + 1] == '=':
                    new_token((LT_LTGTEQUAL, LS_LTGTEQUAL, i - 2, (i := i + 2)))
                elif source[i] == '=':
                    if (i := i + 1) < len_source and source[i] == '>':
                        new_token((LT_LTEQUALGT, LS_LTEQUALGT, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_LTEQUAL, LS_LTEQUAL, i - 2, i))
                else:
                    new_token((LT_LT, LS_LT, i - 1, i))
            else:
                new_token((LT_LT, LS_LT, i - 1, i))
        elif source[i] == '>':
            if (i := i + 1) < len_source:
                if source[i] == '>':
                    if (i := i + 1) < len_source:
                        if source[i] == '>':
                            if (i := i + 1) < len_source and source[i] == '=':
                                new_token((LT_TRPLGTEQUAL, LS_TRPLGTEQUAL, i - 3, (i := i + 1)))
                            else:
                                new_token((LT_TRPLGT, LS_TRPLGT, i - 3, i))
                        elif source[i] == '=':
                            new_token((LT_DBLGTEQUAL, LS_DBLGTEQUAL, i - 2, (i := i + 1)))
                        else:
                            new_token((LT_DBLGT, LS_DBLGT, i - 2, i))
                    else:
                        new_token((LT_DBLGT, LS_DBLGT, i - 2, i))
                elif source[i] == '<' and i + 1 < len_source and source[i + 1] == '=':
                    new_token((LT_GTLTEQUAL, LS_GTLTEQUAL, i - 2, (i := i + 2)))
                elif source[i] == '=':
                    new_token((LT_GTEQUAL, LS_GTEQUAL, i - 1, (i := i + 1)))
                else:
                    new_token((LT_GT, LS_GT, i - 1, i))
            else:
                new_token((LT_GT, LS_GT, i - 1, i))
        elif source[i] == '$':
            if (i := i + 1) < len_source:
                if source[i] == '$':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_DBLDOLLAREQUAL, LS_DBLDOLLAREQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_DBLDOLLAR, LS_DBLDOLLAR, i - 2, i))
                elif source[i] == '=':
                    new_token((LT_DOLLAREQUAL, LS_DOLLAREQUAL, i - 1, (i := i + 1)))
                else:
                    new_token((LT_DOLLAR, LS_DOLLAR, i - 1, i))
            else:
                new_token((LT_DOLLAR, LS_DOLLAR, i - 1, i))
        elif source[i] == '|':
            if (i := i + 1) < len_source:
                if source[i] == '|':
                    if (i := i + 1) < len_source and source[i] == '=':
                        new_token((LT_DBLPIPEEQUAL, LS_DBLPIPEEQUAL, i - 2, (i := i + 1)))
                    else:
                        new_token((LT_DBLPIPE, LS_DBLPIPE, i - 1, i))
                elif source[i] == '=':
                    new_token((LT_PIPEEQUAL, LS_PIPEEQUAL, i - 1, (i := i + 1)))
                else:
                    new_token((LT_PIPE, LS_PIPE, i - 1, i))
            else:
                new_token((LT_PIPE, LS_PIPE, i - 1, i))
        elif source[i] == '`':
            start = i = i + 1
            while i < len_source and source[i] != '`':
                i += 1
            if i < len_source:
                new_token((LT_IDENT, source[start:i], start, (i := i + 1)))
            else:
                return LexerErrorWithStart("Unexpected EOF while parsing backtick identifier",
                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                           "note: started backtick identifier here",
                                           (l:=onenewl_source[:start].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start].split('\n')[l]))
        elif source[i] == '=':
            if (i := i + 1) < len_source:
                if source[i] == '=':
                    new_token((LT_DBLEQUAL, LS_DBLEQUAL, i - 1, (i := i + 1)))
                elif source[i] == '<':
                    new_token((LT_EQUALLT, LS_EQUALLT, i - 1, (i := i + 1)))
                elif source[i] == '>':
                    new_token((LT_EQUALGT, LS_EQUALGT, i - 1, (i := i + 1)))
                else:
                    new_token((LT_EQUAL, LS_EQUAL, i - 1, i))
            else:
                new_token((LT_EQUAL, LS_EQUAL, i - 1, i))
        elif source[i] == '@':
            if (i := i + 1) < len_source and source[i] == '=':
                new_token((LT_CMATEQUAL, LS_CMATEQUAL, i - 1, (i := i + 1)))
            else:
                new_token((LT_CMAT, LS_CMAT, i-1, i))
        elif source[i] == "'":
            start = i = i + 1
            start_token = start - len(string_specifier) - 1
            if start == len_source:
                return LexerErrorWithStart("Unexpected EOF while parsing single-quoted string",
                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                           "note: started string here",
                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
            is_raw = 'r' in string_specifier
            is_ascii = 'a' in string_specifier
            is_non_ascii = 'u' in string_specifier
            if is_ascii and is_non_ascii:
                is_ascii = is_non_ascii = False
            is_bytes = 'b' in string_specifier
            is_formatted = 'f' in string_specifier
            if (is_char := 'c' in string_specifier):
                char = source[i]
                if char in newlines:
                    i += 1
                    if i < len_source and source[i] == "'":
                        new_token((LT_STRING, char, is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                        i += 1
                        continue
                    else:
                        return LexerErrorWithStart(f"Expected single quote character, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                   "note: started string here",
                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                if is_raw:
                    i += 1
                    if i < len_source and source[i] == "'":
                        new_token((LT_STRING, char, is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                        i += 1
                    else:
                        return LexerErrorWithStart(f"Expected single quote closing character, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                   "note: started string here",
                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                else:
                    if char == '\\':
                        i += 1
                        if i == len_source:
                            return LexerErrorWithStart("Unexpected EOF",
                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                       "note: started string here",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        if source[i] == 'x':
                            i += 1
                            if i == len_source:
                                return LexerErrorWithStart("Unexpected EOF",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            
                            if source[i] in hex_digits:
                                i += 1
                                if i == len_source:
                                    return LexerErrorWithStart("Unexpected EOF",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                if source[i] in hex_digits:
                                    i += 1
                                    if i < len_source and source[i] == "'":
                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                        i += 1
                                    else:
                                        return LexerErrorWithStart(f"Expected single quote closing character after hex escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                elif source[i] == "'":
                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                    i += 1
                                else:
                                    return LexerErrorWithStart(f"Expected single quote closing character after hex escape, got {f'U+{ord(source[i]):04x}'}",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            elif source[i] == "'":
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected single quote closing character after hex escape, got {f'U+{ord(source[i]):04x}'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        elif source[i] == 'u':
                            i += 1
                            if i == len_source:
                                return LexerErrorWithStart("Unexpected EOF",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            if source[i] in hex_digits:
                                i += 1
                                if i == len_source:
                                    return LexerErrorWithStart("Unexpected EOF",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                if source[i] in hex_digits:
                                    i += 1
                                    if i == len_source:
                                        return LexerErrorWithStart("Unexpected EOF",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    if source[i] in hex_digits:
                                        i += 1
                                        if i == len_source:
                                            return LexerErrorWithStart("Unexpected EOF",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        if source[i] in hex_digits:
                                            i += 1
                                            if i < len_source and source[i] == "'":
                                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                i += 1
                                            else:
                                                return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                           "note: started string here",
                                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        elif source[i] == "'":
                                            new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                            i += 1
                                        else:
                                            return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    elif source[i] == "'":
                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                        i += 1
                                    else:
                                        return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                elif source[i] == "'":
                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                    i += 1
                                else:
                                    return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            elif source[i] == "'":
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        
                        elif source[i] == 'U':
                            i += 1
                            if i == len_source:
                                return LexerErrorWithStart("Unexpected EOF",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            if source[i] in hex_digits:
                                i += 1
                                if i == len_source:
                                    return LexerErrorWithStart("Unexpected EOF",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                if source[i] in hex_digits:
                                    i += 1
                                    if i == len_source:
                                        return LexerErrorWithStart("Unexpected EOF",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    if source[i] in hex_digits:
                                        i += 1
                                        if i == len_source:
                                            return LexerErrorWithStart("Unexpected EOF",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        if source[i] in hex_digits:
                                            i += 1
                                            if i == len_source:
                                                return LexerErrorWithStart("Unexpected EOF",
                                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                           "note: started string here",
                                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                            if source[i] in hex_digits:
                                                i += 1
                                                if i == len_source:
                                                    return LexerErrorWithStart("Unexpected EOF",
                                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                               "note: started string here",
                                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                                if source[i] in hex_digits:
                                                    i += 1
                                                    if i < len_source and source[i] == "'":
                                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                        i += 1
                                                    else:
                                                        return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                                   "note: started string here",
                                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                                elif source[i] == "'":
                                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                    i += 1
                                                else:
                                                    return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                               "note: started string here",
                                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                            elif source[i] == "'":
                                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                i += 1
                                            else:
                                                return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                           "note: started string here",
                                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        elif source[i] == "'":
                                            new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                            i += 1
                                        else:
                                            return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    elif source[i] == "'":
                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                        i += 1
                                    else:
                                        return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                elif source[i] == "'":
                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                    i += 1
                                else:
                                    return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            elif source[i] == "'":
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected single quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        elif source[i] in escapables:
                            i += 1
                            if i < len_source and source[i] == "'":
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected single quote closing character after escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        else:
                            return LexerErrorWithStart(f"Expected escapable character after backslash, got {f'U+{ord(source[i]):04x}'}",
                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                       "note: started string here",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                    else:
                        if (i := i + 1) < len_source and source[i] == "'":
                            i += 1
                            new_token((LT_STRING, char, is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i))
                        else:
                            return LexerErrorWithStart(f"Expected single quote closing character after character, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                       "note: started string here",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
            else:
                if is_raw:
                    while i < len_source and (char := source[i]) != "'":
                        if char == "\\":
                            source = source[:i] + '\\' + source[i:]
                            i += 1
                        i += 1
                else:
                    can_escape = False
                    while i < len_source and ((char := source[i]) != "'" or can_escape):
                        if char == '\\':
                            can_escape = not can_escape
                        elif can_escape:
                            can_escape = 0
                        i += 1
                if i == len_source:
                    return LexerErrorWithStart(f"Unexpected EOF when lexing single-line string",
                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                               "note: started string here",
                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                i += 1
        elif source[i] == '"':
            start = i = i + 1
            start_token = start - len(string_specifier) - 1
            if start == len_source:
                return LexerErrorWithStart("Unexpected EOF",
                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                           "note: started string here",
                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
            is_raw = 'r' in string_specifier
            is_ascii = 'a' in string_specifier
            is_non_ascii = 'u' in string_specifier
            if is_ascii and is_non_ascii:
                is_ascii = is_non_ascii = 0
            is_bytes = 'b' in string_specifier
            is_formatted = 'f' in string_specifier
            if (is_char := 'c' in string_specifier):
                char = source[i]
                if char in newlines:
                    i += 1
                    if i < len_source and source[i] == '"':
                        new_token((LT_STRING, char, is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                        i += 1
                        continue
                    else:
                        return LexerErrorWithStart(f"Expected double quote closing character after character, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                   "note: started string here",
                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                if is_raw:
                    i += 1
                    if i < len_source and source[i] == '"':
                        new_token((LT_STRING, char, is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                        i += 1
                    else:
                        return LexerErrorWithStart(f"Expected double quote closing character, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                   "note: started string here",
                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                else:
                    if char == '\\':
                        i += 1
                        if i == len_source:
                            return LexerErrorWithStart("Unexpected EOF",
                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                       "note: started string here",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        if source[i] == 'x':
                            i += 1
                            if i == len_source:
                                return LexerErrorWithStart("Unexpected EOF",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            
                            if source[i] in hex_digits:
                                i += 1
                                if i == len_source:
                                    return LexerErrorWithStart("Unexpected EOF",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                if source[i] in hex_digits:
                                    i += 1
                                    if i < len_source and source[i] == '"':
                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                        i += 1
                                    else:
                                        return LexerErrorWithStart(f"Expected double quote closing character after hex escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                elif source[i] == '"':
                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                    i += 1
                                else:
                                    return LexerErrorWithStart(f"Expected double quote closing character after hex escape, got {f'U+{ord(source[i]):04x}'}",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            elif source[i] == '"':
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected double quote closing character after hex escape, got {f'U+{ord(source[i]):04x}'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        elif source[i] == 'u':
                            i += 1
                            if i == len_source:
                                return LexerErrorWithStart("Unexpected EOF",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            if source[i] in hex_digits:
                                i += 1
                                if i == len_source:
                                    return LexerErrorWithStart("Unexpected EOF",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                if source[i] in hex_digits:
                                    i += 1
                                    if i == len_source:
                                        return LexerErrorWithStart("Unexpected EOF",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    if source[i] in hex_digits:
                                        i += 1
                                        if i == len_source:
                                            return LexerErrorWithStart("Unexpected EOF",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        if source[i] in hex_digits:
                                            i += 1
                                            if i < len_source and source[i] == '"':
                                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                i += 1
                                            else:
                                                return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                           "note: started string here",
                                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        elif source[i] == '"':
                                            new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                            i += 1
                                        else:
                                            return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    elif source[i] == '"':
                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                        i += 1
                                    else:
                                        return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                elif source[i] == '"':
                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                    i += 1
                                else:
                                    return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            elif source[i] == '"':
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        
                        elif source[i] == 'U':
                            i += 1
                            if i == len_source:
                                return LexerErrorWithStart("Unexpected EOF",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            if source[i] in hex_digits:
                                i += 1
                                if i == len_source:
                                    return LexerErrorWithStart("Unexpected EOF",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                if source[i] in hex_digits:
                                    i += 1
                                    if i == len_source:
                                        return LexerErrorWithStart("Unexpected EOF",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    if source[i] in hex_digits:
                                        i += 1
                                        if i == len_source:
                                            return LexerErrorWithStart("Unexpected EOF",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        if source[i] in hex_digits:
                                            i += 1
                                            if i == len_source:
                                                return LexerErrorWithStart("Unexpected EOF",
                                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                           "note: started string here",
                                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                            if source[i] in hex_digits:
                                                i += 1
                                                if i == len_source:
                                                    return LexerErrorWithStart("Unexpected EOF",
                                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                               "note: started string here",
                                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                                if source[i] in hex_digits:
                                                    i += 1
                                                    if i < len_source and source[i] == '"':
                                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                        i += 1
                                                    else:
                                                        return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                                   "note: started string here",
                                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                                elif source[i] == '"':
                                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                    i += 1
                                                else:
                                                    return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                               "note: started string here",
                                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                            elif source[i] == '"':
                                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                                i += 1
                                            else:
                                                return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                           "note: started string here",
                                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                        elif source[i] == '"':
                                            new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                            i += 1
                                        else:
                                            return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                       "note: started string here",
                                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                    elif source[i] == '"':
                                        new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                        i += 1
                                    else:
                                        return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                                   "note: started string here",
                                                                   (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                                elif source[i] == '"':
                                    new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                    i += 1
                                else:
                                    return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                               "note: started string here",
                                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                            elif source[i] == '"':
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected double quote closing character after unicode escape, got {f'U+{ord(source[i]):04x}'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        elif source[i] in escapables:
                            i += 1
                            if i < len_source and source[i] == '"':
                                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                                i += 1
                            else:
                                return LexerErrorWithStart(f"Expected double quote closing character after escape, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                           "note: started string here",
                                                           (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                        else:
                            return LexerErrorWithStart(f"Expected escapable character after backslash, got {f'U+{ord(source[i]):04x}'}",
                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                       "note: started string here",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                    else:
                        if (i := i + 1) < len_source and source[i] == '"':
                            i += 1
                            new_token((LT_STRING, char, is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                        else:
                            i += 1
                            return LexerErrorWithStart(f"Expected double quote closing character after character, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                       "note: started string here",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
            else:
                if is_raw:
                    while i < len_source and (char := source[i]) != '"':
                        if char == "\\":
                            source = source[:i] + '\\' + source[i:]
                            i += 1
                        i += 1
                else:
                    can_escape = False
                    while i < len_source and ((char := source[i]) != '"' or can_escape):
                        if char == '\\':
                            can_escape = not can_escape
                        elif can_escape:
                            can_escape = 0
                        i += 1
                if i == len_source:
                    return LexerErrorWithStart(f"Unexpected EOF when lexing single-line string",
                                               (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                               "note: started string here",
                                               (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]))
                new_token((LT_STRING, source[start:i], is_formatted, is_ascii, is_non_ascii, is_bytes, is_char, start_token, i + 1))
                i += 1
        elif source[i] in identifier_characters:
            start = i
            while (i := i + 1) < len_source and source[i] in ident_digits:
                pass
            ident = source[start:i]
            if i < len_source and source[i] in quotes and ''.join(set(ident)) in string_specifiers:
                string_specifier = ident.lower()
            else:
                new_token((LT_IDENT, ident, start, i))
        elif source[i] == '0' and i + 1 < len_source and (modestr := source[i + 1]) in 'xbosfdl':
            start_token = i
            start_num = i = i + 2
            possible_specifier = ''
            if source[i] in 'xbo':
                possible_specifier = modestr
                modestr = source[i]
                start_num = i = i + 1
            elif modestr not in 'xbo':
                return LexerErrorWithTildeAndCaret(f"0 with identifier character {modestr} is not a valid number; mode is not valid",
                                                   (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]),
                                                   len(possible_specifier) + 1, 1)
            is_dec = False
            supposed_digits = specifier_digits[mode := int((modestr != 'b') + (modestr == 'o'))]
            while i < len_source and source[i] in supposed_digits:
                i += 1
            if i < len_source and source[i] == '.':
                if i + 1 >= len_source or source[i + 1] != '.':
                    is_dec = True
                    while (i := i + 1) < len_source and source[i] in supposed_digits:
                        pass
            if i == start_num:
                if mode == 2:
                    return LexerErrorWithTildeAndCaret(f"Expected at least one octal digit after octal number specifier, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]),
                                                       len(possible_specifier) + 2, 1)
                elif not mode:
                    return LexerErrorWithTildeAndCaret(f"Expected at least one binary digit after binary number specifier, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]),
                                                       len(possible_specifier) + 2, 1)
                else:
                    return LexerErrorWithTildeAndCaret(f"Expected at least one hex digit after hex number specifier, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l]),
                                                       len(possible_specifier) + 2, 1)
            end_num = i
            specifier = ''
            if possible_specifier in number_specifiers[is_dec]:
                specifier = possible_specifier
            elif possible_specifier:
                print(LexerWarning(f"Ignoring number specifier '{possible_specifier}'; number type {'decimal' if is_dec else 'integer'} does not have such a specifier", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l])))
            if i < len_source and source[i] == 'p':
                start_exp = i = i + 1
                err_if_no_num = start_exp + 1
                err_if_no_digits = start_exp
                if i < len_source and source[i] in '+-':
                    i += 1
                    err_if_no_num += 1
                    err_if_no_digits += 1
                if i < len_source and source[i] == '0' and i + 1 < len_source and source[i + 1] in 'xbo':
                    i += 1
                    supposed_digits = specifier_digits[(source[i] != 'b') + (source[i] == 'o')]
                    while (i := i + 1) < len_source and source[i] in supposed_digits:
                        pass
                    if source[i - 1] == 'x':
                        return LexerErrorWithTildeAndCaret(f"Expected hexadecimal digits after hex number exponent, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:err_if_no_digits].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:err_if_no_digits].split('\n')[l]),
                                                           2, 1)
                    elif source[i - 1] == 'b':
                        return LexerErrorWithTildeAndCaret(f"Expected binary digits after binary number exponent, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:err_if_no_digits].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:err_if_no_digits].split('\n')[l]),
                                                           2, 1)
                    elif source[i - 1] == 'o':
                        return LexerErrorWithTildeAndCaret(f"Expected octal digits after octal number exponent, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:err_if_no_digits].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:err_if_no_digits].split('\n')[l]),
                                                           2, 1)
                elif i < len_source and source[i] in digits:
                    while (i := i + 1) < len_source and source[i] in digits:
                        pass
                else:
                    return LexerErrorWithTildeAndCaret(f"Expected number after exponent indicator, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:start_token].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_token].split('\n')[l])-1,
                                                       err_if_no_num - start_token, 1)
                new_token((int_or_dec[is_dec], source[start_num:end_num], eval(source[start_exp:i] or '0'), specifier, mode, start_token, i))
            else:
                new_token((int_or_dec[is_dec], source[start_num:end_num], 0, specifier, mode, start_token, i))
        elif source[i] in digits or source[i] == '.' and i + 1 < len_source and source[i + 1] in digits:
            start_token = start_num = i
            is_dec = False
            while (i := i + 1) < len_source and source[i] in digits:
                pass
            if i < len_source and source[i] == '.':
                if i + 1 >= len_source or source[i + 1] != '.':
                    is_dec = True
                    while (i := i + 1) < len_source and source[i] in digits:
                        pass
            specifier = ''
            end_num = i
            if i < len_source and source[i] in number_specifiers[is_dec]:
                specifier = source[i]
                i += 1
            if i < len_source and source[i] == 'e':
                start_exp = i = i + 1
                err_if_no_num = start_exp + 1
                err_if_no_digits = start_exp
                if i < len_source and source[i] in '+-':
                    i += 1
                    err_if_no_num += 1
                    err_if_no_digits += 1
                if i < len_source and source[i] == '0' and source[i + 1] in 'xbo':
                    i += 1
                    supposed_digits = specifier_digits[(source[i] != 'b') + (source[i] == 'o')]
                    while (i := i + 1) < len_source and source[i] in supposed_digits:
                        pass
                    if source[i - 1] == 'x':
                        return LexerErrorWithTildeAndCaret(f"Expected hexadecimal digits after hex number exponent, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:err_if_no_digits].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:err_if_no_digits].split('\n')[l]),
                                                           2, 1)
                    elif source[i - 1] == 'b':
                        return LexerErrorWithTildeAndCaret(f"Expected binary digits after binary number exponent, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:err_if_no_digits].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:err_if_no_digits].split('\n')[l]),
                                                           2, 1)
                    elif source[i - 1] == 'o':
                        return LexerErrorWithTildeAndCaret(f"Expected octal digits after octal number exponent, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                           (l:=onenewl_source[:err_if_no_digits].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:err_if_no_digits].split('\n')[l]),
                                                           2, 1)
                elif i < len_source and source[i] in digits:
                    while (i := i + 1) < len_source and source[i] in digits:
                        pass
                else:
                    return LexerErrorWithTildeAndCaret(f"Expected number after exponent indicator, got {i < len_source and f'U+{ord(source[i]):04x}' or 'EOF'}",
                                                       (l:=onenewl_source[:start_num].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:start_num].split('\n')[l]),
                                                       err_if_no_digits - start_num, 1)
                new_token((int_or_dec[is_dec], source[start_num:end_num], eval(source[start_exp:i] or '0'), specifier, 3, start_token, i))
            else:
                new_token((int_or_dec[is_dec], source[start_num:end_num], 0, specifier, 3, start_token, i))
        else:
            print(LexerWarning(f"Ignoring unexpected character {f'U+{ord(source[i]):04x}'}", (l:=onenewl_source[:i].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:i].split('\n')[l]), len(onenewl_source[:i].split('\n')[l])))
    if bracket_stack:
        j = bracket_stack[-1][1]
        return LexerError(f"Bracket was never closed: {bracket_stack[-1][0]}",
                          (l:=onenewl_source[:j].count('\n'))+1, onenewl_source.split('\n')[l], len(onenewl_source[:j].split('\n')[l]))
    new_token((LT_EOF, 'EOF', -1, -1))
    yield None
    yield tokens

def lexer(source):
    """
    Lexer for the Estil language.
    """
    gen = _lexer(source)
    try:
        next(gen)
    except StopIteration as e:
        return e.args[0]
    except TypeError:
        return next(gen)
    else:
        return next(gen)

if 0:
    [*lexer(r"5.7de-12339341444841231232323333124.7")]
    [*lexer("crbfua'\u2424'")]
    print(lexer("\\ "))
    lexer('0bb1101')
    lexer('0lb1')
    lexer('0bb.3')
    lexer('0bx3.87')
    lexer('0sb.2')
    print(lexer("0x.3p"))
    print(lexer("1.3e"))
    print(lexer("0x.3p0x"))
    print(lexer("1.3e0b"))
    print(lexer("[((({})]"))
