class AST():
    def __init__(self, classes):
        self.classes = classes
        self.methods = []
        self.variables = []
        self.constructors = []
        self.setup()
    
    def print(self):
        for x in self.classes:
            x.print()
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

class Node():
    def __init__(self):
        self.parent = None

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
    def addField(self, field):
        self.fields.update({len(self.fields) : field})

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
    def __init__(self, _id, vis):
        self.id = _id
        self.visibility = vis
        self.parameters = []
        self.variable_table = {}
        self.body = []
    
    def __str__(self):
        print("CONSTRUCTOR: " + str(self.id) + ", " + self.visibility)
        print("Constructor Parameters: ", end ="")
        for x in self.parameters:
            print(x, end = " ")
        print()
        print("Variable Table:")
        print("Method Body:")
        return ""

class Method(Node):
    def __init__(self, name, _id, cont, vis, appl, params, ret):
        self.name = name
        self.id = _id
        self.containing_class = cont
        self.visibilty = vis
        self.applicability = appl
        self.parameters = params
        self.return_type = ret
        self.variable_table = []
        self.body = []
    
    def __str__(self):
        print("METHOD: " + str(self.id) + ", " + self.name + ", " + self.containing_class + ", " + self.visibilty + ", " + self.applicability + ", " + self.return_type)
        print("Method Parameters: ", end ="")
        for x in self.parameters:
            print(x, end = " ")
        print()
        print("Variable Table: ")
        print("Method Body: ")
        return ""

class Field(Node):
    def __init__(self, name, _id, cont, vis, appl, typ):
        self.name = name
        self.id = _id
        self.containing_class = cont
        self.visibility = vis
        self.applicability = appl
        self.type = typ
    
    def __str__(self):
        return "Field " + str(self.id) + ", " + self.name + ", " + self.containing_class + ", " + self.visibility + ", " + self.applicability + ", " + self.type

class Variable(Node):
    def __init__(self, name, _id, kind, typ):
        self.name = name
        self.id = _id
        self.kind = kind
        self.type = typ

class Type(Node):
    def __init__(self, typ):
        self.type = typ

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

class While(Statement):
    def __init__(self, line, cond, body):
        super().__init__(line)
        self.condition = cond
        self.body = body

class For(Statement):
    def __init__(self, line, init, cond, up, bod):
        super().__init__(line)
        self.initialize = init
        self.loop_condition = cond
        self.update_expression = up
        self.body = bod
    def __str__(self):
        return "FOR()"

class Return(Statement):
    def __init__(self, line):
        super().__init__(line)
        self.value = None
    def __str__(self):
        return "RETURN()"
        

class Block(Statement):
    def __init__(self, line):
        super().__init__(line)
        self.expressions = []
    def __str__(self):
        return "BLOCK()"
    
class Break(Statement):
    def __init__(self, line):
        super().__init__(line)
    def __str__(self):
        return "BREAK"

class Continue(Statement):
    def __init__(self, line):
        super().__init__(line)
    def __str__(self):
        return "CONTINUE"

class Skip(Statement):
    def __init__(self, line):
        super().__init__(line)
    def __str__(self):
        return "SKIP"

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
        return "ConstExpression()"

class VarExpression(Expression):
    def __init__(self, lin, id, val):
        super().__init__(lin)
        self.id  = id
    def __str__(self):
        return "VarExpression()"

class UnaryExpression(Expression):
    def __init__(self, lin, operand, operator):
        super().__init__(lin)
        self.operand = operand
        self.operator = operator
    
    def __str__(self):
        return "UnaryExpression()"

class BinaryExpression(Expression):
    def __init__(self, lin, left, oper, right):
        super().__init__(lin)
        self.left_operand = left
        self.operator = oper
        self.right_operand = right
    def __str__(self):
        return "BinExpression()"

class AssignExpression(Expression):
    def __init__(self, lin, left, right):
        super().__init__(lin)
        self.left_expression = left
        self.right_expression = right
    def __str__(self):
        return "AssignExpression()"

class AutoExpression(Expression):
    def __init__(self, lin , op, exp, pop):
        super().__init__(lin)
        self.operand = op
        self.expresiion = exp
        self.postOrPre = pop
    def __str__(self):
        return "AutoExpression()"

class FieldAccessExpression(Expression):
    def __init__(self, lin, base, field):
        super().__init__(lin)
        self.base = base
        self.fieldName = field
    def __str__(self):
        return "FieldAccessExpression()"

class MethodCallExpression(Expression):
    def __init__(self, lin, base, name, args):
        super().__init__(lin)
        self.base = base
        self.methodName = name
        self.arguments = args
    def __str__(self):
        return "MethodCallExpression()"
class NewObjectExpression(Expression):
    def __init__(self, lin, base):
        super().__init__(lin)
        self.paramaters = []
        self.baseClass = base
    def __str__(self):
        return "NewObjectExpression()"


class ThisExpression(Expression):
    def __init__(self, lin):
        super().__init__(lin)
        self.value = "this"
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




