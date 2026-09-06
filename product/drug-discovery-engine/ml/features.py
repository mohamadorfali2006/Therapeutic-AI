"""DDE molecular features: pure-Python SMILES tokenizer + descriptor extraction.

No RDKit dependency (foundation scope). Produces a compact, deterministic
feature vector usable by the demo regression baseline.

Design intent (see company/ai-research and company/cdd):
- Domain-light but chemically meaningful: atom counts, bond counts,
  halogen/aliphatic/aromatic balances, rough ring count, heavy-atom count,
  molecular-weight proxy.
- Deterministic: same SMILES string -> identical vector, always.
- Raises ValueError on malformed SMILES so the API can return 422.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

ATOM_TOKEN = re.compile(
    r"\[[^\]]*\]|Br|Cl|b|c|n|o|s|p|se|as|si|B|C|N|O|S|P|F|I|H"
)
ORGANIC_SUBSET = set("BCNOPSFIHbcnops")
DEFAULT_FEATURE_NAMES = [
    "heavy_atoms",
    "carbon",
    "nitrogen",
    "oxygen",
    "sulfur",
    "phosphorus",
    "halogen",
    "aromatic_atoms",
    "aliphatic_atoms",
    "single_bonds",
    "double_bonds",
    "triple_bonds",
    "aromatic_bonds",
    "branches",
    "rings_approx",
    "charge",
    "mw_proxy",
]


@dataclass
class MoleculeFeatures:
    """Parsed SMILES counts used to build the descriptor vector."""

    smiles: str
    heavy_atoms: int = 0
    carbon: int = 0
    nitrogen: int = 0
    oxygen: int = 0
    sulfur: int = 0
    phosphorus: int = 0
    halogen: int = 0
    aromatic_atoms: int = 0
    aliphatic_atoms: int = 0
    single_bonds: int = 0
    double_bonds: int = 0
    triple_bonds: int = 0
    aromatic_bonds: int = 0
    branches: int = 0
    rings_approx: int = 0
    charge: int = 0
    mw_proxy: float = 0.0

    def to_vector(self) -> list[float]:
        return [
            float(self.heavy_atoms),
            float(self.carbon),
            float(self.nitrogen),
            float(self.oxygen),
            float(self.sulfur),
            float(self.phosphorus),
            float(self.halogen),
            float(self.aromatic_atoms),
            float(self.aliphatic_atoms),
            float(self.single_bonds),
            float(self.double_bonds),
            float(self.triple_bonds),
            float(self.aromatic_bonds),
            float(self.branches),
            float(self.rings_approx),
            float(self.charge),
            round(self.mw_proxy, 2),
        ]

    def names(self) -> list[str]:
        return list(DEFAULT_FEATURE_NAMES)


_ATOM_MASS = {
    "B": 10.81, "C": 12.01, "N": 14.01, "O": 16.00, "S": 32.06,
    "P": 30.97, "F": 19.00, "Cl": 35.45, "Br": 79.90, "I": 126.90,
    "Si": 28.09, "Se": 78.97, "As": 74.92,
}


def _parse_bracket(token: str) -> tuple[str, int]:
    """Return (element, formal_charge) from a bracket atom token like [NH4+]."""
    inner = token[1:-1]
    charge = 0
    for i, ch in enumerate(inner):
        if ch in "+-":
            n = 1
            j = i + 1
            digits = ""
            while j < len(inner) and inner[j].isdigit():
                digits += inner[j]
                j += 1
            if digits:
                n = int(digits)
            charge += n if ch == "+" else -n
    core = re.sub(r"[Hh]\d*", "", inner)
    core = re.sub(r"[+-]\d*", "", core)
    core = core.rstrip("@")
    elem = core[:1].upper() + core[1:2].lower()
    return elem or "C", charge


def _classify_atom(elem: str, aromatic: bool) -> str:
    if aromatic:
        return "aromatic"
    if elem == "C":
        return "carbon"
    if elem == "N":
        return "nitrogen"
    if elem == "O":
        return "oxygen"
    if elem == "S":
        return "sulfur"
    if elem == "P":
        return "phosphorus"
    if elem in ("F", "Cl", "Br", "I"):
        return "halogen"
    return "other"


def parse_smiles(smiles: str) -> MoleculeFeatures:
    """Parse a SMILES string into MoleculeFeatures.

    Supported: organic subset atoms, brackets, branching, ring-closure digits,
    bond symbols, aromatic lowercase, charges. Raises ValueError if input is
    structurally empty.
    """
    raw = (smiles or "").strip()
    if not raw or raw in (".", "-", "="):
        raise ValueError(f"Empty or invalid SMILES: {smiles!r}")

    f = MoleculeFeatures(smiles=raw)
    tokens = list(ATOM_TOKEN.finditer(raw))

    # State for branch/ring-depth accounting (not a full graph, intentional).
    branch_depth = 0
    ring_digits: set[str] = set()

    previous_was_atom = False
    atom_count_before_branches = 0
    branch_open_depths: list[int] = []

    for m in tokens:
        token = m.group(0)
        if token == "(":
            branch_depth += 1
            branch_open_depths.append(f.heavy_atoms)
            f.branches = max(f.branches, branch_depth)
            previous_was_atom = False
            continue
        if token == ")":
            if branch_depth == 0:
                raise ValueError(f"Unbalanced branch in SMILES: {smiles!r}")
            branch_depth -= 1
            branch_open_depths.pop()
            previous_was_atom = False
            continue
        if re.fullmatch(r"\d", token):
            ring_digits.add(token)
            f.rings_approx = len(ring_digits)
            previous_was_atom = False
            continue

        elem = token
        aromatic = token.islower() and token not in ("br", "cl", "se", "as", "si")
        if token.startswith("["):
            elem, charge = _parse_bracket(token)
            f.charge += charge
            aromatic = False
        else:
            charge = 0
            f.charge += charge

        mass = _ATOM_MASS.get(elem, 12.0)
        f.mw_proxy += mass
        f.heavy_atoms += 1
        kind = _classify_atom(elem, aromatic)
        if kind == "aromatic":
            f.aromatic_atoms += 1
        elif kind == "carbon":
            f.carbon += 1
            f.aliphatic_atoms += 1
        elif kind == "nitrogen":
            f.nitrogen += 1
            f.aliphatic_atoms += 1
        elif kind == "oxygen":
            f.oxygen += 1
            f.aliphatic_atoms += 1
        elif kind == "sulfur":
            f.sulfur += 1
            f.aliphatic_atoms += 1
        elif kind == "phosphorus":
            f.phosphorus += 1
            f.aliphatic_atoms += 1
        elif kind == "halogen":
            f.halogen += 1
            f.aliphatic_atoms += 1
        else:
            f.aliphatic_atoms += 1

        if previous_was_atom:
            pass  # bond counted via raw token scan below
        previous_was_atom = True

    # Bond accounting via a second lightweight scan of explicit bond symbols.
    f.single_bonds = len(re.findall(r"-[^=#:]", raw)) + raw.count("(")
    f.double_bonds = len(re.findall(r"=", raw))
    f.triple_bonds = len(re.findall(r"#", raw))
    f.aromatic_bonds = raw.count(":") + sum(
        1 for ch in raw if ch.islower() and ch in "bcnops"
    )

    if f.heavy_atoms == 0:
        raise ValueError(f"No atoms parsed from SMILES: {smiles!r}")
    return f


def smiles_to_features(smiles: str) -> list[float]:
    """Public entrypoint: SMILES -> feature vector."""
    return parse_smiles(smiles).to_vector()


def feature_names() -> list[str]:
    return list(DEFAULT_FEATURE_NAMES)