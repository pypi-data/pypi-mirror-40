class Formula(object):
    """
    Classes to programmatically build
    and represent formulae and terms of the language
    specified in Definition 1.
    """
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2

    def makeConjunction(s):
        """
        >>> Formula.makeConjunction(["a"])
        'a'
        >>> Formula.makeConjunction(["a", "b", "c"])
        And("c", And("b", "a"))
        """
        f = None
        for e in s:
            if f == None:
                f = e
            else:
                f = And(e, f)
        return f

    def makeDisjunction(s):
        """
        >>> Formula.makeDisjunction(["a"])
        'a'
        >>> Formula.makeDisjunction(["a", "b", "c"])
        Or("c", Or("b", "a"))
        """
        f = None
        for e in s:
            if f == None:
                f = e
            else:
                f = Or(e, f)
        return f
        
    def substituteVariable(var, new, formula):
        newFormula = repr(formula)
        if isinstance(new, Not):
            newFormula = newFormula.replace("'"+var+"'", ""+repr(new)+"")
        else:
            newFormula = newFormula.replace(var, "'"+new+"'").replace("''","'")
        return eval(newFormula)

    def __eq__(self, other):
        return self.f1 == other.f1 and self.f2 == other.f2 if self.__class__ == other.__class__ else False

    def __hash__(self):
        return hash((self.f1, self.f2))

    def __repr__(self):
        if isinstance(self.f1, str):
            f1 = "'"+self.f1+"'"
        else:
            f1 = str(self.f1)
        if isinstance(self.f2, str):
            f2 = "'"+self.f2+"'"
        else:
            f2 = str(self.f2)

        if isinstance(self, Atom):
            return "Atom("+str(f1)+")"
        if isinstance(self, Good):
            return "Good("+str(f1)+")"
        if isinstance(self, Bad):
            return "Bad("+str(f1)+")"
        if isinstance(self, Neutral):
            return "Neutral("+str(f1)+")"
        if isinstance(self, Not):
            return "Not("+str(f1)+")"
        if isinstance(self, Or):
            return "Or("+str(f1)+", "+str(f2)+")"
        if isinstance(self, And):
            return "And("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Impl):
            return "Impl("+str(f1)+", "+str(f2)+")"
        if isinstance(self, BiImpl):
            return "BiImpl("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Affects):
            return "Affects("+str(f1)+", "+str(f2)+")"
        if isinstance(self, AffectsPos):
            return "AffectsPos("+str(f1)+", "+str(f2)+")"
        if isinstance(self, AffectsNeg):
            return "AffectsNeg("+str(f1)+", "+str(f2)+")"
        if isinstance(self, I):
            return "I("+str(f1)+")"
        if isinstance(self, End):
            return "End("+str(f1)+")"
        if isinstance(self, Means):
            return "Means("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Causes):
            return "Causes("+str(f1)+", "+str(f2)+")"
        if isinstance(self, PCauses):
            return "PCauses("+str(f1)+", "+str(f2)+")"
        if isinstance(self, SCauses):
            return "SCauses("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Explains):
            return "Explains("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Prevents):
            return "Prevents("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Because):
            return "Because("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Intervention):
            return "Intervention("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Exists):
            return "Exists("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Forall):
            return "Forall("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Gt):
            return "Gt("+str(f1)+", "+str(f2)+")"
        if isinstance(self, GEq):
            return "GEq("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Eq):
            return "Eq("+str(f1)+", "+str(f2)+")"
        if isinstance(self, Must):
            return "Must("+str(f1)+")"
        if isinstance(self, May):
            return "May("+str(f1)+")"
        if isinstance(self, K):
            return "K("+str(f1)+")"
        if isinstance(self, Consequence):
            return "Consequence("+str(f1)+")"
        if isinstance(self, Goal):
            return "Goal("+str(f1)+")"
        if isinstance(self, Choice):
            return "Choice("+str(f1)+")"
        if isinstance(self, Patient):
            return "Patient("+str(f1)+")"

    def getPosLiteralsEvent(self):
        """ 
        For Event Formula Only. 
        Make sure that event formulae are 
        conjunctions of literals!
        """
        r = []
        l = self.getAllLiteralsEvent()
        for e in l:
            if isinstance(e, Not):
                r.append(e.f1)
            else:
                r.append(e)
        return r

    def getAllLiteralsEvent(self):
        """ 
        For Event Formula Only. 
        Make sure that event formulae are 
        conjunctions of literals!
        """
        if isinstance(self, Not):
            return [self]
        if isinstance(self, And):
            f1 = []
            f2 = []
            if isinstance(self.f1, str):
                f1 = f1 + [self.f1]
            else:
                f1 = f1 + self.f1.getAllLiteralsEvent()
            if isinstance(self.f2, str):
                f2 = f2 + [self.f2]
            else:
                f2 = f2 + self.f2.getAllLiteralsEvent()
            return f1 + f2

    def stripParentsFromMechanism(self):
        """ Only for preprocessing the mechanisms. """
        if self.f2 is None:
            if isinstance(self.f1, str):
                return [self.f1]
            return self.f1.stripParentsFromMechanism()
        if isinstance(self.f1, str) and isinstance(self.f2, str):
            return [self.f1, self.f2]
        if isinstance(self.f1, str) and not isinstance(self.f2, str):
            return [self.f1] + self.f2.stripParentsFromMechanism()
        if not isinstance(self.f1, str) and isinstance(self.f2, str):
            return [self.f2] + self.f1.stripParentsFromMechanism()
        
        #else:
        #    return self.f1.stripParentsFromMechanism() + self.f2.stripParentsFromMechanism()

    def getNegation(self, c = None):
        if c == None:
            c = self
        if isinstance(c, str):
            return Not(c)
        if isinstance(c, Not):
            if isinstance(c.f1, Not):
                return self.getNegation(c.f1.f1)
            else:
                return c.f1
        return Not(c)

class Atom(Formula):
    def __init__(self, f1):
        super(Atom, self).__init__(f1, None)
        
class Good(Formula):
    def __init__(self, f1):
        super(Good, self).__init__(f1, None)
        
class Bad(Formula):
    def __init__(self, f1):
        super(Bad, self).__init__(f1, None)
        
class Neutral(Formula):
    def __init__(self, f1):
        super(Neutral, self).__init__(f1, None)

        
class Not(Formula):
    def __init__(self, f1):
        super(Not, self).__init__(f1, None)


class And(Formula):
    def __init__(self, f1, f2):
        super(And, self).__init__(f1, f2)


class Or(Formula):
    def __init__(self, f1, f2):
        super(Or, self).__init__(f1, f2)


class Impl(Formula):
    def __init__(self, f1, f2):
        super(Impl, self).__init__(f1, f2)
        
        
class BiImpl(Formula):
    def __init__(self, f1, f2):
        super(BiImpl, self).__init__(f1, f2)


class Affects(Formula):
    def __init__(self, f1, f2):
        super(Affects, self).__init__(f1, f2)
        
        
class AffectsPos(Formula):
    def __init__(self, f1, f2):
        super(AffectsPos, self).__init__(f1, f2)
        
        
class AffectsNeg(Formula):
    def __init__(self, f1, f2):
        super(AffectsNeg, self).__init__(f1, f2)
        
        
class I(Formula):
    def __init__(self, f1):
        super(I, self).__init__(f1, None)
        
        
class Goal(Formula):
    def __init__(self, f1):
        super(Goal, self).__init__(f1, None)
        
        
class Choice(Formula):
    def __init__(self, f1):
        super(Choice, self).__init__(f1, None)
        
class Patient(Formula):
    def __init__(self, f1):
        super(Patient, self).__init__(f1, None)
        
        
class End(Formula):
    def __init__(self, f1):
        super(End, self).__init__(f1, None)

        
class Means(Formula):
    def __init__(self, f1, f2):
        super(Means, self).__init__(f1, f2)


class K(Formula):
    def __init__(self, f1):
        super(K, self).__init__(f1, None)
        
        
class Consequence(Formula):
    def __init__(self, f1):
        super(Consequence, self).__init__(f1, None)


class May(Formula):
    def __init__(self, f1):
        super(May, self).__init__(f1, None)


class Must(Formula):
    def __init__(self, f1):
        super(Must, self).__init__(f1, None)


class Causes(Formula):
    def __init__(self, f1, f2):
        super(Causes, self).__init__(f1, f2)


class PCauses(Formula):
    def __init__(self, f1, f2):
        super(PCauses, self).__init__(f1, f2)


class SCauses(Formula):
    def __init__(self, f1, f2):
        super(SCauses, self).__init__(f1, f2)


class Explains(Formula):
    def __init__(self, f1, f2):
        super(Explains, self).__init__(f1, f2)


class Prevents(Formula):
    def __init__(self, f1, f2):
        super(Prevents, self).__init__(f1, f2)


class Intervention(Formula):
    def __init__(self, f1, f2):
        super(Intervention, self).__init__(f1, f2)
        
        
class Exists(Formula):
    def __init__(self, f1, f2):
        super(Exists, self).__init__(f1, f2)
        
        
class Forall(Formula):
    def __init__(self, f1, f2):
        super(Forall, self).__init__(f1, f2)


class Eq(Formula):
    def __init__(self, f1, f2):
        super(Eq, self).__init__(f1, f2)


class Gt(Formula):
    def __init__(self, f1, f2):
        super(Gt, self).__init__(f1, f2)


class GEq(Formula):
    def __init__(self, f1, f2):
        super(GEq, self).__init__(f1, f2)


class Because(Formula):
    def __init__(self, f1, f2):
        super(Because, self).__init__(f1, f2)

class Term(object):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2

    def __eq__(self, other):
        return self.t1 == other.t1 and self.t2 == other.t2 if self.__class__ == other.__class__ else False

    def __hash__(self):
        return hash((self.t1, self.t2))

    def __repr__(self):
        if isinstance(self.t1, str):
            t1 = "'"+self.t1+"'"
        else:
            t1 = str(self.t1)
        if isinstance(self.t2, str):
            t2 = "'"+self.t2+"'"
        else:
            t2 = str(self.t2)

        if isinstance(self, U):
            return "U("+str(t1)+")"
        if isinstance(self, DR):
            return "DR("+str(t1)+", +"+str(t2)+")"
        if isinstance(self, DB):
            return "DB("+str(t1)+", +"+str(t2)+")"
        if isinstance(self, Minus):
            return "Minus("+str(t1)+")"
        if isinstance(self, Sub):
            return "Sub("+str(t1)+", +"+str(t2)+")"
        if isinstance(self, Add):
            return "Add("+str(t1)+", +"+str(t2)+")"

class U(Term):
    def __init__(self, t1):
        super(U, self).__init__(t1, None)

        
class DR(Term):
    def __init__(self, t1, t2):
        super(DR, self).__init__(t1, t2)
        
        
class DB(Term):
    def __init__(self, t1, t2):
        super(DB, self).__init__(t1, t2)


class Minus(Term):
    def __init__(self, t1):
        super(Minus, self).__init__(t1, None)


class Sub(Term):
    def __init__(self, t1, t2):
        super(Sub, self).__init__(t1, t2)


class Add(Term):
    def __init__(self, t1, t2):
        super(Add, self).__init__(t1, t2)
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

