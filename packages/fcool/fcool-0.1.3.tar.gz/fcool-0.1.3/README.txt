Introduction
=============

Abstract
----------
A cool tool for functional programming. Operating Functions as in math. Type testing is implemented in an awsome way.

Keywords
----------
Functional Programming, Type Testing

Feature:

    1. function with domain, the domain can be used to type testing
    2. operator on functions, for example, f + g: x -> f(x) + g(x) where f, g,  f+g are functions
    3. to glue functions with glue function or method that can be used to define piecewise functions
    4. no 3rd part requirement 
    5. implement memoization in oo way.
    6. use MathFunction for math functions where keyword arguments are deprecated.  (new in this version)


Content
=========

Classes::

    BaseFunction -> Type (or Domain), Function
    BaseFunction: func: function (or number)
    Function: func,
              domain: Type, the definition domain of func

Functions::

    Interval(a:num, b:num) -> Type
    restrict(t:Type) -> decorator(f:function -> Function(f, t))

Constants::

    TURE, FALSE(Type) represent universal set, empty set

Grammar
=========

Basic grammar
-------------

import::

    import fcool (or from fcool import *)

Define Function with domain::

    F = Function(lambda x:x, Type(lambda x:x>2))
    F(3)

Operators on Functions::

    (F + F)(3)
    (F * F)(4)
    (2 * F)(3)

2D Functions and Types::

    f = 3     # or lambda x,y: 3
    g = lambda x,y: 2/x
    t = Type(lambda x:x<5 and isinstance(x, int)) * TRUE  # define type(domain) and functions on it
        <=> Type(lambda x, y:x<5) & Type(lambda x, y:isinstance(x, int))
    G = Function(g, t)
    F = Function(f, t)

Memoize::

   
   f.memoize()    # f is the object of BaseFunction
   f.unmemoize()  # prohibit to use memo (memo is not deleted)
   f.del_memo()   # just clear the memo, will update the memo in next time
   f.forget()     # f.del_memo() and f.unmemoize()


Advanced Grammar
----------------

Glue Functions::

    print(G.glue(F)(3,4), glue(G, F)(3,4))    # glue functions

    ID = Function(lambda x:x)
    print(ID.compose(F)(3,4))      # composition

Type testing with restrict decorator::

    @restrict(Interval(1,2))       # restriction decorator
    def f(x):
        return x

    print(f(1))
    try:
        print(f(3))
    except Exception as ex:
        print(ex)

    G=Function(lambda x:x)
    print(G(3))
    G = G | Interval(1,2)           # restriction method   
    print(G(3))