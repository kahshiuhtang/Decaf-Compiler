

import sys
from decaf_lexer import *
import decaf_ast as ast

names = {}
precedence = (('right', 'ASSIGN'),
              ('left', 'OR'),
              ('left', 'AND'),
              ('nonassoc', 'EQ', 'NOT_EQ'),
              ('nonassoc', 'LT', 'LTE', 'GT', 'GTE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'STAR', 'F_SLASH'),
              ('right', 'UMINUS', 'UPLUS', 'NOT')
              )

def p_program(p):
    'program : class_decl_list'
    ans = ast.AST(p[1])
    ans.print()
    return ans

def p_class_decl_list(p):
    '''class_decl_list : class_decl class_decl_list
                       | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = []
        p[0].append(p[1])
        if p[2] is not None:
            p[0] = p[0] + p[2]

def p_class_decl(p):
    '''class_decl : CLASS ID LEFT_CB class_body_decl_list RIGHT_CB
                  | CLASS ID EXTENDS ID LEFT_CB class_body_decl_list  RIGHT_CB'''
    if p[3] == '{':
        p[0] = ast.Class(p[2], "")
        for x in p[4][0]:
            x.containing_class = p[2]
            p[0].addField(x)
        for x in p[4][2]:
            p[0].addConstructor(x)
        for x in p[4][1]:
            x.containing_class = p[2]
            p[0].addMethod(x)
    else:
        p[0] = ast.Class(p[2], p[4])
    pass

def p_class_body_decl_list(p):
    'class_body_decl_list : class_body_decl class_body_decl_cont'
    if p[2] == None:
        p[0] = [[],[],[]]
        if p[1][0] == "f":
            p[0][0].append(p[1][1])
        elif p[1][0] == "m":
            p[0][1].append(p[1][1])
        elif p[1][0] == "c":
            p[0][2].append(p[1][1])
    else:
        p[0] = [[],[],[]]
        if p[1][0] == "f":
            p[0][0].append(p[1][1])
        elif p[1][0] == "m":
            p[0][1].append(p[1][1])
        elif p[1][0] == "c":
            p[0][2].append(p[1][1])
        if p[2] is not None:
            p[0][0] = p[0][0] + p[2][0] 
            p[0][1] = p[0][1] + p[2][1] 
            p[0][2] = p[0][2] + p[2][2]

def p_class_body_decl_cont(p):
    '''class_body_decl_cont : class_body_decl class_body_decl_cont
                            | empty'''
    if p[1] == None:
        p[0] = [[],[],[]]
    else:
        p[0] = [[],[],[]]
        if p[1][0] == "f":
            p[0][0].append(p[1][1])
        elif p[1][0] == "c":
            p[0][2].append(p[1][1])
        elif p[1][0] == "m":
            p[0][1].append(p[1][1])
        if p[2] is not None:
            p[0][0] = p[0][0] + p[2][0]
            p[0][1] = p[0][1] + p[2][1]
            p[0][2] = p[0][2] + p[2][2]

def p_class_body_decl(p):
    '''class_body_decl : field_decl
                       | method_decl
                       | constructor_decl'''
    if isinstance(p[1], list) and isinstance(p[1][0], ast.Field):
        p[0]= ["f", p[1][0]]
    elif isinstance(p[1], list) and isinstance(p[1][0], ast.Method):
        p[0]= ["m", p[1][0]]
    elif isinstance(p[1], list) and isinstance(p[1][0], ast.Constructor):
        p[0]= ["c", p[1][0]]

def p_field_decl(p):
    'field_decl : modifier var_decl'
    ans = []
    for x in p[2][1]:
        ans.append(ast.Field(x, 0, "", p[1][0], p[1][1], p[2][0]))
    p[0] = ans
    pass

def p_modifier(p):
    '''modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | empty'''
    if len(p) == 2:
        p[0] = ["private", "instance"]
    elif len(p) == 3:
        if p[1] == "static":
            p[0] = ["private", "static"]
        else:
            p[0] = [p[1], "instance"]
    else:
        p[0] = [p[1], "static"]

def p_var_decl(p):
    'var_decl : type variables SEMI_COLON'
    p[0] = [p[1], p[2]]
    pass

def p_type(p):
    '''type : TYPE_INT
            | TYPE_FLOAT
            | TYPE_BOOLEAN
            | ID'''
    if p[1] == "int" or p[1] == "float" or p[1] == "boolean":    
        p[0] = p[1]
    else:
        p[0] = "user(" + p[1] + ")"
    pass

def p_variables(p):
    'variables : variable variables_cont'
    if len(p) == 2 or p[2] == None:
        p[0] == [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_variables_cont(p):
    '''variables_cont : COMMA variable variables_cont
                      | empty'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2] + p[3]

def p_variable(p):
    'variable : ID'
    p[0] = p[1]

def p_method_decl(p):
    '''method_decl : modifier type ID LEFT_PN formals RIGHT_PN block
                   | modifier TYPE_VOID ID LEFT_PN formals RIGHT_PN block'''
    if p[2] == 'void':
        params = []
        for x in p[5]:
            params.append(ast.Variable(x[1], len(params), "formal", x[0]))
        p[0] = [ast.Method(p[3], 0, "", p[1][0], p[1][1], p[5], "void")]
        p[0][0].parameters = [(x+1) for x in range(len(params))]
        p[0][0].variable_table = params
    else:
        params = []
        for x in p[5]:
            params.append(ast.Variable(x[1], len(params), "formal", x[0]))
        p[0] = [ast.Method(p[3], 0, "", p[1][0], p[1][1], p[5], p[2])]
        p[0][0].parameters = [(x+1) for x in range(len(params))]
        p[0][0].variable_table = params

def p_constructor_decl(p):
    'constructor_decl : modifier ID LEFT_PN formals RIGHT_PN block'
    p[0] = [ast.Constructor(0, p[1][0])]
    params = []
    for x in p[4]:
        params.append(ast.Variable(x[1], len(params), "formal", x[0]))
    p[0] = [ast.Constructor(0, p[1][0])]
    p[0][0].parameters = [(x+1) for x in range(len(params))]
    p[0][0].variable_table = params
    

def p_formals(p):
    '''formals : formal_param formals_cont
               | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_formals_cont(p):
    '''formals_cont : COMMA formal_param formals_cont
                    | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[2]] + p[3] 
            
    pass

def p_formal_param(p):
    'formal_param : type variable'
    p[0] = [p[1], p[2]]
    pass

def p_block(p):
    'block : LEFT_CB stmt_list RIGHT_CB'
    p[0] = p[2]
    pass

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | empty'''
    if p[1] == None:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]


def p_stmt(p):
    '''stmt : IF LEFT_PN expr RIGHT_PN stmt 
            | IF LEFT_PN expr RIGHT_PN stmt ELSE stmt
            | WHILE LEFT_PN expr RIGHT_PN stmt
            | FOR LEFT_PN for_cond1 SEMI_COLON for_cond2 SEMI_COLON for_cond3 RIGHT_PN stmt
            | RETURN return_val SEMI_COLON
            | stmt_expr SEMI_COLON
            | BREAK SEMI_COLON
            | CONTINUE SEMI_COLON
            | block
            | var_decl
            | SEMI_COLON'''
    if p[1] == 'break':
        p[0] = ast.Break(p.lineno)
    elif p[1] == 'continue':
        p[0] = ast.Continue(p.lineno)
    elif p[1] == ';':
        p[0] = ast.Skip(p.lineno)
    elif p[1] = 'while':
        pass
    elif p[1] = 'for':
        pass

def p_for_cond1(p):
    '''for_cond1 : stmt_expr
                 | empty'''
    if p[1] = None:
        p[0] = []
    else:
        p[0] = [p[1]]

def p_for_cond2(p):
    '''for_cond2 : expr
                 | empty'''
    if p[1] = None:
        p[0] = []
    else:
        p[0] = [p[1]]

def p_for_cond3(p):
    '''for_cond3 : stmt_expr
                 | empty'''
    if p[1] = None:
        p[0] = []
    else:
        p[0] = [p[1]]

def p_return_val(p):
    '''return_val : expr
                  | empty'''
    pass

def p_literal(p):
    '''literal : INT_CONST
               | FLOAT_CONST
               | STRING_CONST
               | NULL
               | TRUE
               | FALSE'''
    pass

def p_primary(p):
    '''primary : literal
               | THIS
               | SUPER
               | LEFT_PN expr RIGHT_PN
               | NEW ID LEFT_PN arguments RIGHT_PN
               | lhs
               | method_invocation'''
    pass

def p_arguments(p):
    '''arguments : expr arguments_cont
                 | empty'''
    pass

def p_arguments_cont(p):
    '''arguments_cont : COMMA expr arguments_cont
                      | empty'''
    pass

def p_lhs(p):
    'lhs : field_access'
    pass

def p_field_access(p):
    '''field_access : primary DOT ID
                    | ID'''
    pass

def p_method_invocation(p):
    'method_invocation : field_access LEFT_PN arguments RIGHT_PN'
    pass

def p_expr(p):
    '''expr : primary
            | assign'''
    pass
    
#def p_expr(p):
#   '''expr : primary
#            | assign
#            | expr arith_op expr
#            | expr bool_op expr
#            | unary_op expr'''
#    pass

def p_assign(p):
    '''assign : lhs ASSIGN expr
              | lhs INCREMENT
              | INCREMENT lhs
              | lhs DECREMENT
              | DECREMENT lhs'''
    pass

#def p_assign(p):
#    '''assign : lhs ASSIGN expr
#              | lhs PLUS PLUS
#              | PLUS PLUS lhs
#              | lhs MINUS MINUS
#              | MINUS MINUS lhs'''
#    pass

def p_add_expr(p):
    'expr : expr PLUS expr'
    pass

def p_sub_expr(p):
    'expr : expr MINUS expr'
    pass

def p_mult_exp(p):
    'expr : expr STAR expr'
    pass

def p_div_expr(p):
    'expr : expr F_SLASH expr'
    pass

def p_conj_expr(p):
    'expr : expr AND expr'
    pass

def p_disj_expr(p):
    'expr : expr OR expr'
    pass

def p_equals_expr(p):
    'expr : expr EQ expr'
    pass

def p_notequals_expr(p):
    'expr : expr NOT_EQ expr'
    pass

def p_lt_expr(p):
    'expr : expr LT expr'
    pass

def p_lte_expr(p):
    'expr : expr LTE expr'
    pass

def p_gt_expr(p):
    'expr : expr GT expr'
    pass

def p_gte_expr(p):
    'expr : expr GTE expr'
    pass

def p_pos_expr(p):
    'expr : PLUS expr %prec UPLUS'
    pass

def p_minus_expr(p):
    'expr : MINUS expr %prec UMINUS'
    pass

def p_not_expr(p):
    'expr : NOT expr'
    pass

#def p_arith_op(p):
#    '''arith_op : PLUS
#                | MINUS
#                | STAR
#                | F_SLASH'''
#    pass

#def p_bool_op(p):
#    '''bool_op : AND
#               | OR
#               | EQ
#               | NOT_EQ
#               | LT
#               | GT
#               | LTE
#               | GTE'''
#    pass

#def p_unary_op(p):
#    '''unary_op : PLUS
#                | MINUS
#                | NOT'''
#    pass

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print()
    if p:
        print("Syntax error at token,", p.type, ", line", p.lineno)
    else:
        print("Syntax error at EOF")
    print()
    sys.exit()
