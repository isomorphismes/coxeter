# Suspension response maps: retain the structure before the matrix

Date: 2026-09-11.

**Status: mathematical design note. No new reducer, backend, type checker, or suspension calibration is implemented here.** Existing reflection/word-analysis work is not changed or treated as acceptance of this application.

## Why this example belongs here

The [ASE suspension derivation](https://github.com/the-twin-pines/ASE/blob/a4-suspension-steering/notes/dakota-cam-jacobian-curvature.md) begins with a real question: how do two eccentric-cam settings change caster and camber? Its inspected source blob was `4e0e47d6813db3c4dc5bc1dd68f23f9c98fe9287`. [ASE's evidence plan](https://github.com/the-twin-pines/ASE/blob/a4-suspension-steering/notes/suspension-response-cross-repository.md) owns the physical measurement and safety boundary.

This is a useful test of whether algebraic representations preserve their meaning. An adjustment, a coordinate change, a reflection, a derivative, and a curvature operator can all be represented by matrices at some stage. They are not the same mathematical object.

[Fulton's geometry note](https://github.com/walnut-burgundy/fulton/blob/main/references/mikhail-gromov/suspension-response-geometry.md) supplies the source-linked geometric argument. [Econometrician's note](https://github.com/bl4ckb4ll/econometrician/blob/main/notes/suspension-response-identification.md) separates identification from inversion. The local [Gromov reading guide](../references/gromov/sign-and-geometric-meaning-of-curvature.md) remains a guide to the paper, not a proof that group-word machinery solves alignment.

## 1. The compositional objects

At fixed conditions and on a repeatable settled branch, distinguish

$$q\ \xrightarrow{c}\ u\ \xrightarrow{F}\ y.$$

`q` is eccentric rotation with declared angle zeros and directions. `u` is actual pivot displacement along specified slots. `y` is the pair of camber/caster measurements, or a larger declared observation space. Mechanical closure, passive motion, and the measurement procedure are part of the response map, not implicit entries in a guessed matrix.

The derivative is a linear map between tangent spaces at specified points:

$$D(F\circ c)_q=DF_{c(q)}\circ Dc_q.$$

A matrix represents this map only after bases and units are chosen. The local response depends on the operating point and fixed conditions. Retaining a typed space name without those dependencies is not enough.

The second derivative has an additional term:

$$D^2(F\circ c)[v,w]=D^2F[Dc\,v,Dc\,w]+DF\,D^2c[v,w].$$

Dropping the latter term would confuse cam-speed variation with a response linear in pivot displacement. It is a concrete counterexample target for any future differentiation or simplification system.

## 2. Coordinate transformations and physical actions are different

For invertible linear recodings `q_tilde=A q`, `y_tilde=R y`, the same response has

$$J_{tilde}=R J A^{-1}.$$

If the original output metric is `W`, representing the **same** geometry requires

$$W_{tilde}=R^{-T}W R^{-1},\qquad
 g_{tilde}=A^{-T}(J^T WJ)A^{-1}.$$

These transformation laws explain how units and bases should travel with a derivative. Changing angle units without transforming the metric changes numerical distances; choosing different tolerance weights on purpose changes the geometry rather than merely recoding it.

In Euclidean standardized output coordinates, an orthogonal frame change preserves inner products. A reflection reverses orientation; a rotation in SO(n) preserves it. More generally, a linear transformation is an isometry of a fixed metric only when it satisfies `R^T W R=W`.

None of this says that turning an eccentric physically applies `R` to the output space. A coordinate rotation changes description; a physical adjustment changes the system state. A nonlinear settled response is not automatically a group action, a linear representation, or an isometry.

## 3. Keep the different signs separate

The sign of caster or camber uses the alignment convention. The sign of `det J` uses input and output orientations. Signed plane-curve curvature also uses a traversal and plane orientation. A second fundamental form uses a selected normal when represented as a scalar form. Gaussian curvature is another object again.

For example,

$$\det J_{tilde}=\frac{\det R}{\det A}\det J.$$

Reversing one coordinate reverses this determinant without changing the physical suspension. It cannot be a coordinate-independent test of positive or negative intrinsic curvature.

For a regular curve in an oriented Euclidean output plane,

$$\kappa=\frac{\det(z',z'')}{\|z'\|^3}.$$

Reflecting the output plane reverses this signed value while preserving its magnitude. Reversing traversal also reverses this convention. Normal reversal changes the scalar second fundamental form's sign, not the underlying normal-valued geometric object.

## 4. Two examples a structure-aware system should not conflate

**Speed without bending.** Take a constant linear response `F(u)=B u` and one eccentric displacement `u_1=e cos(q_1)` with the other input fixed. The output follows a straight line, but its second derivative with respect to `q_1` is usually nonzero. Curvature is zero at regular points; the parameterization stops being regular at a displacement extremum.

**Curved path inside a flat response metric.** Take

$$F(a,b)=(a,b+c a^2),\qquad W=I.$$

The pullback `g=DF^T DF` has varying entries but is flat: the two components of `F` themselves form local Euclidean coordinates. Holding `b` fixed nevertheless gives a curved parabola. A constrained path and the full two-control metric are different objects.

More generally, a smooth locally invertible two-input/two-output map pulls a fixed Euclidean output metric back to a locally flat metric. Rank loss makes that pullback degenerate. Additional measurements, a different state space, or a variable metric require a new analysis.

These are exact mathematical examples, not numerical estimates for the Dakota.

## 5. Normal projection removes coordinate-only acceleration

For an immersion `Z` into a fixed standardized Euclidean measurement space, let

$$J=DZ,\quad g=J^TJ,\quad
 P_\perp=I-Jg^{-1}J^T,\quad
 B_{ij}=P_\perp\partial_i\partial_j Z.$$

This requires full column rank. Under a locally invertible reparameterization `q=phi(v)`,

$$\partial_a\partial_b(Z\circ\phi)
=\partial_i\partial_j Z\,\partial_a\phi^i\partial_b\phi^j
+\partial_i Z\,\partial_a\partial_b\phi^i.$$

The last term lies in the tangent image and vanishes after `P_perp`. Thus the normal-valued second fundamental form transforms bilinearly even though raw second coordinate derivatives do not. This is precisely why a Hessian matrix alone is not the whole geometry.

For a two-dimensional response surface in flat measurement space, the intrinsic Gaussian curvature is

$$K=\frac{\langle B_{11},B_{22}\rangle-\|B_{12}\|^2}{\det g}.$$

One must identify this surface and metric before evaluating the formula. It does not turn an arbitrary determinant, covariance, or Hessian into a curvature tensor.

## 6. Proposed semantic records, not a chosen syntax

A future experiment could explicitly retain the control space and units; pivot and observation spaces; a settled-state/condition record; a response map and evaluation point; its tangent map; an output metric with its purpose; and separate regularity/rank hypotheses. Normal projection and induced geometry would then consume those objects rather than reconstructing them from unlabelled arrays.

The important distinctions include measured versus illustrative parameters, exact versus estimated derivatives, conditional versus total responses, tolerance weighting versus noise weighting, and local rank versus global reachability. A certificate that merely assumes an unmeasured condition does not establish it on the truck.

Useful proposed checks are the two counterexamples above, the second-order chain rule, metric transformation under units/basis changes, determinant reversal without intrinsic-curvature change, and refusal to use `g^{-1}` at rank loss. No new executable acceptance for these checks is claimed by this note.

## 7. Boundary for Coxeter and CP^n/SO(n) work

Certified products of genuine reflection or rotation maps may be simplified using their proved relations. Such algebra does not establish the suspension response model, a curvature bound, or a stable inverse. A proof about a fixed orthogonal frame transformation cannot be substituted for a proof about the physical cam map.

Likewise, using projective or SO(n) geometry elsewhere requires explicit spaces, metrics, normalizations, actions, and applicable theorems. Gromov's paper supplies mathematical sources to study; this cross-post does not validate speculative type theory or demonstrate a speedup.
