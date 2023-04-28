import decaf_ast as ast
import sys
class TypeChecker():
    def __init__(self):
        pass
    def check(self, tree):
        self.tree = tree
        for c in tree.classes:
            for m in c.methods.values():
                self.check_method(tree,c,m)
    def check_method(self, tree, cls, mth):
        for stmt in mth.body.expressions:
            self.find(stmt, cls, mth)
    def find(self, stmt, cls, mth):
        if not isinstance(stmt, list): 
            if isinstance(stmt, ast.Statement):
                if isinstance(stmt, ast.If):
                    if stmt.condition.type == None:
                        self.resolve(stmt.condition, cls, mth)
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
                        self.resolve(stmt.condition, cls, mth)
                    if stmt.condition.type != "boolean":
                        print("Error: while loop condition is not a boolean in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    for stm in stmt.body.expressions:
                        self.find(stm, cls, mth)
                elif isinstance(stmt, ast.For):
                    if stmt.intialize != None and stmt.initialize.type == None:
                        self.resolve(stmt.initialize, cls, mth)
                    if stmt.loop_condition != None and stmt.loop_condition.type == None:
                        self.resolve(stmt.loop_condition, cls, mth)
                    if stmt.loop_condition.type != "boolean": # Empty thing in the ; ; parts of for loop?
                        print("Error: while loop condition is not a boolean in " + mth.name + " of class " + cls.name)
                        sys.exit()
                    if stmt.update_expression != None and stmt.update_expression.type == None:
                        self.resolve(stmt.update_expression, cls, mth)
                    for stm in stmt.body.expressions:
                        self.find(stm, cls, mth)
                elif isinstance(stmt, ast.Return):
                    pass
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
                    pass
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
                elif isinstance(stmt, ast.AssignExpression):
                    if stmt.left_expression.type == None:
                        self.find(stmt.left_expression, cls, mth)
                    if stmt.right_expression.type == None:
                        self.find(stmt.right_expression, cls, mth)
                    self.type_resolve(stmt.left_expression, stmt.right_expression, cls, mth)
                elif isinstance(stmt, ast.AutoExpression):
                    if stmt.expression.type == None:
                        self.find(stmt.expression, cls, mth)
                    if stmt.expression.type != "float" and stmt.expression.type != "int":
                        print("Error: trying to auto increment variable/constant that is not a float/int in " + mth.name + " of class " + cls.name)
                        sys.exit()
                elif isinstance(stmt, ast.FieldAccessExpression):
                    if stmt.base.type.__str__()[:14] != "class-literal(":
                        print("Not class literal in base of field access")
                    class_name = stmt.base.type.__str__()[14:len(stmt.base.type.__str__()) - 1]
                    if class_name not in self.tree.class_dict.keys():
                        print("Not class exists for base of field access expression")
                    else:
                        pass
                elif isinstance(stmt, ast.MethodCallExpression):
                    pass
                elif isinstance(stmt, ast.NewObjectExpression):
                    pass
                elif isinstance(stmt, ast.ThisExpression):
                    pass
                elif isinstance(stmt, ast.SuperExpression):
                    pass
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
        
    def find_class(self, current_class, target_name, target_type, son):
        if current_class == None:
            return None, None
        sel = self.tree.class_dict.get(current_class)
        for var in sel.fields.values():
            if var.name == target_name:
                return sel, var
        return self.find_class(sel.super_class_name, target_name, target_type)
    
    def subtype_exists(self, left, right):
        return True
    
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

    
