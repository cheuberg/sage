r"""
Finite residue fields

We can take the residue field of maximal ideals in the ring of integers
of number fields. We can also take the residue field of irreducible
polynomials over `GF(p)`.

EXAMPLES::

    sage: K.<a> = NumberField(x^3 - 7)                                                  # optional - sage.rings.number_field
    sage: P = K.ideal(29).factor()[0][0]                                                # optional - sage.rings.number_field
    sage: k = K.residue_field(P)                                                        # optional - sage.rings.number_field
    sage: k                                                                             # optional - sage.rings.number_field
    Residue field in abar of Fractional ideal (2*a^2 + 3*a - 10)
    sage: k.order()                                                                     # optional - sage.rings.number_field
    841

We reduce mod a prime for which the ring of integers is not
monogenic (i.e., 2 is an essential discriminant divisor)::

    sage: K.<a> = NumberField(x^3 + x^2 - 2*x + 8)                                      # optional - sage.rings.number_field
    sage: F = K.factor(2); F                                                            # optional - sage.rings.number_field
    (Fractional ideal (-1/2*a^2 + 1/2*a - 1)) * (Fractional ideal (-a^2 + 2*a - 3))
    * (Fractional ideal (3/2*a^2 - 5/2*a + 4))
    sage: F[0][0].residue_field()                                                       # optional - sage.rings.number_field
    Residue field of Fractional ideal (-1/2*a^2 + 1/2*a - 1)
    sage: F[1][0].residue_field()                                                       # optional - sage.rings.number_field
    Residue field of Fractional ideal (-a^2 + 2*a - 3)
    sage: F[2][0].residue_field()                                                       # optional - sage.rings.number_field
    Residue field of Fractional ideal (3/2*a^2 - 5/2*a + 4)

We can also form residue fields from `\ZZ`::

    sage: ZZ.residue_field(17)                                                          # optional - sage.rings.number_field
    Residue field of Integers modulo 17

And for polynomial rings over finite fields::

    sage: R.<t> = GF(5)[]
    sage: I = R.ideal(t^2 + 2)
    sage: k = ResidueField(I); k
    Residue field in tbar of Principal ideal (t^2 + 2) of
     Univariate Polynomial Ring in t over Finite Field of size 5

AUTHORS:

- David Roe (2007-10-3): initial version
- William Stein (2007-12): bug fixes
- John Cremona (2008-9): extend reduction maps to the whole valuation ring
  add support for residue fields of ZZ
- David Roe (2009-12): added support for `GF(p)(t)` and moved to new coercion
  framework.

TESTS::

    sage: K.<z> = CyclotomicField(7)                                                    # optional - sage.rings.number_field
    sage: P = K.factor(17)[0][0]                                                        # optional - sage.rings.number_field
    sage: ff = K.residue_field(P)                                                       # optional - sage.rings.number_field
    sage: loads(dumps(ff)) is ff                                                        # optional - sage.rings.number_field
    True
    sage: a = ff(z)                                                                     # optional - sage.rings.number_field
    sage: parent(a*a)                                                                   # optional - sage.rings.number_field
    Residue field in zbar of Fractional ideal (17)
    sage: TestSuite(ff).run()

Verify that :trac:`15192` has been resolved::

    sage: a.is_unit()                                                                   # optional - sage.rings.number_field
    True

    sage: R.<t> = GF(11)[]; P = R.ideal(t^3 + t + 4)
    sage: ff.<a> = ResidueField(P)
    sage: a == ff(t)
    True
    sage: parent(a*a)
    Residue field in a of Principal ideal (t^3 + t + 4) of
     Univariate Polynomial Ring in t over Finite Field of size 11

Verify that :trac:`7475` is fixed::

    sage: K = ZZ.residue_field(2)
    sage: loads(dumps(K)) is K
    True

Reducing a curve modulo a prime::

    sage: K.<s> = NumberField(x^2 + 23)                                                 # optional - sage.rings.number_field
    sage: OK = K.ring_of_integers()                                                     # optional - sage.rings.number_field
    sage: E = EllipticCurve([0,0,0,K(1),K(5)])                                          # optional - sage.rings.number_field
    sage: pp = K.factor(13)[0][0]                                                       # optional - sage.rings.number_field
    sage: Fpp = OK.residue_field(pp)                                                    # optional - sage.rings.number_field
    sage: E.base_extend(Fpp)                                                            # optional - sage.rings.number_field
    Elliptic Curve defined by y^2 = x^3 + x + 5 over
     Residue field of Fractional ideal (13, 1/2*s + 9/2)

    sage: R.<t> = GF(11)[]
    sage: P = R.ideal(t^3 + t + 4)
    sage: ff.<a> = R.residue_field(P)
    sage: E = EllipticCurve([0,0,0,R(1),R(t)])
    sage: E.base_extend(ff)
    Elliptic Curve defined by y^2 = x^3 + x + a over
     Residue field in a of Principal ideal (t^3 + t + 4) of
      Univariate Polynomial Ring in t over Finite Field of size 11

Calculating Groebner bases over various residue fields.
First over a small non-prime field::

    sage: F1.<u> = NumberField(x^6 + 6*x^5 + 124*x^4                                    # optional - sage.rings.number_field
    ....:                      + 452*x^3 + 4336*x^2 + 8200*x + 42316)
    sage: reduct_id = F1.factor(47)[0][0]                                               # optional - sage.rings.number_field
    sage: Rf = F1.residue_field(reduct_id)                                              # optional - sage.rings.number_field
    sage: type(Rf)                                                                      # optional - sage.rings.number_field
    <class 'sage.rings.finite_rings.residue_field_pari_ffelt.ResidueFiniteField_pari_ffelt_with_category'>
    sage: Rf.cardinality().factor()                                                     # optional - sage.rings.number_field
    47^3
    sage: R.<X, Y> = PolynomialRing(Rf)                                                 # optional - sage.rings.number_field
    sage: ubar = Rf(u)                                                                  # optional - sage.rings.number_field
    sage: I = ideal([ubar*X + Y]); I                                                    # optional - sage.rings.number_field
    Ideal (ubar*X + Y) of Multivariate Polynomial Ring in X, Y over
     Residue field in ubar of Fractional ideal
      (47, 517/55860*u^5 + 235/3724*u^4 + 9829/13965*u^3
            + 54106/13965*u^2 + 64517/27930*u + 755696/13965)
    sage: I.groebner_basis()                                                            # optional - sage.rings.number_field
    [X + (-19*ubar^2 - 5*ubar - 17)*Y]

And now over a large prime field::

    sage: x = ZZ['x'].0
    sage: F1.<u> = NumberField(x^2 + 6*x + 324)                                         # optional - sage.rings.number_field
    sage: reduct_id = F1.prime_above(next_prime(2^42))                                  # optional - sage.rings.number_field
    sage: Rf = F1.residue_field(reduct_id)                                              # optional - sage.rings.number_field
    sage: type(Rf)                                                                      # optional - sage.rings.number_field
    <class 'sage.rings.finite_rings.residue_field.ResidueFiniteField_prime_modn_with_category'>
    sage: Rf.cardinality().factor()                                                     # optional - sage.rings.number_field
    4398046511119
    sage: S.<X, Y, Z> = PolynomialRing(Rf, order='lex')                                 # optional - sage.rings.number_field
    sage: I = ideal([2*X - Y^2, Y + Z])                                                 # optional - sage.rings.number_field
    sage: I.groebner_basis()                                                            # optional - sage.rings.number_field
    [X + 2199023255559*Z^2, Y + Z]
    sage: S.<X, Y, Z> = PolynomialRing(Rf, order='deglex')                              # optional - sage.rings.number_field
    sage: I = ideal([2*X - Y^2, Y + Z])                                                 # optional - sage.rings.number_field
    sage: I.groebner_basis()                                                            # optional - sage.rings.number_field
    [Z^2 + 4398046511117*X, Y + Z]
"""

# *****************************************************************************
#       Copyright (C) 2007-2019 David Roe <roed@math.harvard.edu>
#                     2007      William Stein <wstein@gmail.com>
#                     2008      John Cremona
#                     2008      Robert Bradshaw
#                     2009      Nick Alexander
#                     2010      Robert L. Miller
#                     2010-2013 Simon King
#                     2010-2017 Jeroen Demeyer
#                     2012      Travis Scrimshaw
#                     2016-2021 Frédéric Chapoton
#                     2021-2022 Antonio Rojas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
# *****************************************************************************


from sage.rings.ring cimport Field
from sage.rings.integer cimport Integer
from sage.rings.rational cimport Rational
from sage.categories.homset import Hom
from sage.categories.basic import Fields, Rings
from sage.categories.pushout import AlgebraicExtensionFunctor
from sage.rings.finite_rings.integer_mod_ring import Integers
from sage.rings.integer_ring import ZZ
from sage.rings.rational_field import QQ
from sage.rings.finite_rings.finite_field_constructor import zech_log_bound, FiniteField as GF
from sage.rings.finite_rings.finite_field_prime_modn import FiniteField_prime_modn
from sage.rings.ideal import is_Ideal
from sage.rings.number_field.number_field_element_base import NumberFieldElement_base
from sage.structure.element cimport Element

from sage.rings.number_field.number_field_ideal import is_NumberFieldIdeal

from sage.modules.free_module_element import FreeModuleElement
from sage.rings.fraction_field import is_FractionField

from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.polynomial.polynomial_ring import is_PolynomialRing
from sage.rings.polynomial.polynomial_element import Polynomial

from sage.structure.factory import UniqueFactory
from sage.structure.element cimport parent
from sage.structure.richcmp cimport richcmp, richcmp_not_equal


class ResidueFieldFactory(UniqueFactory):
    """
    A factory that returns the residue class field of a prime ideal `p`
    of the ring of integers of a number field, or of a polynomial ring
    over a finite field.

    INPUT:

        - ``p`` -- a prime ideal of an order in a number field.

        - ``names`` -- the variable name for the finite field created.
          Defaults to the name of the number field variable but with
          bar placed after it.

        - ``check`` -- whether or not to check if `p` is prime.

    OUTPUT:

         - The residue field at the prime `p`.

    EXAMPLES::

        sage: K.<a> = NumberField(x^3 - 7)                                              # optional - sage.rings.number_field
        sage: P = K.ideal(29).factor()[0][0]                                            # optional - sage.rings.number_field
        sage: ResidueField(P)                                                           # optional - sage.rings.number_field
        Residue field in abar of Fractional ideal (2*a^2 + 3*a - 10)

    The result is cached::

        sage: ResidueField(P) is ResidueField(P)                                        # optional - sage.rings.number_field
        True
        sage: k = K.residue_field(P); k                                                 # optional - sage.rings.number_field
        Residue field in abar of Fractional ideal (2*a^2 + 3*a - 10)
        sage: k.order()                                                                 # optional - sage.rings.number_field
        841

    It also works for polynomial rings::

        sage: R.<t> = GF(31)[]
        sage: P = R.ideal(t^5 + 2*t + 11)
        sage: ResidueField(P)
        Residue field in tbar of Principal ideal (t^5 + 2*t + 11) of
         Univariate Polynomial Ring in t over Finite Field of size 31

        sage: ResidueField(P) is ResidueField(P)
        True
        sage: k = ResidueField(P); k.order()
        28629151

    An example where the generator of the number field doesn't
    generate the residue class field::

        sage: K.<a> = NumberField(x^3 - 875)                                            # optional - sage.rings.number_field
        sage: P = K.ideal(5).factor()[0][0]; k = K.residue_field(P); k                  # optional - sage.rings.number_field
        Residue field in abar of Fractional ideal (5, 1/25*a^2 - 2/5*a - 1)
        sage: k.polynomial()                                                            # optional - sage.rings.number_field
        abar^2 + 3*abar + 4
        sage: k.0^3 - 875                                                               # optional - sage.rings.number_field
        2

    An example where the residue class field is large but of degree 1::

        sage: K.<a> = NumberField(x^3 - 875)                                            # optional - sage.rings.number_field
        sage: P = K.ideal(2007).factor()[2][0]; k = K.residue_field(P); k               # optional - sage.rings.number_field
        Residue field of Fractional ideal (223, 1/5*a + 11)
        sage: k(a)                                                                      # optional - sage.rings.number_field
        168
        sage: k(a)^3 - 875                                                              # optional - sage.rings.number_field
        0

    And for polynomial rings::

        sage: R.<t> = GF(next_prime(2^18))[]
        sage: P = R.ideal(t - 5)
        sage: k = ResidueField(P); k
        Residue field of Principal ideal (t + 262142) of
         Univariate Polynomial Ring in t over Finite Field of size 262147
        sage: k(t)
        5

    In this example, 2 is an inessential discriminant divisor, so divides
    the index of ``ZZ[a]`` in the maximal order for all ``a``::

        sage: K.<a> = NumberField(x^3 + x^2 - 2*x + 8)                                  # optional - sage.rings.number_field
        sage: P = K.ideal(2).factor()[0][0]; P                                          # optional - sage.rings.number_field
        Fractional ideal (-1/2*a^2 + 1/2*a - 1)
        sage: F = K.residue_field(P); F                                                 # optional - sage.rings.number_field
        Residue field of Fractional ideal (-1/2*a^2 + 1/2*a - 1)
        sage: F(a)                                                                      # optional - sage.rings.number_field
        0
        sage: B = K.maximal_order().basis(); B                                          # optional - sage.rings.number_field
        [1, 1/2*a^2 + 1/2*a, a^2]
        sage: F(B[1])                                                                   # optional - sage.rings.number_field
        1
        sage: F(B[2])                                                                   # optional - sage.rings.number_field
        0
        sage: F                                                                         # optional - sage.rings.number_field
        Residue field of Fractional ideal (-1/2*a^2 + 1/2*a - 1)
        sage: F.degree()                                                                # optional - sage.rings.number_field
        1

    TESTS::

        sage: K.<a> = NumberField(polygen(QQ))                                          # optional - sage.rings.number_field
        sage: K.residue_field(K.ideal(3))                                               # optional - sage.rings.number_field
        Residue field of Fractional ideal (3)
    """
    def create_key_and_extra_args(self, p, names = None, check=True, impl=None, **kwds):
        """
        Return a tuple containing the key (uniquely defining data)
        and any extra arguments.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 7)                                          # optional - sage.rings.number_field
            sage: ResidueField(K.ideal(29).factor()[0][0])  # indirect doctest          # optional - sage.rings.number_field
            Residue field in abar of Fractional ideal (2*a^2 + 3*a - 10)
        """
        if check:
            if not is_Ideal(p):
                if isinstance(p, (int, Integer, Rational)):
                    p = ZZ.ideal(p)
                elif isinstance(p, NumberFieldElement_base):
                    if p.parent().is_field():
                        p = p.parent().ring_of_integers().ideal(p)
                    else:
                        p = p.parent().ideal(p)
                elif isinstance(p, Polynomial):
                    p = p.parent().ideal(p)
                #elif isinstance(p.parent(), FractionField_1poly_field):
                #    p = p.parent().ring_of_integers().ideal(p)
                # will eventually support other function fields here.
                else:
                    raise ValueError("p must be an ideal or element of a number field or function field.")
            if not p.is_prime():
                raise ValueError("p (%s) must be prime" % p)
            if is_PolynomialRing(p.ring()):
                if not p.ring().base_ring().is_finite():
                    raise ValueError("residue fields only supported for polynomial rings over finite fields")
                if not p.ring().base_ring().is_prime_field():
                    # neither of these will work over non-prime fields quite yet.  We should use relative finite field extensions.
                    raise NotImplementedError
            elif not (is_NumberFieldIdeal(p) or p.ring() is ZZ):
                raise NotImplementedError
        if isinstance(names, tuple):
            if names:
                names = str(names[0])
            else:
                names = None
        if names is None and p.ring() is not ZZ:
            names = '%sbar' % p.ring().fraction_field().variable_name()
        key = (p, names, impl)
        return key, kwds

    def create_object(self, version, key, **kwds):
        """
        Create the object from the key and extra arguments. This is only
        called if the object was not found in the cache.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 7)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: ResidueField(P) is ResidueField(P)  # indirect doctest                # optional - sage.rings.number_field
            True
        """
        p, names, impl = key
        pring = p.ring()

        if pring is ZZ:
            return ResidueFiniteField_prime_modn(p, names, p.gen(), None, None, None)
        if is_PolynomialRing(pring):
            K = pring.fraction_field()
            Kbase = pring.base_ring()
            f = p.gen()
            characteristic = Kbase.order()
            if f.degree() == 1 and Kbase.is_prime_field() and (impl is None or impl == 'modn'):
                return ResidueFiniteField_prime_modn(p, None, Kbase.order(), None, None, None)
            else:
                q = characteristic**(f.degree())
                if q < zech_log_bound and (impl is None or impl == 'givaro'):
                    from .residue_field_givaro import ResidueFiniteField_givaro
                    return ResidueFiniteField_givaro(p, q, names, f, None, None, None)
                elif (q % 2 == 0) and (impl is None or impl == 'ntl'):
                    from .residue_field_ntl_gf2e import ResidueFiniteField_ntl_gf2e
                    return ResidueFiniteField_ntl_gf2e(q, names, f, "poly", p, None, None, None)
                elif impl is None or impl == 'pari':
                    from .residue_field_pari_ffelt import ResidueFiniteField_pari_ffelt
                    return ResidueFiniteField_pari_ffelt(p, characteristic, names, f, None, None, None)
                else:
                    raise ValueError("unrecognized finite field type")

        # Should generalize to allowing residue fields of relative extensions to be extensions of finite fields.
        if is_NumberFieldIdeal(p):
            characteristic = p.smallest_integer()
        else: # ideal of a function field
            characteristic = pring.base_ring().characteristic()
        # Once we have function fields, we should probably have an if statement here.
        K = pring.fraction_field()
        #OK = K.maximal_order() # Need to change to p.order inside the __init__s for the residue fields.

        U, to_vs, to_order = p._p_quotient(characteristic)
        k = U.base_ring()
        R = PolynomialRing(k, names)
        n = p.residue_class_degree()
        gen_ok = False
        from sage.matrix.constructor import matrix
        try:
            x = K.gen()
            if not x:
                LL = [to_vs(1).list()] + [to_vs(x**i).list() for i in range(1,n+1)]
                M = matrix(k, n+1, n, LL)
            else:
                M = matrix(k, n+1, n, [to_vs(x**i).list() for i in range(n+1)])

            W = M.transpose().echelon_form()
            if M.rank() == n:
                PB = M.matrix_from_rows(range(n))
                gen_ok = True
                f = R((-W.column(n)).list() + [1])
        except (TypeError, ZeroDivisionError):
            pass
        if not gen_ok:
            bad = True
            for u in U: # using this iterator may not be optimal, we may get a long string of non-generators
                if u:
                    x = to_order(u)
                    M = matrix(k, n+1, n, [to_vs(x**i).list() for i in range(n+1)])
                    W = M.transpose().echelon_form()
                    if W.rank() == n:
                        f = R((-W.column(n)).list() + [1])
                        PB = M.matrix_from_rows(range(n))
                        bad = False
                        break
            assert not bad, "error -- didn't find a generator."
        # The reduction map is just x |--> k(to_vs(x) * (PB**(-1)))
        # The lifting map is just x |--> to_order(x * PB)
        # These are constructed inside the field __init__
        if n == 1:
            return ResidueFiniteField_prime_modn(p, names, p.smallest_integer(), to_vs, to_order, PB)
        else:
            q = characteristic**(f.degree())
            if q < zech_log_bound and (impl is None or impl == 'givaro'):
                from .residue_field_givaro import ResidueFiniteField_givaro
                return ResidueFiniteField_givaro(p, q, names, f, to_vs, to_order, PB)
            elif (q % 2 == 0) and (impl is None or impl == 'ntl'):
                from .residue_field_ntl_gf2e import ResidueFiniteField_ntl_gf2e
                return ResidueFiniteField_ntl_gf2e(q, names, f, "poly", p, to_vs, to_order, PB)
            elif impl is None or impl == 'pari':
                from .residue_field_pari_ffelt import ResidueFiniteField_pari_ffelt
                return ResidueFiniteField_pari_ffelt(p, characteristic, names, f, to_vs, to_order, PB)
            else:
                raise ValueError("unrecognized finite field type")

ResidueField = ResidueFieldFactory("ResidueField")

class ResidueField_generic(Field):
    """
    The class representing a generic residue field.

    EXAMPLES::

        sage: I = QQ[i].factor(2)[0][0]; I                                              # optional - sage.rings.number_field
        Fractional ideal (I + 1)
        sage: k = I.residue_field(); k                                                  # optional - sage.rings.number_field
        Residue field of Fractional ideal (I + 1)
        sage: type(k)                                                                   # optional - sage.rings.number_field
        <class 'sage.rings.finite_rings.residue_field.ResidueFiniteField_prime_modn_with_category'>

        sage: R.<t> = GF(29)[]; P = R.ideal(t^2 + 2); k.<a> = ResidueField(P); k
        Residue field in a of Principal ideal (t^2 + 2) of
         Univariate Polynomial Ring in t over Finite Field of size 29
        sage: type(k)
        <class 'sage.rings.finite_rings.residue_field_givaro.ResidueFiniteField_givaro_with_category'>
    """
    def __init__(self, p):
        """
        .. WARNING::

            This function does not call up the ``__init__`` chain, since many
            residue fields use multiple inheritance and will be calling
            ``__init__`` via their other superclass.

            If this is not the case, one should call ``Parent.__init__``
            manually for any subclass.

        INPUT:

           - ``p`` -- the prime (ideal) defining this residue field

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 17)                                         # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)    # indirect doctest                          # optional - sage.rings.number_field
            sage: F = ZZ.residue_field(17)  # indirect doctest

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field() # indirect doctest

            sage: k.category()
            Category of finite enumerated fields
            sage: F.category()
            Join of Category of finite enumerated fields
             and Category of subquotients of monoids
             and Category of quotients of semigroups

        TESTS::

            sage: TestSuite(k).run()
            sage: TestSuite(F).run()
        """
        self.p = p
        # Note: we don't call Parent.__init__ since many residue fields use multiple inheritance and will be calling __init__ via their other superclass.

    def construction(self):
        """
        Construction of this residue field.

        OUTPUT:

        An :class:`~sage.categories.pushout.AlgebraicExtensionFunctor` and the
        number field that this residue field has been obtained from.

        The residue field is determined by a prime (fractional) ideal in a
        number field. If this ideal can be coerced into a different number
        field, then the construction functor applied to this number field will
        return the corresponding residue field. See :trac:`15223`.

        EXAMPLES::

            sage: K.<z> = CyclotomicField(7)                                            # optional - sage.rings.number_field
            sage: P = K.factor(17)[0][0]                                                # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: k                                                                     # optional - sage.rings.number_field
            Residue field in zbar of Fractional ideal (17)
            sage: F, R = k.construction()                                               # optional - sage.rings.number_field
            sage: F                                                                     # optional - sage.rings.number_field
            AlgebraicExtensionFunctor
            sage: R                                                                     # optional - sage.rings.number_field
            Cyclotomic Field of order 7 and degree 6
            sage: F(R) is k                                                             # optional - sage.rings.number_field
            True
            sage: F(ZZ)                                                                 # optional - sage.rings.number_field
            Residue field of Integers modulo 17
            sage: F(CyclotomicField(49))                                                # optional - sage.rings.number_field
            Residue field in zbar of Fractional ideal (17)

        """
        return AlgebraicExtensionFunctor([self.polynomial()], [self.variable_name()], [None], residue=self.p), self.p.ring()

    def ideal(self):
        r"""
        Return the maximal ideal that this residue field is the quotient by.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 + x + 1)                                      # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P) # indirect doctest                             # optional - sage.rings.number_field
            sage: k.ideal() is P                                                        # optional - sage.rings.number_field
            True
            sage: p = next_prime(2^40); p                                               # optional - sage.rings.number_field
            1099511627791
            sage: k = K.residue_field(K.prime_above(p))                                 # optional - sage.rings.number_field
            sage: k.ideal().norm() == p                                                 # optional - sage.rings.number_field
            True

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = R.residue_field(P)
            sage: k.ideal()
            Principal ideal (t^3 + t^2 + 7) of
             Univariate Polynomial Ring in t over Finite Field of size 17
        """
        return self.p

    def _element_constructor_(self, x):
        """
        This is called after ``x`` fails to convert into ``self`` as
        abstract finite field (without considering the underlying
        number field).

        So the strategy is to try to convert into the number field,
        and then proceed to the residue field.

        .. NOTE::

            The behaviour of this method was changed in :trac:`8800`.
            Before, an error was raised if there was no coercion. Now,
            a conversion is possible even when there is no coercion.
            This is like for different finite fields.

        EXAMPLES::

            sage: from sage.rings.finite_rings.residue_field import ResidueField_generic
            sage: K.<i> = NumberField(x^2 + 1)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(-3*i - 2)                                                 # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: F = OK.residue_field(P)                                               # optional - sage.rings.number_field
            sage: ResidueField_generic._element_constructor_(F, i)                      # optional - sage.rings.number_field
            8

        With :trac:`8800`, we also have::

            sage: ResidueField_generic._element_constructor_(F, GF(13)(8))              # optional - sage.rings.number_field
            8

        Here is a test that was temporarily removed, but newly introduced
        in :trac:`8800`::

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field()
            sage: k(t)
            a
            sage: k(GF(17)(4))
            4
        """
        K = OK = self.p.ring()
        R = parent(x)
        if OK.is_field():
            OK = OK.ring_of_integers()
        else:
            K = K.fraction_field()
        if OK.has_coerce_map_from(R):
            x = OK(x)
        elif K.has_coerce_map_from(R):
            x = K(x)
        else:
            try:
                x = K(x)
            except (TypeError, ValueError):
                raise TypeError("cannot coerce %s" % type(x))
        return self(x)

    def _coerce_map_from_(self, R):
        """
        Returns ``True`` if there is a coercion map from ``R`` to ``self``.

        EXAMPLES::

            sage: K.<i> = NumberField(x^2 + 1)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(-3*i - 2)                                                 # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: F = OK.residue_field(P)                                               # optional - sage.rings.number_field
            sage: F.has_coerce_map_from(GF(13)) # indirect doctest                      # optional - sage.rings.number_field
            True

        TESTS:

        Check that :trac:`11319` is fixed::

            sage: GF(13).has_coerce_map_from(F)
            True

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field()
            sage: k.has_coerce_map_from(Qp(17)) # indirect doctest
            False
        """
        OK = self.p.ring()
        if OK.is_field():
            OK = OK.ring_of_integers()
        return self.base_ring().has_coerce_map_from(R) or OK.has_coerce_map_from(R)

    def __repr__(self):
        """
        Returns a string describing this residue field.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 7)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P); k                                             # optional - sage.rings.number_field
            Residue field in abar of Fractional ideal (2*a^2 + 3*a - 10)

            sage: F = ZZ.residue_field(17); F
            Residue field of Integers modulo 17

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field(); k  # indirect doctest
            Residue field in a of Principal ideal (t^3 + t^2 + 7) of
             Univariate Polynomial Ring in t over Finite Field of size 17
        """
        if self.p.ring() is ZZ:
            return "Residue field of Integers modulo %s"%self.p.gen()
        return "Residue field %sof %s"%('in %s '%self.gen() if self.degree() > 1 else '', self.p)

    def lift(self, x):
        """
        Returns a lift of ``x`` to the Order, returning a "polynomial" in the
        generator with coefficients between 0 and `p-1`.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 7)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: c = OK(a)                                                             # optional - sage.rings.number_field
            sage: b = k(a)                                                              # optional - sage.rings.number_field
            sage: k.lift(13*b + 5)                                                      # optional - sage.rings.number_field
            13*a + 5
            sage: k.lift(12821*b + 918)                                                 # optional - sage.rings.number_field
            3*a + 19

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field()
            sage: k.lift(a^2 + 5)
            t^2 + 5
        """
        if hasattr(self.p, "ring"):
            R = self.p.ring()
            if R.is_field():
                R = R.ring_of_integers()
            return R(x)
        else:
            return x.lift()

    def reduction_map(self):
        """
        Return the partially defined reduction map from the number
        field to this residue class field.

        EXAMPLES::

            sage: I = QQ[2^(1/3)].factor(2)[0][0]; I                                    # optional - sage.rings.number_field sage.symbolic
            Fractional ideal (a)
            sage: k = I.residue_field(); k                                              # optional - sage.rings.number_field sage.symbolic
            Residue field of Fractional ideal (a)
            sage: pi = k.reduction_map(); pi                                            # optional - sage.rings.number_field sage.symbolic
            Partially defined reduction map:
              From: Number Field in a with defining polynomial x^3 - 2
                    with a = 1.259921049894873?
              To:   Residue field of Fractional ideal (a)
            sage: pi.domain()                                                           # optional - sage.rings.number_field sage.symbolic
            Number Field in a with defining polynomial x^3 - 2 with a = 1.259921049894873?
            sage: pi.codomain()                                                         # optional - sage.rings.number_field sage.symbolic
            Residue field of Fractional ideal (a)

            sage: K.<a> = NumberField(x^3 + x^2 - 2*x + 32)                             # optional - sage.rings.number_field
            sage: F = K.factor(2)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: F.reduction_map().domain()                                            # optional - sage.rings.number_field
            Number Field in a with defining polynomial x^3 + x^2 - 2*x + 32
            sage: K.<a> = NumberField(x^3 + 128)                                        # optional - sage.rings.number_field
            sage: F = K.factor(2)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: F.reduction_map().codomain()                                          # optional - sage.rings.number_field
            Residue field of Fractional ideal (1/4*a)

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field(); f = k.reduction_map(); f
            Partially defined reduction map:
              From: Fraction Field of Univariate Polynomial Ring in t
                    over Finite Field of size 17
              To:   Residue field in a of Principal ideal (t^3 + t^2 + 7) of
                    Univariate Polynomial Ring in t over Finite Field of size 17
            sage: f(1/t)
            12*a^2 + 12*a
        """
        return self.convert_map_from(self.p.ring().fraction_field())

    def lift_map(self):
        """
        Returns the standard map from this residue field up to the ring of
        integers lifting the canonical projection.

        EXAMPLES::

            sage: I = QQ[3^(1/3)].factor(5)[1][0]; I                                    # optional - sage.rings.number_field sage.symbolic
            Fractional ideal (a - 2)
            sage: k = I.residue_field(); k                                              # optional - sage.rings.number_field sage.symbolic
            Residue field of Fractional ideal (a - 2)
            sage: f = k.lift_map(); f                                                   # optional - sage.rings.number_field sage.symbolic
            Lifting map:
              From: Residue field of Fractional ideal (a - 2)
              To:   Maximal Order in Number Field in a with defining polynomial x^3 - 3
                    with a = 1.442249570307409?
            sage: f.domain()                                                            # optional - sage.rings.number_field sage.symbolic
            Residue field of Fractional ideal (a - 2)
            sage: f.codomain()                                                          # optional - sage.rings.number_field sage.symbolic
            Maximal Order in Number Field in a with defining polynomial x^3 - 3
             with a = 1.442249570307409?
            sage: f(k.0)                                                                # optional - sage.rings.number_field sage.symbolic
            1

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field()
            sage: f = k.lift_map(); f
            (map internal to coercion system -- copy before use)
            Lifting map:
              From: Residue field in a of Principal ideal (t^3 + t^2 + 7) of
                    Univariate Polynomial Ring in t over Finite Field of size 17
              To:   Univariate Polynomial Ring in t over Finite Field of size 17
            sage: f(a^2 + 5)
            t^2 + 5
        """
        OK = self.p.ring()
        if OK.is_field():
            OK = OK.ring_of_integers()
        return self._internal_coerce_map_from(OK).section()

    def _richcmp_(self, x, op):
        """
        Compares two residue fields: they are equal iff the primes
        defining them are equal and they have the same variable name.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 11)                                                                 # optional - sage.rings.number_field
            sage: F = K.ideal(37).factor(); F                                                                   # optional - sage.rings.number_field
            (Fractional ideal (37, a + 9)) * (Fractional ideal (37, a + 12)) * (Fractional ideal (-2*a + 5))
            sage: k = K.residue_field(F[0][0])                                                                  # optional - sage.rings.number_field
            sage: l = K.residue_field(F[1][0])                                                                  # optional - sage.rings.number_field
            sage: k == l                                                                                        # optional - sage.rings.number_field
            False

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field()
            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 11)
            sage: l.<b> = P.residue_field()
            sage: k == l
            False
            sage: ll.<c> = P.residue_field()
            sage: ll == l
            False
        """
        if not isinstance(x, ResidueField_generic):
            return NotImplemented
        lp = self.p
        rp = x.p
        if lp != rp:
            return richcmp_not_equal(lp, rp, op)
        return richcmp(self.variable_name(), x.variable_name(), op)

    def __hash__(self):
        r"""
        Return the hash of ``self``.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 + x + 1)                                      # optional - sage.rings.number_field
            sage: hash(K.residue_field(K.prime_above(17)))    # random                  # optional - sage.rings.number_field
            -6463132282686559142
            sage: hash(K.residue_field(K.prime_above(2^60)))  # random                  # optional - sage.rings.number_field
            -6939519969600666586
            sage: R.<t> = GF(13)[]
            sage: hash(R.residue_field(t + 2)) # random
            3521289879659800254
        """
        return 1 + hash(self.ideal())

cdef class ReductionMap(Map):
    """
    A reduction map from a (subset) of a number field or function field to
    this residue class field.

    It will be defined on those elements of the field with non-negative
    valuation at the specified prime.

    EXAMPLES::

        sage: I = QQ[sqrt(17)].factor(5)[0][0]; I                                       # optional - sage.rings.number_field sage.symbolic
        Fractional ideal (5)
        sage: k = I.residue_field(); k                                                  # optional - sage.rings.number_field sage.symbolic
        Residue field in sqrt17bar of Fractional ideal (5)
        sage: R = k.reduction_map(); R                                                  # optional - sage.rings.number_field sage.symbolic
        Partially defined reduction map:
          From: Number Field in sqrt17 with defining polynomial x^2 - 17
                with sqrt17 = 4.123105625617660?
          To:   Residue field in sqrt17bar of Fractional ideal (5)

        sage: R.<t> = GF(next_prime(2^20))[]; P = R.ideal(t^2 + t + 1)
        sage: k = P.residue_field()
        sage: k.reduction_map()
        Partially defined reduction map:
          From: Fraction Field of
                Univariate Polynomial Ring in t over Finite Field of size 1048583
          To:   Residue field in tbar of Principal ideal (t^2 + t + 1) of
                Univariate Polynomial Ring in t over Finite Field of size 1048583
    """
    def __init__(self, K, F, to_vs, to_order, PB, PBinv):
        """
        Create a reduction map.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 + x^2 - 2*x + 8)                              # optional - sage.rings.number_field
            sage: F = K.factor(2)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: F.reduction_map()                                                     # optional - sage.rings.number_field
            Partially defined reduction map:
              From: Number Field in a with defining polynomial x^3 + x^2 - 2*x + 8
              To:   Residue field of Fractional ideal (-1/2*a^2 + 1/2*a - 1)

            sage: K.<theta_5> = CyclotomicField(5)                                      # optional - sage.rings.number_field
            sage: F = K.factor(7)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: F.reduction_map()                                                     # optional - sage.rings.number_field
            Partially defined reduction map:
              From: Cyclotomic Field of order 5 and degree 4
              To:   Residue field in theta_5bar of Fractional ideal (7)

            sage: R.<t> = GF(2)[]; P = R.ideal(t^7 + t^6 + t^5 + t^4 + 1)
            sage: k = P.residue_field()
            sage: k.reduction_map()
            Partially defined reduction map:
              From: Fraction Field of
                    Univariate Polynomial Ring in t over Finite Field of size 2 (using GF2X)
              To:   Residue field in tbar of Principal ideal (t^7 + t^6 + t^5 + t^4 + 1) of
                    Univariate Polynomial Ring in t over Finite Field of size 2 (using GF2X)
            sage: type(k)
            <class 'sage.rings.finite_rings.residue_field_givaro.ResidueFiniteField_givaro_with_category'>
        """
        self._K = K
        self._F = F   # finite field
        self._to_vs = to_vs
        self._PBinv = PBinv
        self._to_order = to_order # used for lift
        self._PB = PB # used for lift
        from sage.categories.sets_with_partial_maps import SetsWithPartialMaps
        self._repr_type_str = "Partially defined reduction"
        Map.__init__(self, Hom(K, F, SetsWithPartialMaps()))

    cdef dict _extra_slots(self):
        """
        Helper for copying and pickling.

        EXAMPLES::

            sage: K.<a> = NumberField(x^2 + 1)                                          # optional - sage.rings.number_field
            sage: F = K.factor(2)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: r = F.reduction_map()                                                 # optional - sage.rings.number_field
            sage: cr = copy(r) # indirect doctest                                       # optional - sage.rings.number_field
            sage: cr                                                                    # optional - sage.rings.number_field
            Partially defined reduction map:
              From: Number Field in a with defining polynomial x^2 + 1
              To:   Residue field of Fractional ideal (a + 1)
            sage: cr == r      # todo: comparison not implemented                       # optional - sage.rings.number_field
            True
            sage: r(2 + a) == cr(2 + a)                                                 # optional - sage.rings.number_field
            True
        """
        slots = Map._extra_slots(self)
        slots['_K'] = self._K
        slots['_F'] = self._F
        slots['_to_vs'] = self._to_vs
        slots['_PBinv'] = self._PBinv
        slots['_to_order'] = self._to_order
        slots['_PB'] = self._PB
        slots['_section'] = self._section
        return slots

    cdef _update_slots(self, dict _slots):
        """
        Helper for copying and pickling.

        EXAMPLES::

            sage: K.<a> = NumberField(x^2 + 1)                                          # optional - sage.rings.number_field
            sage: F = K.factor(2)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: r = F.reduction_map()                                                 # optional - sage.rings.number_field
            sage: cr = copy(r) # indirect doctest                                       # optional - sage.rings.number_field
            sage: cr                                                                    # optional - sage.rings.number_field
            Partially defined reduction map:
              From: Number Field in a with defining polynomial x^2 + 1
              To:   Residue field of Fractional ideal (a + 1)
            sage: cr == r      # todo: comparison not implemented                       # optional - sage.rings.number_field
            True
            sage: r(2 + a) == cr(2 + a)                                                 # optional - sage.rings.number_field
            True
        """
        Map._update_slots(self, _slots)
        self._K = _slots['_K']
        self._F = _slots['_F']
        self._to_vs = _slots['_to_vs']
        self._PBinv = _slots['_PBinv']
        self._to_order = _slots['_to_order']
        self._PB = _slots['_PB']
        self._section = _slots['_section']

    cpdef Element _call_(self, x):
        """
        Apply this reduction map to an element that coerces into the global
        field.

        If ``x`` doesn't map because it has negative valuation, then a
        ``ZeroDivisionError`` exception is raised.

        EXAMPLES::

            sage: K.<a> = NumberField(x^2 + 1)                                          # optional - sage.rings.number_field
            sage: F = K.factor(2)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: r = F.reduction_map(); r                                              # optional - sage.rings.number_field
            Partially defined reduction map:
              From: Number Field in a with defining polynomial x^2 + 1
              To:   Residue field of Fractional ideal (a + 1)

        We test that calling the function also works after copying::

            sage: r = copy(r)                                                           # optional - sage.rings.number_field
            sage: r(2 + a) # indirect doctest                                           # optional - sage.rings.number_field
            1
            sage: r(a/2)                                                                # optional - sage.rings.number_field
            Traceback (most recent call last):
            ...
            ZeroDivisionError: Cannot reduce field element 1/2*a
            modulo Fractional ideal (a + 1): it has negative valuation

            sage: R.<t> = GF(2)[]; h = t^5 + t^2 + 1
            sage: k.<a> = R.residue_field(h)
            sage: K = R.fraction_field()
            sage: f = k.convert_map_from(K)
            sage: type(f)
            <class 'sage.rings.finite_rings.residue_field.ReductionMap'>
            sage: f(1/t)
            a^4 + a
            sage: f(1/h)
            Traceback (most recent call last):
            ...
            ZeroDivisionError: division by zero in finite field

        An example to show that the issue raised in :trac:`1951`
        has been fixed::

            sage: K.<i> = NumberField(x^2 + 1)                                          # optional - sage.rings.number_field
            sage: P1, P2 = [g[0] for g in K.factor(5)]; P1, P2                          # optional - sage.rings.number_field
            (Fractional ideal (-i - 2), Fractional ideal (2*i + 1))
            sage: a = 1/(1+2*i)                                                         # optional - sage.rings.number_field
            sage: F1, F2 = [g.residue_field() for g in [P1,P2]]; F1, F2                 # optional - sage.rings.number_field
            (Residue field of Fractional ideal (-i - 2),
             Residue field of Fractional ideal (2*i + 1))
            sage: a.valuation(P1)                                                       # optional - sage.rings.number_field
            0
            sage: F1(i/7)                                                               # optional - sage.rings.number_field
            4
            sage: F1(a)                                                                 # optional - sage.rings.number_field
            3
            sage: a.valuation(P2)                                                       # optional - sage.rings.number_field
            -1
            sage: F2(a)                                                                 # optional - sage.rings.number_field
            Traceback (most recent call last):
            ...
            ZeroDivisionError: Cannot reduce field element -2/5*i + 1/5
            modulo Fractional ideal (2*i + 1): it has negative valuation
        """
        # The reduction map is just x |--> F(to_vs(x) * (PB**(-1))) if
        # either x is integral or the denominator of x is coprime to
        # p; otherwise we work harder.
        p = self._F.p

        # Special code for residue fields of Q:
        if self._K is QQ:
            try:
                return FiniteField_prime_modn._element_constructor_(self._F, x)
            except ZeroDivisionError:
                raise ZeroDivisionError("Cannot reduce rational %s modulo %s: it has negative valuation" % (x, p.gen()))
        elif is_FractionField(self._K):
            p = p.gen()
            if p.degree() == 1:
                return self._F((x.numerator() % p)[0] / (x.denominator() % p)[0])
            else:
                return self._F((x.numerator() % p).list()) / self._F((x.denominator() % p).list())

        try:
            return self._F(self._to_vs(x) * self._PBinv)
        except Exception:
            pass

        # Now we do have to work harder...below this point we handle
        # cases which failed before trac 1951 was fixed.
        R = self._K.ring_of_integers()
        dx = R(x.denominator())
        nx = R(dx*x)
        vnx = nx.valuation(p)
        vdx = dx.valuation(p)
        if vnx > vdx:
            return self(0)
        if vnx < vdx:
            raise ZeroDivisionError("Cannot reduce field element %s modulo %s: it has negative valuation" % (x, p))

        a = self._K.uniformizer(p,'negative') ** vnx
        nx /= a
        dx /= a
        # Assertions for debugging!
        # assert nx.valuation(p) == 0 and dx.valuation(p) == 0 and x == nx/dx
        # assert nx.is_integral() and dx.is_integral()
        # print("nx = ",nx,"; dx = ",dx, ": recursing")

        # NB at this point nx and dx are in the ring of integers and
        # both are p-units.  Recursion is now safe, since integral
        # elements will not cause further recursion; and neither
        # self(nx) nor self(dx) will be 0 since nx, dx are p-units.
        return self(nx)/self(dx)

    def section(self):
        """
        Computes a section of the map, namely a map that lifts elements of the
        residue field to elements of the field.

        EXAMPLES::

            sage: K.<a> = NumberField(x^5 - 5*x + 2)                                    # optional - sage.rings.number_field
            sage: P = K.ideal(47).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: f = k.convert_map_from(K)                                             # optional - sage.rings.number_field
            sage: s = f.section(); s                                                    # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of
                    Fractional ideal (-14*a^4 + 24*a^3 + 26*a^2 - 58*a + 15)
              To:   Number Field in a with defining polynomial x^5 - 5*x + 2
            sage: s(k.gen())                                                            # optional - sage.rings.number_field
            a
            sage: L.<b> = NumberField(x^5 + 17*x + 1)                                   # optional - sage.rings.number_field
            sage: P = L.factor(53)[0][0]                                                # optional - sage.rings.number_field
            sage: l = L.residue_field(P)                                                # optional - sage.rings.number_field
            sage: g = l.convert_map_from(L)                                             # optional - sage.rings.number_field
            sage: s = g.section(); s                                                    # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in bbar of Fractional ideal (53, b^2 + 23*b + 8)
              To:   Number Field in b with defining polynomial x^5 + 17*x + 1
            sage: s(l.gen()).parent()                                                   # optional - sage.rings.number_field
            Number Field in b with defining polynomial x^5 + 17*x + 1

            sage: R.<t> = GF(2)[]; h = t^5 + t^2 + 1
            sage: k.<a> = R.residue_field(h)
            sage: K = R.fraction_field()
            sage: f = k.convert_map_from(K)
            sage: f.section()
            Lifting map:
              From: Residue field in a of Principal ideal (t^5 + t^2 + 1) of
                    Univariate Polynomial Ring in t over Finite Field of size 2 (using GF2X)
              To:   Fraction Field of
                    Univariate Polynomial Ring in t over Finite Field of size 2 (using GF2X)
        """
        if self._section is None:
            self._section = LiftingMap(self, self._to_order, self._PB)
        return self._section


cdef class ResidueFieldHomomorphism_global(RingHomomorphism):
    """
    The class representing a homomorphism from the order of a number
    field or function field to the residue field at a given prime.

    EXAMPLES::

        sage: K.<a> = NumberField(x^3 - 7)                                              # optional - sage.rings.number_field
        sage: P  = K.ideal(29).factor()[0][0]                                           # optional - sage.rings.number_field
        sage: k  = K.residue_field(P)                                                   # optional - sage.rings.number_field
        sage: OK = K.maximal_order()                                                    # optional - sage.rings.number_field
        sage: abar = k(OK.1); abar                                                      # optional - sage.rings.number_field
        abar
        sage: (1+abar)^179                                                              # optional - sage.rings.number_field
        24*abar + 12

        sage: phi = k.coerce_map_from(OK); phi                                          # optional - sage.rings.number_field
        Ring morphism:
          From: Maximal Order in Number Field in a with defining polynomial x^3 - 7
          To:   Residue field in abar of Fractional ideal (2*a^2 + 3*a - 10)
        sage: phi in Hom(OK,k)                                                          # optional - sage.rings.number_field
        True
        sage: phi(OK.1)                                                                 # optional - sage.rings.number_field
        abar

        sage: R.<t> = GF(19)[]; P = R.ideal(t^2 + 5)
        sage: k.<a> = R.residue_field(P)
        sage: f = k.coerce_map_from(R); f
        Ring morphism:
          From: Univariate Polynomial Ring in t over Finite Field of size 19
          To:   Residue field in a of Principal ideal (t^2 + 5) of
                Univariate Polynomial Ring in t over Finite Field of size 19
    """
    def __init__(self, K, F, to_vs, to_order, PB, PBinv):
        """
        Initialize ``self``.

        INPUT:

        - ``k`` -- The residue field that is the codomain of this morphism

        - ``p`` -- The prime ideal defining this residue field

        - ``im_gen`` -- The image of the generator of the number field

        EXAMPLES:

        We create a residue field homomorphism::

            sage: K.<theta> = CyclotomicField(5)                                        # optional - sage.rings.number_field
            sage: P = K.factor(7)[0][0]                                                 # optional - sage.rings.number_field
            sage: P.residue_class_degree()                                              # optional - sage.rings.number_field
            4
            sage: kk.<a> = P.residue_field(); kk                                        # optional - sage.rings.number_field
            Residue field in a of Fractional ideal (7)
            sage: phi = kk.coerce_map_from(K.maximal_order()); phi                      # optional - sage.rings.number_field
            Ring morphism:
              From: Maximal Order in Cyclotomic Field of order 5 and degree 4
              To:   Residue field in a of Fractional ideal (7)
            sage: type(phi)                                                             # optional - sage.rings.number_field
            <class 'sage.rings.finite_rings.residue_field.ResidueFieldHomomorphism_global'>

            sage: R.<t> = GF(2)[]; P = R.ideal(t^7 + t^6 + t^5 + t^4 + 1)
            sage: k = P.residue_field(); f = k.coerce_map_from(R)
            sage: f(t^10)
            tbar^6 + tbar^3 + tbar^2
        """
        self._K = K
        self._F = F   # finite field
        self._to_vs = to_vs
        self._PBinv = PBinv
        self._PB = PB # used for lift
        self._to_order = to_order # used for lift
        self._repr_type_str = "Reduction"
        RingHomomorphism.__init__(self, Hom(K,F))

    cdef dict _extra_slots(self):
        """
        Helper for copying and pickling.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - x + 8)                                      # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: phi = k.coerce_map_from(OK)                                           # optional - sage.rings.number_field
            sage: psi = copy(phi); psi    # indirect doctest                            # optional - sage.rings.number_field
            Ring morphism:
              From: Maximal Order in Number Field in a with defining polynomial x^3 - x + 8
              To:   Residue field in abar of Fractional ideal (29)
            sage: psi == phi   # todo: comparison not implemented                       # optional - sage.rings.number_field
            True
            sage: psi(OK.an_element()) == phi(OK.an_element())                          # optional - sage.rings.number_field
            True
        """
        slots = RingHomomorphism._extra_slots(self)
        slots['_K'] = self._K
        slots['_F'] = self._F
        slots['_to_vs'] = self._to_vs
        slots['_PBinv'] = self._PBinv
        slots['_to_order'] = self._to_order
        slots['_PB'] = self._PB
        slots['_section'] = self._section
        return slots

    cdef _update_slots(self, dict _slots):
        """
        Helper for copying and pickling.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - x + 8)                                      # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: phi = k.coerce_map_from(OK)                                           # optional - sage.rings.number_field
            sage: psi = copy(phi); psi    # indirect doctest                            # optional - sage.rings.number_field
            Ring morphism:
              From: Maximal Order in Number Field in a with defining polynomial x^3 - x + 8
              To:   Residue field in abar of Fractional ideal (29)
            sage: psi == phi   # todo: comparison not implemented                       # optional - sage.rings.number_field
            True
            sage: psi(OK.an_element()) == phi(OK.an_element())                          # optional - sage.rings.number_field
            True
        """
        RingHomomorphism._update_slots(self, _slots)
        self._K = _slots['_K']
        self._F = _slots['_F']
        self._to_vs = _slots['_to_vs']
        self._PBinv = _slots['_PBinv']
        self._to_order = _slots['_to_order']
        self._PB = _slots['_PB']
        self._section = _slots['_section']

    cpdef Element _call_(self, x):
        """
        Applies this morphism to an element.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - x + 8)                                      # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: k.coerce_map_from(OK)(OK(a)^7) # indirect doctest                     # optional - sage.rings.number_field
            13*abar^2 + 7*abar + 21

            sage: R.<t> = GF(next_prime(2^18))[]; P = R.ideal(t - 71)
            sage: k = ResidueField(P); f = k.coerce_map_from(R); f
            Ring morphism:
              From: Univariate Polynomial Ring in t over Finite Field of size 262147
              To:   Residue field of Principal ideal (t + 262076) of
                    Univariate Polynomial Ring in t over Finite Field of size 262147
            sage: f(t^2)
            5041
        """
        # The reduction map is just x |--> F(to_vs(x) * (PB**(-1))) if
        # either x is integral or the denominator of x is coprime to
        # p; otherwise we work harder.

        # No special code for residue fields of Z, since we just use the normal reduction map to GF(p)
        if self._K is ZZ:
            return self._F(x)
        if is_PolynomialRing(self._K):
            p = self._F.p.gen()
            if p.degree() == 1:
                return self._F((x % p)[0])
            else:
                return self._F((x % p).list())
        return self._F(self._to_vs(x) * self._PBinv)
        #return self._F(self._to_vs(x.parent().fraction_field()(x)) * self._PBinv)

    def section(self):
        """
        Computes a section of the map, namely a map that lifts elements of
        the residue field to elements of the ring of integers.

        EXAMPLES::

            sage: K.<a> = NumberField(x^5 - 5*x + 2)                                    # optional - sage.rings.number_field
            sage: P = K.ideal(47).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: f = k.coerce_map_from(K.ring_of_integers())                           # optional - sage.rings.number_field
            sage: s = f.section(); s                                                    # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of
                    Fractional ideal (-14*a^4 + 24*a^3 + 26*a^2 - 58*a + 15)
              To:   Maximal Order in Number Field in a with defining polynomial x^5 - 5*x + 2
            sage: s(k.gen())
            a
            sage: L.<b> = NumberField(x^5 + 17*x + 1)                                   # optional - sage.rings.number_field
            sage: P = L.factor(53)[0][0]                                                # optional - sage.rings.number_field
            sage: l = L.residue_field(P)                                                # optional - sage.rings.number_field
            sage: g = l.coerce_map_from(L.ring_of_integers())                           # optional - sage.rings.number_field
            sage: s = g.section(); s                                                    # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in bbar of Fractional ideal (53, b^2 + 23*b + 8)
              To:   Maximal Order in Number Field in b
                    with defining polynomial x^5 + 17*x + 1
            sage: s(l.gen()).parent()                                                   # optional - sage.rings.number_field
            Maximal Order in Number Field in b with defining polynomial x^5 + 17*x + 1

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field()
            sage: f = k.coerce_map_from(R)
            sage: f.section()
            (map internal to coercion system -- copy before use)
            Lifting map:
              From: Residue field in a of Principal ideal (t^3 + t^2 + 7) of
                    Univariate Polynomial Ring in t over Finite Field of size 17
              To:   Univariate Polynomial Ring in t over Finite Field of size 17
        """
        if self._section is None:
            self._section = LiftingMap(self, self._to_order, self._PB)
        return self._section

    def lift(self, x):
        """
        Returns a lift of ``x`` to the Order, returning a "polynomial" in
        the generator with coefficients between 0 and `p-1`.

        EXAMPLES::

            sage: K.<a> = NumberField(x^3 - 7)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[0][0]                                        # optional - sage.rings.number_field
            sage: k = K.residue_field(P)                                                # optional - sage.rings.number_field
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: f = k.coerce_map_from(OK)                                             # optional - sage.rings.number_field
            sage: c = OK(a)                                                             # optional - sage.rings.number_field
            sage: b = k(a)                                                              # optional - sage.rings.number_field
            sage: f.lift(13*b + 5)                                                      # optional - sage.rings.number_field
            13*a + 5
            sage: f.lift(12821*b + 918)                                                 # optional - sage.rings.number_field
            3*a + 19

            sage: R.<t> = GF(17)[]; P = R.ideal(t^3 + t^2 + 7)
            sage: k.<a> = P.residue_field(); f = k.coerce_map_from(R)
            sage: f.lift(a^2 + 5*a + 1)
            t^2 + 5*t + 1
            sage: f(f.lift(a^2 + 5*a + 1)) == a^2 + 5*a + 1
            True
        """
        if self.domain() is ZZ:
            return x.lift()
        else:
            return self.section()(x)

cdef class LiftingMap(Section):
    """
    Lifting map from residue class field to number field.

    EXAMPLES::

        sage: K.<a> = NumberField(x^3 + 2)                                              # optional - sage.rings.number_field
        sage: F = K.factor(5)[0][0].residue_field()                                     # optional - sage.rings.number_field
        sage: F.degree()                                                                # optional - sage.rings.number_field
        2
        sage: L = F.lift_map(); L                                                       # optional - sage.rings.number_field
        Lifting map:
          From: Residue field in abar of Fractional ideal (a^2 + 2*a - 1)
          To:   Maximal Order in Number Field in a with defining polynomial x^3 + 2
        sage: L(F.0^2)                                                                  # optional - sage.rings.number_field
        3*a + 1
        sage: L(3*a + 1) == F.0^2                                                       # optional - sage.rings.number_field
        True

        sage: R.<t> = GF(13)[]
        sage: P = R.ideal(8*t^12 + 9*t^11 + 11*t^10 + 2*t^9 + 11*t^8
        ....:             + 3*t^7 + 12*t^6 + t^4 + 7*t^3 + 5*t^2 + 12*t + 1)
        sage: k.<a> = P.residue_field()
        sage: k.lift_map()
        Lifting map:
          From: Residue field in a of Principal ideal (t^12 + 6*t^11 + 3*t^10
                + 10*t^9 + 3*t^8 + 2*t^7 + 8*t^6 + 5*t^4 + 9*t^3 + 12*t^2 + 8*t + 5) of
                Univariate Polynomial Ring in t over Finite Field of size 13
          To:   Univariate Polynomial Ring in t over Finite Field of size 13
    """
    def __init__(self, reduction, to_order, PB):
        """
        Create a lifting map.

        EXAMPLES::

            sage: K.<theta_5> = CyclotomicField(5)                                      # optional - sage.rings.number_field
            sage: F = K.factor(7)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: F.lift_map()                                                          # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in theta_5bar of Fractional ideal (7)
              To:   Maximal Order in Cyclotomic Field of order 5 and degree 4

            sage: K.<a> = NumberField(x^5 + 2)                                          # optional - sage.rings.number_field
            sage: F = K.factor(7)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: L = F.lift_map(); L                                                   # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of Fractional ideal (2*a^4 - a^3 + 4*a^2 - 2*a + 1)
              To:   Maximal Order in Number Field in a
                    with defining polynomial x^5 + 2
            sage: L.domain()                                                            # optional - sage.rings.number_field
            Residue field in abar of Fractional ideal (2*a^4 - a^3 + 4*a^2 - 2*a + 1)

            sage: K.<a> = CyclotomicField(7)                                            # optional - sage.rings.number_field
            sage: F = K.factor(5)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: L = F.lift_map(); L                                                   # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of Fractional ideal (5)
              To:   Maximal Order in Cyclotomic Field of order 7 and degree 6
            sage: L.codomain()                                                          # optional - sage.rings.number_field
            Maximal Order in Cyclotomic Field of order 7 and degree 6

            sage: R.<t> = GF(2)[]; h = t^5 + t^2 + 1
            sage: k.<a> = R.residue_field(h)
            sage: K = R.fraction_field()
            sage: L = k.lift_map(); L.codomain()
            Univariate Polynomial Ring in t over Finite Field of size 2 (using GF2X)
        """
        self._K = reduction._K
        self._F = reduction._F   # finite field
        self._to_order = to_order
        self._PB = PB
        Section.__init__(self, reduction)

    cdef dict _extra_slots(self):
        """
        Helper for copying and pickling.

        EXAMPLES::

            sage: K.<a> = CyclotomicField(7)                                            # optional - sage.rings.number_field
            sage: F = K.factor(5)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: phi = F.lift_map()                                                    # optional - sage.rings.number_field
            sage: psi = copy(phi); psi   # indirect doctest                             # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of Fractional ideal (5)
              To:   Maximal Order in Cyclotomic Field of order 7 and degree 6
            sage: psi == phi             # todo: comparison not implemented             # optional - sage.rings.number_field
            False
            sage: phi(F.0) == psi(F.0)                                                  # optional - sage.rings.number_field
            True
        """
        slots = Section._extra_slots(self)
        slots['_K'] = self._K
        slots['_F'] = self._F
        slots['_to_order'] = self._to_order
        slots['_PB'] = self._PB
        return slots

    cdef _update_slots(self, dict _slots):
        """
        Helper for copying and pickling.

        EXAMPLES::

            sage: K.<a> = CyclotomicField(7)                                            # optional - sage.rings.number_field
            sage: F = K.factor(5)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: phi = F.lift_map()                                                    # optional - sage.rings.number_field
            sage: psi = copy(phi); psi   # indirect doctest                             # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of Fractional ideal (5)
              To:   Maximal Order in Cyclotomic Field of order 7 and degree 6
            sage: psi == phi             # todo: comparison not implemented             # optional - sage.rings.number_field
            False
            sage: phi(F.0) == psi(F.0)                                                  # optional - sage.rings.number_field
            True
        """
        Section._update_slots(self, _slots)
        self._K = _slots['_K']
        self._F = _slots['_F']
        self._to_order = _slots['_to_order']
        self._PB = _slots['_PB']

    cpdef Element _call_(self, x):
        """
        Lift from this residue class field to the number field.

        EXAMPLES::

            sage: K.<a> = CyclotomicField(7)                                            # optional - sage.rings.number_field
            sage: F = K.factor(5)[0][0].residue_field()                                 # optional - sage.rings.number_field
            sage: L = F.lift_map(); L                                                   # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in abar of Fractional ideal (5)
              To:   Maximal Order in Cyclotomic Field of order 7 and degree 6
            sage: L(F.0) # indirect doctest                                             # optional - sage.rings.number_field
            a
            sage: F(a)                                                                  # optional - sage.rings.number_field
            abar

            sage: R.<t> = GF(2)[]; h = t^5 + t^2 + 1
            sage: k.<a> = R.residue_field(h)
            sage: K = R.fraction_field()
            sage: f = k.lift_map()
            sage: f(a^2)
            t^2
            sage: f(a^6)
            t^3 + t
        """
        if self._K is QQ or self._K is ZZ:
            return self._K(x.lift())  # x.lift() is in ZZ
        elif is_FractionField(self._K):
            if self._F.p.degree() == 1:
                return self._K(self._K.ring_of_integers()(x))
            else:
                return self._K(self._K.ring_of_integers()(x.polynomial().list()))
        elif is_PolynomialRing(self._K):
            return self._K(x.polynomial().list())
        # Else the lifting map is just x |--> to_order(x * PB)
        x = self._F(x)
        v = x.polynomial().padded_list(self._F.degree())
        ans = self._to_order(self._PB.linear_combination_of_rows(v))
        if ans.parent() is self._K:
            return ans
        else:
            return self._K(ans)

    def _repr_type(self):
        """
        EXAMPLES::

            sage: K.<theta_12> = CyclotomicField(12)                                    # optional - sage.rings.number_field
            sage: F.<tmod> = K.factor(7)[0][0].residue_field()                          # optional - sage.rings.number_field
            sage: F.lift_map() #indirect doctest                                        # optional - sage.rings.number_field
            Lifting map:
              From: Residue field in tmod of Fractional ideal (theta_12^2 + 2)
              To:   Maximal Order in Cyclotomic Field of order 12 and degree 4
        """
        return "Lifting"

class ResidueFiniteField_prime_modn(ResidueField_generic, FiniteField_prime_modn):
    """
    The class representing residue fields of number fields that have
    prime order.

    EXAMPLES::

        sage: R.<x> = QQ[]
        sage: K.<a> = NumberField(x^3 - 7)                                              # optional - sage.rings.number_field
        sage: P = K.ideal(29).factor()[1][0]                                            # optional - sage.rings.number_field
        sage: k = ResidueField(P)                                                       # optional - sage.rings.number_field
        sage: k                                                                         # optional - sage.rings.number_field
        Residue field of Fractional ideal (-a^2 - 2*a - 2)
        sage: k.order()                                                                 # optional - sage.rings.number_field
        29
        sage: OK = K.maximal_order()                                                    # optional - sage.rings.number_field
        sage: c = OK(a)                                                                 # optional - sage.rings.number_field
        sage: b = k(a)                                                                  # optional - sage.rings.number_field
        sage: k.coerce_map_from(OK)(c)                                                  # optional - sage.rings.number_field
        16
        sage: k(4)                                                                      # optional - sage.rings.number_field
        4
        sage: k(c + 5)                                                                  # optional - sage.rings.number_field
        21
        sage: b + c                                                                     # optional - sage.rings.number_field
        3

        sage: R.<t> = GF(7)[]; P = R.ideal(2*t + 3)
        sage: k = P.residue_field(); k
        Residue field of Principal ideal (t + 5) of
         Univariate Polynomial Ring in t over Finite Field of size 7
        sage: k(t^2)
        4
        sage: k.order()
        7
    """
    def __init__(self, p, name, intp, to_vs, to_order, PB):
        """
        Initialize ``self``.

        INPUT:

        - ``p`` -- A prime ideal of a number field

        - ``name`` -- the name of the generator of this extension

        - ``intp`` -- the rational prime that ``p`` lies over

        EXAMPLES::

            sage: K.<i> = QuadraticField(-1)                                            # optional - sage.rings.number_field
            sage: kk = ResidueField(K.factor(5)[0][0])                                  # optional - sage.rings.number_field
            sage: type(kk)                                                              # optional - sage.rings.number_field
            <class 'sage.rings.finite_rings.residue_field.ResidueFiniteField_prime_modn_with_category'>

            sage: R.<t> = GF(7)[]; P = R.ideal(2*t + 3)
            sage: k = P.residue_field(); type(k)
            <class 'sage.rings.finite_rings.residue_field.ResidueFiniteField_prime_modn_with_category'>
        """
        ResidueField_generic.__init__(self, p)
        FiniteField_prime_modn.__init__(self, intp)
        from sage.rings.finite_rings.integer_mod import IntegerMod_to_IntegerMod, Integer_to_IntegerMod, Int_to_IntegerMod
        K = OK = p.ring()
        if OK.is_field():
            OK = OK.ring_of_integers()
        else:
            K = K.fraction_field()
        if PB is None:
            if OK is ZZ:
                # integer case
                coerce_list = [IntegerMod_to_IntegerMod(GF(intp), self), Integer_to_IntegerMod(self), Int_to_IntegerMod(self)]
            else:
                # polynomial ring case.
                coerce_list = [ResidueFieldHomomorphism_global(OK, self, None, None, None, None), OK.base_ring()]
            self._populate_coercion_lists_(coerce_list=coerce_list,
                                           convert_list=[ReductionMap(K, self, None, None, None, None)])  # could be special-cased a bit more.
        else:
            PBinv = PB**(-1)
            self._populate_coercion_lists_(coerce_list=[IntegerMod_to_IntegerMod(GF(intp), self),
                                                        Integer_to_IntegerMod(self),
                                                        Int_to_IntegerMod(self),
                                                        ResidueFieldHomomorphism_global(OK, self, to_vs, to_order, PB, PBinv)],
                                           convert_list=[ReductionMap(K, self, to_vs, to_order, PB, PBinv)])

    def _element_constructor_(self, x):
        """
        Construct and/or coerce ``x`` into an element of ``self``.

        INPUT:

           - ``x`` -- something to cast in to ``self``.

        EXAMPLES::

            sage: R.<x> = QQ[]
            sage: K.<a> = NumberField(x^3 - 7)                                          # optional - sage.rings.number_field
            sage: P = K.ideal(29).factor()[1][0]                                        # optional - sage.rings.number_field
            sage: k = ResidueField(P)                                                   # optional - sage.rings.number_field
            sage: k                                                                     # optional - sage.rings.number_field
            Residue field of Fractional ideal (-a^2 - 2*a - 2)
            sage: OK = K.maximal_order()                                                # optional - sage.rings.number_field
            sage: c = OK(a)                                                             # optional - sage.rings.number_field
            sage: b = k(a); b                                                           # optional - sage.rings.number_field
            16
            sage: k(2r)                                                                 # optional - sage.rings.number_field
            2
            sage: V = k.vector_space(map=False); v = V([3])                             # optional - sage.rings.number_field
            sage: type(k.convert_map_from(V))                                           # optional - sage.rings.number_field
            <class 'sage.structure.coerce_maps.DefaultConvertMap_unique'>
            sage: k(v) # indirect doctest                                               # optional - sage.rings.number_field
            3

            sage: R.<t> = GF(2)[]; P = R.ideal(t + 1); k.<a> = P.residue_field()
            sage: V = k.vector_space(map=False); v = V([1])
            sage: k(v)
            1
        """
        if isinstance(x, FreeModuleElement) and len(x) == 1:
            x = x[0]
        try:
            return FiniteField_prime_modn._element_constructor_(self, x)
        except TypeError:
            return ResidueField_generic._element_constructor_(self, x)
