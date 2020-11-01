class Application:
    def __init__(self,head,arg):
        self.head = head 
        self.arg = arg
    def __str__(self):
        return f"({self.head} {self.arg})"
    def beta_reduce(self,budget):
        if budget <= 0:
            raise ValueError("budget exceeded")
        head = self.head
        if isinstance(head,(Lambda,Builtin)):
            return head.apply(self.arg,budget)#body.subst(self.arg, 0).beta_reduce(budget-1)
        #elif isinstance(head,Builtin): #todo: less hacky
        #    return self
        else:
            return Application(self.head.beta_reduce(budget), self.arg.beta_reduce(budget)).beta_reduce(budget-1)
    def subst(self,term,index):
        return Application(self.head.subst(term,index), self.arg.subst(term,index))

class Lambda:
    def __init__(self,body):
        self.body = body
    def __str__(self):
        return f"λ{self.body}"
    def beta_reduce(self,budget):
        return self
    def subst(self,term,index):
        return Lambda(self.body.subst(term,index+1))
    def apply(self,arg,budget):
        return self.body.subst(arg,0).beta_reduce(budget-1)

class Variable:
    def __init__(self,index):
        self.index = index
    def __str__(self):
        return f"τ{self.index}"
    def beta_reduce(self,budget):
        return self
    def subst(self,term,index):
        if index == self.index:
            return term
        else:
            return self

class Builtin:
    def __init__(self,name):
        self.name = name 
    def __str__(self):
        return str(self.name)
    def beta_reduce(self,budget):
        return self
    def subst(self,term,index):
        return self
    def apply(self,arg,budget):
        return Builtin(f"[{self.name} of {arg}]")

class UnchurchSucc(Builtin):
    def apply(self,arg,budget):
        value = arg.beta_reduce(budget-1)
        if isinstance(value,UnchurchNum):
            return UnchurchNum(value.name, value.val + 1)
        else:
            return Builtin(f"[{self.name} of {arg}]")
class UnchurchNum(Builtin):
    def __init__(self,name,val=0):
        self.name = name 
        self.val = val
    def __str__(self):
        return f"{self.name}{{{self.val}}}"

# util things, because i cba making an actual parser just for testing
def λ(body):
    return Lambda(body)
def a(*args):
    t = Application(args[0],args[1])
    for g in args[2:]:
        t = Application(t,g)
    return t
def ar(*args):
    t = Application(args[-2],args[-1])
    for g in args[-3::-1]:
        t = Application(g,t)
    return t
def v(n):
    return Variable(n)

def λ2(b):
    return λ(λ(b))
def λ3(b):
    return λ(λ(λ(b)))

# S ::= λx.λy.λz.((x z) (y z))
#   ::= λλλ.((τ2 τ0) (τ1 τ0))
S = λ3( a( a(v(2), v(0)),  a(v(1), v(0))  )  )

# K ::= λx.λy.x
#   ::= λλ.τ1
K = λ2( v(1) )

# I ::= λx.x
#   ::= λ.τ0
I = λ( v(0) )

# succ ::= λn.λf.λx.(f ((n f) x))
#      ::= λλλ.(τ1 ((τ2 τ1) τ0))
succ = λ3( a(v(1), a(a(v(2), v(1)), v(0))) )

# pair ::= λx.λy.λf.((f x) y)
#      ::= λλλ.((τ0 τ2) τ1)
pair = λ3( a(v(0),v(2),v(1)) )

# frst ::= λp.(p λx.λy.x)
#      ::= λ.(τ0 λλ.τ1)
frst = λ( a(v(0), λ2(v(1)) ) )

# scnd ::= λp.(p λx.λy.y)
#      ::= λ.(τ0 λλ.τ0)
scnd = λ( a(v(0), λ2(v(0)) ) )



def church(n):
    if n == 0:
        return λ(I)
    else:
        return λ2( ar(*([v(1)]*n)+[v(0)] ) )

p0 = a(pair, church(0), church(0))

# sp ::= λp.(pair (scnd p) (succ (scnd p)))
#    ::= λ.(pair (scnd τ0) (succ (scnd τ0)))
sp = λ( a(pair, a(scnd,v(0)), a(succ, a(scnd, v(0))) ) )

# pred ::= λv.(frst ((v sp) p0))
#      ::= λ.(frst ((τ0 sp) p0))
pred = λ(a(frst, a(a(v(0), sp), p0)))


b = Builtin("b")
c = Builtin("c")

z = UnchurchNum("n",0)
usucc = UnchurchSucc("usucc")

t = a(a(pred,church(70)), usucc, z)

print(str(t))
print(t.beta_reduce(1000))