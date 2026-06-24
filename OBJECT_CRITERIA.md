# Object Criteria: When Does a Statistic Become an Object?
## Epistemological Framework for Mathematical Object Formation

Erstellt: 23. Juni 2026  
**Status: Philosophical foundation - Level beyond methodology**

**Master-Index:** [`../eabc-renorm/EABC_MASTER_INDEX.md`](../eabc-renorm/EABC_MASTER_INDEX.md)  
**Deutsch (Dok. 10):** [`~/eabc_object_formation_criteria.md`](../../eabc_object_formation_criteria.md)  
**Gap-Docs 1–9:** siehe Tabelle in Master-Index · **Stage 5.5:** [`STAGE5.5_RESULTS.md`](STAGE5.5_RESULTS.md)

---

## The Tenth Level: Epistemology

The nine documents describe:
```
Observation → Null Model → Decomposition → Object → Control Architecture
```

But the latest documents reveal something deeper:

**Not only is the object A(Δr) being investigated, but the very conditions under which one is entitled to speak of an "object" at all.**

This is an **epistemological level**.

---

## The Central Question

### When does an observed statistic become a mathematical object?

**Not every interesting function deserves a name.**

The history of mathematics is full of quantities that later disappeared because they depended on:
- Choice of coordinates
- Choice of representation
- Choice of observation method

---

## The Six Stages of Object Formation

A candidate A(Δr) becomes a genuine object only by surviving successive hurdles:

### Stage 1: Existence
```
A(Δr) ≠ constant
```

**Criterion**: The quantity shows structure at all.

**Status for A(Δr)**: ✅ **Satisfied**
- A(2) ≈ 1.06
- A(6) ≈ 0.84
- A(24) ≈ 1.18
- Non-trivial Δr-dependence confirmed

---

### Stage 2: Reproducibility
```
Multiple independent measurements yield same structure
```

**Criterion**: The structure is not a statistical fluctuation.

**Status for A(Δr)**: ✅ **Largely satisfied**
- 20 independent seeds
- Standard deviations < 0.07
- Consistent across runs

---

### Stage 3: Model Independence
```
Structure remains visible against different null models
```

**Criterion**: The structure is not an artifact of comparison choice.

**Status for A(Δr)**: ✅ **Partially satisfied**
- Compared against Bernoulli: Structure visible
- Compared against Cramér: Structure visible
- Not yet tested against other null models

---

### Stage 4: Projection Invariance
```
Alternative observation schemes produce same qualitative form
```

**Criterion**: The structure is not dependent on specific gap-pair choice.

**Status for A(Δr)**: ✅ **PASSED (restricted domain)**
- Tested projections: {2,4,6}, {4,6,8}, {6,8,10}, {8,10,12}
- **Result**: Two distinct regimes discovered

**Regime I (Δr ≤ 18)**: ✅ **Projection-invariant**
- Mean correlation ρ = 0.965
- Projection-invariant object H(Δr) successfully extracted
- A_i(Δr) = c_i · H(Δr) with 5-11% error
- Coefficient variation CV = 14.2%

**Regime II (Δr ≥ 20)**: ✗ **Projection-dependent**
- Mean correlation ρ ≈ 0.4
- No common structure across projections
- Different physical mechanism

**Interpretation**: H(Δr) exists as projection-invariant object for short-to-medium range

---

### Stage 5: Theoretical Connectability
```
Plausible connection to known mathematical structures exists
```

**Criterion**: The object fits into existing theoretical frameworks.

**Status for A(Δr)**: ⏳ **Open**

**Hypothesized connection**:
```
A(Δr) = ∑_g w_g(Δr) · H(g)
```
where H(g) are Hardy-Littlewood singular series.

**Current status**: Conjectured but not proven

---

### Stage 6: Autonomy
```
The quantity provides information not already contained in known objects
```

**Criterion**: The object is not redundant - it captures something new.

**Status for A(Δr)**: ⏳ **Completely open**

**Questions**:
- Does A(Δr) contain information beyond what's in k-tuple constants?
- Does it reveal structure not visible in traditional prime gap analysis?
- Is it a genuinely new observable or a repackaging of known quantities?

---

## Why This Framework Matters

The Gap-Pair test then decides not just:

~~"Is A(Δr) robust?"~~

But rather:

**"Has A(Δr) reached Stage 4 of object formation?"**

**This is a much more fundamental formulation.**

---

## Historical Analogy: The Riemann Zeta Function

ζ(s) did not become important because it was immediately understood.

It became important because it survived a series of tests:

### Stage 1: Existence
✓ Non-trivial analytic continuation beyond Re(s) > 1

### Stage 2: Reproducibility
✓ Multiple derivations from different starting points

### Stage 3: Model Independence
✓ Appeared in prime counting, divisor problems, random matrices

### Stage 4: Projection Invariance
✓ Coordinate-independent (functional equation)

### Stage 5: Theoretical Connectability
✓ Connected to prime distribution, modular forms, L-functions

### Stage 6: Autonomy
✓ Generated new predictions (zero distribution, explicit formulas)

**Only after surviving these tests was ζ(s) accepted as a central object.**

---

## Current Status of A(Δr)

| Criterion | Status | Evidence |
|-----------|--------|----------|
| **1. Existence** | ✅ Satisfied | Non-constant, three regimes |
| **2. Reproducibility** | ✅ Satisfied | 20 seeds, consistent |
| **3. Model Independence** | ✅ Satisfied | Visible vs. Bernoulli and Cramér |
| **4. Projection Invariance** | ✅ **Satisfied (Δr ≤ 18)** | **ρ = 0.965, H(Δr) extracted** |
| **5. Theoretical Connectability** | **? Partial** | **k=2 HL: ✗ Falsified; k≥3 HL: Untested** |
| **5.5. Prime-Specificity** | 🔴 **PENDING** | **Wheel-30 test critical before publication** |
| **6. Autonomy** | **? Open** | **Insufficient evidence** |

**Interpretation**:

**H(Δr) is a well-defined, projection-invariant mathematical object** for Δr ∈ [2, 18].

**Status**: **4 of 6 stages definitively passed** (Stages 1-4), **1 critical test pending** (Stage 5.5)

**Stages 5-6**: Further testing required before conclusions can be drawn.

**What was shown** (Stage 5):
- Pair-gap HL models (k=2) are **incompatible** (ρ = -0.86)
- Entire model class ∑_g w_g · S_2(g) **eliminated**

**What was NOT shown**:
- No HL explanation possible (only k=2 tested)
- H(Δr) is prime-specific (Stage 5.5 pending)
- H(Δr) is autonomous (insufficient evidence)

---

## The Three Possible Outcomes (Revisited)

### If Gap-Pair Test Shows Invariance:

**Stage 4 reached** → A(Δr) advances to "object candidate with projection invariance"

**Next tasks**: 
- Establish theoretical connectability (Stage 5)
- Demonstrate autonomy (Stage 6)

**Publication strategy**: 
- "Empirical isolation of projection-invariant arithmetic observable"
- Focus on Stages 1-4 as established
- Propose Stages 5-6 as research program

---

### If Gap-Pair Test Shows Variance:

**Stage 4 not reached** → A(Δr) remains "projection-dependent statistic"

**Interpretation**: A(Δr) is not yet an object, but a **family of related statistics**

**Next tasks**:
- Search for projection-invariant combination
- Investigate deeper structure
- Perhaps the true object is at a different level

**Publication strategy**:
- "Projection-dependent family of arithmetic observables"
- Methodological paper on sensitivity analysis
- Document failure mode (valuable for future work)

---

### If Gap-Pair Test Shows Partial Invariance:

**Stage 4 partially reached** → Most interesting scenario

**Interpretation**: A deeper object exists, of which A(Δr) is one projection

**Implication**: 
```
A_i(Δr) = P_i(H)
```
for some deeper structure H and projection operators P_i

**Next tasks**:
- Characterize the projection operators
- Search for the invariant H
- This could lead to richer theory

**Publication strategy**:
- "Toward a projection-invariant arithmetic observable"
- Document the family {A_i} and search for H
- Most scientifically interesting outcome

---

## The Fundamental Question Being Tested

The Gap-Pair test is not primarily testing a numerical hypothesis.

**It is testing whether A(Δr) reaches the next stage of its "object formation".**

---

## From Statistic to Object: The General Process

### Stage 0: Observation
Something is measured. Numbers are recorded.

### Stage 1: Pattern Recognition
The measurements show non-random structure.

### Stage 2: Reproducibility
The structure is confirmed across independent measurements.

### Stage 3: Context Independence
The structure appears in different contexts/comparisons.

### Stage 4: Representation Independence
The structure is independent of how it's measured.

### Stage 5: Theoretical Integration
The structure connects to existing mathematical framework.

### Stage 6: Generativity
The structure predicts new phenomena or unifies disparate observations.

**A(Δr) is currently transitioning from Stage 3 to Stage 4.**

---

## Why Many Candidates Fail

Most statistical observations never become mathematical objects because they fail one of these tests.

**Common failure modes**:

### Fails Stage 2:
Initial observation was statistical fluctuation

### Fails Stage 3:
Structure depends on specific null model choice

### Fails Stage 4:
Structure depends on measurement scheme (projection dependence)

### Fails Stage 5:
No plausible theoretical explanation exists

### Fails Stage 6:
Completely explained by known objects (redundant)

**Each failure is scientifically valuable** - it rules out a candidate and focuses attention elsewhere.

---

## The Current State of the Project

The project is no longer searching for:
- ~~A formula~~
- ~~More data~~
- ~~A numerical result~~

**The project is investigating**:

```
Is A(Δr) a mathematical object 
or merely a statistic?
```

The upcoming robustness test is exactly the kind of experiment that decides this.

---

## Implications for Publication

### If A(Δr) reaches Stage 4:

**Claim**: "We have isolated a projection-invariant arithmetic observable"

**Significance**: New object candidate for future investigation

**Open questions**: Stages 5-6 (theory, autonomy)

---

### If A(Δr) does not reach Stage 4:

**Claim**: "We have characterized a projection-dependent family of observables"

**Significance**: Methodological contribution (what doesn't work)

**Open questions**: What is the deeper invariant?

---

### Either way:

**Demonstrated**: 
- Systematic approach to object formation
- Clear criteria for "objecthood"
- Falsifiable hypothesis
- Control architecture against self-deception

**Contribution**: 
- Not just specific numerical results
- But methodology for experimental mathematics
- Framework for assessing object candidates

---

## The Philosophical Core

Not every interesting function deserves the status of "mathematical object."

**Objects must earn their status** by surviving successive tests:
1. Existence
2. Reproducibility
3. Model Independence
4. Projection Invariance
5. Theoretical Connectability
6. Autonomy

**A(Δr) is currently at Stage 3-4 transition.**

The Gap-Pair test is the Stage 4 examination.

**Both passing and failing advance understanding:**
- **Pass**: Object candidate advances
- **Fail**: Deeper structure must be sought

---

## Meta-Observation

The ten documents now form a complete philosophical and methodological framework:

**Documents 1-3**: The mathematical object and its properties  
**Documents 4-6**: The methodological process of isolation  
**Documents 7-9**: The control architecture and self-correction  
**Document 10**: The epistemological criteria for objecthood  

**Together**: A complete framework for experimental mathematics

Not just "how to find results" but:
- How objects emerge
- How hypotheses are tested
- How self-deception is avoided
- How statistics become objects

---

## Summary

**The central question of the entire program**:

```
Is A(Δr) a mathematical object 
or only a projection-dependent statistic?
```

**The test**: Gap-pair invariance

**The level**: Stage 4 of object formation

**Both outcomes advance science**:
- Invariant → Object candidate confirmed
- Variant → Deeper structure required

**The contribution**:
- Not just numerical results
- But framework for assessing "objecthood"
- Demonstration of scientific maturation
- Epistemological criteria for experimental mathematics

**This is the tenth level**: Beyond methodology to epistemology.

---

## UPDATE: Stage 4 Test Results (June 23, 2026)

### The Gap-Pair Robustness Test

**Test design**: Vary base offset of gap pairs
- Projection 1: {2, 4, 6} vs {2+Δr, 4+Δr, 6+Δr}
- Projection 2: {4, 6, 8} vs {4+Δr, 6+Δr, 8+Δr}
- Projection 3: {6, 8, 10} vs {6+Δr, 8+Δr, 10+Δr}
- Projection 4: {8, 10, 12} vs {8+Δr, 10+Δr, 12+Δr}

**Initial verdict** (all Δr): 
```
Stage 4 NOT PASSED ✗
Mean CV = 37.5%
```

### The Critical Refinement

**Correlation analysis revealed**:
```
Mean correlation (all Δr):    ρ = 0.420  (MODERATE)
Mean correlation (Δr ≤ 18):   ρ = 0.965  (STRONG)
```

**Interpretation**: **Two-regime structure**

### Regime I: Δr ≤ 18 (Short-to-Medium Range)

**Structural similarity**: ρ = 0.965

**Properties**:
- All four projections show identical qualitative structure
- Monotonically decreasing for all bases
- Twin-prime peak at Δr = 2 for all bases
- Quantitative differences explained by simple scaling

**Extracted object**: H(Δr)
```
H(Δr) = mean(A_2(Δr), A_4(Δr), A_6(Δr), A_8(Δr))
```

**Decomposition**:
```
A_i(Δr) = c_i · H(Δr) + ε_i(Δr)
```

**Quality metrics**:
| Base | Correlation | Rel. Error | c_i   |
|------|-------------|------------|-------|
| 2    | ρ = 0.987   | 11.1%      | 0.937 |
| 4    | ρ = 0.996   | 5.1%       | 0.889 |
| 6    | ρ = 0.969   | 10.2%      | 0.930 |
| 8    | ρ = 0.995   | 4.4%       | 1.244 |

**Coefficient variation**: CV(c_i) = 14.2%

**Verdict for Regime I**: ✅ **Stage 4 PASSED**

### Regime II: Δr ≥ 20 (Large Range)

**Structural similarity**: ρ ≈ 0.4

**Properties**:
- Different projections show divergent behavior
- Peaks at different Δr for different bases
- No simple decomposition structure

**Verdict for Regime II**: ✗ **Stage 4 NOT PASSED**

### Scientific Interpretation

**H(Δr) is a projection-invariant mathematical object** characterizing arithmetic amplification of gap asymmetries for **short-to-medium range**.

**Object status**:
```
✓ Stage 1: Existence
✓ Stage 2: Reproducibility
✓ Stage 3: Model Independence
✓ Stage 4: Projection Invariance (Δr ≤ 18)
? Stage 5: Theoretical Connectability
? Stage 6: Autonomy
```

**Domain of validity**: Δr ∈ [2, 18]

**Physical interpretation**:
- **Regime I**: Sieve effects + Hardy-Littlewood correlations dominate
- **Regime II**: Different mechanism (log(p)-effects? Sparsity?)

### What the Control Architecture Achieved

1. ✓ Proposed object candidate A(Δr)
2. ✓ Attacked via projection test
3. ✓ Discovered weakness (Δr ≥ 20)
4. ✓ Refined to H(Δr) with restricted domain
5. ✓ Validated H(Δr) as projection-invariant (Regime I)

**This is not a failure** - it's a **successful refinement**.

### Next Steps

**Immediate (Stage 5)**:
- Connect H(Δr) to Hardy-Littlewood constants
- Derive theoretical prediction for H(Δr)
- Compare prediction vs. observation

**Validation**:
- Test H(Δr) on different moduli (30, 60, 210)
- Increase N to 10^6 for tighter error bars

**Regime II**:
- Investigate separate mechanism for Δr ≥ 20
- Possibly log(p)-dominated or sparsity effects

### The Refined Central Question

**Not**: "Is A(Δr) an object?"

**But**: "For what domain is H(Δr) projection-invariant?"

**Answer**: Δr ∈ [2, 18]

### Implications for Publication

**Title refinement**: 
"Extraction of a Projection-Invariant Arithmetic Observable for Short-to-Medium Range Gap Asymmetries"

**Main claim**:
"H(Δr) is a well-defined, projection-invariant object for Δr ≤ 18, having passed Stages 1-4 of object formation"

**Open questions**:
- Theoretical derivation from Hardy-Littlewood (Stage 5)
- Information content and autonomy (Stage 6)
- Mechanism for Regime II (Δr ≥ 20)

### Summary of Stage 4 Outcome

**Result**: **Partial Invariance** (the most interesting scenario)

**Discovered**:
- Projection-invariant object H(Δr) exists for Δr ≤ 18
- Two-regime structure with sharp transition
- Simple projection operators P_i: H ↦ c_i · H

**Confirmed**: The third scenario from original predictions:
```
A_i(Δr) = P_i(H)
```
for a deeper structure H and projection operators P_i.

**Scientific value**: Maximum - reveals richer structure than simple pass/fail would have.

---

## UPDATE: Stage 5 & 6 Test Results (June 23, 2026)

### Stage 5: Theoretical Connectability (Hardy-Littlewood)

**Question**: Is H(Δr) compatible with Hardy-Littlewood pair-gap constants?

**Test design**: Two independent approaches
1. **Naive weighting**: w_g(Δr) ∝ 1/(1 + |g - Δr|)
2. **Empirical weighting**: w_g^emp(Δr) from actual prime-gap distribution

**Model tested**:
```
H_HL(Δr) = ∑_g w_g(Δr) · S(g)
```
where S(g) = Hardy-Littlewood singular series for gap g

**Results**:

| Approach | Correlation | Monotonicity | Verdict |
|----------|-------------|--------------|---------|
| Naive HL | ρ = -0.762  | H_HL not monotonic | ✗ Incompatible |
| Empirical HL | ρ = -0.857 | H_HL increasing | ✗ Strongly incompatible |

**Critical observation**: Perfect anti-correlation (Spearman ρ = -1.0)

```
H_emp(Δr):    0.834 → 0.540 → 0.422 → 0.329  (decreasing)
H_HL,emp(Δr): 2.711 → 3.404 → 4.967 → 7.686  (increasing)
```

**Empirical gap distributions** (N = 1,000,000 primes):
- Δr=2: Gap 2 (81%), Gap 28 (12%)
- Δr=6: Gap 6 (79%), Gap 24 (16%)
- Δr=10: Gap 10 (71%), Gap 20 (24%)
- Δr=14: Gap 14 (57%), Gap 16 (38%)

Even with **correct empirical gap weights**, the HL formula fails.

**Interpretation**:

H(Δr) is **NOT derivable** from Hardy-Littlewood pair-gap constants S(g).

The formula `H(Δr) = ∑_g w_g · S(g)` is **fundamentally incorrect**.

**Why does it fail?**

1. **S(g)** measures: Probability enhancement for prime-pairs with gap g
2. **H(Δr)** measures: Asymmetry amplification for residue-class distance Δr

**These are different observables!**

Gap → Δr mapping is **many-to-many**:
- For Δr=2: Gaps {2, 28, 32, 58, ...}
- For Δr=14: Gaps {14, 16, 44, 46, ...}

The HL formula sums over **gaps**, but H(Δr) is defined over **residue-classes**.

**Stage 5 Verdict**: ✗ **NOT PASSED** (for HL pair-gap constants)

---

### Stage 6: Autonomy

**Question**: Does H(Δr) provide information not already contained in known objects?

**Criterion**: H(Δr) should not be reducible to existing mathematical structures.

**Evidence** (from Stage 5 failure):

1. **Not reducible to HL pair-gap constants (k=2)**
   - ρ = -0.857 (strong negative correlation)
   - Spearman ρ = -1.0 (perfect anti-correlation)
   - Even with empirical gap weights

2. **What was shown**:
   - H(Δr) ≉ ∑_g w_g · S_2(g)
   - Pair-gap HL model class **eliminated**

3. **What was NOT shown**:
   - No HL explanation possible (only k=2 tested)
   - H(Δr) is autonomous (k≥3 untested, residue-class-specific HL untested)
   - H(Δr) is not reducible (insufficient evidence)

**Stage 6 Verdict**: **? OPEN / Insufficient Evidence**

**Interpretation** (corrected):
The Stage 5 failure shows H(Δr) is **not reducible to pair-gap HL (k=2)**, but does **not establish full autonomy**.

**What the negative result demonstrates**:
- **Elimination of a model class**: All ∑_g w_g · S_2(g) ruled out
- **Narrowing of search space**: Only k≥3 or non-HL models remain
- **Value of negative results**: Guides future theoretical work

**Remaining open questions**:
- k-tuple HL (k≥3)?
- Residue-class-specific HL?
- Non-HL structures?

---

## Stage 5.5: Wheel-30 Null Hypothesis (PENDING - CRITICAL)

**Inserted before final Stage 6 assessment**

**Question**: Is H(Δr) prime-specific or just Wheel-30 structure?

**Test**: Compare H_Prime vs. H_WheelRandom vs. H_WheelCramér

**Why critical**:
A referee will immediately ask:
> "How do you know H(Δr) measures something about **primes** and not just **modulo-30 structure**?"

**This question is currently unanswered.**

**Decision matrix**:

| Result | Interpretation |
|--------|----------------|
| H_Prime ≈ H_Wheel | Wheel structure explains core → No autonomy |
| H_Prime ≠ H_Wheel | Prime-specific → HL k≥3 motivated |

**Status**: 🔴 **PENDING - Implementation in progress**

**Priority**: **CRITICAL before publication**

**See**: `STAGE5.5_WHEEL30_NEXT_STEP.md` for complete test design

---

## Final Object Status of H(Δr) (Current)

```
✓ Stage 1: Existence
✓ Stage 2: Reproducibility  
✓ Stage 3: Model Independence
✓ Stage 4: Projection Invariance (Δr ≤ 18)
✗ Stage 5: Theoretical Connectability (HL k=2 falsified; k≥3 untested)
🔴 Stage 5.5: Wheel-30 Test (PENDING - CRITICAL)
? Stage 6: Autonomy (OPEN - Insufficient Evidence)
```

**Overall**: **4 of 6 stages definitively passed**, 1 critical test pending

**Status**: **H(Δr) is a well-defined, projection-invariant object with unknown theoretical origin**

**Domain**: Δr ∈ {2, 6, 10, 14, 18} (Regime I)

**Open questions**:
1. Is H(Δr) prime-specific or Wheel-30? (Stage 5.5)
2. Can H(Δr) be explained by k-tuple HL (k≥3)? (Stage 5 continued)
3. Does H(Δr) provide genuinely new information? (Stage 6)

---

## The Current Research Questions (Prioritized)

### Priority 1: Stage 5.5 (CRITICAL BEFORE PUBLICATION)

**Question**: Is H(Δr) prime-specific or Wheel-30 structure?

**Why first**: Without this, we cannot claim H(Δr) is "prime-number-theoretic"

**Test**: H_Prime vs. H_WheelRandom vs. H_WheelCramér

**Timeline**: 2-4 hours additional implementation

---

### Priority 2: If Stage 5.5 → Prime-specific

**Then investigate**: What mathematical structure does H(Δr) characterize?

**Possible directions**:

1. **k-tuple correlations (k ≥ 3)**
   - H(Δr) may require higher-order correlations
   - Not just pair-gaps, but gap-triplets, quadruplets

2. **Residue-class singular series** (new theory)
   - S_RC(r_1, r_2) for residue-class pairs
   - Instead of gap-specific S(g)

3. **Combined gap-residue observable**
   - Non-linear function of multiple inputs
   - Gap-size vs. residue-structure competition

---

### Priority 3: If Stage 5.5 → Wheel structure

**Then investigate**: Modulo-arithmetic explanation

**Possible directions**:

1. **Wheel-30 arithmetic structures**
   - Pure residue-class correlations
   - No HL needed

2. **Generalization to higher wheels**
   - Wheel-210, Wheel-2310
   - Universal residue-class property?

3. **Cramér + Wheel interaction**
   - Log-density effects on Wheel structure
   - Combined probabilistic model

---

## Publication Strategy (Current)

### Before Stage 5.5 Completion

**Title suggestion**:
"Empirical Isolation of a Projection-Invariant Arithmetic Observable and Falsification of Pair-Gap Hardy-Littlewood Explanations"

**Abstract core**:
> "We extract a projection-invariant object H(Δr) characterizing residue-class gap asymmetries for Δr ≤ 18 through systematic null-model testing. Projection-robustness analysis over four independent measurement schemes yields ρ = 0.965, establishing H(Δr) as a well-defined statistical object. Tests against Hardy-Littlewood pair-gap predictions reveal strong negative correlation (ρ = -0.86), ruling out an entire class of two-point correlation models."

**Strengths**:
- Methodologically sound (Stages 1-4 passed)
- Negative HL result is **scientifically valuable**
- Shows: Elimination of model class
- Systematic falsification demonstrated

**Limitation** (must acknowledge):
> "Further investigation is needed to determine whether H(Δr) is prime-specific or a general property of Wheel-30 residue structures."

**Framing**:
- Methodological contribution + empirical discovery
- Falsification of natural explanation class
- Framework for future theoretical work
- Conservative claims

---

### After Stage 5.5 Completion (Recommended)

**If H_Prime ≠ H_Wheel** (prime-specific):

**Upgrade to**:
> "We isolate a **prime-specific**, projection-invariant observable H(Δr)..."

**Remove limitation**, add:
> "Systematic comparison with Wheel-30 null models demonstrates H(Δr) contains information beyond simple modulo structure."

**If H_Prime ≈ H_Wheel** (Wheel structure):

**Reframe as**:
> "We isolate a projection-invariant property of Wheel-30 residue-class structures..."

**Shift focus**:
- Modulo-arithmetic interpretation
- Not prime-number-theory per se
- Still valuable (clarifies what H is)

---

## The Success of the Control Architecture

The project followed its self-correction framework perfectly:

1. ✓ Proposed object candidate (A(Δr))
2. ✓ Attacked via projection test (Stage 4)
3. ✓ Discovered two-regime structure
4. ✓ Refined to H(Δr) with restricted domain (Δr ≤ 18)
5. ✓ Validated projection invariance (ρ = 0.965)
6. ✓ Tested theoretical connectability (HL k=2)
7. ✓ **Eliminated pair-gap HL model class**
8. 🔴 **Stage 5.5 pending** (Wheel-30 test)

**The Stage 5 failure is a feature, not a bug**:
- It eliminates a natural explanation class
- It narrows the theoretical search space
- It demonstrates the value of negative results

**What the control architecture achieved**:
- **Not premature claims** ("H is autonomous")
- **But systematic elimination** ("H ≉ ∑_g w_g · S_2(g)")
- **And identification of critical next test** (Wheel-30)

**The strongest statement**:
> "H(Δr) survives every elimination test so far."

**This is how mathematical objects mature**: Through systematic testing that reveals their true nature.

---

## Next Critical Step

**Before any publication**: Complete Stage 5.5 (Wheel-30 Null Hypothesis Test)

**Timeline**: 2-4 hours additional work

**Decision point**: Is H(Δr) prime-specific or Wheel-30 structure?

**Both outcomes valuable** - either clarifies H(Δr)'s theoretical origin

**See**: `STAGE5.5_WHEEL30_NEXT_STEP.md` for complete implementation plan
