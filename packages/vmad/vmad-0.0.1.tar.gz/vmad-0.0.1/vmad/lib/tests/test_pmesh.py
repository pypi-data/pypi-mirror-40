from __future__ import print_function
from pprint import pprint
import numpy
from vmad import autooperator

from vmad.testing import BaseScalarTest
from mpi4py import MPI
from numpy.testing import assert_allclose

from pmesh.pm import RealField, ComplexField

from vmad.lib import fastpm, linalg, pmesh

def test_pmesh():
    pmesh.ParticleMesh
    with Builder() as m:
        x = m.input(pmesh.RealField('x'))
        m.output(x)


