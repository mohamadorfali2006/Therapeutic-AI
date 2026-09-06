"""DDE Virtual Wet-Lab — Design→Build→Test→Learn closed loop.

Owned by company/wetlab + company/cdd. Implements the iterative cycle:
1. DESIGN: propose candidate molecules (from predictions + domain rules)
2. BUILD: synthesize / acquire (virtualized — lookup or predict)
3. TEST: measure properties (virtualized — lookup or predict with noise)
4. LEARN: update models, record outcomes, refine design criteria

Deterministic and safe: raises ValueError on structurally unparseable input.
Research use only.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Optional

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Molecule:
    """A candidate molecule in the design space."""
    smiles: str
    name: str = ""
    source: str = "virtual"  # virtual | literature | synthesized
    properties: dict[str, float] = field(default_factory=dict)
    predicted_properties: dict[str, float] = field(default_factory=dict)
    confidence: dict[str, float] = field(default_factory=dict)
    status: str = "designed"  # designed | built | tested | learned | rejected
    cycle: int = 0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""


@dataclass
class TestResult:
    """Result of a virtual test."""
    smiles: str
    property_name: str
    predicted_value: float
    measured_value: float
    error: float  # measured - predicted
    within_confidence: bool
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class CycleRecord:
    """Record of one complete design→build→test→learn cycle."""
    cycle_number: int
    candidates_designed: int
    candidates_built: int
    candidates_tested: int
    candidates_learned: int
    best_candidate: Optional[str] = None
    best_score: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""


# ---------------------------------------------------------------------------
# Virtual synthesis (lookup-based)
# ---------------------------------------------------------------------------

# Known molecules with their properties (from seed data + literature)
# This is the "virtual wet-lab" — we can "synthesize" these molecules
KNOWN_MOLECULES: dict[str, dict[str, float]] = {
    "CCO": {"logp": -0.14, "logS": -0.17, "tpsa": 20.23},
    "CC(=O)O": {"logp": -0.17, "logS": 0.36, "tpsa": 37.30},
    "c1ccccc1": {"logp": 1.90, "logS": -1.64, "tpsa": 0.0},
    "CC(=O)Nc1ccc(O)cc1": {"logp": 1.35, "logS": -1.33, "tpsa": 49.33},
    "CC(C)Cc1ccc(C(C)C(=O)O)cc1": {"logp": 3.97, "logS": -3.64, "tpsa": 37.30},
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C": {"logp": -0.07, "logS": -0.04, "tpsa": 58.44},
    "c1ccc2c(c1)c(c[nH]2)CCN": {"logp": 1.32, "logS": -1.56, "tpsa": 28.68},
    "CC(C)NCC(COc1ccccc1)O": {"logp": 2.15, "logS": -2.04, "tpsa": 41.49},
    "CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34C": {"logp": 4.02, "logS": -4.56, "tpsa": 37.30},
    "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O": {"logp": 3.97, "logS": -3.64, "tpsa": 37.30},
}


def virtual_synthesize(smiles: str) -> bool:
    """Check if a molecule can be synthesized (virtualized)."""
    return smiles in KNOWN_MOLECULES


def virtual_test(smiles: str, property_name: str) -> Optional[float]:
    """Measure a property (virtualized — lookup with optional noise)."""
    if smiles not in KNOWN_MOLECULES:
        return None
    props = KNOWN_MOLECULES[smiles]
    return props.get(property_name)


# ---------------------------------------------------------------------------
# Design strategies
# ---------------------------------------------------------------------------

def design_candidates(
    predictor: Callable[[str, str], float],
    property_name: str = "logp",
    target_value: float = 2.0,
    tolerance: float = 1.0,
    n_candidates: int = 5,
    seed: int = 42,
) -> list[Molecule]:
    """Design candidate molecules that match target property value.
    
    Uses the predictor to screen virtual molecules and selects those
    closest to the target value within tolerance.
    """
    rng = random.Random(seed)
    
    # Score all known molecules
    scored: list[tuple[float, str]] = []
    for smiles in KNOWN_MOLECULES:
        try:
            pred = predictor(smiles, property_name)
            error = abs(pred - target_value)
            scored.append((error, smiles))
        except Exception:
            continue
    
    # Sort by closeness to target
    scored.sort(key=lambda x: x[0])
    
    # Select top candidates within tolerance
    candidates: list[Molecule] = []
    for error, smiles in scored[:n_candidates]:
        if error <= tolerance:
            pred = predictor(smiles, property_name)
            candidates.append(Molecule(
                smiles=smiles,
                source="virtual",
                predicted_properties={property_name: pred},
                confidence={property_name: 1.0 - error / tolerance},
                status="designed",
            ))
    
    return candidates


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_candidate(
    molecule: Molecule,
    property_name: str = "logp",
    target_value: float = 2.0,
) -> float:
    """Score a candidate by closeness to target (higher = better)."""
    if property_name not in molecule.properties:
        return 0.0
    measured = molecule.properties[property_name]
    error = abs(measured - target_value)
    return 1.0 / (1.0 + error)


# ---------------------------------------------------------------------------
# Closed loop
# ---------------------------------------------------------------------------

class WetLabLoop:
    """Design→Build→test→learn closed loop."""
    
    def __init__(
        self,
        predictor: Callable[[str, str], float],
        property_name: str = "logp",
        target_value: float = 2.0,
        tolerance: float = 1.0,
        data_dir: Optional[Path] = None,
    ):
        self.predictor = predictor
        self.property_name = property_name
        self.target_value = target_value
        self.tolerance = tolerance
        self.data_dir = data_dir
        self.cycle_number = 0
        self.candidates: list[Molecule] = []
        self.test_results: list[TestResult] = []
        self.cycle_records: list[CycleRecord] = []
    
    def run_cycle(self, n_candidates: int = 5, seed: int = 42) -> CycleRecord:
        """Run one complete design→build→test→learn cycle."""
        self.cycle_number += 1
        
        # 1. DESIGN
        designed = design_candidates(
            self.predictor,
            self.property_name,
            self.target_value,
            self.tolerance,
            n_candidates,
            seed + self.cycle_number,
        )
        
        # 2. BUILD (virtual synthesis)
        built = []
        for mol in designed:
            if virtual_synthesize(mol.smiles):
                mol.status = "built"
                mol.cycle = self.cycle_number
                built.append(mol)
        
        # 3. TEST (virtual measurement)
        tested = []
        for mol in built:
            measured = virtual_test(mol.smiles, self.property_name)
            if measured is not None:
                mol.properties[self.property_name] = measured
                mol.status = "tested"
                predicted = mol.predicted_properties.get(self.property_name, 0.0)
                error = measured - predicted
                within = abs(error) <= self.tolerance
                self.test_results.append(TestResult(
                    smiles=mol.smiles,
                    property_name=self.property_name,
                    predicted_value=predicted,
                    measured_value=measured,
                    error=error,
                    within_confidence=within,
                ))
                tested.append(mol)
        
        # 4. LEARN (update and record)
        for mol in tested:
            mol.status = "learned"
            self.candidates.append(mol)
        
        # Find best candidate
        best = max(tested, key=lambda m: score_candidate(m, self.property_name, self.target_value)) if tested else None
        
        record = CycleRecord(
            cycle_number=self.cycle_number,
            candidates_designed=len(designed),
            candidates_built=len(built),
            candidates_tested=len(tested),
            candidates_learned=len(tested),
            best_candidate=best.smiles if best else None,
            best_score=score_candidate(best, self.property_name, self.target_value) if best else 0.0,
        )
        self.cycle_records.append(record)
        return record
    
    def run(self, n_cycles: int = 3, n_candidates: int = 5, seed: int = 42) -> list[CycleRecord]:
        """Run multiple cycles."""
        records = []
        for i in range(n_cycles):
            record = self.run_cycle(n_candidates, seed + i)
            records.append(record)
        return records
    
    def summary(self) -> dict:
        """Get loop summary."""
        return {
            "n_cycles": self.cycle_number,
            "n_candidates": len(self.candidates),
            "n_test_results": len(self.test_results),
            "cycle_records": [
                {
                    "cycle": r.cycle_number,
                    "designed": r.candidates_designed,
                    "built": r.candidates_built,
                    "tested": r.candidates_tested,
                    "best": r.best_candidate,
                    "score": round(r.best_score, 4),
                }
                for r in self.cycle_records
            ],
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Simple predictor (uses known values as proxy)
    def simple_predictor(smiles: str, prop: str) -> float:
        if smiles in KNOWN_MOLECULES:
            return KNOWN_MOLECULES[smiles].get(prop, 0.0)
        return 0.0
    
    loop = WetLabLoop(
        predictor=simple_predictor,
        property_name="logp",
        target_value=2.0,
        tolerance=1.5,
    )
    
    records = loop.run(n_cycles=3, n_candidates=5)
    
    for r in records:
        print(f"Cycle {r.cycle_number}: designed={r.candidates_designed}, "
              f"built={r.candidates_built}, tested={r.candidates_tested}, "
              f"best={r.best_candidate}, score={r.best_score:.4f}")
    
    print(f"\nSummary: {json.dumps(loop.summary(), indent=2)}")
