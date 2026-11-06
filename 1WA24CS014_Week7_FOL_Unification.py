def isVariable(x):
    return isinstance(x, str) and x.startswith("?")

def occurs(var,x, theta):   
    x=substitute(x, theta)
    if var == x:
        return True

    if isinstance(x, tuple):
        return any(occurs(var, item, theta) for item in x[1:])

    return False

def substitute(x, subst):
    if isVariable(x) and x in subst:
        return substitute(subst[x], subst)

    if isinstance(x, tuple):
        return tuple(substitute(item, subst) for item in x)
    return x

def unify(x,y,subst=None):
    if subst is None:
        subst={}

    x=substitute(x,subst)
    y=substitute(y, subst)

    if not isinstance(x,tuple) or not isinstance(y, tuple):
        if x==y:
            return subst

        if isVariable(x):
            if occurs(x,y,subst):
                return None
            subst[x]=y
            return subst

        if isVariable(y):
            if occurs(y,x,subst):
                return None
            subst[y]=x
            return subst
        return None

    if x[0]!=y[0]:
        return None

    if len(x)!=len(y):
        return None

    for a,b in zip(x[1:], y[1:]):
        subst=unify(a,b,subst)
        if subst is None:
            return None
    return subst



psi1 = ("P", "?x", "a")
psi2 = ("P", "b", "?y")

result = unify(psi1, psi2)

if result is None:
    print("Unification Failed")
else:
    print("MGU = ", result)
    