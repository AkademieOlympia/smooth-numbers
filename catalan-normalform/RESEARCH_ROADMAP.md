# Research Roadmap (Revised after H11 Critical Review)

**Datum:** 24. Juni 2026  
**Status:** Active Strategy

---

## Strategic Priority Hierarchy

The project now follows a clear sequential strategy, not unlimited analogy formation:

```
H10 (Information Content)
        ↓
Tamari Geometry (Clean Development)
        ↓
Quaternionic EABC Invariants (If H10 succeeds)
        ↓
Octonions (Only if necessary)
```

---

## Phase 1: H10 – The Critical Question (Immediate Priority)

**Question:** Does M_C(n) carry information **beyond** Ω(n)?

$$I(M_C; n \mid \Omega(n)) > 0 \text{ ?}$$

**Evidence Level:** B (testable)

**Current Status:** E02 suggests ΔR²_H = 0.22, but requires:
- Cross-validation
- Permutation tests
- Larger sample sizes

**If H10 fails (M_C contains no additional information):**
→ Catalan structures are only "bookkeeping" for tree shapes
→ Much of the program becomes moot
→ Focus shifts to pure EABC arithmetic

**If H10 succeeds:**
→ Proceed to Phase 2

**Timeline:** Next 2-3 months

---

## Phase 2: Tamari Geometry (Clean Mathematical Development)

**Assumption:** H10 succeeded

**Goal:** Develop Tamari lattice theory **independently of EABC first**

**Tasks:**
1. Formalize Tamari lattice in Lean
2. Study Tamari distance metrics
3. Investigate rotation energy: $E(T) = \sum \|[a,b,c]\|^2$
4. Connection to M_C(n) without premature algebraic interpretation

**Evidence Level:** A/B (mathematical theory + testable hypotheses)

**Timeline:** 3-6 months

**Potential Output:** Standalone paper on "Tamari Lattices and Tree Energy"

---

## Phase 3: Quaternionic EABC Invariants (Cautious Extension)

**Assumption:** H10 succeeded AND Tamari geometry established

**Goal:** Investigate whether EABC has natural quaternionic structure

**Questions:**
- Do ABCE cycles correspond to SU(2) operations?
- Are there quaternionic invariants?
- Do chiral classes have quaternionic meaning?
- Can gap asymmetries be expressed as quaternionic rotations?

**Evidence Level:** B/C (testable + interpretative)

**Timeline:** 3-6 months

**Critical Check:** Does ℍ structure add **measurable** information beyond Tamari?

---

## Phase 4: Octonions (Only If Absolutely Necessary)

**Assumption:** H10, Tamari, AND Quaternions all succeeded

**Prerequisites:**
1. ✓ Corrected embedding that escapes all quaternionic subalgebras
2. ✓ Proof that EABC classes relate to Fano plane
3. ✓ Empirical evidence that octonionic structures carry arithmetic information

**Without these: Remains Level D (speculation)**

**Timeline:** 6-12 months (if ever pursued)

---

## Anti-Pattern: What We Explicitly Avoid

```
❌ Interesting Structure → New Analogy → New Analogy → New Analogy
```

**Problem:** Unlimited expansion without testing

**Our Pattern:**

```
✓ Hypothesis → Test → ΔR² Measurement → Document Failure/Success → Next Step
```

---

## Documented Failures Guide Future Work

**Failed:**
- EABC→𝕆 via {1,i,j,k} (structural impossibility)

**Succeeded:**
- Catalan–Tamari–Associator connection (robust, independent of EABC)
- EABC↔Gauß-Eisenstein (Level A, proven)
- Gap asymmetry mod 12 (Level B+, empirically supported)

**The failures are as valuable as successes** for directing research strategy.

---

## Key Strategic Principle

$$\boxed{
\text{The project pursues no unbounded analogy formation,}
}$$

$$\boxed{
\text{but works with explicit null models, priorities, and documented failures.}
}$$

This transforms "speculative mathematics" into a **controlled research program**.

---

## Reviewer/Collaborator Guidance

**Priority for external collaborators:**

1. **H10** (highest priority) – needs empirical validation
2. **Tamari geometry** (mathematically cleanest) – needs formalization
3. **Quaternionic EABC** (plausible) – needs exploration after #1-2
4. **Octonions** (lowest priority) – only after major successes in #1-3

**Not recommended for immediate work:**
- Spectral theory (technically difficult, unclear connection)
- Collatz couplings (very weak mathematical basis)
- Cosmological analogies (Level D speculation)

---

## Success Metrics

**H10 Phase:**
- Clear yes/no answer with ΔR² > 0.05 or < 0.01
- Published experiment protocol
- Reproducible code

**Tamari Phase:**
- Formalized definitions in Lean
- At least 3 theorems about Tamari-tree relationships
- Connection to M_C established or refuted

**Quaternionic Phase:**
- At least one measurable quaternionic invariant
- ΔR² test showing additional information beyond Tamari
- Or explicit documentation of failure

---

## Status: Active

This roadmap replaces previous ad-hoc exploration with a **sequential, evidence-based strategy**.

**Next checkpoint:** H10 completion (target: August 2026)
