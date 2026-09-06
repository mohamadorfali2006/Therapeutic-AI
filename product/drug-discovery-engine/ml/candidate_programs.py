"""DDE Candidate Programs — first 3 molecule programs.

Owned by company/cdd. Defines 3 candidate molecules with:
- Target properties (logP, logS, TPSA) with desired ranges
- Predicted vs measured tracking
- Program status (active | on-hold | advanced | discontinued)
- Decision log

Research use only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class TargetSpec:
    """Target property specification."""
    property_name: str
    min_value: float
    max_value: float
    ideal_value: float
    unit: str = ""
    weight: float = 1.0  # importance weight


@dataclass
class CandidateMolecule:
    """A candidate molecule in a program."""
    smiles: str
    name: str
    program_id: str
    status: str = "active"  # active | on-hold | advanced | discontinued
    properties_predicted: dict[str, float] = field(default_factory=dict)
    properties_measured: dict[str, float] = field(default_factory=dict)
    targets: list[TargetSpec] = field(default_factory=list)
    score: float = 0.0
    decision_log: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""


@dataclass
class CandidateProgram:
    """A candidate program (collection of related molecules)."""
    program_id: str
    name: str
    description: str
    status: str = "active"
    candidates: list[CandidateMolecule] = field(default_factory=list)
    targets: list[TargetSpec] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    notes: str = ""


def calculate_score(
    properties: dict[str, float],
    targets: list[TargetSpec],
) -> float:
    """Calculate a multi-property score (0-100).
    
    For each target, score 100 if within range, decreasing linearly outside.
    Weighted average across all targets.
    """
    if not targets:
        return 0.0
    
    total_weight = sum(t.weight for t in targets)
    weighted_score = 0.0
    
    for target in targets:
        value = properties.get(target.property_name)
        if value is None:
            continue
        
        if target.min_value <= value <= target.max_value:
            # Within range — score 100
            target_score = 100.0
        else:
            # Outside range — linear penalty
            if value < target.min_value:
                distance = target.min_value - value
                range_width = target.max_value - target.min_value
            else:
                distance = value - target.max_value
                range_width = target.max_value - target.min_value
            
            if range_width > 0:
                penalty = min(100.0, (distance / range_width) * 100.0)
                target_score = 100.0 - penalty
            else:
                target_score = 0.0
        
        weighted_score += target_score * target.weight
    
    return weighted_score / total_weight if total_weight > 0 else 0.0


def get_first_candidate_programs() -> list[CandidateProgram]:
    """Get the first 3 candidate programs for Therapeutic-AI.
    
    Each program has a specific therapeutic goal and target profile:
    - Program 1: Oral drug-like (balanced logP, good solubility)
    - Program 2: CNS-penetrant (higher logP, lower TPSA)
    - Program 3: Polar/excellent solubility (lower logP, higher TPSA)
    """
    
    programs = []
    
    # Program 1: Oral drug-like
    p1 = CandidateProgram(
        program_id="PROG-001",
        name="Oral Drug-Like Lead",
        description="Balanced oral drug-like properties per Lipinski's Rule of Five",
        targets=[
            TargetSpec("logp", 0.0, 3.0, 1.5, weight=1.0),
            TargetSpec("logS", -3.0, 0.0, -1.5, weight=0.8),
            TargetSpec("tpsa", 20.0, 90.0, 60.0, weight=0.6),
        ],
    )
    p1.candidates = [
        CandidateMolecule(
            smiles="CC(=O)Nc1ccc(O)cc1",
            name="Acetaminophen (proxy)",
            program_id="PROG-001",
            properties_predicted={"logp": 1.35, "logS": -1.33, "tpsa": 49.33},
            targets=p1.targets,
            notes="Well-known oral analgesic — good starting point",
        ),
        CandidateMolecule(
            smiles="CC(C)Cc1ccc(C(C)C(=O)O)cc1",
            name="Ibuprofen (proxy)",
            program_id="PROG-001",
            properties_predicted={"logp": 3.97, "logS": -3.64, "tpsa": 37.30},
            targets=p1.targets,
            notes="NSAID — slightly high logP but proven oral bioavailability",
        ),
    ]
    programs.append(p1)
    
    # Program 2: CNS-penetrant
    p2 = CandidateProgram(
        program_id="PROG-002",
        name="CNS Penetrant Lead",
        description="Optimized for blood-brain barrier penetration (higher logP, lower TPSA)",
        targets=[
            TargetSpec("logp", 2.0, 4.5, 3.0, weight=1.0),
            TargetSpec("logS", -3.5, -1.0, -2.0, weight=0.7),
            TargetSpec("tpsa", 0.0, 60.0, 40.0, weight=0.9),
        ],
    )
    p2.candidates = [
        CandidateMolecule(
            smiles="c1ccc2c(c1)c(c[nH]2)CCN",
            name="Tryptamine (proxy)",
            program_id="PROG-002",
            properties_predicted={"logp": 1.32, "logS": -1.56, "tpsa": 28.68},
            targets=p2.targets,
            notes="CNS-active scaffold — logP slightly low but TPSA excellent",
        ),
        CandidateMolecule(
            smiles="CC(C)NCC(COc1ccccc1)O",
            name="Propranolol (proxy)",
            program_id="PROG-002",
            properties_predicted={"logp": 2.15, "logS": -2.04, "tpsa": 41.49},
            targets=p2.targets,
            notes="Beta-blocker with known CNS penetration",
        ),
    ]
    programs.append(p2)
    
    # Program 3: Polar/excellent solubility
    p3 = CandidateProgram(
        program_id="PROG-003",
        name="High-Solubility Lead",
        description="Optimized for aqueous solubility (lower logP, higher TPSA)",
        targets=[
            TargetSpec("logp", -1.0, 1.5, 0.0, weight=1.0),
            TargetSpec("logS", -1.0, 0.0, -0.5, weight=1.0),
            TargetSpec("tpsa", 40.0, 120.0, 80.0, weight=0.7),
        ],
    )
    p3.candidates = [
        CandidateMolecule(
            smiles="CC(=O)O",
            name="Acetic acid (proxy)",
            program_id="PROG-003",
            properties_predicted={"logp": -0.17, "logS": 0.36, "tpsa": 37.30},
            targets=p3.targets,
            notes="Simple polar molecule — excellent solubility, low logP",
        ),
        CandidateMolecule(
            smiles="CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
            name="Caffeine (proxy)",
            program_id="PROG-003",
            properties_predicted={"logp": -0.07, "logS": -0.04, "tpsa": 58.44},
            targets=p3.targets,
            notes="Highly soluble, multiple H-bond acceptors",
        ),
    ]
    programs.append(p3)
    
    # Calculate scores for all candidates
    for prog in programs:
        for cand in prog.candidates:
            cand.score = calculate_score(cand.properties_predicted, prog.targets)
    
    return programs


def format_program_summary(programs: list[CandidateProgram]) -> str:
    """Format a human-readable summary of candidate programs."""
    lines = []
    lines.append("=" * 60)
    lines.append("THERAPEUTIC-AI — First Candidate Programs")
    lines.append("=" * 60)
    
    for prog in programs:
        lines.append(f"\n[{prog.program_id}] {prog.name}")
        lines.append(f"  Status: {prog.status}")
        lines.append(f"  Description: {prog.description}")
        lines.append(f"  Targets:")
        for t in prog.targets:
            lines.append(f"    {t.property_name}: {t.min_value}-{t.max_value} (ideal {t.ideal_value})")
        lines.append(f"  Candidates:")
        for cand in prog.candidates:
            lines.append(f"    - {cand.name} ({cand.smiles})")
            lines.append(f"      Score: {cand.score:.1f}/100")
            props = ", ".join(f"{k}={v:.2f}" for k, v in cand.properties_predicted.items())
            lines.append(f"      Predicted: {props}")
            if cand.notes:
                lines.append(f"      Notes: {cand.notes}")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


if __name__ == "__main__":
    programs = get_first_candidate_programs()
    print(format_program_summary(programs))
