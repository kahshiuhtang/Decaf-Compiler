class Register():
    def __init__(self):
        self.name = None
        self.type = None
        self.value = None
class Temp(Register):
    def __init__(self, name):
        self.name = name
        self.type = "Temp"
    def __str__(self):
        return self.name
class Arg(Register):
    def __init__(self, name):
        self.name = name
        self.type = "Arg"
    def __str__(self):
        return self.name
class Label():
    def __init__(self, name, comment):
        self.name = name
        self.comment = comment
    
    def __str__(self):
        return self.name + self.comment
class Machine():
    def __init__(self, ast):
        self.args = []
        self.args_status = []
        self.temps = []
        self.temps_status = []
        self.code = []
        self.labels = 0
        self.ast = ast
    def capp(self, inst, tabs=0):
        self.code.append([inst, tabs])
    def arg_reg(self):
        for i in range(len(self.args)):
            if self.args_status[i]:
                self.args_status[i] = False
                return self.args[i]
        return self.new_reg("arg")

    def temp_reg(self):
        for i in range(len(self.temps)):
            if self.temp_status[i]:
                self.temp_status[i] = False
                return self.temp[i]
        return self.new_reg("temp")
    def label(self, comment=""):
        self.labels += 1
        return Label("L" + str(self.labels) + ":", comment)
    def new_reg(self, typ):
        stat = self.args_status if typ == "arg" else self.temp_status
        regs = self.args if typ == "arg" else self.temp
        new_reg = Arg("a" + str(len(self.args))) if typ == "arg" else Temp("t" + str(len(self.temp)))
        regs.append(new_reg)
        stat.append(False)
        return new_reg
    def top(self):
        return self.code[len(self.code) - 1]
    def clean(self):
        self.args = []
        self.args_status = []
        self.temp = []
        self.temp_status = []

class Instructions():
    def __init__(self, name):
        self.name = name
class Move(Instructions):
    def __init__(self, name):
        super().__init__(name)
class IntArith(Instructions):
    def __init__(self, name):
        super().__init__(name)
class FloatArith(Instructions):
    def __init__(self, name):
        super().__init__(name)
class Conversions(Instructions):
    def __init__(self, name):
        super().__init__(name)
class Branches(Instructions):
    def __init__(self, name):
        super().__init__(name)
class HeapMan(Instructions):
    def __init__(self, name):
        super().__init__(name)
class Proced(Instructions):
    def __init__(self, name):
        super().__init__(name)

class move_immed_i(Move):
    def __init__(self,r,i):
        super().__init__("move_immed_i")
        self.r = r
        self.i = i
    def __str__(self):
        return self.name + " " + self.r.__str__() + " " + str(self.i)
class move_immed_f(Move):
    def __init__(self,r,i):
        super().__init__("move_immed_f")
        self.r = r
        self.i = i
    def __str__(self):
        return self.name + " " + self.r.__str__() + " " + str(self.i)
class move(Move):
    def __init__(self,r1,r2):
        super().__init__("move")
        self.r1 = r1
        self.r2 = r2
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() 
class iadd(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("iadd")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class isub(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("isub")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class imul(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("imul")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class idiv(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("idiv")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class imod(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("imod")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class igt(IntArith): 
    def __init__(self,r1,r2,r3):
        super().__init__("igt")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class igeq(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("igeq")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class ilt(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("ilt")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class ileq(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("ileq")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fadd(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("fadd")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fsub(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("fsub")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fmul(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("fmul")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fdiv(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("fdiv")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fgt(FloatArith): 
    def __init__(self,r1,r2,r3):
        super().__init__("fgt")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fgeq(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("fgeq")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class flt(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("flt")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class fleq(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("fleq")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class ftoi(Conversions):
    def __init__(self,r1,r2):
        super().__init__("ftoi")
        self.r1 = r1
        self.r2 = r2
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__()
class itof(Conversions):
    def __init__(self,r1,r2):
        super().__init__("itof")
        self.r1 = r1
        self.r2 = r2
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__()
class bz(Branches):
    def __init__(self,r1,L):
        super().__init__("bz")
        self.r1 = r1
        self.L = L
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.L.__str__()[:len(self.L.__str__()) - 1]
class bnz(Branches):
    def __init__(self,r1,L):
        super().__init__("bnz")
        self.r1 = r1
        self.L = L
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.L.__str__()[:len(self.L.__str__()) - 1]
class jmp(Branches):
    def __init__(self,L):
        super().__init__("jmp")
        self.L = L
    def __str__(self):
        return self.name + " " + self.L.__str__()[:len(self.L.__str__()) - 1]
class hload(HeapMan):
    def __init__(self,r1,r2,r3):
        super().__init__("hload")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class hstore(HeapMan):
    def __init__(self,r1,r2,r3):
        super().__init__("hstore")
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__() + " " + self.r3.__str__()
class halloc(HeapMan):
    def __init__(self,r1,r2):
        super().__init__("")
        self.r1 = r1
        self.r2 = r2
    def __str__(self):
        return self.name + " " + self.r1.__str__() + " " + self.r2.__str__()
class call(Proced):
    def __init__(self,L):
        super().__init__("")
        self.L = L
    def __str__(self):
        return self.name + " " + self.L.__str__()[:len(self.L.__str__()) - 1]
class ret(Proced):
    def __init__(self):
        super().__init__("")
    def __str__(self):
        return self.name
class save(Proced):
    def __init__(self,r):
        super().__init__("save")
        self.r = r
    def __str__(self):
        return self.name + " " + self.r.__str__()
class restore(Proced):
    def __init__(self,r):
        super().__init__("restore")
        self.r = r
    def __str__(self):
        return self.name + " " + self.r.__str__()





    