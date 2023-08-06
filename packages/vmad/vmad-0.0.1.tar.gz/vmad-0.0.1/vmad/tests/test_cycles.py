from runtests.cycles import assert_no_backcycles
import pytest

def test_vmad3_backcycles():
    from vmad import Builder

    """ this test demonstrates building a model directly """
    with Builder() as m:
        a, b = m.input('a', 'b')

        t1 = a + a
        t2 = b + 0
        c = t1 + t2

        m.output(c=c)

    assert_no_backcycles(m, t1, t2, c, a, b)

def test_tape_backcycles():
    from vmad import Builder

    """ this test demonstrates building a model directly """
    with Builder() as m:
        a, b = m.input('a', 'b')

        t1 = a + a
        t2 = b + 0
        c = t1 + t2

        m.output(c=c)

    c, tape = m.compute('c', init=dict(a=1, b=2), return_tape=True)

    assert_no_backcycles(tape)

@pytest.mark.skip(reason="This hangs when ran with other tests")
def test_operator_backcycles():
    from vmad.core.stdlib import mul
    from vmad import Builder

    with Builder() as m:
        a, b = m.input('a', 'b')

        t1 = mul(a, b)
        c = t1 + t1
        m.output(c=c)

    assert_no_backcycles(mul)

def test_autooperator_backcycles():
    from vmad import autooperator

    @autooperator
    class mymodel:
        ain = {'a' : '*',
               'b' : '*'}
        aout = {'c' : '*'}

        def main(model, a, b, n):
            for i in range(n):
                a = add(a, a)

            t2 = add(b, 0)
            return dict(c=add(a, t2))

    assert_no_backcycles(mymodel)

