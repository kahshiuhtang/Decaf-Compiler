import decaf_absmc as mc
import decaf_ast as ast
class CodeGenerator():
    def __init__(self, ast):
        self.ast = ast
        self.machine = mc.Machine(self.ast)

    def generate(self):
        static_fields = 0
        for c in self.ast.class_dict.values():
            for var in c.fields:
                if c.fields.get(var).applicability == "static":
                    static_fields += 1
        if static_fields != 0:
            self.machine.capp("")
        for meth in self.ast.methods.values():
            self.machine.clean()
            args = {}
            temps = {}
            for var in meth.variable_table:
                if var.kind == "local":
                    reg = self.machine.temp_reg()
                    temps.update({var.id: reg})
                else:
                    reg = self.machine.arg_reg()
                    args.update({var.id: reg})
            for stmt in meth.body.expressions:
                self.write(stmt, args, temps, meth)
        for s in self.machine.code:
            print(s)

    def write(self, stmt, args, temp, meth):
        if isinstance(stmt, list):
            pass
        elif isinstance(stmt, ast.If):
            self.machine.capp(self.machine.label()) 
            self.write(stmt.condition, args, temp, meth)
        elif isinstance(stmt, ast.While):
            pass
        elif isinstance(stmt, ast.For):
            pass
        elif isinstance(stmt, ast.Return):
            pass
        elif isinstance(stmt, ast.Block):
            pass
        elif isinstance(stmt, ast.Break):
            pass
        elif isinstance(stmt, ast.Continue):
            pass
        elif isinstance(stmt, ast.Skip):
            pass
        elif isinstance(stmt, ast.Expression):
            if isinstance(stmt, ast.ConstantExpression):
                reg = self.machine.temp_reg()
                if stmt.type == "int":
                    self.machine.capp(mc.move_immed_i(reg.name, stmt.value))
                elif stmt.type == "float":
                    self.machine.capp(mc.move_immed_i(reg.name, stmt.value))
                elif stmt.value == "false":
                    self.machine.capp(mc.move_immed_i(reg.name, 0))
                else:
                    self.machine.capp(mc.move_immed_i(reg.name, 1))
                return reg
            elif isinstance(stmt, ast.VarExpression):
                pass
            elif isinstance(stmt, ast.UnaryExpression):
                pass
            elif isinstance(stmt, ast.BinaryExpression):
                r1 = self.write(stmt.left_operand,args, temp, meth)
                r2 = self.write(stmt.right_operand, args, temp, meth)
                r3 = self.machine.temp_reg()
                flt = False
                if stmt.left_operand.type == "float" or stmt.right_operand.type == "float":
                    flt = True
                if stmt.operator == "add":
                    if flt:
                        ast.machine.capp(mc.fadd(r3,r1,r2))
                    else:
                        ast.machine.capp(mc.iadd(r3,r1,r2))
                elif stmt.operator == "min":
                    if flt:
                        ast.machine.capp(mc.fsub(r3,r1,r2))
                    else:
                        ast.machine.capp(mc.isub(r3,r1,r2))
                elif stmt.operator == "div":
                    if flt:
                        ast.machine.capp(mc.fdiv(r3,r1,r2))
                    else:
                        ast.machine.capp(mc.idiv(r3,r1,r2))
                elif stmt.operator == "mul":
                    if flt:
                        ast.machine.capp(mc.fmul(r3,r1,r2))
                    else:
                        ast.machine.capp(mc.imul(r3,r1,r2))
                elif stmt.operator == "or":
                    ast.machine.capp(mc.fmul(r3,r1,r2))
                elif stmt.operator == "and":

                elif stmt.operator == "eq":
           
                elif stmt.operator == "neq":
                
                elif stmt.operator == "lt":
              
                elif stmt.operator == "gt":
         
                elif stmt.operator =="leq":
 
                elif stmt.operator == "geq":

            elif isinstance(stmt, ast.AssignExpression):
                pass
            elif isinstance(stmt, ast.AutoExpression):
                pass
            elif isinstance(stmt, ast.FieldAccessExpression):
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