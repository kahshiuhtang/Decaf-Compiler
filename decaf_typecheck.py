import decaf_ast as ast
import sys
class TypeChecker():
    def __init__(self):
        pass
    def check(self, tree):
        self.tree = tree
        for c in tree.classes:
            for m in c.methods.values():
                self.check_method(c,m)
    def check_method(self, cls, mth):
        for stmt in mth.body.expressions:
            self.find(stmt, cls, mth)

    def find(self, stmt, cls, mth):
        if not isinstance(stmt, list): 
            if isinstance(stmt, ast.Statement):
                if isinstance(stmt, ast.If):
                    if stmt.condition.type == None:
                        self.find(stmt.condition, cls, mth)
                    if stmt.condition.type != "boolean":
                        print("Error: if condition is not a boolean in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    if stmt.then_part != None:
                        for stm in stmt.then_part.expressions:
                            self.find(stm, cls, mth)
                    if stmt.else_part != None:
                        for stm in stmt.else_part.expressions:
                            self.find(stm, cls, mth)
                elif isinstance(stmt, ast.While):
                    if stmt.condition.type == None:
                        self.find(stmt.condition, cls, mth)
                    if stmt.condition.type != "boolean":
                        print("Error: while loop condition is not a boolean in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    for stm in stmt.body.expressions:
                        self.find(stm, cls, mth)
                elif isinstance(stmt, ast.For):
                    if len(stmt.initialize) != 0 and stmt.initialize[0].type == None:
                        self.find(stmt.initialize[0], cls, mth)
                    if len(stmt.loop_condition) != 0 and stmt.loop_condition[0].type == None:
                        self.find(stmt.loop_condition[0], cls, mth)
                    if len(stmt.loop_condition) != 0 and stmt.loop_condition[0].type != "boolean": 
                        print("Error: for loop condition is not a boolean in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    if len(stmt.update_expression) != None and stmt.update_expression[0].type == None:
                        self.find(stmt.update_expression[0], cls, mth)
                    for stm in stmt.body.expressions:
                        self.find(stm, cls, mth)
                elif isinstance(stmt, ast.Return):
                    if stmt.value == "None" or stmt.value == None:
                        stmt.type = "void"
                    if not isinstance(stmt.value, str) and stmt.value.type == None:
                        self.find(stmt.value, cls, mth)
                    if not isinstance(stmt.value, str) and self.subtype_exists_str(mth.return_type, stmt.value.type) == False:
                        print("Error: return statement type is not subtype of method return type " + mth.name + " of class " + cls.name)
                        sys.exit()
                    if isinstance(stmt.value, str) and self.subtype_exists_str(mth.return_type, stmt.type) == False:
                        print("Error: return statement type is not subtype of method return type " + mth.name + " of class " + cls.name)
                        sys.exit()

                elif isinstance(stmt, ast.Block):
                    for stm in stmt.body.expressions:
                        self.find(stm, cls, mth)
                elif isinstance(stmt, ast.Break):
                    pass
                elif isinstance(stmt, ast.Continue):
                    pass
                elif isinstance(stmt, ast.Skip):
                    pass
            elif isinstance(stmt, ast.Expression):
                if isinstance(stmt, ast.ConstantExpression):
                    pass
                elif isinstance(stmt, ast.VarExpression):
                    if stmt.type == None:
                        self.resolve(stmt, cls, mth)
                elif isinstance(stmt, ast.UnaryExpression):
                    if stmt.operand.type == None:
                        self.find(stmt.operand, cls, mth)
                    if stmt.operator == "neg":
                        if stmt.operand.type != "boolean":
                            print("Error: Neg unary expression cannot be applied to a variable that is not a boolean. Found in method " + mth.name + " in class " + cls.name)
                            sys.exit()
                        stmt.type = "boolean"
                    elif stmt.operator == "-":
                        if stmt.operand.type != "float" and stmt.operand.type != "int" :
                            print("Error: Uminus unary expression cannot be applied to a variable that is not a boolean. Found in method " + mth.name + " in class " + cls.name)
                            sys.exit()
                        stmt.type = stmt.operand.type
                    else:
                        print(stmt.operator)
                elif isinstance(stmt, ast.BinaryExpression):
                    if stmt.left_operand.type == None:
                        self.find(stmt.left_operand, cls, mth)
                    if stmt.right_operand.type == None:
                        self.find(stmt.right_operand, cls, mth)
                    f, s = self.binary_type(stmt.operator)
                    if f != None:
                        if f == "arith" and (not self.FOI(stmt.left_operand.type) or not self.FOI(stmt.right_operand.type)):
                            print("Error: Arithmetic binary operations must have an int/float on both sides of the operation: Found in method " +mth.name + " in class " + cls.name)
                            sys.exit()
                        if f == "eq":
                            pass
                        if f == "bool" and (stmt.left_operand.type != "boolean" or stmt.right_operand.type != "boolean"):
                            print("Error: Boolean binary operations must have a boolean type on both sides: Found in method " +mth.name + " in class " + cls.name)
                            sys.exit()
                    if f == "bool":
                        stmt.type = "boolean"
                    elif s == "comp":
                        stmt.type = "boolean"
                    elif stmt.right_operand.type =="float" or stmt.left_operand.type == "float":
                        stmt.type = "float"
                    else:
                        stmt.type = "int"
                elif isinstance(stmt, ast.AssignExpression):
                    if stmt.left_expression.type == None:
                        self.find(stmt.left_expression, cls, mth)
                    if stmt.right_expression.type == None:
                        self.find(stmt.right_expression, cls, mth)
                    if isinstance(stmt.right_expression.type, list):
                        valid = False;
                        for item in stmt.right_expression.type:
                            if isinstance(item, ast.Method) and self.subtype_exists_str(stmt.left_expression.type, item.return_type):
                                valid = True
                                stmt.right_expression.type = item.return_type
                                stmt.right_expression.ref_id = item.id
                                break
                            elif not isinstance(item, ast.Method) and self.subtype_exists_str(stmt.left_expression.type, item.type):
                                valid = True
                                stmt.right_expression.type = item.type
                                stmt.right_expression.ref_id = item.id
                                break
                        if not valid:
                            print("Error: subtype does not exist in assignment expression: Found in method " +mth.name + " in class " + cls.name)
                            sys.exit()
                    if not self.subtype_exists_str(stmt.left_expression.type, stmt.right_expression.type):
                        print("Error: subtype does not exist in assignment expression: Found in method " + mth.name + " in class " + cls.name)
                        sys.exit()
                elif isinstance(stmt, ast.AutoExpression):
                    if stmt.expression.type == None:
                        self.find(stmt.expression, cls, mth)
                    if stmt.expression.type != "float" and stmt.expression.type != "int":
                        print("Error: trying to auto increment variable/constant that is not a float/int in " + mth.name + " of class " + cls.name)
                        sys.exit()
                elif isinstance(stmt, ast.FieldAccessExpression):
                    if stmt.base.type == None:
                        self.find(stmt.base, cls, mth)
                    sons = None
                    class_name = None
                    if stmt.base.type.__str__()[:14] == "class-literal(":
                        sons = "static"
                        class_name = stmt.base.type.__str__()[14:len(stmt.base.type.__str__()) - 1]
                    elif stmt.base.type.__str__()[:4] == "user":
                        sons = "instance"
                        class_name = stmt.base.type.__str__()[5:len(stmt.base.type.__str__()) - 1]
                    else:
                        print("Error: invalid field access base in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    if class_name not in self.tree.class_dict.keys():
                        print("No class exists for base of field access expression")
                    else:
                        stmt.type = self.find_field(class_name, sons, stmt.fieldName)
                        if len(stmt.type) == 0:
                            print("Error: no possible fields found in " + mth.name + " of class " + cls.name)
                            sys.exit()
                        elif len(stmt.type) == 1:
                            stmt.ref_id = stmt.type[0].id
                            stmt.type = stmt.type[0].type
                elif isinstance(stmt, ast.MethodCallExpression):
                    if stmt.base.type == None:
                        self.find(stmt.base, cls, mth)
                    if stmt.base.type[:4] != "user" and stmt.base.type[:13] != "class-literal":
                        print("Error: invalid base type in method call expression in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    st = None
                    if stmt.base.type[:4] == "user":
                        st = "instance"
                    else:
                        st = "static"
                    method = self.find_method(cls.name, stmt.arguments, stmt.methodName,st)
                    if len(method) == 0:
                        print("Error: no possible fields found in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    elif len(method) == 1:
                        stmt.type = method[0].return_type
                        stmt.ref_id = method[0].id
                    else:
                        stmt.type = method
                elif isinstance(stmt, ast.NewObjectExpression):
                    ret = self.find_constructor(stmt.baseClass, stmt.parameters, cls.name)
                    if ret == None:
                        print("Error: no possible constructor found for new object creation in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    stmt.type = "user(" + stmt.baseClass + ")"
                    stmt.ref_id = ret.id
                elif isinstance(stmt, ast.ThisExpression):
                    stmt.type = "user(" + str(cls.name) + ")"
                elif isinstance(stmt, ast.SuperExpression):
                    parent = cls.super_class_name
                    if parent == None:
                        print("Error: referenced super class in class with no super class in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    stmt.type = "user(" + str(parent) + ")"
                elif isinstance(stmt, ast.ClassReferenceExpression):
                    pass
            else:
                print("HMMM, unknown type" + stmt.__str__())
    def resolve(self, stmt, cls, mth):
        if isinstance(stmt, ast.VarExpression):
            for var in mth.variable_table:
                if var.name == stmt.val and stmt.id == var.id:
                    stmt.type = var.type
                    return

    def type_resolve(self, stmt1, stmt2, cls, mth):
        if stmt2.type == "int" and stmt1.type != "float" and stmt1.type != "int":
            print("Error: trying to assign int with type that is not int/float in method " + mth.name + " of class " + cls.name)
            sys.exit()
        if stmt2.type == "float" and stmt1.type != "float":
            print("Error: trying to assign float to  type that is not float in method" + mth.name + " of class " + cls.name)
            sys.exit()
        if stmt2.type == "boolean" and stmt1.type != "boolean":
            print("Error: trying to assign boolean with type that is not boolean in method " + mth.name + " of class " + cls.name)
            sys.exit()
        if not self.subtype_exists(stmt1, stmt2):
            print("Error: invalid assignment due to subtyping not existing" + mth.name + " of class " + cls.name)
            sys.exit()
        
    def find_field(self, current_class, SONS, field):
        curr = current_class
        if not isinstance(current_class, str):
            curr = current_class.name
        ans = []
        first = True
        while True:
            if curr == "" or curr == None:
                return ans
            new_class = self.tree.class_dict.get(curr)
            if new_class == None:
                return ans
            fields = new_class.fields
            for f in fields.values():
                if f.name == field and (f.visibility == "public" or first) and SONS == f.applicability:
                   ans.append(f)
            first = False
            curr = self.tree.class_dict.get(curr).super_class_name

    def find_method(self, curr_class, arguments, method_name, SONS):
        curr = curr_class
        ans = []
        first = True
        while True:
            if curr == None or curr == "":
                return ans
            methods = self.tree.class_dict.get(curr).methods
            for m in methods.values():
                if m.name == method_name and (m.visibility == "public" or first) and SONS == m.applicability: #should check for which method to choose from
                    if self.check_parameters(self.convert(m.parameters, m.variable_table), arguments):
                        ans.append(m)
            first = False
            curr = self.tree.class_dict.get(curr).super_class_name

    def find_constructor(self, class_name, arguments, current_class_name):
        class_dict = self.tree.class_dict
        for cls in class_dict.values():
            if cls.name == class_name:
                for constructor in cls.constructors.values():
                     if (constructor.visibility == "public" or current_class_name == class_name) and self.check_parameters(self.convert(constructor.parameters, constructor.variable_table), arguments):
                        return constructor
        return None

    def check_parameters(self, parameters, arguments):
        if len(parameters) != len(arguments):
            return False
        for ind in range(len(parameters)):
            if not self.subtype_exists(parameters[ind], arguments[ind]):
                return False
        return True
        
    def convert(self, parameters, variable_table):
        ans = []
        for param in parameters:
            for variable in variable_table:
                if param == variable.id:
                    ans.append(variable)
        return ans

    def subtype_exists(self, left, right):
        if left.type == right.type:
            return True
        if left.type == "float" and right.type == "int":
            return True
        if left.type[:4] == "user" and right.type == "null":
            return True
        right_type = None
        left_type = None
        if right.type[:4] == "user":
            right_type = right.type[5:len(right.type) - 1]
            if left.type[:4] != "user":
                return False
            else:
                left_type = left.type[5:len(left.type) - 1]
        elif right.type[:13] == "class-literal":
            right_type = right.type[14:len(right.type) - 1]
            if left.type[:13] != "class-literal":
                return False
            else:
                left_type = left.type[14:len(left.type) - 1]
        else:
            return False
        while True:
            parent = self.tree.class_dict.get(right_type).super_class_name
            if parent == None:
                return False
            if parent == left_type:
                return True
            right_type = parent

    def subtype_exists_str(self, left, right):
        if left == right:
            return True
        if left == "float" and right == "int":
            return True
        if left[:4] == "user" and right == "null":
            return True
        if right == "boolean":
            return False
        right_type = None
        left_type = None
        if right[:4] == "user":
            right_type = right[5:len(right) - 1]
            if left[:4] != "user":
                return False
            else:
                left_type = left[5:len(left) - 1]
        elif right[:13] == "class-literal":
            right_type = right[14:len(right) - 1]
            if left[:13] != "class-literal":
                return False
            else:
                left_type = left[14:len(left) - 1]
        else:
            return False
        while True:
            parent = self.tree.class_dict.get(right_type).super_class_name
            if parent == None:
                return False
            if parent == left_type:
                return True
            right_type = parent

    def binary_type(self, op):
        if op == "add" or op == "min" or op =="mul" or op == "div":
            return "arith", "op"
        if op == "and" or op == "or":
            return "bool", "op"
        if op == "lt" or op == "leq" or op =="gt" or op == "geq":
            return "arith", "comp"
        if op == "eq" or op == "neq":
            return "eq", "comp"
        return None, None
    def FOI(self, typ):
        return typ == "int" or typ =="float"

    
