import sys
import copy 
class AST():
    def __init__(self, classes):
        self.classes = classes
        self.methods = []
        self.variables = []
        self.constructors = []
        self.setup()
    
    def print(self):
        if self.errors():
            return
        for x in self.classes:
            x.print()
            print("----------------------")
    def setup(self):
        for x in self.classes:
            for field in x.fields.values():
                field.id = len(self.variables) + 1
                self.variables.append(field)
            for method in x.methods.values():
                method.id = len(self.methods) + 1
                self.methods.append(method)
            for constructor in x.constructors.values():
                constructor.id = len(self.constructors) + 1
                self.constructors.append(constructor)
        self.setup_selfdefined()
    def errors(self):
        names = set()
        for x in self.classes:
            if x.name in names:
                print("Error: Duplicate Classes")
                return True
            names.add(x.name)
        return False
    
    def setup_selfdefined(self):
        inclass = Class("In", "")
        outclass = Class("Out", "")
        scan_int = Method("scan_int", len(self.methods) + 1, "In", "public", "static", [], "int", Block(-1, []))
        self.methods.append(scan_int)
        inclass.addMethod(scan_int);
        scan_float = Method("scan_float", len(self.methods) + 1, "In", "public", "static", [], "float", Block(-1, []));
        self.methods.append(scan_float)
        inclass.addMethod(scan_float)
        printi = Method("print", len(self.methods) + 1, "Out", "public", "static", [1], "void", Block(-1, [])); # int i
        printi.variable_table = [Variable("i", 1, "formal", "int")]
        outclass.addMethod(printi)
        self.methods.append(printi)
        printf = Method("print", len(self.methods) + 1, "Out", "public", "static", [1], "void", Block(-1, [])); # float f
        printf.variable_table = [Variable("f", 1, "formal", "float")]
        outclass.addMethod(printf)
        self.methods.append(printf)
        printb = Method("print", len(self.methods) + 1, "Out", "public", "static", [1], "void", Block(-1, [])); # boolean b
        printb.variable_table = [Variable("b", 1, "formal", "boolean")]
        outclass.addMethod(printb)
        self.methods.append(printb)
        prints = Method("print", len(self.methods) + 1, "Out", "public", "static", [1], "void", Block(-1, [])); # string s
        prints.variable_table = [Variable("s", 1, "formal", "string")]
        outclass.addMethod(prints)
        self.methods.append(prints)
        self.classes.append(inclass)
        self.classes.append(outclass)

class Node():
    def __init__(self):
        self.parent = None
        self.child = []

class Class(Node):
    def __init__(self, name, super_class):
        self.name = name
        self.super_class_name = super_class
        self.constructors = {}
        self.methods = {}
        self.fields = {}

    def addConstructor(self, cons):
        self.constructors.update({len(self.constructors) : cons})
    def addMethod(self, meth):
        self.methods.update({len(self.methods) : meth})
        if meth.containing_class != "Out" and meth.containing_class != "In" and self.error_check():
            sys.exit()
    def addField(self, field):
        self.fields.update({len(self.fields) : field})
        if self.error_check():
            sys.exit()
    
    def error_check(self):
        methods = set()
        for x in self.constructors.values():
            x.check_params()
        for x in self.methods.values():
            x.check_params()
            if x.name in methods:
                print("Error: Duplicate Method Names: " + x.name)
                sys.exit()
            methods.add(x.name)
        fields = set()
        for x in self.fields.values():
            if x.name in fields:
                print("Error: Duplicate Field Names: " + x.name)
                sys.exit()
            fields.add(x.name)


    def print(self):
        print("Class Name: " + self.name)
        print("Superclass Name: " + self.super_class_name)
        print("Fields:")
        for x in self.fields.values():
            print(x)
        print("Constructors:")
        for x in self.constructors.values():
            x.__str__()
        print("Methods:")
        for x in self.methods.values():
            x.__str__()


class Constructor(Node):
    def __init__(self, _id, vis, bod, params):
        self.id = _id
        self.visibility = vis
        self.parameters = params
        self.variable_table = params
        self.body = bod
        self.setup()
    
    def __str__(self):
        print("CONSTRUCTOR: " + str(self.id) + ", " + self.visibility)
        print("Constructor Parameters: ", end ="")
        for x in self.parameters:
            print(x, end = " ")
        print()
        print("Variable Table:")
        for x in self.variable_table:
            print(x.__str__())
        print("Method Body:")
        print(self.body.__str__())
        return ""
    
    def setup(self):
        names = {}
        for i in range(len(self.body.expressions)):
            if isinstance(self.body.expressions[i], list):
                for x in self.body.expressions[i][1]:
                    self.variable_table.append(Variable(x, len(self.variable_table) + 1, "local", self.body.expressions[i][0]))
        currTab = copy.deepcopy(self.variable_table)
        for i in range(len(self.body.expressions)):
            if isinstance(self.body.expressions[i], Block):
                self.addVarTable(block, currTab)
            elif isinstance(self.body.expressions[i], While):
                self.searchExpression(self.body.expressions[i].condition, currTab)
                self.addVarTable(self.body.expressions[i].body, currTab)
            elif isinstance(self.body.expressions[i], For):
                self.searchExpression(self.body.expressions[i].initialize, currTab)
                self.searchExpression(self.body.expressions[i].loop_condition, currTab)
                self.searchExpression(self.body.expressions[i].update_expression, currTab)
                self.addVarTable(self.body.expressions[i].body, currTab)
            elif isinstance(self.body.expressions[i], If):
                self.searchExpression(self.body.expressions[i].condition, currTab)
                if self.body.expressions[i].else_part == None:
                    self.addVarTable(self.body.expressions[i].then_part, currTab)
                else:
                    self.addVarTable(self.body.expressions[i].then_part, currTab)
                    self.addVarTable(self.body.expressions[i].else_part, currTab)
            elif isinstance(self.body.expressions[i], Expression):
                self.searchExpression(self.body.expressions[i], currTab)
    def addVarTable(self, block, curr_table):
        if not isinstance(block, Block) or not isinstance(block.expressions, list):
            if isinstance(block, Expression):
                self.searchExpression(block, curr_table)
            return
        new_curr_table = copy.deepcopy(curr_table)
        for i in range(len(block.expressions)):
            if isinstance(block.expressions[i], list):
                for x in block.expressions[i][1]:
                    var = Variable(x, len(self.variable_table) + 1, "local", block.expressions[i][0])
                    self.variable_table.append(var)
                    new_curr_table.append(var);
            elif isinstance(block.expressions[i], Block):
                self.addVarTable(block.expressions[i], new_curr_table)
                # self.fill(block.expressions[i], new_curr_table)
            elif isinstance(block.expressions[i], While):
                self.searchExpression(block.expressions[i].condition, new_curr_table)
                self.addVarTable(block.expressions[i].body, new_curr_table)
                # self.fill(block.expressions[i].body, new_curr_table)
            elif isinstance(block.expressions[i], For):
                self.searchExpression(block.expressions[i].initialize, new_curr_table)
                self.searchExpression(block.expressions[i].loop_condition, new_curr_table)
                self.searchExpression(block.expressions[i].update_expression, new_curr_table)
                self.addVarTable(block.expressions[i].body, new_curr_table)
                # self.fill(block.expressions[i].body, new_curr_table)
            elif isinstance(block.expressions[i], If):
                self.searchExpression(block.expressions[i].condition, new_curr_table)
                if block.expressions[i].else_part == None:
                    self.addVarTable(block.expressions[i].then_part, new_curr_table)
                    # self.fill(block.expressions[i].then_part, new_curr_table)
                else:
                    self.addVarTable(block.expressions[i].then_part, new_curr_table)
                    # self.fill(block.expressions[i].then_part, new_curr_table)
                    self.addVarTable(block.expressions[i].else_part, new_curr_table)
                    # self.fill(block.expressions[i].else_part, new_curr_table)
            elif isinstance(block.expressions[i], Expression):
                self.searchExpression(block.expressions[i], new_curr_table)
            elif isinstance(block.expressions[i], Return):
                self.searchExpression(block.expressions[i].value, new_curr_table)
    def searchExpression(self, expr, curr_table):
        if isinstance(expr, list):
            for x in expr:
                self.searchExpression(x, curr_table)
            return
        if isinstance(expr, VarExpression):
            for elem in reversed(curr_table):
                if elem.name == expr.val:
                    expr.id = elem.id
                    return
            print("Error: Unfound reference in constructor with variable: " + expr.val)
            sys.exit()
        elif isinstance(expr, UnaryExpression):
            self.searchExpression(expr.operand, curr_table)
            self.searchExpression(expr.operator, curr_table)
        elif isinstance(expr, BinaryExpression):
            self.searchExpression(expr.left_operand, curr_table)
            self.searchExpression(expr.right_operand, curr_table)
        elif isinstance(expr, AssignExpression):
            self.searchExpression(expr.left_expression, curr_table)
            self.searchExpression(expr.right_expression, curr_table)
        elif isinstance(expr, AutoExpression):
            self.searchExpression(expr.expression, curr_table)
        elif isinstance (expr, FieldAccessExpression):
            self.searchExpression(expr.base, curr_table)
        elif isinstance(expr, MethodCallExpression):
            self.searchExpression(expr.base, curr_table)
            for x in expr.arguments:
                self.searchExpression(x, curr_table)
        elif isinstance(expr, NewObjectExpression):
            for x in expr.parameters:
                self.searchExpression(x, curr_table)
        return
    def check_params(self):
        params = set()
        for x in self.parameters:
            params.add(self.variable_table[x - 1].name)
        for var in self.variable_table:
            if var.name in params and var.kind != "formal":
                print("Error: parameters have same name as local variables [" + var.name + "]")
                sys.exit()
class Method(Node):
    def __init__(self, name, _id, cont, vis, appl, params, ret, bod):
        self.name = name
        self.id = _id
        self.containing_class = cont
        self.visibilty = vis
        self.applicability = appl
        self.parameters = params
        self.return_type = ret
        self.variable_table = []
        self.body = bod
    
    def __str__(self):
        print("METHOD: " + str(self.id) + ", " + self.name + ", " + self.containing_class + ", " + self.visibilty + ", " + self.applicability + ", " + self.return_type)
        print("Method parameters: ", end ="")
        for x in self.parameters:
            print(x, end = " ")
        print()
        print("Variable Table: ")
        for x in self.variable_table:
            print(x.__str__())
        print("Method Body: ")
        print(self.body.__str__())
        return ""
    
    def setup(self):
        names = {}
        for i in range(len(self.body.expressions)):
            if isinstance(self.body.expressions[i], list):
                for x in self.body.expressions[i][1]:
                    self.variable_table.append(Variable(x, len(self.variable_table) + 1, "local", self.body.expressions[i][0]))
        currTab = copy.deepcopy(self.variable_table)
        for i in range(len(self.body.expressions)):
            if isinstance(self.body.expressions[i], Block):
                self.addVarTable(block, currTab)
            elif isinstance(self.body.expressions[i], While):
                self.searchExpression(self.body.expressions[i].condition, currTab)
                self.addVarTable(self.body.expressions[i].body, currTab)
            elif isinstance(self.body.expressions[i], For):
                self.searchExpression(self.body.expressions[i].initialize, currTab)
                self.searchExpression(self.body.expressions[i].loop_condition, currTab)
                self.searchExpression(self.body.expressions[i].update_expression, currTab)
                self.addVarTable(self.body.expressions[i].body, currTab)
            elif isinstance(self.body.expressions[i], If):
                self.searchExpression(self.body.expressions[i].condition, currTab)
                if self.body.expressions[i].else_part == None:
                    self.addVarTable(self.body.expressions[i].then_part, currTab)
                else:
                    self.addVarTable(self.body.expressions[i].then_part, currTab)
                    self.addVarTable(self.body.expressions[i].else_part, currTab)
            elif isinstance(self.body.expressions[i], Expression):
                self.searchExpression(self.body.expressions[i], currTab)
            elif isinstance(self.body.expressions[i], Return):
                self.searchExpression(self.body.expressions[i].value, currTab)
    def addVarTable(self, block, curr_table):
        if not isinstance(block, Block) or not isinstance(block.expressions, list):
            if isinstance(block, Expression):
                self.searchExpression(block, curr_table)
            return
        new_curr_table = copy.deepcopy(curr_table)
        for i in range(len(block.expressions)):
            if isinstance(block.expressions[i], list):
                for x in block.expressions[i][1]:
                    var = Variable(x, len(self.variable_table) + 1, "local", block.expressions[i][0])
                    self.variable_table.append(var)
                    new_curr_table.append(var);
            elif isinstance(block.expressions[i], Block):
                self.addVarTable(block.expressions[i], new_curr_table)
                # self.fill(block.expressions[i], new_curr_table)
            elif isinstance(block.expressions[i], While):
                self.searchExpression(block.expressions[i].condition, new_curr_table)
                self.addVarTable(block.expressions[i].body, new_curr_table)
                # self.fill(block.expressions[i].body, new_curr_table)
            elif isinstance(block.expressions[i], For):
                self.searchExpression(block.expressions[i].initialize, new_curr_table)
                self.searchExpression(block.expressions[i].loop_condition, new_curr_table)
                self.searchExpression(block.expressions[i].update_expression, new_curr_table)
                self.addVarTable(block.expressions[i].body, new_curr_table)
                # self.fill(block.expressions[i].body, new_curr_table)
            elif isinstance(block.expressions[i], If):
                self.searchExpression(block.expressions[i].condition, new_curr_table)
                if block.expressions[i].else_part == None:
                    self.addVarTable(block.expressions[i].then_part, new_curr_table)
                    # self.fill(block.expressions[i].then_part, new_curr_table)
                else:
                    self.addVarTable(block.expressions[i].then_part, new_curr_table)
                    # self.fill(block.expressions[i].then_part, new_curr_table)
                    self.addVarTable(block.expressions[i].else_part, new_curr_table)
                    # self.fill(block.expressions[i].else_part, new_curr_table)
            elif isinstance(block.expressions[i], Expression):
                self.searchExpression(block.expressions[i], new_curr_table)
            elif isinstance(block.expressions[i], Return):
                self.searchExpression(block.expressions[i].value, new_curr_table)
    def searchExpression(self, expr, curr_table):
        if isinstance(expr, list):
            for x in expr:
                self.searchExpression(x, curr_table)
            return
        if isinstance(expr, VarExpression):
            for elem in reversed(curr_table):
                if elem.name == expr.val:
                    expr.id = elem.id
                    return
            print("Error: Unfound Reference in " + self.name +  " method: variable " + expr.val)
            sys.exit()
        elif isinstance(expr, UnaryExpression):
            self.searchExpression(expr.operand, curr_table)
            self.searchExpression(expr.operator, curr_table)
        elif isinstance(expr, BinaryExpression):
            self.searchExpression(expr.left_operand, curr_table)
            self.searchExpression(expr.right_operand, curr_table)
        elif isinstance(expr, AssignExpression):
            self.searchExpression(expr.left_expression, curr_table)
            self.searchExpression(expr.right_expression, curr_table)
        elif isinstance(expr, AutoExpression):
            self.searchExpression(expr.expression, curr_table)
        elif isinstance (expr, FieldAccessExpression):
            self.searchExpression(expr.base, curr_table)
        elif isinstance(expr, MethodCallExpression):
            self.searchExpression(expr.base, curr_table)
            for x in expr.arguments:
                self.searchExpression(x, curr_table)
        elif isinstance(expr, NewObjectExpression):
            for x in expr.parameters:
                self.searchExpression(x, curr_table)
        return
    def check_params(self):
        params = set()
        for x in self.parameters:
            params.add(self.variable_table[x - 1].name)
        for var in self.variable_table:
            if var.name in params and var.kind != "formal":
                print("Error: parameters have same name as local variables: [" + var.name +"]")
                sys.exit()

class Field(Node):
    def __init__(self, name, _id, cont, vis, appl, typ):
        self.name = name
        self.id = _id
        self.containing_class = cont
        self.visibility = vis
        self.applicability = appl
        self.type = typ
    
    def __str__(self):
        return "FIELD " + str(self.id) + ", " + self.name + ", " + self.containing_class + ", " + self.visibility + ", " + self.applicability + ", " + self.type

class Variable(Node):
    def __init__(self, name, _id, kind, typ):
        self.name = name
        self.id = _id
        self.kind = kind
        self.type = typ
    
    def __str__(self):
        return "VARIABLE " + str(self.id) +", " + self.name +", " + self.kind + ", " + self.type

class Type(Node):
    def __init__(self, typ):
        self.type = typ

    def __str__(self):
        return self.typ

class Statement(Node):
    def __init__(self, line):
        self.lineNumber = line

    def toString():
        print("STATEMENT")

class If(Statement):
    def __init__(self, line, condition, then_part, else_part):
        super().__init__(line)
        self.condition = condition
        self.then_part = then_part
        self.else_part = else_part

    def __str__(self):
        if self.else_part == None:
            return  "If(" + self.condition.__str__() + ", " + self.then_part.__str__() +  ")"
        return "If(" + self.condition.__str__() + ", " + self.then_part.__str__() + ", " + self.else_part.__str__() +  ")"

class While(Statement):
    def __init__(self, line, cond, body):
        super().__init__(line)
        self.condition = cond
        self.body = body
    
    def __str__(self):
        return "While(" + self.condition.__str__() + "," + self.body.__str__() + ")"

class For(Statement):
    def __init__(self, line, init, cond, up, bod):
        super().__init__(line)
        self.initialize = init
        self.loop_condition = cond
        self.update_expression = up
        self.body = bod
    def __str__(self):
        ans = ""
        i = self.initialize.__str__()
        l = self.loop_condition.__str__()
        u = self.update_expression.__str__()
        if isinstance(self.initialize, list):
            i = ""
            for x in self.initialize:
                i += x.__str__() + ","
            i = i[:-1]
        if isinstance(self.loop_condition, list):
            l = ""
            for x in self.loop_condition:
                l += x.__str__() + ","
            l = l[:-1]
        if isinstance(self.update_expression, list):
            u = ""
            for x in self.update_expression:
                u += x.__str__() + ","
            u = u[:-1]
        if isinstance(self.body, list):
            for x in self.body:
                ans += x.__str__() + ","
            ans = ans[:-1]
        else:
            ans = self.body.__str__()
        return "FOR(" + i + ", " + l + ", " + u + ", " + ans + ")"

class Return(Statement):
    def __init__(self, line, val):
        super().__init__(line)
        self.value = val
    def __str__(self):
        if self.value == None:
            return "Return()"
        return "Return(" + self.value.__str__() + ")"
        

class Block(Statement):
    def __init__(self, line, expressions):
        super().__init__(line)
        self.expressions = expressions
    def __str__(self):
        if not isinstance(self.expressions, list):
            return "Block([\n" + self.expressions.__str__() +"\n])"
        if len(self.expressions) == 0:
            return "Block([])"
        ans = ""
        for x in self.expressions:
            if not isinstance(x, list):
                ans += x.__str__() + ",\n"
        ans = ans[:-2]
        return "Block([\n" + ans + "])"
    
class Break(Statement):
    def __init__(self, line):
        super().__init__(line)
    def __str__(self):
        return "Break"

class Continue(Statement):
    def __init__(self, line):
        super().__init__(line)
    def __str__(self):
        return "Continue"

class Skip(Statement):
    def __init__(self, line):
        super().__init__(line)
    def __str__(self):
        return "Skip"

class Expression(Node):
    def __init__(self, lin):
        self.lineNumber = lin
    def __str__(self):
        pass

    
class ConstantExpression(Expression):
    def __init__(self, lin, typ, val):
        super().__init__(lin)
        self.type = typ
        self.value = val

    def __str__(self):
        if self.type == "null" or self.type == "false" or self.type == "true":
            return "ConstExpression(" + self.type.__str__() + ")"
        return "ConstExpression(" + self.type.__str__() + ", " + self.value.__str__() + ")"

class VarExpression(Expression):
    def __init__(self, lin, id, val):
        super().__init__(lin)
        self.id  = 0
        self.val = val
    def __str__(self):
        return "Variable(" + self.id.__str__() + ", " + self.val.__str__() + ")"

class UnaryExpression(Expression):
    def __init__(self, lin, operand, operator):
        super().__init__(lin)
        self.operand = operand
        self.operator = operator
    
    def __str__(self):
        return "UnaryExpression(" + self.operand.__str__() + ", " + self.operator.__str__() + ")"

class BinaryExpression(Expression):
    def __init__(self, lin, left, oper, right):
        super().__init__(lin)
        self.left_operand = left
        self.operator = self.fix(oper)
        self.right_operand = right

    def __str__(self):
        return "Binary(" + self.left_operand.__str__() + ", " + str(self.operator) + ", " + self.right_operand.__str__() + ")"

    def fix(self, oper):
        if oper == "+":
            return "add"
        elif oper == "-":
            return "min"
        elif oper == "/":
            return "div"
        elif oper == "*":
            return "mul"
        elif oper == "||":
            return "or"
        elif oper == "&&":
            return "and"
        elif oper == "==":
            return "eq"
        elif oper == "!=":
            return "neq"
        elif oper == "<":
            return "lt"
        elif oper == ">":
            return ">"
        elif oper == "<=":
            return "leq"
        elif oper == ">=":
            return "geq"
class AssignExpression(Expression):
    def __init__(self, lin, left, right):
        super().__init__(lin)
        self.left_expression = left
        self.right_expression = right
    def __str__(self):
        return "AssignExpression(" + self.left_expression.__str__() + ", " + self.right_expression.__str__() + ")"

class AutoExpression(Expression):
    def __init__(self, lin , op, exp, pop):
        super().__init__(lin)
        self.operand = op
        self.expression = exp
        self.postOrPre = pop
        if self.operand == "+":
            self.operand = "inc"
        else:
            self.operand = "dec"
    def __str__(self):
        return "AutoExpression(" + self.operand.__str__() + ", " + self.expression.__str__() + ", " + self.postOrPre.__str__() + ")"

class FieldAccessExpression(Expression):
    def __init__(self, lin, base, field):
        super().__init__(lin)
        self.base = base
        self.fieldName = field
    def __str__(self):
        if isinstance(self.fieldName, list):
            name = ""
            for x in self.fieldName:
                name += x + ", "
            name = name[:-1]
            return "FieldAccessExpression(" + self.base.__str__() + ", " +  name + ")"
        return "FieldAccessExpression(" + self.base.__str__() + ", " + self.fieldName.__str__() + ")"

class MethodCallExpression(Expression):
    def __init__(self, lin, base, name, args):
        super().__init__(lin)
        self.base = base
        self.methodName = name
        self.arguments = args
    def __str__(self):
        arguments = self.arguments
        if isinstance(self.arguments, list):
            arguments = ""
            for x in self.arguments:
                arguments += x.__str__() + ", "
            arguments = arguments[:-2]
            arguments = "(" + arguments + ")"

        return "MethodCallExpression(" + self.base.__str__() + ", " + self.methodName.__str__() + ", "+ arguments +")"
class NewObjectExpression(Expression):
    def __init__(self, lin, base, args):
        super().__init__(lin)
        self.parameters = args
        self.baseClass = base
    def __str__(self):
        params = ""
        if len(self.parameters) > 0:
            for x in self.parameters:
                params += x.__str__() + ", "
            params = params[:-2]
            params = "[" + params + "]"
        else:
            params ="[]"
        return "NewObjectExpression(" + self.baseClass +", " + params+ ")"


class ThisExpression(Expression):
    def __init__(self, lin):
        super().__init__(lin)

    def __str__(self):
        return "This"

class SuperExpression(Expression):
    def __init__(self, lin):
        super().__init__(lin)
        self.value = "super"
    def __str__(self):
        return "Super"

class ClassReferenceExpression(Expression):
    def __init__(self, lin, ref):
        super().__init__(lin)
        self.classReference = ref
    def __str__(self):
        return "ClassReference(" + self.classReference + ")"