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
        super().__init__("")
class move_immed_f(Move):
    def __init__(self,r,i):
        super().__init__("")
class move(Move):
    def __init__(self,r1,r2):
        super().__init__("")
class iadd(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class isub(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class imul(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class idiv(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class imod(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class igt(IntArith): 
    def __init__(self,r1,r2,r3):
        super().__init__("")
class igeq(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class ilt(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class ileq(IntArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fadd(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fsub(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fmul(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fdiv(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fgt(FloatArith): 
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fgeq(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class flt(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class fleq(FloatArith):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class ftoi(Conversions):
    def __init__(self,r1,r2):
        super().__init__("")
class itof(Conversions):
    def __init__(self,r1,r2):
        super().__init__("")
class bz(Branches):
    def __init__(self,r1,L):
        super().__init__("")
class bnz(Branches):
    def __init__(self,r1,L):
        super().__init__("")
class jmp(Branches):
    def __init__(self,L):
        super().__init__("")
class hload(HeapMan):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class hstore(HeapMan):
    def __init__(self,r1,r2,r3):
        super().__init__("")
class halloc(HeapMan):
    def __init__(self,r1,r2):
        super().__init__("")
class call(Proced):
    def __init__(self,L):
        super().__init__("")
class ret(Proced):
    def __init__(self):
        super().__init__("")
class save(Proced):
    def __init__(self,r):
        super().__init__("")
class store(Proced):
    def __init__(self,r):
        super().__init__("")




