"""DDE logS seed dataset — aqueous solubility proxy targets (logS = log10 of
molar aqueous solubility, mol/L), approximate literature landmarks,
research-use only, owned by CDD (see company/cdd).

Curation policy (see company/cdd): molecules are common, well-known compounds
with approximate logS reference values drawn from literature landmarks.
Target values are approximate and used ONLY to exercise the demo pipeline and
NOT for regulatory or medical use. Research use only.

Format: SDF-style simple tuples (smiles, target_logs).
Properties supported by the DDE foundation: "logS".
"""

from __future__ import annotations

DEMO_TARGETS = [
    {"id": "logS", "name": "logS (aqueous solubility proxy, log mol/L)", "task": "regression", "unit": ""},
]

SEED_DATA: list[tuple[str, float]] = [
    ("CCO", -0.1),
    ("C[C@H](O)C", -0.1),
    ("CCCCO", -0.5),
    ("CC(C)(C)O", -0.4),
    ("C1=CC=CC=C1", -1.6),
    ("C1=CC=C(C=C1)C", -2.4),
    ("C1=CC=C(C=C1)O", -0.5),
    ("C1=CC=C(C=C1)N", -0.7),
    ("C1=CC=C(C=C1)Cl", -2.4),
    ("C1=CC=C(C=C1)Br", -2.6),
    ("C1=CC=C(C=C1)C(F)(F)F", -2.9),
    ("C1=CC=CC2=CC=CC=C12", -3.6),
    ("C1=CC=C2C(=C1)C=CC=C2", -3.6),
    ("c1ccccc1c2ccccc2", -4.2),
    ("CCN(CC)CC", -1.0),
    ("CCOC(=O)C", -0.6),
    ("CC(C)C(=O)O", -0.3),
    ("CC(=O)C", -0.2),
    ("CCCCCC", -3.9),
    ("CCCCCCCC", -4.7),
    ("CC1=CC=C(C=C1)C", -2.9),
    ("C1=CC(=CC=C1C)C", -2.9),
    ("COC", -0.6),
    ("C(C)O", -0.1),
    ("C1CCCCC1", -3.1),
    ("C1CCC(CC1)O", -1.5),
    ("C1CCC(CC1)N", -1.8),
    ("CC(=O)O", -0.3),
    ("C(N)", -0.3),
    ("CS(=O)C", -0.4),
    ("CC#N", -0.4),
    ("CCC=O", -0.6),
    ("CC(C)C", -2.2),
    ("CCCl", -1.6),
    ("CCCCl", -2.0),
    ("CBr", -1.3),
    ("CCBr", -1.6),
    ("CCI", -1.8),
    ("CCCC(N)C(=O)O", -0.6),
    ("NC(=O)C", -1.0),
    ("C1=CC=C(C=C1)C(C)C", -3.1),
    ("CC1=CC=CC=C1O", -0.9),
    ("C1=CC=C(C=C1)OC", -1.7),
    ("C1=CC=C(C=C1)S", -3.2),
    ("C1=CC=C(C=C1)S(=O)(=O)N", -1.3),
    ("FC(F)(F)C1=CC=CC=C1", -2.9),
    ("C1=CC2=C(C=C1)C3=C(C=CC=C3)C=C2", -4.8),
    ("CC(C(O)=O)(C)O", -0.4),
    ("C1=CSC=C1", -1.6),
    ("C1=CC=NC=C1", -0.7),
    ("C1=CN=CC=C1", -0.7),
    ("C1=CC=CC=N1", -0.7),
    ("C1CCNCC1", -1.0),
    ("C1CNCCC1", -1.0),
    ("CC(=O)C1=CC=CC=C1", -2.1),
    ("OC1=CC=CC=C1C(=O)O", -1.5),
    ("C1=CC2=C(C=C1)N=C(C=C2)O", -2.2),
]


def load_seed_data() -> list[tuple[str, float]]:
    return list(SEED_DATA)


def target_range() -> tuple[float, float]:
    vals = [t for _, t in SEED_DATA]
    return min(vals), max(vals)


if __name__ == "__main__":  # pragma: no cover
    lo, hi = target_range()
    print(f"seed records: {len(SEED_DATA)}  target range: ({lo:.2f}, {hi:.2f})")
