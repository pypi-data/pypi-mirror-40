from pmesh.pm import ParticleMesh

from vmad.core.symbol import Symbol
from vmad.core.operator import operator

class Field(Symbol):
    def __init__(self, self, name, model=None):
        Symbol.__init__(self, name, model)

class RealField(Field):
    @operator
    class r2c:
        ain = {'x' : 'RealField'}
        aout = {'y' : 'ComplexField'}

        def apl(node, x):
            return dict(y=x.r2c(), pm=x.pm)
        def vjp(node, _y, pm):
            _y = pm.create(mode='complex', value=_y)
            return dict(_x=_y.r2c_vjp())
        def jvp(node, x_, pm):
            x_ = pm.create(mode='real', value=x_)
            return dict(y_=x_.r2c())

class ComplexField(Field):
    @operator
    class c2r:
        ain = {'x' : 'ComplexField'}
        aout = {'y' : 'RealField'}

        def apl(node, x):
            return dict(y=x.c2r(), pm=x.pm)
        def vjp(node, _y, pm):
            _y = pm.create(mode='real', value=_y)
            return dict(_x=_y.c2r_vjp())
        def jvp(node, x_, pm):
            x_ = pm.create(mode='complex', value=x_)
            return dict(y_=x_.c2r())

    @operator
    class apply:
        ain = {'x' : 'ComplexField'}
        aout = {'y' : 'ComplexField'}

        def apl(node, x, filter, kind='wavenumber', conj_filter=None):
            if conj_filter is None:
                conj_filter = filter
            return dict(y=x.apply(filter, kind=kind), conj_filter=conj_filter)

        def vjp(node, _y, conj_filter, kind):
            return dict(_x=_y.apply(conj_filter, kind=kind))

        def jvp(node, x_, filter, kind):
            return dict(y_=x_.apply(filter, kind=kind))
