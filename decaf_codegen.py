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
            self.machine.capp(self.machine.label("Method: " + meth.name))
            for var in meth.variable_table:
                if var.kind == "local":
                    reg = self.machine.temp_reg()
                    temps.update({var.id: reg})
                else:
                    reg = self.machine.arg_reg()
                    args.update({var.id: reg})
            for stmt in meth.body.expressions:
                self.write(stmt, args, temps, meth, 1)
        for s in self.machine.code:
            space = ""
            if not isinstance(s[0], mc.Label):
                space = " "
            print(self.generate_tabs(s[1]) + space + str(s[0]))
    def generate_tabs(self, tab):
        st = ""
        for i in range(tab):
            st += '\t'
        return st
    def write(self, stmt, args, temp, meth, t):
        if isinstance(stmt, list):
            pass
        elif isinstance(stmt, ast.If):
            self.machine.capp(self.machine.label(" # If Statement"), t) 
            self.write(stmt.condition, args, temp, meth, t)
        elif isinstance(stmt, ast.While):
            self.machine.capp(self.machine.label(" # While Loop Statement"), t) 
        elif isinstance(stmt, ast.For):
            self.machine.capp(self.machine.label(" # For Loop Statement"), t) 
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
                    self.machine.capp(mc.move_immed_i(reg.name, stmt.value), t)
                elif stmt.type == "float":
                    self.machine.capp(mc.move_immed_i(reg.name, stmt.value), t)
                elif stmt.value == "false":
                    self.machine.capp(mc.move_immed_i(reg.name, 0), t)
                else:
                    self.machine.capp(mc.move_immed_i(reg.name, 1), t)
                return reg
            elif isinstance(stmt, ast.VarExpression):
                if stmt.id in args.keys():
                    return args.get(stmt.id)
                elif stmt.id in temp.keys():
                    return temp.get(stmt.id)
            elif isinstance(stmt, ast.UnaryExpression):
                reg = self.write(stmt.operand, args, temp, meth, t)
                
            elif isinstance(stmt, ast.BinaryExpression):
                r1 = self.write(stmt.left_operand,args, temp, meth, t)
                r2 = self.write(stmt.right_operand, args, temp, meth, t)
                r3 = self.machine.temp_reg()
                flt = False
                if stmt.left_operand.type == "float" or stmt.right_operand.type == "float":
                    flt = True
                if stmt.operator == "add":
                    if flt:
                        self.machine.capp(mc.fadd(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.iadd(r3,r1,r2), t)
                    return r3
                elif stmt.operator == "min":
                    if flt:
                        self.machine.capp(mc.fsub(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.isub(r3,r1,r2), t)
                    return r3
                elif stmt.operator == "div":
                    if flt:
                        self.machine.capp(mc.fdiv(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.idiv(r3,r1,r2), t)
                    return r3
                elif stmt.operator == "mul":
                    if flt:
                        self.machine.capp(mc.fmul(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.imul(r3,r1,r2), t)
                    return r3
                elif stmt.operator == "or":
                    self.machine.capp(mc.save(r1), t)
                    self.machine.capp(mc.save(r2), t)
                    self.machine.capp(mc.iadd(r3,r1,r2), t)
                    self.machine.capp(mc.move_immed_i(r1, 0), t)
                    self.machine.capp(mc.igt(r2, r3, r1), t)
                    self.machine.capp(mc.move(r3, r2), t)
                    self.machine.capp(mc.restore(r1), t)
                    self.machine.capp(mc.restore(r2), t)
                    return r3
                elif stmt.operator == "and":
                    self.machine.capp(mc.save(r1), t)
                    self.machine.capp(mc.save(r2), t)
                    self.machine.capp(mc.iadd(r3,r1,r2), t)
                    self.machine.capp(mc.move_immed_i(r1, 1), t)
                    self.machine.capp(mc.igt(r2, r3, r1), t)
                    self.machine.capp(mc.move(r3, r2), t)
                    self.machine.capp(mc.restore(r1), t)
                    self.machine.capp(mc.restore(r2), t)
                    return r3
                elif stmt.operator == "eq":
                    self.machine.capp(mc.save(r1), t)
                    self.machine.capp(mc.save(r2), t)
                    self.machine.capp(mc.fsub(r3,r1,r2), t)
                    self.machine.capp(mc.move_immed_f(r1, 0), t)
                    l1 = self.machine.label()
                    l2 = self.machine.label()
                    self.machine.capp(mc.fgt(r2,r3,r1), t)
                    self.machine.capp(mc.bnz(r2, l1), t)
                    self.machine.capp(mc.flt(r2,r3,r1), t)
                    self.machine.capp(mc.bnz(r2, l1), t)
                    self.machine.capp(mc.move_immed_i(r2, 1), t)
                    self.machine.capp(mc.jmp(l2), t)
                    self.machine.capp(l1, t)
                    self.machine.capp(mc.move_immed_i(r2, 0), t)
                    self.machine.capp(l2, t)
                    self.machine.capp(mc.move(r3, r2), t)
                    self.machine.capp(mc.restore(r1), t)
                    self.machine.capp(mc.restore(r2), t)
                    return r3
                elif stmt.operator == "neq":
                    self.machine.capp(mc.save(r1), t)
                    self.machine.capp(mc.save(r2), t)
                    self.machine.capp(mc.fsub(r3,r1,r2), t)
                    self.machine.capp(mc.move_immed_f(r1, 0), t)
                    l1 = self.machine.label()
                    l2 = self.machine.label()
                    self.machine.capp(mc.fgt(r2,r3,r1), t)
                    self.machine.capp(mc.bnz(r2, l1), t)
                    self.machine.capp(mc.flt(r2,r3,r1), t)
                    self.machine.capp(mc.bnz(r2, l1), t)
                    self.machine.capp(mc.move_immed_i(r2, 0), t)
                    self.machine.capp(mc.jmp(l2), t)
                    self.machine.capp(l1, t)
                    self.machine.capp(mc.move_immed_i(r2, 1), t)
                    self.machine.capp(l2, t)
                    self.machine.capp(mc.move(r3, r2), t)
                    self.machine.capp(mc.restore(r1), t)
                    self.machine.capp(mc.restore(r2), t)
                    return r3
                elif stmt.operator == "lt":
                    if flt:
                        self.machine.capp(mc.flt(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.ilt(r3,r1,r2), t)
                    return r3
                elif stmt.operator == "gt":
                    if flt:
                        self.machine.capp(mc.fgt(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.igt(r3,r1,r2), t)
                    return r3
                elif stmt.operator =="leq":
                    if flt:
                        self.machine.capp(mc.fleq(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.ileq(r3,r1,r2), t)
                    return r3
                elif stmt.operator == "geq":
                    if flt:
                        self.machine.capp(mc.fgeq(r3,r1,r2), t)
                    else:
                        self.machine.capp(mc.igeq(r3,r1,r2), t)

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