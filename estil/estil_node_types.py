from estil_lexer import lexer
from itertools import zip_longest
from decimal import Decimal

class AST_Node:
    __module__ = 'builtins'
    __slots__ = ('start_pos', 'value', '_name')
    def __init__(self, value, _name='AST_Node', start_pos=-1):
        self.value = value
        self._name = _name
        self.start_pos = start_pos
    def __repr__(self):
        return f"{self._name}({self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.value!s}"

class AST_Exec(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Exec", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return '\n'.join(map(str, self.value))

class AST_Eval(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Eval", start_pos=start_pos)

class AST_Expr(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Expr", start_pos=start_pos)

class AST_LabeledBlock(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, value, start_pos=-1):
        super().__init__(value, "AST_LabeledBlock", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_LabeledBlock({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.name!s} = {self.value!s}"

class AST_RawLoopStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_RawLoopStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"loop {self.value!s}"

class AST_WhileStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, condition, value, *, do_first, start_pos=-1):
        super().__init__(value, "AST_WhileStmt", start_pos=start_pos)
        self.condition = condition
        self.do_first = do_first
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_WhileStmt({self.condition!r}, {self.value!r}, do_first={self.do_first!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.do_first:
            return f"do {self.value!s} while ({self.condition!s})"
        return f"while ({self.condition!s}) {self.value!s}"

class AST_SimpleForStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, iterable, value, start_pos=-1):
        super().__init__(value, "AST_SimpleForStmt", start_pos=start_pos)
        self.iterable = iterable
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_SimpleForStmt({self.iterable!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"for {self.iterable!s} {self.value!s}"

class AST_ForStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, targets, iterable, value, start_pos=-1):
        super().__init__(value, "AST_ForStmt", start_pos=start_pos)
        self.targets = targets
        self.iterable = iterable
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_ForStmt({self.targets!r}, {self.iterable!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"for {self.targets!s} ~> {self.iterable!s} {self.value!s}"

class AST_CForStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, setup, condition, update, value, start_pos=-1):
        super().__init__(value, "AST_CForStmt", start_pos=start_pos)
        self.setup = setup
        self.condition = condition
        self.update = update
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_CForStmt({self.setup!r}, {self.condition!r}, {self.update!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"for ({self.setup!s} : {self.condition!s} : {self.update!s}) {self.value!s}"

class AST_FuncDef(AST_Node):
    __module__ = 'builtins'
    def __init__(self, tspec, name, params, captures, value, variation, is_op=False, start_pos=-1):
        super().__init__(value, "AST_FuncDef", start_pos=start_pos)
        self.tspec = tspec
        self.name = name
        self.params = params
        self.captures = captures
        self.variation = variation
        self.is_op = is_op
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_FuncDef({self.tspec!r}, {self.name!r}, {self.params!r}, {self.captures!r}, {self.value!r}, {self.variation!r}, is_op={self.is_op!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.captures:
            captures_s = f"[{'; '.join(map(str, self.captures))}]"
        else:
            captures_s = ""
        if (tspecs := self.tspec):
            if len(tspecs) == 1:
                tspec_s = f"{tspecs[0]!s} "
            else:
                tspec_s = f"({', '.join(map(str, tspecs))}) "
        else:
            tspec_s = ""
        if isinstance(self.name, list) and isinstance(self.params, list):
            _list = [*zip_longest(self.name, self.params, fillvalue=AST_Param)]
            last = _list[-1]
            if last[1] is AST_Param:
                name_params_s = f"{last[0]!s}"
            else:
                name_params_s = f"{last[0]!s}({', '.join(map(str, last[1])) if last[1] else ''})"
            name_params_s = ''.join(map(lambda x: f"{x[0]!s}({', '.join(map(str, x[1]))})", _list[:-1])) + name_params_s
        elif self.is_op:
            name_params_s = f"op {self.name!s}({', '.join(map(str, self.params))})"
        else:
            name_params_s = ""
        return f"{captures_s}{tspec_s}{name_params_s}{self.variation or ''!s} {self.value!s}"

class AST_IfStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_IfStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        len_value = len(self.value)
        if_s = ""
        for i, (condition, block) in enumerate(self.value):
            if not i:
                if_s = f"if {condition!s} {block!s}"
            else:
                if condition is True and i == len_value - 1:
                    if_s = f"{if_s} else {block!s}"
                else:
                    if_s = f"{if_s} elif {condition!s} {block!s}"
        return if_s

class AST_SwitchStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, expr, value, start_pos=-1):
        super().__init__(value, "AST_SwitchStmt", start_pos=start_pos)
        self.expr = expr
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_SwitchStmt({self.expr!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        switch_s = f"switch {self.expr!s} {{ "
        for x in self.value:
            switch_s = f"{switch_s} {x!s} "
        return f"{switch_s}}}"

class AST_SwitchCaseStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, expr, targets, conditions, value, start_pos=-1):
        super().__init__(value, "AST_SwitchCaseStmt", start_pos=start_pos)
        self.expr = expr
        self.targets = targets
        self.conditions = conditions
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_SwitchCaseStmt({self.expr!r}, {self.targets!r}, {self.conditions!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.targets:
            targets_s = f" as {self.targets!s} "
        else:
            targets_s = ""
        if self.conditions:
            conditions_s = f" if {' if '.join(map(str, self.conditions))} "
        else:
            conditions_s = ""
        return f"case {self.expr!s}{targets_s}{conditions_s} {self.value!s}"

"""
class AST_MatchStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, expr, value, start_pos=-1):
        super().__init__(value, "AST_MatchStmt", start_pos=start_pos)
        self.expr = expr
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_MatchStmt({self.expr!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        match_s = f"match {self.expr!s} {{ "
        for x in self.value:
            match_s = f"{match_s} {x!s} "
        return f"{match_s}}}"

class AST_MatchCaseStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, expr, targets, conditions, value, start_pos=-1):
        super().__init__(value, "AST_MatchCaseStmt", start_pos=start_pos)
        self.expr = expr
        self.targets = targets
        self.conditions = conditions
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_MatchCaseStmt({self.expr!r}, {self.targets!r}, {self.conditions!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.targets:
            targets_s = f" as {self.targets!s} "
        else:
            targets_s = ""
        if self.conditions:
            conditions_s = f" if {' if '.join(map(str, self.conditions))} "
        else:
            conditions_s = ""
        return f"case {self.expr!s}{targets_s}{conditions_s} {self.value!s}"

"""
class AST_StructDef(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, value, start_pos=-1):
        super().__init__(value, "AST_StructDef", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_StructDef({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"struct {self.name!s} {{ {' '.join(map(str, self.value))} }}"

class AST_UnionDef(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, value, start_pos=-1):
        super().__init__(value, "AST_UnionDef", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_UnionDef({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"union {self.name!s} {{ {' '.join(map(str, self.value))} }}"

class AST_Field(AST_Node):
    __module__ = 'builtins'
    def __init__(self, tspec, value, start_pos=-1):
        super().__init__(value, "AST_Field", start_pos=start_pos)
        self.tspec = tspec
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Field({self.tspec!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.tspec!s} {self.value!s};"

class AST_EnumDef(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, value, start_pos=-1):
        super().__init__(value, "AST_EnumDef", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_EnumDef({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"enum {self.name!s} {{ {', '.join(map(str, self.value))} }}"

class AST_EnumField(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, value, start_pos=-1):
        super().__init__(value, "AST_EnumField", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_EnumField({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.value:
            return f"{self.name!s} = {self.value!s}"
        return f"{self.name!s}"

one_indent = '    '

class AST_Block(AST_Node):
    __module__ = 'builtins'
    __slots__ = 'indentlevel'
    def __init__(self, value, indentlevel=1, start_pos=-1):
        super().__init__(value, "AST_Block", start_pos=start_pos)
        self.indentlevel = indentlevel
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Block({self.value!r}, indentlevel={self.indentlevel!r}, start_pos={self.start_pos!r})"
    def __str__(self):
        indentlevel = self.indentlevel
        value = self.value
        if value and isinstance((last := self.value[-1]), AST_RetStmt) and last.start_pos == -1:
            value = value[:-1]
        if value:
            lines = '\n'.join(map(lambda x:f'{indentlevel * one_indent}{x!s}', value))
            return f"{{\n{lines}\n{(indentlevel-1) * one_indent}}}"
        return "{}"

class AST_FuncDcl(AST_Node):
    __module__ = 'builtins'
    def __init__(self, tspecs, name, value, start_pos=-1):
        super().__init__(value, "AST_FuncDcl", start_pos=start_pos)
        self.tspecs = tspecs
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_FuncDcl({self.tspecs!r}, {self.name!r}, {self.value!r}, start, start_pos={self.start_pos})"
    def __str__(self):
        if self.tspecs:
            tspecs_s = "dcl"
        else:
            if len(self.tspecs) == 1:
                tspecs_s = f"{self.tspecs[0]!s}"
            else:
                tspecs_s = f"({', '.join(map(str, self.tspecs))})"
        return f"{tspecs_s} {self.name!s}({', '.join(map(str, self.value))})"

class AST_StructDcl(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_StructDcl", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"struct {self.value!s}"

class AST_UnionDcl(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_UnionDcl", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"union {self.value!s}"

class AST_EnumDcl(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_EnumDcl", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"enum {self.value!s}"

class AST_RetStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, variation, value, implicit=False, start_pos=-1):
        super().__init__(value, "AST_RetStmt", start_pos=start_pos)
        self.variation = variation
        self.implicit = implicit
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_RetStmt({self.variation!r}, {self.value!r}, implicit={self.implicit!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.implicit:
            return f"{self.value!s}"
        elif self.value:
            return f"ret{self.variation or ''!s} {self.value!s}"
        else:
            return f"ret{self.variation or ''!s}"

class AST_ContStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_ContStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"cont{'' if self.value else self.value!s}"

class AST_BreakStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_BreakStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"break{'' if self.value else self.value!s}"

class AST_GotoStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_GotoStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"{self.value!s}::"

class AST_LabelStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_LabelStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"::{self.value!s}"

class AST_DelStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_DelStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"del {', '.join(map(str, self.value))}"

class AST_DclStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, tspec, value, start_pos=-1):
        super().__init__(value, "AST_DclStmt", start_pos=start_pos)
        self.tspec = tspec
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_DclStmt({self.tspec!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.tspec:
            tspec_s = f"{self.tspec!s}"
        else:
            tspec_s = "dcl"
        return f"{tspec_s} {', '.join(map(str, self.value))}"

class AST_UseStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_UseStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        self_s = ""
        for name, targets in self.value:
            if targets:
                self_s = f"{self_s}, {name!s} = ({targets!s})"
            else:
                self_s = f"{self_s}, {name!s}"
        return f"use {self_s[2:]}"

class AST_SubscrUse(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, index, start_pos=-1):
        super().__init__(value, "AST_SubscrUse", start_pos=start_pos)
        self.index = index
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_SubscrUse({self.value!r}, {self.index!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.value!s}[{self.index!s}]"

class AST_AttrUse(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_AttrUse", start_pos=start_pos)
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_AttrUse({self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return '.'.join(map(str, self.value))

class AST_InclStmt(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_InclStmt", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        self_s = ""
        for name, targets in self.value:
            if targets:
                self_s = f"{self_s}, {name!s} = ({targets!s})"
            else:
                self_s = f"{self_s}, {name!s}"
        return f"incl {self_s[:2]}"

class AST_AttrIncl(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_AttrIncl", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return '.'.join(map(str, self.value))

class AST_SubscrIncl(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, index, start_pos=-1):
        super().__init__(value, "AST_SubscrIncl", start_pos=start_pos)
        self.index = index
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_SubscrIncl({self.value!r}, {self.index!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.value!s}[{self.index!s}]"

class AST_Lambda(AST_Node):
    __module__ = 'builtins'
    def __init__(self, captures, tspec, args, value, is_simple=False, start_pos=-1):
        super().__init__(value, "AST_Lambda", start_pos=start_pos)
        self.captures = captures
        self.tspec = tspec
        self.args = args
        self.is_simple = is_simple
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Lambda({self.captures!r}, {self.tspec!r}, {self.args!r}, {self.value!r}, is_simple={self.is_simple!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.is_simple:
            if self.args:
                args_s = f"|{','.join(map(lambda x: f' {x!s}' if x else '', self.args))}|"
                if args_s[1] == ' ':
                    args_s = f"{args_s[0]}{args_s[2:]}"
            else:
                args_s = "||"
            return f"{args_s} {self.value.value[0]!s}"
        if self.captures:
            captures_s = f"[{'; '.join(map(str, self.captures))}] "
        else:
            captures_s = ""
        if self.tspec:
            if len(self.tspec) == 1:
                tspec_s = f"{self.tspec[0]!s} "
            else:
                tspec_s = f"({', '.join(map(str, self.tspec))}) "
        else:
            tspec_s = ""
        if self.args:
            args_s = f"({','.join(map(lambda x: f' {x!s}' if x else '', self.args))})"
            if args_s[1] == ' ':
                args_s = f"{args_s[0]}{args_s[2:]}"
        else:
            args_s = "()"
        return f"{captures_s}{tspec_s}{args_s}: {self.value!s}"

SeqUnpack = 0
MapUnpack = SeqUnpack + 1
Not = MapUnpack + 1
USub = Not + 1
UAdd = USub + 1
Invert = UAdd + 1
Fact = Invert + 1
Len = Fact + 1
Ref = Len + 1
Deref = Ref + 1
Safe = Deref + 1
postfix = {Fact, Safe}
unr_symbols = ["@", "$", "!", "-", "+", "~", "!", "#", "&", "*", "?"]

class AST_UnaryOp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, optype, value, *, precedence, start_pos=-1):
        super().__init__(value, "AST_UnaryOp", start_pos=start_pos)
        self.optype = optype
        self.precedence = precedence
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_UnaryOp({self.optype!r}, {self.value!r}, precedence={self.precedence!r}, start_pos={self.start_pos})"
    def __str__(self):
        val = self.value
        if isinstance(val, AST_UnaryOp) and val.precedence <= self.precedence:
            if (((self.optype in postfix) is not (val.optype in postfix))
                or val.optype in postfix and val.precedence is self.precedence):
                val_s = f"({val!s})"
            else:
                val_s = f"{val!s}"
        elif (isinstance(val, (AST_BinOp, AST_TernOp, AST_Compare,
                               AST_Assignment, AST_AugAssignment,
                               AST_Range, AST_Cast, AST_Primary))
                and val.precedence < self.precedence):
            val_s = f"({val!s})"
        else:
            val_s = f"{val!s}"
        if self.optype in postfix:
            return f"{val_s}{unr_symbols[self.optype]!s}"
        return f"{unr_symbols[self.optype]!s}{val_s}"

empty = ""
space = " "

class AST_Assignment(AST_Node):
    __module__ = 'builtins'
    def __init__(self, targets, value, start_pos=-1):
        super().__init__(value, "AST_Assignment", start_pos=start_pos)
        self.targets = targets
        self.precedence = 1
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Assignment({self.targets!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.targets!s} = {self.value!s}"

Then = 0
Also = Then + 1
TAnd = Also + 1
Clsc = TAnd + 1
BinOr = Clsc + 1
BinXor = BinOr + 1
BinAnd = BinXor + 1
BinNOr = BinAnd + 1
BinNXor = BinNOr + 1
BinNAnd = BinNXor + 1
Comp = BinNAnd + 1
Sub = Comp + 1
Add = Sub + 1
BNOr = Add + 1
BOr = BNOr + 1
BNXor = BOr + 1
BXor = BNXor + 1
BNAnd = BXor + 1
BAnd = BNAnd + 1
ARS = BAnd + 1
ALS = ARS + 1
BRR = ALS + 1
BLR = BRR + 1
BRS = BLR + 1
BLS = BRS + 1
CDiv = BLS + 1
Mod = CDiv + 1
Div = Mod + 1
FDiv = Div + 1
Mul = FDiv + 1
Pow = Mul + 1
Attr = Pow + 1
Call = Attr + 1
Subscr = Call + 1
bin_special_case = {Call, Subscr}
bin_symbols = ["=>", "=<", "?", "??", "||", "$$", "&&", "!||", "!$$", "!&&", "`",
               "-", "+", "~|", "|", "~$", "$", "~&", "&", ">>>", "<<<", "><",
               "<>", ">>", "<<", r"\\", "%", "/", "//", "*", "^", ".",
               ["(=", ")"], ["[=", "]"]]
special_augmented = Subscr + 1
Hyp = special_augmented
other_symbols = ["{0} {{{2}}}= {1}"]
class AST_AugAssignment(AST_Node):
    __module__ = 'builtins'
    def __init__(self, targets, optype, value, third=None, start_pos=-1):
        super().__init__(value, "AST_AugAssignment", start_pos=start_pos)
        self.targets = targets
        self.optype = optype
        self.third = third
        self.precedence = 1
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_AugAssignment({self.targets!r}, {self.optype!r}, {self.value!r}, {self.third!r}, start_pos={self.start_pos})"
    def __str__(self):
        optype = self.optype
        if optype >= special_augmented:
            return other_symbols[optype - special_augmented].format(self.targets, self.value, self.third)
        if optype in bin_special_case:
            return f"{self.targets!s}{f'{self.value!s}'.join(bin_symbols[optype])}"
        else:
            return f"{self.targets!s} {bin_symbols[optype]!s}= {self.value!s}"

TTern = 0
THyp = TTern + 1
tern_symbols = [[" ? ", " : "], ["{|", "|}"]]
class AST_TernOp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, op, *value, precedence, start_pos=-1):
        super().__init__(value, "AST_TernOp", start_pos=start_pos)
        self.left, self.mid, self.right = value
        self.op = op
        self.precedence = precedence
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_TernOp({self.op!r}, {self.left!r}, {self.mid!r}, {self.right!r}, precedence={self.precedence!r}, start_pos={self.start_pos})"
    def __str__(self):
        l = tern_symbols[self.op]
        return f"{self.left!s}{l[0]}{self.mid!s}{l[1]}{self.right!s}"

class AST_BinOp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, *value, precedence, start_pos=-1):
        super().__init__(value, "AST_BinOp", start_pos=start_pos)
        self.lhs, self.optype, self.rhs = value
        self.precedence = precedence
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_BinOp({self.lhs!r}, {self.optype!r}, {self.rhs!r}, precedence={self.precedence!r}, start_pos={self.start_pos})"
    def __str__(self):
        lhs = self.lhs
        if (isinstance(lhs, (AST_UnaryOp, AST_BinOp, AST_TernOp,
                             AST_Compare, AST_Assignment, AST_Primary,
                             AST_AugAssignment, AST_Range, AST_Cast))
                and lhs.precedence < self.precedence):
            lhs_s = f"({lhs!s})"
        else:
            lhs_s = f"{lhs!s}"
        rhs = self.rhs
        if (isinstance(rhs, (AST_UnaryOp, AST_BinOp, AST_TernOp,
                             AST_Compare, AST_Assignment, AST_Primary,
                             AST_AugAssignment, AST_Range, AST_Cast))
                and rhs.precedence < self.precedence):
            rhs_s = f"({rhs!s})"
        else:
            rhs_s = f"{rhs!s}"
        return f"{lhs_s} {bin_symbols[self.optype]!s} {rhs_s}"

LNOr = 0
LOr = LNOr + 1
Or = LNOr
LNXor = LOr + 1
LXor = LNXor + 1
Xor = LNXor
LNAnd = LXor + 1
LAnd = LNAnd + 1
And = LNAnd
bool_symbols = ["!||", "||", "!$$", "$$", "!&&", "&&"]
class AST_BoolOp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, left, optype, value, *, precedence, start_pos=-1):
        super().__init__(value, "AST_BoolOp", start_pos=start_pos)
        self.left = left
        self.optype = optype
        self.precedence = precedence
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_BoolOp({self.left!r}, {self.optype!r}, {self.value!r}, precedence={self.precedence!r}, start_pos={self.start_pos})"
    def __str__(self):
        values = self.value
        if (isinstance(self.left, (AST_UnaryOp, AST_BinOp, AST_TernOp))
                and self.left.precedence < self.precedence):
            values_s = f"({self.left!s})"
        else:
            values_s = f"{self.left!s}"
        for op, value in values:
            if (isinstance(value, (AST_UnaryOp, AST_BinOp, AST_TernOp))
                    and value.precedence < self.precedence):
                values_s = f"{values_s} {bool_symbols[op]} ({value})"
            else:
                values_s = f"{values_s} {bool_symbols[op]} {value}"
        return values_s

RichCmp = 0
GTE = RichCmp + 1
LTE = GTE + 1
GT = LTE + 1
LT = GT + 1
NotEq = LT + 1
Eq = NotEq + 1
IsNot = Eq + 1
Is = IsNot + 1
NotIn = Is + 1
In = NotIn + 1
cmp_symbols = ["<=>", ">=", "<=", ">", "<", "!=", "==", "#!", "#=", "~!", "~>"]
class AST_Compare(AST_Node):
    __module__ = 'builtins'
    def __init__(self, left, value, start_pos=-1):
        super().__init__(value, "AST_Compare", start_pos=start_pos)
        self.left = left
        self.ops = value
        self.precedence = 9
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Compare({self.left!r}, {self.ops!r}, start_pos={self.start_pos})"
    def __str__(self):
        left = self.left
        if (isinstance(left,
                      (AST_TernOp, AST_Compare, AST_Assignment,
                       AST_AugAssignment))
            or
            isinstance(left, (AST_UnaryOp, AST_BinOp))
                and left.precedence < self.precedence):
            self_s = f"({left!s})"
        else:
            self_s = f"{left!s}"
        for op in self.ops:
            right = op[1]
            if (isinstance(right,
                      (AST_TernOp, AST_Compare, AST_Assignment,
                       AST_AugAssignment))
                or
                isinstance(right, (AST_UnaryOp, AST_BinOp))
                    and right.precedence < self.precedence):
                right_s = f"({right!s})"
            else:
                right_s = f"{right!s}"
            self_s = f"{self_s} {cmp_symbols[op[0]]!s} {right_s}"
        return self_s

class AST_Range(AST_Node):
    __module__ = 'builtins'
    def __init__(self, *value, end_exclusive, frozen, start_pos=-1):
        super().__init__(value, "AST_Range", start_pos=start_pos)
        self.left, self.right = value
        self.end_exclusive = end_exclusive
        self.frozen = frozen
        self.symbol = f"{':' if frozen else '-' if end_exclusive else '.'}{'>' if end_exclusive else '.'}"
        self.precedence = 23
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Range({self.left!r}, {self.right!r}, end_exclusive={self.end_exclusive!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        left = self.left
        if (left
            and
            isinstance(left,
                      (AST_TernOp, AST_Compare, AST_Assignment,
                       AST_AugAssignment, AST_Range))
            or
            isinstance(left, (AST_UnaryOp, AST_BinOp))
                and left.precedence < self.precedence):
            left_s = f"({left!s})"
        else:
            left_s = f"{left!s}" if left else ''
        right = self.right
        if (right
            and
            isinstance(right,
                      (AST_TernOp, AST_Compare, AST_Assignment,
                       AST_AugAssignment, AST_Range))
            or
            isinstance(right, (AST_UnaryOp, AST_BinOp))
                and right.precedence < self.precedence):
            right_s = f"({right!s})"
        else:
            right_s = f"{right!s}" if right else ''
        return f"{left_s}{self.symbol}{right_s}"

class AST_Cast(AST_Node):
    __module__ = 'builtins'
    def __init__(self, tspec, value, start_pos=-1):
        super().__init__(value, "AST_Cast", start_pos=start_pos)
        self.tspec = tspec
        self.precedence = 24
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Cast({self.tspec!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        value = self.value
        if (isinstance(value,
                      (AST_TernOp, AST_Compare, AST_Assignment,
                       AST_AugAssignment, AST_Range))
            or
            isinstance(value, (AST_UnaryOp, AST_BinOp))
                and value.precedence < self.precedence):
            value_s = f"({value!s})"
        else:
            value_s = f"{value!s}"
        return f"<{self.tspec!s}>{value_s}"

AttrP = 0
SubscrP = AttrP + 1
CallP = SubscrP + 1
primary_symbols = [".", "[]", "()"]
primary_special_case = {SubscrP, CallP}

class AST_Primary(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, primaries, start_pos=-1):
        super().__init__(value, "AST_Primary", start_pos=start_pos)
        self.primaries = primaries
        self.precedence = 26
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Primary({self.value!r}, {self.primaries!r}, start_pos={self.start_pos})"
    def __str__(self):
        left = self.value
        if (isinstance(left,
                      (AST_TernOp, AST_Compare, AST_Assignment,
                       AST_AugAssignment, AST_Range, AST_Cast,
                       AST_Primary))
            or
            isinstance(left, (AST_UnaryOp, AST_BinOp))
                and left.precedence < self.precedence):
            self_s = f"({left!s})"
        else:
            self_s = f"{left!s}"
        for primary in self.primaries:
            right = primary[1]
            if primary[0] is CallP:
                if right:
                    right_s = ""
                    for arg in right:
                        if isinstance(arg, (AST_Assignment, AST_AugAssignment)):
                            right_s = f"{right_s} ({arg!s}),"
                        elif arg:
                            right_s = f"{right_s} {arg!s},"
                        else:
                            right_s = f"{right_s},"
                    right_s = right_s[right[0] is not None:-(right[-1] is not None)]
                else:
                    right_s = ""
            elif primary[0] is SubscrP:
                if isinstance(right, AST_Tuple):
                    right_s = f"{right!s}"
                else:
                    right_s = f"{right!s}"
            elif (isinstance(right,
                           (AST_TernOp, AST_Compare, AST_Assignment,
                            AST_AugAssignment, AST_Range, AST_Cast,
                            AST_Primary))
                    or
                    isinstance(right, (AST_UnaryOp, AST_BinOp))
                               and right.precedence < self.precedence):
                right_s = f"({right!s})"
            else:
                right_s = f"{right!s}"
            if primary[0] in primary_special_case:
                self_s = f"{self_s}{right_s.join(primary_symbols[primary[0]])}"
            else:
                self_s = f"{self_s}{primary_symbols[primary[0]]}{right_s}"
        return self_s

constant_None = None
constant_True = None
constant_False = None

class AST_Constant(AST_Node):
    __module__ = 'builtins'
    def __new__(self, value, start_pos=-1):
        global constant_None, constant_True, constant_False
        if value is None and constant_None:
            return constant_None
        elif value is None:
            constant_None = super().__new__(self)
            return constant_None
        elif value is True and constant_True:
            return constant_True
        elif value is True:
            constant_True = super().__new__(self)
            return constant_True
        elif value is False and constant_False:
            return constant_False
        elif value is False:
            constant_False = super().__new__(self)
            return constant_False
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Constant", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        if self.value is None:
            return "nil"
        elif self.value is True:
            return "true"
        else:
            return "false"

class AST_NameWithDefault(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, *, default, start_pos=-1):
        super().__init__(default, "AST_NameWithDefault", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_NameWithDefault({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{self.name}"

class AST_Modifier(AST_Node):
    __module__ = 'builtins'
    def __init__(self, start_pos=-1):
        super().__init__(self, "AST_Modifier", start_pos=start_pos)
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Modifier(start_pos={self.start_pos})"
    def __str__(self):
        return "@"

class AST_GenComp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, targets, iterables, conditions, start_pos=-1):
        super().__init__(value, "AST_GenComp", start_pos=start_pos)
        self.targets = targets
        self.iterables = iterables
        self.conditions = conditions
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_GenComp({self.value!r}, {self.targets!r}, {self.iterables!r}, {self.conditions!r}, start_pos={self.start_pos})"
    def __str__(self):
        self_s = f"{self.value!s} : {self.targets!s} ~> {', '.join(map(str, self.iterables))}"
        if self.conditions:
            self_s = f"{self_s} : {', '.join(map(str, self.conditions))}"
        return self_s

class AST_Tuple(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, *, frozen, without_parens=False, start_pos=-1):
        super().__init__(value, "AST_Tuple", start_pos=start_pos)
        self.frozen = frozen
        self.without_parens = without_parens
        self.start_pos = start_pos
    def __repr__(self):
        if self.without_parens:
            return f"AST_Tuple({self.value!r}, frozen={self.frozen!r}, without_parens=True, start_pos={self.start_pos})"
        else:
            return f"AST_Tuple({self.value!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        if len(self.value) == 1:
            value_s = f"{self.value[0]!s},"
        else:
            value_s = ', '.join(map(lambda x: f"({x!s})" if isinstance(x, (AST_Assignment, AST_AugAssignment)) else f"{x!s}", self.value))
        if self.without_parens:
            return f"{'' if self.frozen else ':'}{value_s}"
        else:
            return f"({'' if self.frozen else ':'}{value_s})"

class AST_List(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, *, frozen, start_pos=-1):
        super().__init__(value, "AST_List", start_pos=start_pos)
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_List({self.value!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"[{':' if self.frozen else ''}{', '.join(map(lambda x: f'({x!s})' if isinstance(x, (AST_Assignment, AST_AugAssignment)) else f'{x!s}', self.value))}]"

class AST_Set(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, *, frozen, start_pos=-1):
        super().__init__(value, "AST_Set", start_pos=start_pos)
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Set({self.value!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{{{':' if self.frozen else ''}{', '.join(map(lambda x: f'({x!s})' if isinstance(x, (AST_Assignment, AST_AugAssignment)) else f'{x!s}', self.value)) or ','}}}"

parenthesize = (("",""), "()")
class AST_Dict(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, *, frozen, start_pos=-1):
        super().__init__(value, "AST_Dict", start_pos=start_pos)
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Dict({self.value!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        return f"{{{':' if self.frozen else ''}{', '.join(map(lambda x: f'{str(x[0]).join(parenthesize[isinstance(x[0], (AST_Assignment, AST_AugAssignment))])}: {str(x[1]).join(parenthesize[isinstance(x[1], (AST_Assignment, AST_AugAssignment))])}', self.value))}}}"

class AST_TupleComp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, targets, iterables, conditions, *, frozen, start_pos=-1):
        super().__init__(value, "AST_TupleComp", start_pos=start_pos)
        self.targets = targets
        self.iterables = iterables
        self.conditions = conditions
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_TupleComp({self.value!r}, {self.targets!r}, {self.iterables!r}, {self.conditions!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        self_s = f"({'' if self.frozen else ':'}{self.value!s} : {self.targets!s} ~> {', '.join(map(str, self.iterables))}"
        if self.conditions:
            self_s = f"{self_s} : {', '.join(map(str, self.conditions))})"
        else:
            self_s = f"{self_s})"
        return self_s

class AST_ListComp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, targets, iterables, conditions, *, frozen, start_pos=-1):
        super().__init__(value, "AST_ListComp", start_pos=start_pos)
        self.targets = targets
        self.iterables = iterables
        self.conditions = conditions
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_ListComp({self.value!r}, {self.targets!r}, {self.iterables!r}, {self.conditions!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        self_s = f"[{':' if self.frozen else ''}{self.value!s} : {self.targets!s} ~> {', '.join(map(str, self.iterables))}"
        if self.conditions:
            self_s = f"{self_s} : {', '.join(map(str, self.conditions))}]"
        else:
            self_s = f"{self_s}]"
        return self_s

class AST_SetComp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, targets, iterables, conditions, *, frozen, start_pos=-1):
        super().__init__(value, "AST_SetComp", start_pos=start_pos)
        self.targets = targets
        self.iterables = iterables
        self.conditions = conditions
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_SetComp({self.value!r}, {self.targets!r}, {self.iterables!r}, {self.conditions!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        self_s = f"{{{':' if self.frozen else ''}{self.value!s} : {self.targets!s} ~> {', '.join(map(str, self.iterables))}"
        if self.conditions:
            self_s = f"{self_s} : {', '.join(map(str, self.conditions))}}}"
        else:
            self_s = f"{self_s}}}"
        return self_s

class AST_DictComp(AST_Node):
    __module__ = 'builtins'
    def __init__(self, key, value, targets, iterables, conditions, *, frozen, start_pos=-1):
        super().__init__(value, "AST_DictComp", start_pos=start_pos)
        self.key = key
        self.targets = targets
        self.iterables = iterables
        self.conditions = conditions
        self.frozen = frozen
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_DictComp({self.key!r}, {self.value!r}, {self.targets!r}, {self.iterables!r}, {self.conditions!r}, frozen={self.frozen!r}, start_pos={self.start_pos})"
    def __str__(self):
        self_s = f"{{{':' if self.frozen else ''}{self.key!s}: {self.value!s} : {self.targets!s} ~> {', '.join(map(str, self.iterables))}"
        if self.conditions:
            self_s = f"{self_s} : {', '.join(map(str, self.conditions))}}}"
        else:
            self_s = f"{self_s}}}"
        return self_s

strong_string = "strong "

class AST_Targets(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Targets", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"{', '.join(map(lambda x: f'{strong_string if x[0] else empty}{str(x[1])+space if x[1] else empty}{x[2]!s}', self.value))}"

class AST_TypeSpec(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_TypeSpec", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"{' | '.join(map(str, self.value))}"

class AST_Name(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, variation=None, start_pos=-1):
        super().__init__(value, "AST_Name", start_pos=start_pos)
        self.variation = variation
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Name({self.value!r}, {self.variation!r}, start_pos={self.start_pos})"
    def __str__(self):
        value = self.value[1]
        if value[0].isalpha() and value.isalnum():
            return f"{value}{self.variation if self.variation else ''}"
        else:
            return f"`{value}`{self.variation if self.variation else ''}"

class AST_ScopeNum(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_ScopeNum", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"(:{self.value if self.value is not None else ''!s}:)"

class AST_ScopeName(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_ScopeName", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"(|{self.value or ''!s}|)"

class AST_AttrAccess(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_AttrAccess", start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return '.'.join(map(str, self.value))

class AST_Param(AST_Node):
    __module__ = 'builtins'
    def __init__(self, tspec, value, expr, *, late_bound_default=None, start_pos=-1):
        super().__init__(value, "AST_Param", start_pos=start_pos)
        self.tspec = tspec
        self.expr = expr
        self.late_bound_default = late_bound_default
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Param({self.tspec!r}, {self.value!r}, {self.expr!r}, late_bound_default={self.late_bound_default!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.expr is None:
            return f"{f'{self.tspec!s} ' if self.tspec else ''}{self.value!s}"
        else:
            return f"{f'{self.tspec!s} ' if self.tspec else ''}{self.value!s} {'=>' if self.late_bound_default  else ':='} {self.expr!s}"

class AST_Arg(AST_Node):
    __module__ = 'builtins'
    def __init__(self, name, value, start_pos=-1):
        super().__init__(value, "AST_Arg", start_pos=start_pos)
        self.name = name
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Arg({self.name!r}, {self.value!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.name:
            return f"{self.name!s}={self.value!s}"
        else:
            return f"{self.value!s}"

class AST_Slice(AST_Node):
    __module__ = 'builtins'
    def __init__(self, *value, start_pos=-1):
        super().__init__(value, "AST_Slice", start_pos=start_pos)
        self.start, self.stop, self.step = value
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Slice({self.start!r}, {self.stop!r}, {self.step!r}, start_pos={self.start_pos})"
    def __str__(self):
        if self.start:
            if self.stop:
                if self.step:
                    return f"{self.start!s}:{self.stop!s}:{self.step!s}"
                else:
                    return f"{self.start!s}:{self.stop!s}"
            elif self.step:
                return f"{self.start!s}::{self.step!s}"
            else:
                return f"{self.start!s}:"
        elif self.stop:
            if self.step:
                return f":{self.stop!s}:{self.step!s}"
            else:
                return f":{self.stop!s}"
        elif self.step:
            return f"::{self.step!s}"
        else:
            return f":"

class AST_Int(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Int", start_pos=start_pos)

class AST_Dec(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Dec", start_pos=start_pos)

class AST_Strings(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, "AST_Strings", start_pos=start_pos)
    def __str__(self):
        return ''.join(map(str, self.value))

class AST_String(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, 'AST_String', start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"\"{self.value}\""

class AST_ByteString(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, 'AST_ByteString', start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return f"b\"{self.value}\""

class AST_JoinedString(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, 'AST_JoinedString', start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return 'f'+f"\"{''.join(map(str, self.value))}\""

class AST_JoinedByteString(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, start_pos=-1):
        super().__init__(value, 'AST_JoinedByteString', start_pos=start_pos)
        self.start_pos = start_pos
    def __str__(self):
        return 'bf'+f"\"{''.join(map(str, self.value))}\""

class AST_Formatted(AST_Node):
    __module__ = 'builtins'
    def __init__(self, value, spec, is_string=0, start_pos=-1):
        from estil_parser import expression_rule, Parser
        super().__init__(value, 'AST_Formatted', start_pos=start_pos)
        self.spec = spec
        self.is_string = is_string
        if not is_string:
            self.value = expression_rule(Parser(self.value))
        self.start_pos = start_pos
    def __repr__(self):
        return f"AST_Formatted({self.value!r}, {self.spec!r}{', 1' if self.is_string else ''}, start_pos={self.start_pos})"
    def __str__(self):
        if self.is_string:
            return self.value
        else:
            return f"{{{self.value!s}{self.spec and f';{self.spec}' or ''!s}}}"
