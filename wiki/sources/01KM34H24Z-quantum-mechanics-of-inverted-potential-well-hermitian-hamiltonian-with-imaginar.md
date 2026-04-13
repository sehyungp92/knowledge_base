---
type: source
title: Quantum mechanics of inverted potential well -- Hermitian Hamiltonian with
  imaginary eigenvalues, quantum-classical correspondence
source_id: 01KM34H24ZGNDKDFK8E05MF8EH
source_type: paper
authors:
- Ni Liu
- J. -Q. Liang
published_at: '2025-05-01 00:00:00'
theme_ids: []
created: '2026-04-08'
updated: '2026-04-08'
claim_count: 19
tags: []
---
# Quantum mechanics of inverted potential well -- Hermitian Hamiltonian with imaginary eigenvalues, quantum-classical correspondence

**Authors:** Ni Liu, J. -Q. Liang
**Published:** 2025-05-01 00:00:00
**Type:** paper

## Analysis

# Quantum mechanics of inverted potential well -- Hermitian Hamiltonian with imaginary eigenvalues, quantum-classical correspondence
2025-05-01 · paper · Ni Liu, J. -Q. Liang
https://arxiv.org/abs/2505.00475

---

### Motivation & Prior Limitations
Prior work on Hermitian Hamiltonians with complex spectra — specifically for potentials unbounded below, such as the inverted potential well — had not been formulated self-consistently within the standard canonical commutation relation framework of quantum mechanics.
- The decay of metastable states in inverted potentials was previously studied using the instanton method under semiclassical approximation, which provided the imaginary part of eigenvalues as a decay rate but did not yield rigorous complex eigenvalues and their associated eigenstates within the full quantum mechanical formalism.
  - Liang & Müller-Kirsten (1992, 1994) treated the inverted double-well via instanton methods, an approximate technique that bypasses a direct algebraic solution.
- While non-Hermitian Hamiltonians with real spectra (PT-symmetric and pseudo-Hermitian systems) have been extensively studied since Bender & Boettcher (1998), the complementary case — a Hermitian Hamiltonian with a necessarily complex (pure imaginary) spectrum due to an unbounded-below potential — had not received a rigorous, algebraically complete treatment.
  - No prior work had established orthonormality conditions, coherent states, or quantum-classical correspondence for this class of system within the standard operator algebra.

---

### Proposed Approach
The paper solves the inverted potential well Hamiltonian H = p²/2 − ½ω²x² algebraically by introducing imaginary-frequency boson operators, analogous to the standard harmonic oscillator treatment but with the substitution of real frequency ω by an imaginary counterpart.
- Raising and lowering operators are defined with imaginary frequency: â₋ = (i/2)^(1/2)(x̂ + p̂) and â₊ = (i/2)^(1/2)(x̂ − p̂), satisfying the standard bosonic commutation relation [â₋, â₊] = 1.
  - The resulting number operator n̂ = â₊â₋ is non-Hermitian, yet its eigenvalues are real non-negative integers, making it pseudo-Hermitian.
- Because the number operator is non-Hermitian, the paper requires dual sets of eigenstates — "ket" states |n⟩ᵣ and "bra" states |n⟩ₗ corresponding to conjugate eigenvalue equations — with orthonormality defined between the two sets rather than within each.
  - The Hamiltonian eigenvalues are pure imaginary: Eₙ = iω ℏ(n + ½), consistent with the physical requirement that all eigenstates of an inverted potential are unstable.
- Wave functions (generating functions) are derived in coordinate representation: the "ket" ground state is ψ₀ʳ ∝ exp(−ix²/2) and the "bra" ground state is ψ₀ˡ ∝ exp(+ix²/2), both spatially non-localized, with normalization accomplished using an imaginary integration measure ∫ dx identical in form to the Feynman path integral measure.
- Coherent states are defined as eigenstates of the lowering operators for each dual set, and the SU(1,1) algebraic structure of the system is identified with Sᵤ anti-Hermitian and Sᵧ Hermitian, yielding H = 2iωℏ Sᵤ.

---

### Results & Capabilities
The paper establishes that the minimum uncertainty relation Δx·Δp = ½ is satisfied exactly in the imaginary-frequency coherent states, demonstrating that these states are the quantum analogue of classical phase-space trajectories.
- The position and momentum deviations are each computed to be √(−i/2) in magnitude, and their product equals ½ identically, matching the standard coherent-state result for the normal oscillator.

The probability average of the Heisenberg equation of motion in the coherent states reproduces the classical equation of motion ẍ = ω²x exactly, establishing quantum-classical correspondence in the imaginary-eigenvalue system.
- The coherent-state expectation value α(t) satisfies α̈ = ω²α, whose solution x(t) = ±(v/ω) sinh(ωt) is identical to the classical trajectory of a particle launched from the inverted potential top with initial velocity v.

The non-Hermitian density operator ρᵣ,ₗ = |ψ⟩ₗ ⟨ψ|ᵣ constructed between dual-set states is shown to be a dynamical invariant (dρ/dt = 0), consistent with the Schrödinger equation, even though the individual "bra" and "ket" probabilities are not conserved and grow or decay exponentially as e^(±2(n+½)ωt).

---

### Implications
This work provides the first self-consistent algebraic quantum mechanics of a Hermitian Hamiltonian with pure imaginary eigenvalues, filling a conceptual gap between the standard oscillator formalism and non-Hermitian/PT-symmetric quantum mechanics.
- The framework is directly relevant to sphaleron physics in φ⁴ field theory and to any quantum system with an unstable static solution at the top of a potential barrier, where the imaginary eigenvalue encodes the tunneling or decay rate.

The use of imaginary integration measure and non-localized wave functions, shown here to be consistent with the Feynman path integral formalism, suggests that path-integral and operator-algebraic approaches are mutually compatible for this class of unbounded potential and may generalize to field-theoretic instantons.

The demonstration that quantum-classical correspondence survives in the imaginary-eigenvalue setting extends Ehrenfest-type reasoning beyond the standard Hermitian, real-spectrum case and may inform semiclassical treatments of decay and tunneling in metastable quantum field configurations.

---

### Remaining Limitations & Next Steps
The treatment is restricted to the single-mode inverted harmonic potential H = p²/2 − ½ω²x², and no extension to multi-dimensional, anharmonic, or field-theoretic inverted potentials is attempted or discussed.
- In particular, the inverted double-well (which has a richer instanton structure studied in the authors' earlier work) is not treated algebraically here.

The physical interpretation of the imaginary integration measure and the non

## Key Claims

1. A Hermitian Hamiltonian with a potential unbounded below necessarily yields pure imaginary eigenvalues, because all eigenstates of an inverted potential well are unstable.
2. The inverted potential well Hamiltonian problem can be solved by an algebraic method using imaginary-frequency raising and lowering boson operators, analogous to the treatment of the normal harmonic o
3. Prior to this work, rigorous complex eigenvalues and associated eigenstates had not been derived within the framework of quantum mechanics for Hermitian Hamiltonians with potentials unbounded below.
4. The complex spectrum of an inverted double-well potential was previously studied using the instanton method under semiclassical approximation.
5. The boson number operator for the inverted potential well is non-Hermitian, yet its eigenvalues are real integers.
6. Dual sets of eigenstates ('bra' and 'ket') are required for the inverted potential well, corresponding respectively to complex conjugate eigenvalues.
7. An orthonormal condition exists between the 'bra' and 'ket' dual eigenstates: ⟨u_n^l|u_m^r⟩ = δ_nm.
8. The probability densities of both 'bra' and 'ket' eigenstates are not conserved quantities due to the unstable nature of the eigenstates.
9. The imaginary part of the energy eigenvalue characterizes the decay rate or lifetime of the metastable states.
10. Normalization of the bra–ket wave functions requires an imaginary integration measure, consistent with the Feynman path integral formalism.

## Themes
