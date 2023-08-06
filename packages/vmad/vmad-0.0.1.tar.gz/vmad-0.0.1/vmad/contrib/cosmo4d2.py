from vmad import Builder, autooperator
from vmad.lib import fastpm, mpi, linalg
from pmesh.pm import ParticleMesh
from .chisquare import MPIChiSquareProblem
import numpy

@autooperator
class FastPMOperator:
    ain = [('s', '*')]
    aout = [('fs', '*')]

    def main(self, s, q, stages, cosmology, powerspectrum, pm):
        rholnk = s

        if len(stages) == 0:
            rho = fastpm.c2r(rholnk)
            rho = linalg.add(rho, 1.0)
        else:
            dx, p, f = fastpm.nbody(rholnk, q, stages, cosmology, pm)
            x = linalg.add(q, dx)
            layout = fastpm.decompose(x, pm)
            rho = fastpm.paint(x, mass=1, layout=layout, pm=pm)

        return dict(fs=rho, s=rholnk, wn=wn)

@autooperator
class NLResidualOperator:
    ain = [('s', '*'), ('fs', '*')]
    aout = [('y', '*')]
    def main(self, s, fs, d, invvar):
        r = linalg.add(fs, d * -1)
        r = linalg.mul(r, invvar ** 0.5)

        return dict(y = r)

@autooperator
class SmoothedNLResidualOperator:
    ain = [('s', '*'), ('fs', '*')]
    aout = [('y', '*')]
    def main(self, s, fs, d, invvar, scale):
        r = linalg.add(fs, d * -1)
        def tf(k):
            k2 = sum(ki ** 2 for ki in k)
            return numpy.exp(- 0.5 * k2 * scale ** 2)
        c = fastpm.r2c(r)
        c = fastpm.apply_transfer(c, tf)
        r = fastpm.c2r(c)
        r = linalg.mul(r, invvar ** 0.5)
        return dict(y = r)

@autooperator
class LNResidualOperator:
    ain = [('s', '*'), ('fs', '*')]
    aout = [('y', '*')]
    def main(self, s, fs, d, invvar):
        """ t is the truth, used only in evaluation. """
        r = linalg.add(s, d * -1)
        fac = linalg.pow(wn.Nmesh.prod(), -0.5)
        fac = linalg.mul(fac, invvar ** 0.5)
        r = linalg.mul(r, fac)
        return dict(y = r)

@autooperator
class PriorOperator:
    ain = [('s', '*'), ('fs', '*')]
    aout = [('y', '*')]
    def main(self, s, fs, invS):
        fac = linalg.pow(wn.Nmesh.prod(), -0.5)
        fac = linalg.mul(fac, invS ** 0.5)
        s_over_S = linalg.mul(s, fac)
        r = fastpm.cdot(s, s_over_S)
        return dict(y = r)

class ChiSquareProblem(MPIChiSquareProblem):
    def save(self, filename, state):
        with Builder() as m:
            s = m.input('s')
            s, fs = self.forward_operator(s)
            m.output(s=s, fs=fs)

        s, fs = m.compute(['s', 'fs'], init=dict(s=state['x']))

        from nbodykit.lab import FieldMesh

        s = FieldMesh(s)
        fs = FieldMesh(fs)

        s.attrs['y'] = state['y']
        s.attrs['nit'] = state['nit']
        s.attrs['gev'] = state['gev']
        s.attrs['fev'] = state['fev']
        s.attrs['hev'] = state['hev']

        s.save(filename, dataset='s', mode='real', )
        fs.save(filename, dataset='fs', mode='real')

