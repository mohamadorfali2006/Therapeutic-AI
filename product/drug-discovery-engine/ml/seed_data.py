"""DDE seed dataset — demonstration-grade training data, owned by CDD.

Curation policy (see company/cdd): molecules are common, well-known compounds
with approximate octanol-water logP reference values. Target values are
approximate literature landmarks used ONLY to exercise the demo pipeline and NOT
for regulatory or medical use. Research use only.

Format: SDF-style simple tuples (smiles, target_logp).
Properties supported by the DDE foundation: "logp".
"""

from __future__ import annotations

DEMO_TARGETS = [
    {"id": "logp", "name": "logP (octanol/water)", "task": "regression", "unit": ""},
]

SEED_DATA: list[tuple[str, float]] = [
    ("CCO", -0.14),
    ("C[C@H](O)C", -0.07),
    ("CCCCO", 0.88),
    ("CC(C)(C)O", 0.35),
    ("C1=CC=CC=C1", 2.13),
    ("C1=CC=C(C=C1)C", 2.69),
    ("C1=CC=C(C=C1)O", 1.46),
    ("C1=CC=C(C=C1)N", 0.90),
    ("C1=CC=C(C=C1)Cl", 2.84),
    ("C1=CC=C(C=C1)Br", 3.01),
    ("C1=CC=C(C=C1)C(F)(F)F", 3.01),
    ("C1=CC=CC2=CC=CC=C12", 3.45),
    ("C1=CC=C2C(=C1)C=CC=C2", 3.45),
    ("c1ccccc1c2ccccc2", 3.85),
    ("CCN(CC)CC", 0.71),
    ("CCOC(=O)C", 0.66),
    ("CC(C)C(=O)O", 1.20),
    ("CC(=O)C", -0.24),
    ("CCCCCC", 4.03),
    ("CCCCCCCC", 5.10),
    ("CC1=CC=C(C=C1)C", 3.15),
    ("C1=CC(=CC=C1C)C", 3.15),
    ("COC", -0.15),
    ("C(C)O", -0.14),
    ("C1CCCCC1", 2.81),
    ("C1CCC(CC1)O", 1.23),
    ("C1CCC(CC1)N", 1.49),
    ("CC(=O)O", -0.17),
    ("C(N)", -0.83),
    ("CS(=O)C", -1.55),
    ("CC#N", -0.20),
    ("CCC=O", 0.33),
    ("CC(C)C", 2.07),
    ("CCCl", 1.54),
    ("CCCCl", 2.02),
    ("CBr", 1.60),
    ("CCBr", 1.82),
    ("CCI", 2.00),
    ("CCCC(N)C(=O)O", -1.50),
    ("NC(=O)C", -1.24),
    ("C1=CC=C(C=C1)C(C)C", 3.32),
    ("CC1=CC=CC=C1O", 2.10),
    ("C1=CC=C(C=C1)OC", 2.11),
    ("C1=CC=C(C=C1)S", 3.50),
    ("C1=CC=C(C=C1)S(=O)(=O)N", 0.60),
    ("FC(F)(F)C1=CC=CC=C1", 2.98),
    ("C1=CC2=C(C=C1)C3=C(C=CC=C3)C=C2", 5.19),
    ("CC(C(O)=O)(C)O", -0.32),
    ("C1=CSC=C1", 1.81),
    ("C1=CC=NC=C1", 0.65),
    ("C1=CN=CC=C1", 0.65),
    ("C1=CC=CC=N1", 0.73),
    ("C1CCNCC1", 0.00),
    ("C1CNCCC1", 0.00),
    ("CC(=O)C1=CC=CC=C1", 1.87),
    ("OC1=CC=CC=C1C(=O)O", 2.26),
    ("C1=CC2=C(C=C1)N=C(C=C2)O", 2.20),
]


def load_seed_data() -> list[tuple[str, float]]:
    return list(SEED_DATA)


def target_range() -> tuple[float, float]:
    vals = [t for _, t in SEED_DATA]
    return min(vals), max(vals)


if __name__ == "__main__":  # pragma: no cover
    lo, hi = target_range()
    print(f"seed records: {len(SEED_DATA)}  target range: ({lo:.2f}, {hi:.2f})")