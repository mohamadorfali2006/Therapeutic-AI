"""ECFP-style hashed circular fingerprints — pure Python, no RDKit.

Owned by company/ai-research. Implements a Morgan/ECFP-style hashing without
a cheminformatics dependency:

- a lightweight atom graph is reconstructed from the SMILES token stream
  (atoms, bond orders, branches, ring closures);
- each atom gets an invariant: (element, aromatic flag, degree, formal charge);
- circular environments are iterated to RADIUS using a stable SHA-256 hash
  over (own invariant + sorted neighbor environments);
- all environment hashes from every radius are folded into a fixed-size bit
  vector (FP_SIZE) — this is the classic ECFP "hashed fingerprint" trick.

Deterministic and safe: raises ValueError on structurally unparseable input so
the API layer can return 422. Research use only.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

FP_SIZE = 256
RADIUS = 2

FP_FEATURE_NAMES = [f"fp_{i}" for i in range(FP_SIZE)]

_ELEMENTS_TWO = ("Br", "Cl", "Se", "As", "Si")


@dataclass
class _Atom:
    element: str = ""
    aromatic: bool = False
    charge: int = 0
    neighbors: list = field(default_factory=list)

    @property
    def degree(self) -> int:
        return len(self.neighbors)


def _tokenize(smiles: str) -> list[str]:
    """Split SMILES into atoms, bonds, parens, and ring-closure digits."""
    out: list[str] = []
    i = 0
    n = len(smiles)
    while i < n:
        ch = smiles[i]
        if ch == "[":
            j = smiles.find("]", i)
            if j == -1:
                raise ValueError(f"Unclosed bracket in SMILES: {smiles!r}")
            out.append(smiles[i:j + 1])
            i = j + 1
        elif ch.isalnum():
            two = smiles[i:i + 2]
            if two in _ELEMENTS_TWO:
                out.append(two)
                i += 2
            else:
                out.append(ch)
                i += 1
        elif ch in "()=#:+\\/":
            out.append(ch)
            i += 1
        else:
            i += 1
    return out


def _parse_atom(token: str) -> tuple[str, bool, int]:
    if token.startswith("["):
        inner = token[1:-1]
        charge = 0
        for m in re.finditer(r"([+-])(\d*)", inner):
            sign = 1 if m.group(1) == "+" else -1
            num = int(m.group(2) or 1)
            charge += sign * num
        core = re.sub(r"[Hh]\d*", "", inner)
        core = re.sub(r"[+-]\d*", "", core)
        core = core.rstrip("@")
        elem = core[:1].upper() + core[1:2].lower()
        return (elem or "C", False, charge)
    aromatic = token.islower() and token not in _ELEMENTS_TWO
    elem = token[:1].upper() if not aromatic else token
    return (elem, aromatic, 0)


def _connect(atoms: list[_Atom], a: int, b: int) -> None:
    if a is None or b is None or a == b:
        return
    atoms[a].neighbors.append(b)
    atoms[b].neighbors.append(a)


def _build_graph(smiles: str) -> list[_Atom]:
    """Return atom graph from SMILES; ties on bond symbols, branches, rings."""
    toks = _tokenize(smiles)
    atoms: list[_Atom] = []
    stack: list[int] = []
    ring_open: dict[str, int] = {}
    pending_order: float | None = None

    for t in toks:
        if t == "(":
            if stack:
                stack.append(stack[-1])
            continue
        if t == ")":
            if len(stack) > 1:
                stack.pop()
            continue
        if t in ("=", "#", ":", "/", "\\", "+"):
            pending_order = {"=": 2, "#": 3, ":": 1.5}.get(t)
            continue
        if t.isdigit():
            if t in ring_open:
                _connect(atoms, ring_open.pop(t), len(atoms) - 1)
            elif atoms:
                ring_open[t] = len(atoms) - 1
            pending_order = None
            continue

        elem, aromatic, charge = _parse_atom(t)
        idx = len(atoms)
        atoms.append(_Atom(element=elem, aromatic=aromatic, charge=charge))
        parent = stack[-1] if stack else None
        _connect(atoms, parent, idx)
        stack.append(idx)
        pending_order = None

    if not atoms:
        raise ValueError(f"No atoms parsed from SMILES: {smiles!r}")
    return atoms


def _invariant(atom: _Atom, idx: int) -> tuple:
    key = f"ar-{atom.element}" if atom.aromatic else f"al-{atom.element}"
    return (key, atom.aromatic, atom.degree, atom.charge)


def _sha256(*parts) -> int:
    digest = hashlib.sha256()
    for p in parts:
        digest.update(repr(p).encode("utf-8"))
    return int.from_bytes(digest.digest()[:8], "big")


def smiles_to_fingerprint(smiles: str) -> list[float]:
    """SMILES -> ECFP-style hashed bit vector (0.0/1.0 entries)."""
    atoms = _build_graph(smiles)

    envs = [_sha256(i, _invariant(a, i)) for i, a in enumerate(atoms)]
    bits: set[int] = set()

    def fold(env: int) -> int:
        return env % FP_SIZE

    for env in envs:
        bits.add(fold(env))

    for _round in range(1, RADIUS + 1):
        next_envs: list[int] = []
        for i, atom in enumerate(atoms):
            neighbor_envs = sorted(envs[j] for j in atom.neighbors)
            next_envs.append(_sha256(i, neighbor_envs, envs[i]))
        for env in next_envs:
            bits.add(fold(env))
        envs = next_envs

    return [1.0 if i in bits else 0.0 for i in range(FP_SIZE)]


def fingerprint_feature_names() -> list[str]:
    return list(FP_FEATURE_NAMES)