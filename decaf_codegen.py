import decaf_absmc as mc

class CodeGenerator():
    def __init__(self, ast):
        self.ast = ast
        self.machine = mc.Machine(self.ast)

    def generate(self):
        static_fields = 0
        for c in self.ast.class_dict.values():
            for var in c.fields:
                if var.applicability == "static":
                    static_fields += 1
        if static_fields != 0:
            self.machine.addLine()
        for meth in self.ast.methods.values():
            for stmt in meth.body.expressions:
                if isinstance(stmt, list):
                    
