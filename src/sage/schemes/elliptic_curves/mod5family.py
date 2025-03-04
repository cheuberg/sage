"""
Elliptic curves with congruent mod-5 representation

AUTHORS:

- Alice Silverberg and Karl Rubin -- original PARI/GP version

- William Stein -- Sage version
"""
# ****************************************************************************
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.rational_field import QQ
from .constructor import EllipticCurve


def mod5family(a, b):
    """
    Formulas for computing the family of elliptic curves with
    congruent mod-5 representation.

    EXAMPLES::

        sage: from sage.schemes.elliptic_curves.mod5family import mod5family
        sage: mod5family(0,1)
        Elliptic Curve defined by y^2 = x^3 + (t^30+30*t^29+435*t^28+4060*t^27+27405*t^26+142506*t^25+593775*t^24+2035800*t^23+5852925*t^22+14307150*t^21+30045015*t^20+54627300*t^19+86493225*t^18+119759850*t^17+145422675*t^16+155117520*t^15+145422675*t^14+119759850*t^13+86493225*t^12+54627300*t^11+30045015*t^10+14307150*t^9+5852925*t^8+2035800*t^7+593775*t^6+142506*t^5+27405*t^4+4060*t^3+435*t^2+30*t+1) over Fraction Field of Univariate Polynomial Ring in t over Rational Field
    """
    J = 4*a**3 / (4*a**3+27*b**2)

    alpha = [0 for _ in range(21)]
    alpha[0] = 1
    alpha[1] = 0
    alpha[2] = 190*(J - 1)
    alpha[3] = -2280*(J - 1)**2
    alpha[4] = 855*(J - 1)**2*(-17 + 16*J)
    alpha[5] = 3648*(J - 1)**3*(17 - 9*J)
    alpha[6] = 11400*(J - 1)**3*(17 - 8*J)
    alpha[7] = -27360*(J - 1)**4*(17 + 26*J)
    alpha[8] = 7410*(J - 1)**4*(-119 - 448*J + 432*J**2)
    alpha[9] = 79040*(J - 1)**5*(17 + 145*J - 108*J**2)
    alpha[10] = 8892*(J - 1)**5*(187 + 2640*J - 5104*J**2 + 1152*J**3)
    alpha[11] = 98800*(J - 1)**6*(-17 - 388*J + 864*J**2)
    alpha[12] = 7410*(J - 1)**6*(-187 - 6160*J + 24464*J**2 - 24192*J**3)
    alpha[13] = 54720*(J - 1)**7*(17 + 795*J - 3944*J**2 + 9072*J**3)
    alpha[14] = 2280*(J - 1)**7*(221 + 13832*J - 103792*J**2 + 554112*J**3 - 373248*J**4)
    alpha[15] = 1824*(J - 1)**8*(-119 - 9842*J + 92608*J**2 - 911520*J**3 + 373248*J**4)
    alpha[16] = 4275*(J - 1)**8*(-17 - 1792*J + 23264*J**2 - 378368*J**3 + 338688*J**4)
    alpha[17] = 18240*(J - 1)**9*(1 + 133*J - 2132*J**2 + 54000*J**3 - 15552*J**4)
    alpha[18] = 190*(J - 1)**9*(17 + 2784*J - 58080*J**2 + 2116864*J**3 - 946944*J**4 + 2985984*J**5)
    alpha[19] = 360*(J - 1)**10*(-1 + 28*J - 1152*J**2)*(1 + 228*J + 176*J**2 + 1728*J**3)
    alpha[20] = (J - 1)**10*(-19 - 4560*J + 144096*J**2 - 9859328*J**3 - 8798976*J**4 - 226934784*J**5 + 429981696*J**6)

    beta = [0 for _ in range(31)]
    beta[0] = 1
    beta[1] = 30
    beta[2] = -435*(J - 1)
    beta[3] = 580*(J - 1)*(-7 + 9*J)
    beta[4] = 3915*(J - 1)**2*(7 - 8*J)
    beta[5] = 1566*(J - 1)**2*(91 - 78*J + 48*J**2)
    beta[6] = -84825*(J - 1)**3*(7 + 16*J)
    beta[7] = 156600*(J - 1)**3*(-13 - 91*J + 92*J**2)
    beta[8] = 450225*(J - 1)**4*(13 + 208*J - 144*J**2)
    beta[9] = 100050*(J - 1)**4*(143 + 4004*J - 5632*J**2 + 1728*J**3)
    beta[10] = 30015*(J - 1)**5*(-1001 - 45760*J + 44880*J**2 - 6912*J**3)
    beta[11] = 600300*(J - 1)**5*(-91 - 6175*J + 9272*J**2 - 2736*J**3)
    beta[12] = 950475*(J - 1)**6*(91 + 8840*J - 7824*J**2)
    beta[13] = 17108550*(J - 1)**6*(7 + 926*J - 1072*J**2 + 544*J**3)
    beta[14] = 145422675*(J - 1)**7*(-1 - 176*J + 48*J**2 - 384*J**3)
    beta[15] = 155117520*(J - 1)**8*(1 + 228*J + 176*J**2 + 1728*J**3)
    beta[16] = 145422675*(J - 1)**8*(1 + 288*J + 288*J**2 + 5120*J**3 - 6912*J**4)
    beta[17] = 17108550*(J - 1)**8*(7 + 2504*J + 3584*J**2 + 93184*J**3 - 283392*J**4 + 165888*J**5)
    beta[18] = 950475*(J - 1)**9*(-91 - 39936*J - 122976*J**2 - 2960384*J**3 + 11577600*J**4 - 5971968*J**5)
    beta[19] = 600300*(J - 1)**9*(-91 - 48243*J - 191568*J**2 - 6310304*J**3 + 40515072*J**4 - 46455552*J**5 + 11943936*J**6)
    beta[20] = 30015*(J - 1)**10*(1001 + 634920*J + 3880800*J**2 + 142879744*J**3 - 1168475904*J**4 + 1188919296*J**5 - 143327232*J**6)
    beta[21] = 100050*(J - 1)**10*(143 + 107250*J + 808368*J**2 + 38518336*J**3 - 451953408*J**4 + 757651968*J**5 - 367276032*J**6)
    beta[22] = 450225*(J - 1)**11*(-13 - 11440*J - 117216*J**2 - 6444800*J**3 + 94192384*J**4 - 142000128*J**5 + 95551488*J**6)
    beta[23] = 156600*(J - 1)**11*(-13 - 13299*J - 163284*J**2 - 11171552*J**3 +  217203840*J**4 - 474406656*J**5 + 747740160*J**6 - 429981696*J**7)
    beta[24] = 6525*(J - 1)**12*(91 + 107536*J + 1680624*J**2 + 132912128*J**3 -
          3147511552*J**4 + 6260502528*J**5 - 21054173184*J**6 + 10319560704*J**7)
    beta[25] = 1566*(J - 1)**12*(91 + 123292*J + 2261248*J**2 + 216211904*J**3 -
          6487793920*J**4 + 17369596928*J**5 - 97854234624*J**6 + 96136740864*J**7 - 20639121408*J**8)
    beta[26] = 3915*(J - 1)**13*(-7 - 10816*J - 242352*J**2 - 26620160*J**3 + 953885440*J**4 -
          2350596096*J**5 + 26796552192*J**6 - 13329432576*J**7)
    beta[27] = 580*(J - 1)**13*(-7 - 12259*J - 317176*J**2 - 41205008*J**3 +
          1808220160*J**4 - 5714806016*J**5 + 93590857728*J**6 - 70131806208*J**7 - 36118462464*J**8)
    beta[28] = 435*(J - 1)**14*(1 + 1976*J + 60720*J**2 + 8987648*J**3 - 463120640*J**4 + 1359157248*J**5 -
          40644882432*J**6 - 5016453120*J**7 + 61917364224*J**8)
    beta[29] = 30*(J - 1)**14*(1 + 2218*J + 77680*J**2 + 13365152*J**3 -
          822366976*J**4 + 2990693888*J**5 - 118286217216*J**6 - 24514928640*J**7 + 509958291456*J**8 - 743008370688*J**9)
    beta[30] = (J - 1)**15*(-1 - 2480*J - 101040*J**2 - 19642496*J**3 + 1399023872*J**4 -
          4759216128*J**5 + 315623485440*J**6 + 471904911360*J**7 - 2600529297408*J**8 + 8916100448256*J**9)

    R = PolynomialRing(QQ, 't')
    c2 = a * R(alpha)
    c3 = b * R(beta)
    d = c2.denominator().lcm(c3.denominator())
    F = R.fraction_field()
    return EllipticCurve(F, [c2 * d**4, c3 * d**6])
