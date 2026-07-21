/-
P2-T05 machine-checked finite-group selector kernel.

Status: draft/control and proposal-only mathematical support.

The definitions below formalize only the one-object group-action core of the
unchanged P2-T03 theorem. They do not assert that current ontology supplies
the group, action, eligible-choice type, or selector; do not identify a
structural action with physical gauge; and do not authorize any downstream
physics or promotion claim.
-/

import Init

universe u v

namespace EqSrcSelectorKernel

/-- Minimal group data required by the task-local action kernel. -/
structure GroupData (G : Type u) where
  one : G
  mul : G → G → G
  inv : G → G
  one_mul : ∀ g, mul one g = g
  mul_one : ∀ g, mul g one = g
  mul_assoc : ∀ g h k, mul (mul g h) k = mul g (mul h k)
  inv_mul : ∀ g, mul (inv g) g = one
  mul_inv : ∀ g, mul g (inv g) = one

/-- A left action of the declared group data on an eligible-choice type. -/
structure Action (G : Type u) (D : Type v) (group : GroupData G) where
  act : G → D → D
  one_act : ∀ x, act group.one x = x
  mul_act : ∀ g h x, act (group.mul g h) x = act g (act h x)

/-- An eligible choice is fixed when every declared structural action fixes it. -/
def Fixed {G : Type u} {D : Type v} {group : GroupData G}
    (action : Action G D group) (x : D) : Prop :=
  ∀ g, action.act g x = x

/-- In the one-object groupoid core, an invariant selector is exactly a fixed choice. -/
def InvariantSelector {G : Type u} {D : Type v} {group : GroupData G}
    (action : Action G D group) : Type v :=
  {x : D // Fixed action x}

/-- The declared action is transitive when any eligible choice can reach any other. -/
def Transitive {G : Type u} {D : Type v} {group : GroupData G}
    (action : Action G D group) : Prop :=
  ∀ x y, ∃ g, action.act g x = y

/-- Empty fixed locus is equivalent to absence of an invariant selector. -/
theorem empty_fixed_iff_no_invariant_selector
    {G : Type u} {D : Type v} {group : GroupData G}
    (action : Action G D group) :
    (¬ ∃ x, Fixed action x) ↔ ¬ Nonempty (InvariantSelector action) := by
  constructor
  · intro hFixed hSelector
    rcases hSelector with ⟨selector⟩
    exact hFixed ⟨selector.1, selector.2⟩
  · intro hSelector hFixed
    rcases hFixed with ⟨x, hx⟩
    exact hSelector ⟨⟨x, hx⟩⟩

/-- Under transitivity, any fixed choice equals every eligible choice. -/
theorem fixed_choice_unique_of_transitive
    {G : Type u} {D : Type v} {group : GroupData G}
    {action : Action G D group}
    (hTransitive : Transitive action) {x : D} (hFixed : Fixed action x)
    (y : D) : y = x := by
  rcases hTransitive x y with ⟨g, hg⟩
  calc
    y = action.act g x := hg.symm
    _ = x := hFixed g

/-- A transitive action on a type with two distinct choices has no invariant selector. -/
theorem no_invariant_selector_of_transitive_distinct
    {G : Type u} {D : Type v} {group : GroupData G}
    {action : Action G D group}
    (hTransitive : Transitive action) {a b : D} (hDistinct : a ≠ b) :
    ¬ Nonempty (InvariantSelector action) := by
  intro hSelector
  rcases hSelector with ⟨selector⟩
  have ha : a = selector.1 :=
    fixed_choice_unique_of_transitive hTransitive selector.2 a
  have hb : b = selector.1 :=
    fixed_choice_unique_of_transitive hTransitive selector.2 b
  exact hDistinct (ha.trans hb.symm)

/-- Two distinct fixed choices produce two distinct invariant selectors. -/
theorem multiple_fixed_gives_multiple_selectors
    {G : Type u} {D : Type v} {group : GroupData G}
    {action : Action G D group}
    {x y : D} (hx : Fixed action x) (hy : Fixed action y) (hDistinct : x ≠ y) :
    ∃ sx sy : InvariantSelector action, sx ≠ sy := by
  refine ⟨⟨x, hx⟩, ⟨y, hy⟩, ?_⟩
  intro hEqual
  exact hDistinct (congrArg Subtype.val hEqual)

/-- The two-element group used by the preserved sign-swap control. -/
inductive C2 where
  | e
  | s
  deriving DecidableEq, Repr

def c2Mul : C2 → C2 → C2
  | .e, g => g
  | g, .e => g
  | .s, .s => .e

def c2Inv : C2 → C2
  | .e => .e
  | .s => .s

def c2Group : GroupData C2 where
  one := .e
  mul := c2Mul
  inv := c2Inv
  one_mul := by intro g; cases g <;> rfl
  mul_one := by intro g; cases g <;> rfl
  mul_assoc := by intro g h k; cases g <;> cases h <;> cases k <;> rfl
  inv_mul := by intro g; cases g <;> rfl
  mul_inv := by intro g; cases g <;> rfl

/-- The nontrivial element swaps the two historical sign choices. -/
def signSwap : C2 → Bool → Bool
  | .e, x => x
  | .s, x => !x

def signSwapAction : Action C2 Bool c2Group where
  act := signSwap
  one_act := by intro x; rfl
  mul_act := by intro g h x; cases g <;> cases h <;> cases x <;> rfl

theorem sign_swap_transitive : Transitive signSwapAction := by
  intro x y
  cases x <;> cases y
  · exact ⟨.e, rfl⟩
  · exact ⟨.s, rfl⟩
  · exact ⟨.s, rfl⟩
  · exact ⟨.e, rfl⟩

theorem false_ne_true : false ≠ true := by
  intro h
  cases h

/-- Preserved P2-T04 fixture FX-RESP-XEMPTY-SIGN-SWAP has no core selector. -/
theorem historical_sign_swap_no_invariant_selector :
    ¬ Nonempty (InvariantSelector signSwapAction) :=
  no_invariant_selector_of_transitive_distinct sign_swap_transitive false_ne_true

/-- A trivial action supplies the P2-T03/P2-T04 multiple-fixed control. -/
def trivialBoolAction : Action C2 Bool c2Group where
  act := fun _ x => x
  one_act := by intro x; rfl
  mul_act := by intro _ _ x; rfl

theorem trivial_false_fixed : Fixed trivialBoolAction false := by
  intro g
  cases g <;> rfl

theorem trivial_true_fixed : Fixed trivialBoolAction true := by
  intro g
  cases g <;> rfl

theorem trivial_action_has_multiple_selectors :
    ∃ sx sy : InvariantSelector trivialBoolAction, sx ≠ sy :=
  multiple_fixed_gives_multiple_selectors
    trivial_false_fixed trivial_true_fixed false_ne_true

#print axioms empty_fixed_iff_no_invariant_selector
#print axioms fixed_choice_unique_of_transitive
#print axioms no_invariant_selector_of_transitive_distinct
#print axioms multiple_fixed_gives_multiple_selectors
#print axioms historical_sign_swap_no_invariant_selector
#print axioms trivial_action_has_multiple_selectors

end EqSrcSelectorKernel
