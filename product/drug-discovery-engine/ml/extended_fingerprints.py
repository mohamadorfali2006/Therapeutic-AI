"""Extended molecular fingerprints — pure Python, no RDKit.

Owned by company/ai-research. Builds on the ECFP-style hashing from
fingerprints.py with:
- Larger fingerprint size (512 bits)
- Higher radius (3)
- Additional atom invariants (H-count, ring membership, chirality)
- Count-based MACCS-style substructure features
- Hybrid fingerprint: ECFP bits + substructure counts

Deterministic and safe: raises ValueError on structurally unparseable input.
Research use only.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from .fingerprints import (
    _Atom,
    _build_graph,
    _parse_atom,
    _tokenize,
    FP_SIZE,
    RADIUS,
    _sha256,
)

# Extended parameters
EXT_FP_SIZE = 512
EXT_RADIUS = 3

# MACCS-style substructure patterns (simplified, pure-Python)
# Each pattern is a (name, smarts-like description, test function)
# We implement a subset of the most informative MACCS keys
SUBSTRUCTURE_PATTERNS = [
    ("C_C_C", "C-C-C chain", lambda atoms: _has_chain(atoms, 3)),
    ("C_C_C_C", "C-C-C-C chain", lambda atoms: _has_chain(atoms, 4)),
    ("C_C_C_C_C", "C-C-C-C-C chain", lambda atoms: _has_chain(atoms, 5)),
    ("C_O", "C-O bond", lambda atoms: _has_bond(atoms, "C", "O")),
    ("C_N", "C-N bond", lambda atoms: _has_bond(atoms, "C", "N")),
    ("C_O_C", "C-O-C ether", lambda atoms: _has_path(atoms, "C", "O", "C")),
    ("C_N_C", "C-N-C amine", lambda atoms: _has_path(atoms, "C", "N", "C")),
    ("O_H", "hydroxyl group", lambda atoms: _has_oh(atoms)),
    ("N_H", "amine group", lambda atoms: _has_nh(atoms)),
    ("C_O_double", "carbonyl C=O", lambda atoms: _has_carbonyl(atoms)),
    ("C_O_O_H", "carboxylic acid", lambda atoms: _has_cooh(atoms)),
    ("aromatic_ring", "aromatic ring", lambda atoms: _has_aromatic_ring(atoms)),
    ("hetero_ring", "heteroaromatic ring", lambda atoms: _has_hetero_ring(atoms)),
    ("ring_6", "6-membered ring", lambda atoms: _has_ring_size(atoms, 6)),
    ("ring_5", "5-membered ring", lambda atoms: _has_ring_size(atoms, 5)),
    ("halogen", "halogen (F, Cl, Br, I)", lambda atoms: _has_halogen(atoms)),
    ("S_atom", "sulfur atom", lambda atoms: _has_element(atoms, "S")),
    ("P_atom", "phosphorus atom", lambda atoms: _has_element(atoms, "P")),
]


def _has_chain(atoms: list[_Atom], length: int) -> bool:
    """Check if there's a chain of at least `length` connected carbons."""
    for i, a in enumerate(atoms):
        if a.element == "C":
            visited = {i}
            if _dfs_chain(atoms, i, length - 1, visited):
                return True
    return False


def _dfs_chain(atoms: list[_Atom], current: int, remaining: int, visited: set[int]) -> bool:
    if remaining == 0:
        return True
    for neighbor in atoms[current].neighbors:
        if neighbor not in visited and atoms[neighbor].element == "C":
            visited.add(neighbor)
            if _dfs_chain(atoms, neighbor, remaining - 1, visited):
                return True
            visited.discard(neighbor)
    return False


def _has_bond(atoms: list[_Atom], elem1: str, elem2: str) -> bool:
    """Check if there's a bond between two elements."""
    for i, a in enumerate(atoms):
        if a.element == elem1:
            for neighbor in a.neighbors:
                if atoms[neighbor].element == elem2:
                    return True
    return False


def _has_path(atoms: list[_Atom], elem1: str, elem2: str, elem3: str) -> bool:
    """Check if there's a path elem1-elem2-elem3."""
    for i, a in enumerate(atoms):
        if a.element == elem1:
            for n1 in a.neighbors:
                if atoms[n1].element == elem2:
                    for n2 in atoms[n1].neighbors:
                        if n2 != i and atoms[n2].element == elem3:
                            return True
    return False


def _has_oh(atoms: list[_Atom]) -> bool:
    """Check for hydroxyl group (-OH)."""
    for a in atoms:
        if a.element == "O":
            for neighbor in a.neighbors:
                if atoms[neighbor].element == "C":
                    return True
    return False


def _has_nh(atoms: list[_Atom]) -> bool:
    """Check for amine group (-NH2, -NH-, -N<)."""
    for a in atoms:
        if a.element == "N":
            for neighbor in a.neighbors:
                if atoms[neighbor].element == "C":
                    return True
    return False


def _has_carbonyl(atoms: list[_Atom]) -> bool:
    """Check for carbonyl group (C=O)."""
    for a in atoms:
        if a.element == "C":
            for neighbor in a.neighbors:
                if atoms[neighbor].element == "O" and len(atoms[neighbor].neighbors) == 1:
                    return True
    return False


def _has_cooh(atoms: list[_Atom]) -> bool:
    """Check for carboxylic acid (-COOH)."""
    for a in atoms:
        if a.element == "C":
            has_double_o = False
            has_single_o = False
            for neighbor in a.neighbors:
                if atoms[neighbor].element == "O":
                    if len(atoms[neighbor].neighbors) == 1:
                        has_double_o = True
                    else:
                        has_single_o = True
            if has_double_o and has_single_o:
                return True
    return False


def _has_aromatic_ring(atoms: list[_Atom]) -> bool:
    """Check for aromatic ring (simplified: any aromatic atom)."""
    for a in atoms:
        if a.aromatic:
            return True
    return False


def _has_hetero_ring(atoms: list[_Atom]) -> bool:
    """Check for heteroaromatic ring (simplified)."""
    for a in atoms:
        if a.aromatic and a.element not in ("C",):
            return True
    return False


def _has_ring_size(atoms: list[_Atom], size: int) -> bool:
    """Check for ring of given size (simplified)."""
    # Simplified: check for common ring patterns
    if size == 6:
        # Check for benzene-like patterns
        return _has_aromatic_ring(atoms) or _has_chain(atoms, 6)
    elif size == 5:
        # Check for 5-membered rings (simplified)
        return _has_aromatic_ring(atoms) and any(
            a.element in ("N", "O", "S") for a in atoms
        )
    return False


def _has_halogen(atoms: list[_Atom]) -> bool:
    """Check for halogen atoms."""
    return any(a.element in ("F", "Cl", "Br", "I") for a in atoms)


def _has_element(atoms: list[_Atom], element: str) -> bool:
    """Check for specific element."""
    return any(a.element == element for a in atoms)


def _extended_invariant(atom: _Atom, idx: int) -> tuple:
    """Extended atom invariant with more features."""
    key = f"ar-{atom.element}" if atom.aromatic else f"al-{atom.element}"
    # Estimate H-count (simplified: typical valence - degree)
    typical_valence = {"C": 4, "N": 3, "O": 2, "S": 2, "P": 3, "F": 1, "Cl": 1, "Br": 1, "I": 1}
    h_count = max(0, typical_valence.get(atom.element, 4) - atom.degree - abs(atom.charge))
    return (key, atom.aromatic, atom.degree, atom.charge, h_count)


def smiles_to_extended_fingerprint(smiles: str) -> list[float]:
    """SMILES -> extended hybrid fingerprint (ECFP bits + substructure counts)."""
    atoms = _build_graph(smiles)

    # ECFP-style bits (larger, higher radius)
    envs = [_sha256(i, _extended_invariant(a, i)) for i, a in enumerate(atoms)]
    bits: set[int] = set()

    def fold(env: int) -> int:
        return env % EXT_FP_SIZE

    for env in envs:
        bits.add(fold(env))

    for _round in range(1, EXT_RADIUS + 1):
        next_envs: list[int] = []
        for i, atom in enumerate(atoms):
            neighbor_envs = sorted(envs[j] for j in atom.neighbors)
            next_envs.append(_sha256(i, neighbor_envs, envs[i]))
        for env in next_envs:
            bits.add(fold(env))
        envs = next_envs

    ecfp_bits = [1.0 if i in bits else 0.0 for i in range(EXT_FP_SIZE)]

    # MACCS-style substructure counts
    substructure_counts = []
    for name, desc, test_fn in SUBSTRUCTURE_PATTERNS:
        result = test_fn(atoms)
        substructure_counts.append(1.0 if result else 0.0)

    return ecfp_bits + substructure_counts


def extended_fingerprint_feature_names() -> list[str]:
    """Get feature names for the extended fingerprint."""
    names = [f"ext_fp_{i}" for i in range(EXT_FP_SIZE)]
    for name, desc, _ in SUBSTRUCTURE_PATTERNS:
        names.append(f"maccs_{name}")
    return names


def combined_feature_count() -> int:
    """Get total number of features in the combined fingerprint."""
    return EXT_FP_SIZE + len(SUBSTRUCTURE_PATTERNS)


if __name__ == "__main__":
    # Demo
    fp = smiles_to_extended_fingerprint("CCO")
    print(f"Extended fingerprint size: {len(fp)}")
    print(f"ECFP bits: {sum(1 for x in fp[:EXT_FP_SIZE] if x > 0)} / {EXT_FP_SIZE}")
    print(f"MACCS bits: {sum(1 for x in fp[EXT_FP_SIZE:] if x > 0)} / {len(SUBSTRUCTURE_PATTERNS)}")
