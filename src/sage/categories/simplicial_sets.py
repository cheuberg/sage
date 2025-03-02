"""
Simplicial Sets
"""
# ****************************************************************************
#  Copyright (C) 2015 John H. Palmieri <palmieri at math.washington.edu>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  https://www.gnu.org/licenses/
# *****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.categories.category_singleton import Category_singleton
from sage.categories.category_with_axiom import CategoryWithAxiom
from sage.categories.sets_cat import Sets
from sage.categories.homsets import HomsetsCategory
from sage.rings.infinity import Infinity
from sage.rings.integer import Integer


class SimplicialSets(Category_singleton):
    r"""
    The category of simplicial sets.

    A simplicial set `X` is a collection of sets `X_i`, indexed by
    the non-negative integers, together with maps

    .. math::

        d_i: X_n \to X_{n-1}, \quad 0 \leq i \leq n \quad \text{(face maps)} \\
        s_j: X_n \to X_{n+1}, \quad 0 \leq j \leq n \quad \text{(degeneracy maps)}

    satisfying the *simplicial identities*:

    .. math::

        d_i d_j &= d_{j-1} d_i \quad \text{if } i<j \\
        d_i s_j &= s_{j-1} d_i \quad \text{if } i<j \\
        d_j s_j &= 1 = d_{j+1} s_j \\
        d_i s_j &= s_{j} d_{i-1} \quad \text{if } i>j+1 \\
        s_i s_j &= s_{j+1} s_{i} \quad \text{if } i \leq j

    Morphisms are sequences of maps `f_i : X_i \to Y_i` which commute
    with the face and degeneracy maps.

    EXAMPLES::

        sage: from sage.categories.simplicial_sets import SimplicialSets
        sage: C = SimplicialSets(); C
        Category of simplicial sets

    TESTS::

        sage: TestSuite(C).run()
    """
    @cached_method
    def super_categories(self):
        """
        EXAMPLES::

            sage: from sage.categories.simplicial_sets import SimplicialSets
            sage: SimplicialSets().super_categories()
            [Category of sets]
        """
        return [Sets()]

    class ParentMethods:
        def is_finite(self):
            """
            Return ``True`` if this simplicial set is finite, i.e., has a
            finite number of nondegenerate simplices.

            EXAMPLES::

                sage: simplicial_sets.Torus().is_finite()                               # optional - sage.graphs
                True
                sage: C5 = groups.misc.MultiplicativeAbelian([5])                       # optional - sage.graphs sage.groups
                sage: simplicial_sets.ClassifyingSpace(C5).is_finite()                  # optional - sage.graphs sage.groups
                False
            """
            return SimplicialSets.Finite() in self.categories()

        def is_pointed(self):
            """
            Return ``True`` if this simplicial set is pointed, i.e., has a
            base point.

            EXAMPLES::

                sage: from sage.topology.simplicial_set import AbstractSimplex, SimplicialSet       # optional - sage.graphs
                sage: v = AbstractSimplex(0)                                            # optional - sage.graphs
                sage: w = AbstractSimplex(0)                                            # optional - sage.graphs
                sage: e = AbstractSimplex(1)                                            # optional - sage.graphs
                sage: X = SimplicialSet({e: (v, w)})                                    # optional - sage.graphs
                sage: Y = SimplicialSet({e: (v, w)}, base_point=w)                      # optional - sage.graphs
                sage: X.is_pointed()                                                    # optional - sage.graphs
                False
                sage: Y.is_pointed()                                                    # optional - sage.graphs
                True
            """
            return SimplicialSets.Pointed() in self.categories()

        def set_base_point(self, point):
            """
            Return a copy of this simplicial set in which the base point is
            set to ``point``.

            INPUT:

            - ``point`` -- a 0-simplex in this simplicial set

            EXAMPLES::

                sage: from sage.topology.simplicial_set import AbstractSimplex, SimplicialSet       # optional - sage.graphs
                sage: v = AbstractSimplex(0, name='v_0')                                # optional - sage.graphs
                sage: w = AbstractSimplex(0, name='w_0')                                # optional - sage.graphs
                sage: e = AbstractSimplex(1)                                            # optional - sage.graphs
                sage: X = SimplicialSet({e: (v, w)})                                    # optional - sage.graphs
                sage: Y = SimplicialSet({e: (v, w)}, base_point=w)                      # optional - sage.graphs
                sage: Y.base_point()                                                    # optional - sage.graphs
                w_0
                sage: X_star = X.set_base_point(w)                                      # optional - sage.graphs
                sage: X_star.base_point()                                               # optional - sage.graphs
                w_0
                sage: Y_star = Y.set_base_point(v)                                      # optional - sage.graphs
                sage: Y_star.base_point()                                               # optional - sage.graphs
                v_0

            TESTS::

                sage: X.set_base_point(e)                                               # optional - sage.graphs
                Traceback (most recent call last):
                ...
                ValueError: the "point" is not a zero-simplex
                sage: pt = AbstractSimplex(0)                                           # optional - sage.graphs
                sage: X.set_base_point(pt)                                              # optional - sage.graphs
                Traceback (most recent call last):
                ...
                ValueError: the point is not a simplex in this simplicial set
            """
            from sage.topology.simplicial_set import SimplicialSet
            if point.dimension() != 0:
                raise ValueError('the "point" is not a zero-simplex')
            if point not in self._simplices:
                raise ValueError('the point is not a simplex in this '
                                 'simplicial set')
            return SimplicialSet(self.face_data(), base_point=point)

    class Homsets(HomsetsCategory):
        class Endset(CategoryWithAxiom):
            class ParentMethods:
                def one(self):
                    r"""
                    Return the identity morphism in `\operatorname{Hom}(S, S)`.

                    EXAMPLES::

                        sage: T = simplicial_sets.Torus()                               # optional - sage.graphs
                        sage: Hom(T, T).identity()                                      # optional - sage.graphs
                        Simplicial set endomorphism of Torus
                          Defn: Identity map
                    """
                    from sage.topology.simplicial_set_morphism import SimplicialSetMorphism
                    return SimplicialSetMorphism(domain=self.domain(),
                                                 codomain=self.codomain(),
                                                 identity=True)

    class Finite(CategoryWithAxiom):
        """
        Category of finite simplicial sets.

        The objects are simplicial sets with finitely many
        non-degenerate simplices.
        """
        pass

    class SubcategoryMethods:
        def Pointed(self):
            """
            A simplicial set is *pointed* if it has a distinguished base
            point.

            EXAMPLES::

                sage: from sage.categories.simplicial_sets import SimplicialSets
                sage: SimplicialSets().Pointed().Finite()
                Category of finite pointed simplicial sets
                sage: SimplicialSets().Finite().Pointed()
                Category of finite pointed simplicial sets
            """
            return self._with_axiom("Pointed")

    class Pointed(CategoryWithAxiom):
        class ParentMethods:
            def base_point(self):
                """
                Return this simplicial set's base point

                EXAMPLES::

                    sage: from sage.topology.simplicial_set import AbstractSimplex, SimplicialSet   # optional - sage.graphs
                    sage: v = AbstractSimplex(0, name='*')                              # optional - sage.graphs
                    sage: e = AbstractSimplex(1)                                        # optional - sage.graphs
                    sage: S1 = SimplicialSet({e: (v, v)}, base_point=v)                 # optional - sage.graphs
                    sage: S1.is_pointed()                                               # optional - sage.graphs
                    True
                    sage: S1.base_point()                                               # optional - sage.graphs
                    *
                """
                return self._basepoint

            def base_point_map(self, domain=None):
                """
                Return a map from a one-point space to this one, with image the
                base point.

                This raises an error if this simplicial set does not have a
                base point.

                INPUT:

                - ``domain`` -- optional, default ``None``. Use
                  this to specify a particular one-point space as
                  the domain. The default behavior is to use the
                  :func:`sage.topology.simplicial_set.Point`
                  function to use a standard one-point space.

                EXAMPLES::

                    sage: T = simplicial_sets.Torus()                                   # optional - sage.graphs
                    sage: f = T.base_point_map(); f                                     # optional - sage.graphs
                    Simplicial set morphism:
                      From: Point
                      To:   Torus
                      Defn: Constant map at (v_0, v_0)
                    sage: S3 = simplicial_sets.Sphere(3)                                # optional - sage.graphs
                    sage: g = S3.base_point_map()                                       # optional - sage.graphs
                    sage: f.domain() == g.domain()                                      # optional - sage.graphs
                    True
                    sage: RP3 = simplicial_sets.RealProjectiveSpace(3)                  # optional - sage.graphs
                    sage: temp = simplicial_sets.Simplex(0)                             # optional - sage.graphs
                    sage: pt = temp.set_base_point(temp.n_cells(0)[0])                  # optional - sage.graphs
                    sage: h = RP3.base_point_map(domain=pt)                             # optional - sage.graphs
                    sage: f.domain() == h.domain()                                      # optional - sage.graphs
                    False

                    sage: C5 = groups.misc.MultiplicativeAbelian([5])                   # optional - sage.graphs sage.groups
                    sage: BC5 = simplicial_sets.ClassifyingSpace(C5)                    # optional - sage.graphs sage.groups
                    sage: BC5.base_point_map()                                          # optional - sage.graphs sage.groups
                    Simplicial set morphism:
                      From: Point
                      To:   Classifying space of Multiplicative Abelian group isomorphic to C5
                      Defn: Constant map at 1
                """
                from sage.topology.simplicial_set_examples import Point
                if domain is None:
                    domain = Point()
                else:
                    if len(domain._simplices) > 1:
                        raise ValueError('domain has more than one nondegenerate simplex')
                target = self.base_point()
                return domain.Hom(self).constant_map(point=target)

            def fundamental_group(self, simplify=True):
                r"""
                Return the fundamental group of this pointed simplicial set.

                INPUT:

                - ``simplify`` (bool, optional ``True``) -- if
                  ``False``, then return a presentation of the group
                  in terms of generators and relations. If ``True``,
                  the default, simplify as much as GAP is able to.

                Algorithm: we compute the edge-path group -- see
                Section 19 of [Kan1958]_ and
                :wikipedia:`Fundamental_group`. Choose a spanning tree
                for the connected component of the 1-skeleton
                containing the base point, and then the group's
                generators are given by the non-degenerate
                edges. There are two types of relations: `e=1` if `e`
                is in the spanning tree, and for every 2-simplex, if
                its faces are `e_0`, `e_1`, and `e_2`, then we impose
                the relation `e_0 e_1^{-1} e_2 = 1`, where we first
                set `e_i=1` if `e_i` is degenerate.

                EXAMPLES::

                    sage: S1 = simplicial_sets.Sphere(1)                                # optional - sage.graphs
                    sage: eight = S1.wedge(S1)                                          # optional - sage.graphs
                    sage: eight.fundamental_group() # free group on 2 generators        # optional - sage.graphs sage.groups
                    Finitely presented group < e0, e1 |  >

                The fundamental group of a disjoint union of course depends on
                the choice of base point::

                    sage: T = simplicial_sets.Torus()                                   # optional - sage.graphs
                    sage: K = simplicial_sets.KleinBottle()                             # optional - sage.graphs
                    sage: X = T.disjoint_union(K)                                       # optional - sage.graphs

                    sage: X_0 = X.set_base_point(X.n_cells(0)[0])                       # optional - sage.graphs
                    sage: X_0.fundamental_group().is_abelian()                          # optional - sage.graphs sage.groups
                    True
                    sage: X_1 = X.set_base_point(X.n_cells(0)[1])                       # optional - sage.graphs
                    sage: X_1.fundamental_group().is_abelian()                          # optional - sage.graphs sage.groups
                    False

                    sage: RP3 = simplicial_sets.RealProjectiveSpace(3)                  # optional - sage.graphs
                    sage: RP3.fundamental_group()                                       # optional - sage.graphs sage.groups
                    Finitely presented group < e | e^2 >

                Compute the fundamental group of some classifying spaces::

                    sage: C5 = groups.misc.MultiplicativeAbelian([5])                   # optional - sage.graphs sage.groups
                    sage: BC5 = C5.nerve()                                              # optional - sage.graphs sage.groups
                    sage: BC5.fundamental_group()                                       # optional - sage.graphs sage.groups
                    Finitely presented group < e0 | e0^5 >

                    sage: Sigma3 = groups.permutation.Symmetric(3)                      # optional - sage.graphs sage.groups
                    sage: BSigma3 = Sigma3.nerve()                                      # optional - sage.graphs sage.groups
                    sage: pi = BSigma3.fundamental_group(); pi                          # optional - sage.graphs sage.groups
                    Finitely presented group < e1, e2 | e2^2, e1^3, (e2*e1)^2 >
                    sage: pi.order()                                                    # optional - sage.graphs sage.groups
                    6
                    sage: pi.is_abelian()                                               # optional - sage.graphs sage.groups
                    False

                The sphere has a trivial fundamental group::

                    sage: S2 = simplicial_sets.Sphere(2)                                # optional - sage.graphs
                    sage: S2.fundamental_group()                                        # optional - sage.graphs sage.groups
                    Finitely presented group <  |  >
                """
                # Import this here to prevent importing libgap upon startup.
                from sage.groups.free_group import FreeGroup
                if not self.n_cells(1):
                    return FreeGroup([]).quotient([])
                FG = self._universal_cover_dict()[0]
                if simplify:
                    return FG.simplified()
                else:
                    return FG

            def _universal_cover_dict(self):
                r"""
                Return the fundamental group and dictionary sending each edge to
                the corresponding group element

                TESTS::

                    sage: RP2 = simplicial_sets.RealProjectiveSpace(2)
                    sage: RP2._universal_cover_dict()
                    (Finitely presented group < e | e^2 >, {f: e})
                    sage: RP2.nondegenerate_simplices()
                    [1, f, f * f]
                """
                from sage.groups.free_group import FreeGroup
                skel = self.n_skeleton(2)
                graph = skel.graph()
                if not skel.is_connected():
                    graph = graph.subgraph(skel.base_point())
                edges = [e[2] for e in graph.edges(sort=False)]
                spanning_tree = [e[2] for e in graph.min_spanning_tree()]
                gens = [e for e in edges if e not in spanning_tree]
                gens_dict = dict(zip(gens, range(len(gens))))
                FG = FreeGroup(len(gens), 'e')
                rels = []

                for f in skel.n_cells(2):
                    z = dict()
                    for i, sigma in enumerate(skel.faces(f)):
                        if sigma in spanning_tree:
                            z[i] = FG.one()
                        elif sigma.is_degenerate():
                            z[i] = FG.one()
                        elif sigma in edges:
                            z[i] = FG.gen(gens_dict[sigma])
                        else:
                            # sigma is not in the correct connected component.
                            z[i] = FG.one()
                    rels.append(z[0]*z[1].inverse()*z[2])
                G = FG.quotient(rels)
                char = {g : G.gen(i) for i,g in enumerate(gens)}
                for e in edges:
                    if e not in gens:
                        char[e] = G.one()
                return (G, char)

            def universal_cover_map(self):
                r"""
                Return the universal covering map of the simplicial set.

                It requires the fundamental group to be finite.

                EXAMPLES::

                    sage: RP2 = simplicial_sets.RealProjectiveSpace(2)
                    sage: phi = RP2.universal_cover_map()
                    sage: phi
                    Simplicial set morphism:
                      From: Simplicial set with 6 non-degenerate simplices
                      To:   RP^2
                      Defn: [(1, 1), (1, e), (f, 1), (f, e), (f * f, 1), (f * f, e)] --> [1, 1, f, f, f * f, f * f]
                    sage: phi.domain().face_data()
                        {(1, 1): None,
                         (1, e): None,
                         (f, 1): ((1, e), (1, 1)),
                         (f, e): ((1, 1), (1, e)),
                         (f * f, 1): ((f, e), s_0 (1, 1), (f, 1)),
                         (f * f, e): ((f, 1), s_0 (1, e), (f, e))}

                """
                edges = self.n_cells(1)
                if not edges:
                    return self.identity()
                G, char = self._universal_cover_dict()
                return self.covering_map(char)

            def covering_map(self, character):
                r"""
                Return the covering map associated to a character.

                The character is represented by a dictionary that assigns an
                element of a finite group to each nondegenerate 1-dimensional
                cell. It should correspond to an epimorphism from the fundamental
                group.

                INPUT:

                - ``character`` -- a dictionary


                EXAMPLES::

                    sage: S1 = simplicial_sets.Sphere(1)
                    sage: W = S1.wedge(S1)
                    sage: G = CyclicPermutationGroup(3)
                    sage: a, b = W.n_cells(1)
                    sage: C = W.covering_map({a : G.gen(0), b : G.one()})
                    sage: C
                    Simplicial set morphism:
                      From: Simplicial set with 9 non-degenerate simplices
                      To:   Wedge: (S^1 v S^1)
                      Defn: [(*, ()), (*, (1,2,3)), (*, (1,3,2)), (sigma_1, ()), (sigma_1, ()), (sigma_1, (1,2,3)), (sigma_1, (1,2,3)), (sigma_1, (1,3,2)), (sigma_1, (1,3,2))] --> [*, *, *, sigma_1, sigma_1, sigma_1, sigma_1, sigma_1, sigma_1]
                    sage: C.domain()
                    Simplicial set with 9 non-degenerate simplices
                    sage: C.domain().face_data()
                    {(*, ()): None,
                     (*, (1,2,3)): None,
                     (*, (1,3,2)): None,
                     (sigma_1, ()): ((*, (1,2,3)), (*, ())),
                     (sigma_1, ()): ((*, ()), (*, ())),
                     (sigma_1, (1,2,3)): ((*, (1,3,2)), (*, (1,2,3))),
                     (sigma_1, (1,2,3)): ((*, (1,2,3)), (*, (1,2,3))),
                     (sigma_1, (1,3,2)): ((*, ()), (*, (1,3,2))),
                     (sigma_1, (1,3,2)): ((*, (1,3,2)), (*, (1,3,2)))}
                """
                from sage.topology.simplicial_set import AbstractSimplex, SimplicialSet
                from sage.topology.simplicial_set_morphism import SimplicialSetMorphism
                char = {a: b for (a, b) in character.items()}
                G = list(char.values())[0].parent()
                if not G.is_finite():
                    raise NotImplementedError("can only compute universal covers of spaces with finite fundamental group")
                cells_dict = {}
                faces_dict = {}

                for s in self.n_cells(0):
                    for g in G:
                        cell = AbstractSimplex(0, name="({}, {})".format(s, g))
                        cells_dict[(s, g)] = cell
                        char[s] = G.one()

                for d in range(1, self.dimension() + 1):
                    for s in self.n_cells(d):
                        if s not in char.keys():
                            if d == 1 and s.is_degenerate():
                                char[s] = G.one()
                            elif s.is_degenerate():
                                if 0 in s.degeneracies():
                                    char[s] = G.one()
                                else:
                                    char[s] = char[s.nondegenerate()]
                            else:
                                char[s] = char[self.face(s, d)]
                        if s.is_nondegenerate():
                            for g in G:
                                cell = AbstractSimplex(d, name="({}, {})".format(s, g))
                                cells_dict[(s, g)] = cell
                                fd = []
                                faces = self.faces(s)
                                f0 = faces[0]
                                for h in G:
                                    if h == g*char[s]:
                                        lifted = h
                                        break
                                grelems = [cells_dict[(f0.nondegenerate(), lifted)].apply_degeneracies(*f0.degeneracies())]
                                for f in faces[1:]:
                                    grelems.append(cells_dict[(f.nondegenerate(), g)].apply_degeneracies(*f.degeneracies()))
                                faces_dict[cell] = grelems
                cover = SimplicialSet(faces_dict, base_point=cells_dict[(self.base_point(), G.one())])
                cover_map_data = {c : s[0] for (s,c) in cells_dict.items()}
                return SimplicialSetMorphism(data = cover_map_data, domain = cover, codomain = self)

            def cover(self, character):
                r"""
                Return the cover of the simplicial set associated to a character
                of the fundamental group.

                The character is represented by a dictionary, that assigns an
                element of a finite group to each nondegenerate 1-dimensional
                cell. It should correspond to an epimorphism from the fundamental
                group.

                INPUT:

                - ``character`` -- a dictionary

                EXAMPLES::

                    sage: S1 = simplicial_sets.Sphere(1)
                    sage: W = S1.wedge(S1)
                    sage: G = CyclicPermutationGroup(3)
                    sage: (a, b) = W.n_cells(1)
                    sage: C = W.cover({a : G.gen(0), b : G.gen(0)^2})
                    sage: C.face_data()
                    {(*, ()): None,
                     (*, (1,2,3)): None,
                     (*, (1,3,2)): None,
                     (sigma_1, ()): ((*, (1,2,3)), (*, ())),
                     (sigma_1, ()): ((*, (1,3,2)), (*, ())),
                     (sigma_1, (1,2,3)): ((*, (1,3,2)), (*, (1,2,3))),
                     (sigma_1, (1,2,3)): ((*, ()), (*, (1,2,3))),
                     (sigma_1, (1,3,2)): ((*, ()), (*, (1,3,2))),
                     (sigma_1, (1,3,2)): ((*, (1,2,3)), (*, (1,3,2)))}
                    sage: C.homology(1)
                    Z x Z x Z x Z
                    sage: C.fundamental_group()
                    Finitely presented group < e0, e1, e2, e3 |  >
                """
                return self.covering_map(character).domain()

            def universal_cover(self):
                r"""
                Return the universal cover of the simplicial set.
                The fundamental group must be finite in order to ensure that the
                universal cover is a simplicial set of finite type.

                EXAMPLES::

                    sage: RP3 = simplicial_sets.RealProjectiveSpace(3)
                    sage: C = RP3.universal_cover()
                    sage: C
                    Simplicial set with 8 non-degenerate simplices
                    sage: C.face_data()
                    {(1, 1): None,
                     (1, e): None,
                     (f, 1): ((1, e), (1, 1)),
                     (f, e): ((1, 1), (1, e)),
                     (f * f, 1): ((f, e), s_0 (1, 1), (f, 1)),
                     (f * f, e): ((f, 1), s_0 (1, e), (f, e)),
                     (f * f * f, 1): ((f * f, e), s_0 (f, 1), s_1 (f, 1), (f * f, 1)),
                     (f * f * f, e): ((f * f, 1), s_0 (f, e), s_1 (f, e), (f * f, e))}
                    sage: C.fundamental_group()
                    Finitely presented group <  |  >
                """
                return self.universal_cover_map().domain()

            def is_simply_connected(self):
                """
                Return ``True`` if this pointed simplicial set is simply connected.

                .. WARNING::

                    Determining simple connectivity is not always
                    possible, because it requires determining when a
                    group, as given by generators and relations, is
                    trivial. So this conceivably may give a false
                    negative in some cases.

                EXAMPLES::

                    sage: T = simplicial_sets.Torus()                                   # optional - sage.graphs
                    sage: T.is_simply_connected()                                       # optional - sage.graphs
                    False
                    sage: T.suspension().is_simply_connected()                          # optional - sage.graphs
                    True
                    sage: simplicial_sets.KleinBottle().is_simply_connected()           # optional - sage.graphs
                    False

                    sage: S2 = simplicial_sets.Sphere(2)                                # optional - sage.graphs
                    sage: S3 = simplicial_sets.Sphere(3)                                # optional - sage.graphs
                    sage: (S2.wedge(S3)).is_simply_connected()                          # optional - sage.graphs
                    True
                    sage: X = S2.disjoint_union(S3)                                     # optional - sage.graphs
                    sage: X = X.set_base_point(X.n_cells(0)[0])                         # optional - sage.graphs
                    sage: X.is_simply_connected()                                       # optional - sage.graphs
                    False

                    sage: C3 = groups.misc.MultiplicativeAbelian([3])                   # optional - sage.graphs sage.groups
                    sage: BC3 = simplicial_sets.ClassifyingSpace(C3)                    # optional - sage.graphs sage.groups
                    sage: BC3.is_simply_connected()                                     # optional - sage.graphs sage.groups
                    False
                """
                if not self.is_connected():
                    return False
                try:
                    if not self.is_pointed():
                        space = self.set_base_point(self.n_cells(0)[0])
                    else:
                        space = self
                    return bool(space.fundamental_group().IsTrivial())
                except AttributeError:
                    try:
                        return space.fundamental_group().order() == 1
                    except (NotImplementedError, RuntimeError):
                        # I don't know of any simplicial sets for which the
                        # code reaches this point, but there are certainly
                        # groups for which these errors are raised. 'IsTrivial'
                        # works for all of the examples I've seen, though.
                        raise ValueError('unable to determine if the fundamental '
                                         'group is trivial')

            def connectivity(self, max_dim=None):
                """
                Return the connectivity of this pointed simplicial set.

                INPUT:

                - ``max_dim`` -- specify a maximum dimension through
                  which to check. This is required if this simplicial
                  set is simply connected and not finite.

                The dimension of the first nonzero homotopy group. If
                simply connected, this is the same as the dimension of
                the first nonzero homology group.

                .. WARNING::

                   See the warning for the :meth:`is_simply_connected` method.

                The connectivity of a contractible space is ``+Infinity``.

                EXAMPLES::

                    sage: simplicial_sets.Sphere(3).connectivity()                      # optional - sage.graphs
                    2
                    sage: simplicial_sets.Sphere(0).connectivity()                      # optional - sage.graphs
                    -1
                    sage: K = simplicial_sets.Simplex(4)                                # optional - sage.graphs
                    sage: K = K.set_base_point(K.n_cells(0)[0])                         # optional - sage.graphs
                    sage: K.connectivity()                                              # optional - sage.graphs
                    +Infinity
                    sage: X = simplicial_sets.Torus().suspension(2)                     # optional - sage.graphs
                    sage: X.connectivity()                                              # optional - sage.graphs
                    2

                    sage: C2 = groups.misc.MultiplicativeAbelian([2])                   # optional - sage.graphs sage.groups
                    sage: BC2 = simplicial_sets.ClassifyingSpace(C2)                    # optional - sage.graphs sage.groups
                    sage: BC2.connectivity()                                            # optional - sage.graphs sage.groups
                    0
                """
                if not self.is_connected():
                    return Integer(-1)
                if not self.is_simply_connected():
                    return Integer(0)
                if max_dim is None:
                    if self.is_finite():
                        max_dim = self.dimension()
                    else:
                        # Note: at the moment, this will never be reached,
                        # because our only examples (so far) of infinite
                        # simplicial sets are not simply connected.
                        raise ValueError('this simplicial set may be infinite, '
                                         'so specify a maximum dimension through '
                                         'which to check')

                H = self.homology(range(2, max_dim + 1))
                for i in range(2, max_dim + 1):
                    if i in H and H[i].order() != 1:
                        return i-1
                return Infinity

        class Finite(CategoryWithAxiom):
            class ParentMethods():

                def unset_base_point(self):
                    """
                    Return a copy of this simplicial set in which the base point has
                    been forgotten.

                    EXAMPLES::

                        sage: from sage.topology.simplicial_set import AbstractSimplex, SimplicialSet                   # optional - sage.graphs
                        sage: v = AbstractSimplex(0, name='v_0')                        # optional - sage.graphs
                        sage: w = AbstractSimplex(0, name='w_0')                        # optional - sage.graphs
                        sage: e = AbstractSimplex(1)                                    # optional - sage.graphs
                        sage: Y = SimplicialSet({e: (v, w)}, base_point=w)              # optional - sage.graphs
                        sage: Y.is_pointed()                                            # optional - sage.graphs
                        True
                        sage: Y.base_point()                                            # optional - sage.graphs
                        w_0
                        sage: Z = Y.unset_base_point()                                  # optional - sage.graphs
                        sage: Z.is_pointed()                                            # optional - sage.graphs
                        False
                    """
                    from sage.topology.simplicial_set import SimplicialSet
                    return SimplicialSet(self.face_data())

                def fat_wedge(self, n):
                    """
                    Return the `n`-th fat wedge of this pointed simplicial set.

                    This is the subcomplex of the `n`-fold product `X^n`
                    consisting of those points in which at least one
                    factor is the base point. Thus when `n=2`, this is the
                    wedge of the simplicial set with itself, but when `n`
                    is larger, the fat wedge is larger than the `n`-fold
                    wedge.

                    EXAMPLES::

                        sage: S1 = simplicial_sets.Sphere(1)                            # optional - sage.graphs
                        sage: S1.fat_wedge(0)                                           # optional - sage.graphs
                        Point
                        sage: S1.fat_wedge(1)                                           # optional - sage.graphs
                        S^1
                        sage: S1.fat_wedge(2).fundamental_group()                       # optional - sage.graphs sage.groups
                        Finitely presented group < e0, e1 |  >
                        sage: S1.fat_wedge(4).homology()                                # optional - sage.graphs sage.modules
                        {0: 0, 1: Z x Z x Z x Z, 2: Z^6, 3: Z x Z x Z x Z}
                    """
                    from sage.topology.simplicial_set_examples import Point
                    if n == 0:
                        return Point()
                    if n == 1:
                        return self
                    return self.product(*[self]*(n-1)).fat_wedge_as_subset()

                def smash_product(self, *others):
                    """
                    Return the smash product of this simplicial set with ``others``.

                    INPUT:

                    - ``others`` -- one or several simplicial sets

                    EXAMPLES::

                        sage: S1 = simplicial_sets.Sphere(1)                            # optional - sage.graphs
                        sage: RP2 = simplicial_sets.RealProjectiveSpace(2)              # optional - sage.graphs
                        sage: X = S1.smash_product(RP2)                                 # optional - sage.graphs
                        sage: X.homology(base_ring=GF(2))                               # optional - sage.graphs sage.modules
                        {0: Vector space of dimension 0 over Finite Field of size 2,
                         1: Vector space of dimension 0 over Finite Field of size 2,
                         2: Vector space of dimension 1 over Finite Field of size 2,
                         3: Vector space of dimension 1 over Finite Field of size 2}

                        sage: T = S1.product(S1)                                        # optional - sage.graphs
                        sage: X = T.smash_product(S1)                                   # optional - sage.graphs
                        sage: X.homology(reduced=False)                                 # optional - sage.graphs sage.modules
                        {0: Z, 1: 0, 2: Z x Z, 3: Z}
                    """
                    from sage.topology.simplicial_set_constructions import SmashProductOfSimplicialSets_finite
                    return SmashProductOfSimplicialSets_finite((self,) + others)
