import Mathlib.Data.Set.Basic -- Import for Set, ∩, and ⊆

/--
The intersection of two sets A and B is a subset of A.
-/
theorem intersection_subset_left {α : Type*} (A B : Set α) : A ∩ B ⊆ A := by
  -- 1. Unfold the definition of subset: ∀ x, x ∈ A ∩ B → x ∈ A
  intro x hx
  -- 2. hx is a proof that x ∈ A ∩ B (which is defined as x ∈ A ∧ x ∈ B)
  -- We use 'cases' to split this conjunction
  cases hx with
  | intro x_in_A x_in_B =>
    -- 3. We now have two hypotheses:
    -- x_in_A : x ∈ A
    -- x_in_B : x ∈ B
    -- We need to prove x ∈ A, which is exactly x_in_A
    exact x_in_A

-- Alternative short proof using library tactics
theorem intersection_subset_left_short {α : Type*} (A B : Set α) : A ∩ B ⊆ A :=
  Set.inter_subset_left A B
