"""DDE seed dataset — TPSA (Topological Polar Surface Area) demonstration property.

TPSA is a key descriptor for drug-likeness (Lipinski's rule of five).
Approximate values based on Ertl's fragment method (polar fragment contributions).
Values are approximate literature landmarks for demo purposes. Research use only.
"""

from __future__ import annotations

DEMO_TARGETS = [
    {"id": "tpsa", "name": "TPSA (Topological Polar Surface Area)", "task": "regression", "unit": "Å²"},
]

# Approximate TPSA values (Ertl method, fragment contributions)
# Polar fragments: -OH ~20, -NH2 ~26, -COOH ~37, -NO2 ~45, -O- ~9, =O ~17, -NH- ~12
SEED_DATA: list[tuple[str, float]] = [
    ("CCO", 20.23),           # ethanol: one -OH
    ("C[C@H](O)C", 20.23),    # isopropanol: one -OH
    ("CCCCO", 20.23),         # butanol: one -OH
    ("CC(C)(C)O", 20.23),     # tert-butanol: one -OH
    ("C1=CC=CC=C1", 0.0),     # benzene: no polar groups
    ("C1=CC=C(C=C1)C", 0.0),  # toluene: no polar groups
    ("C1=CC=C(C=C1)O", 20.23),         # phenol: one -OH
    ("C1=CC=C(C=C1)N", 26.02),         # aniline: one -NH2
    ("C1=CC=C(C=C1)Cl", 0.0),          # chlorobenzene: no polar groups
    ("C1=CC=C(C=C1)Br", 0.0),          # bromobenzene: no polar groups
    ("C1=CC=C(C=C1)C(F)(F)F", 0.0),    # trifluorotoluene: no polar groups
    ("C1=CC=CC2=CC=CC=C12", 0.0),      # naphthalene: no polar groups
    ("C1=CC=C2C(=C1)C=CC=C2", 0.0),    # anthracene fragment: no polar groups
    ("c1ccccc1c2ccccc2", 0.0),          # biphenyl: no polar groups
    ("CCN(CC)CC", 3.24),                # triethylamine: tertiary amine
    ("CCOC(=O)C", 26.3),                # ethyl acetate: one C=O + one C-O-C
    ("CC(C)C(=O)O", 37.3),              # isobutyric acid: one -COOH
    ("CC(=O)C", 17.07),                 # acetone: one C=O
    ("CCCCCC", 0.0),                    # hexane: no polar groups
    ("CCCCCCCC", 0.0),                  # octane: no polar groups
    ("CC1=CC=C(C=C1)C", 0.0),           # p-xylene: no polar groups
    ("C1=CC(=CC=C1C)C", 0.0),           # m-xylene: no polar groups
    ("COC", 9.23),                      # dimethyl ether: one C-O-C
    ("C(C)O", 20.23),                   # ethanol: one -OH
    ("C1CCCCC1", 0.0),                  # cyclohexane: no polar groups
    ("C1CCC(CC1)O", 20.23),             # cyclohexanol: one -OH
    ("C1CCC(CC1)N", 26.02),             # cyclohexylamine: one -NH2
    ("CC(=O)O", 37.3),                  # acetic acid: one -COOH
    ("C(N)", 26.02),                     # methylamine: one -NH2
    ("CS(=O)C", 36.28),                 # DMSO: S=O polar group
    ("CC#N", 23.79),                    # acetonitrile: C≡N polar
    ("CCC=O", 17.07),                   # propanal: one C=O
    ("CC(C)C", 0.0),                    # isobutane: no polar groups
    ("CCCl", 0.0),                      # chloroethane: no polar groups
    ("CCCCl", 0.0),                     # 1-chloropropane: no polar groups
    ("CBr", 0.0),                       # bromomethane: no polar groups
    ("CCBr", 0.0),                      # bromoethane: no polar groups
    ("CCI", 0.0),                       # iodoethane: no polar groups
    ("CCCC(N)C(=O)O", 63.32),           # norvaline: -NH2 + -COOH
    ("NC(=O)C", 43.09),                 # acetamide: -NH2 + C=O
    ("C1=CC=C(C=C1)C(C)C", 0.0),        # isobutylbenzene: no polar groups
    ("CC1=CC=CC=C1O", 20.23),           # o-cresol: one -OH
    ("C1=CC=C(C=C1)OC", 9.23),          # anisole: one C-O-C
    ("C1=CC=C(C=C1)S", 0.0),            # thiophenol: no polar groups (S not counted in TPSA)
    ("C1=CC=C(C=C1)S(=O)(=O)N", 68.54), # sulfonamide: S(=O)2 + -NH2
    ("FC(F)(F)C1=CC=CC=C1", 0.0),       # trifluorotoluene: no polar groups
    ("C1=CC2=C(C=C1)C3=C(C=CC=C3)C=C2", 0.0),  # phenanthrene: no polar groups
    ("CC(C(O)=O)(C)O", 57.53),          # alpha-hydroxyisobutyric acid: -OH + -COOH
    ("C1=CSC=C1", 0.0),                 # thiophene: no polar groups
    ("C1=CC=NC=C1", 12.89),             # pyridine: N in ring
    ("C1=CN=CC=C1", 12.89),             # pyrazine: N in ring
    ("C1=CC=CC=N1", 12.89),             # pyridine: N in ring
    ("C1CCNCC1", 12.03),                # piperidine: secondary amine
    ("C1CNCCC1", 12.03),                # piperidine: secondary amine
    ("CC(=O)C1=CC=CC=C1", 17.07),       # acetophenone: one C=O
    ("OC1=CC=CC=C1C(=O)O", 74.6),       # salicylic acid: -OH + -COOH
    ("C1=CC2=C(C=C1)N=C(C=C2)O", 46.51), # hydroxyquinoline: -OH + N in ring
]


def load_seed_data() -> list[tuple[str, float]]:
    return list(SEED_DATA)


def target_range() -> tuple[float, float]:
    vals = [t for _, t in SEED_DATA]
    return min(vals), max(vals)


if __name__ == "__main__":  # pragma: no cover
    lo, hi = target_range()
    print(f"TPSA seed records: {len(SEED_DATA)}  target range: ({lo:.2f}, {hi:.2f})")
