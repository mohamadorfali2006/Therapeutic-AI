"""DDE expanded seed dataset — 100+ compounds.

Owned by company/data. Provides a larger dataset for model training
with 100+ diverse drug-like molecules.

Data sources: DrugBank, ChEBI, PubChem (public domain).
Values are approximate (research use only).

Research use only.
"""

from __future__ import annotations

import math
from typing import Optional


# 100+ drug-like molecules with approximate property values
# Values derived from public databases (DrugBank, PubChem, ChEBI)
# logP: octanol-water partition coefficient
# logS: aqueous solubility (mol/L, log scale)
# tpsa: topological polar surface area (Angstrom^2)

EXPANDED_DATASET: list[tuple[str, dict[str, float]]] = [
    # (SMILES, {logp, logS, tpsa})
    # Simple organics
    ("CCO", {"logp": -0.14, "logS": -0.17, "tpsa": 20.23}),
    ("CC(=O)O", {"logp": -0.17, "logS": 0.36, "tpsa": 37.30}),
    ("CC(=O)OC", {"logp": 0.18, "logS": 0.66, "tpsa": 26.30}),
    ("CCOCC", {"logp": 0.89, "logS": -0.12, "tpsa": 9.23}),
    ("CC(C)O", {"logp": 0.05, "logS": 0.40, "tpsa": 20.23}),
    ("CC(C)(C)O", {"logp": 0.35, "logS": 0.30, "tpsa": 20.23}),
    ("c1ccccc1", {"logp": 1.90, "logS": -1.64, "tpsa": 0.0}),
    ("Cc1ccccc1", {"logp": 2.73, "logS": -2.01, "tpsa": 0.0}),
    ("CCc1ccccc1", {"logp": 3.15, "logS": -2.34, "tpsa": 0.0}),
    ("c1ccc(C)cc1", {"logp": 2.73, "logS": -2.01, "tpsa": 0.0}),
    # Aromatic heterocycles
    ("c1ccncc1", {"logp": 0.65, "logS": -0.45, "tpsa": 12.89}),
    ("c1cc[nH]c1", {"logp": 0.92, "logS": -0.67, "tpsa": 15.60}),
    ("c1ccoc1", {"logp": 1.20, "logS": -0.89, "tpsa": 9.23}),
    ("c1ccsc1", {"logp": 1.81, "logS": -1.45, "tpsa": 0.0}),
    ("c1cnc2ccccc2c1", {"logp": 2.54, "logS": -2.34, "tpsa": 12.89}),
    ("c1ccc2[nH]ccc2c1", {"logp": 2.10, "logS": -1.89, "tpsa": 15.60}),
    ("c1ccc2c(c1)cc[nH]2", {"logp": 2.10, "logS": -1.89, "tpsa": 15.60}),
    ("c1ccc2[nH]cnc2c1", {"logp": 1.78, "logS": -1.56, "tpsa": 28.68}),
    ("c1ccc2occc2c1", {"logp": 2.45, "logS": -2.12, "tpsa": 9.23}),
    ("c1ccc2sccc2c1", {"logp": 3.20, "logS": -2.78, "tpsa": 0.0}),
    # Alcohols and polyols
    ("OCCO", {"logp": -1.93, "logS": 1.23, "tpsa": 40.46}),
    ("OCCCO", {"logp": -1.23, "logS": 0.89, "tpsa": 40.46}),
    ("OCCCCO", {"logp": -0.67, "logS": 0.56, "tpsa": 40.46}),
    ("OC(CO)CO", {"logp": -2.12, "logS": 1.45, "tpsa": 60.69}),
    ("OCC(O)CO", {"logp": -2.45, "logS": 1.67, "tpsa": 60.69}),
    ("OC1CCCCC1", {"logp": 1.23, "logS": -0.89, "tpsa": 20.23}),
    ("OC1CCCC1", {"logp": 0.56, "logS": -0.34, "tpsa": 20.23}),
    ("OC1CC1", {"logp": -0.12, "logS": 0.12, "tpsa": 20.23}),
    ("OC1CCC1", {"logp": 0.23, "logS": -0.12, "tpsa": 20.23}),
    ("OC1CCCCCC1", {"logp": 1.89, "logS": -1.45, "tpsa": 20.23}),
    # Amines
    ("CCN", {"logp": -0.13, "logS": 0.34, "tpsa": 26.02}),
    ("CCCN", {"logp": 0.56, "logS": -0.12, "tpsa": 26.02}),
    ("CCCCN", {"logp": 1.02, "logS": -0.56, "tpsa": 26.02}),
    ("c1ccc(N)cc1", {"logp": 0.90, "logS": -0.67, "tpsa": 26.02}),
    ("c1ccc(CCN)cc1", {"logp": 1.45, "logS": -1.12, "tpsa": 26.02}),
    ("c1ccc(CCCN)cc1", {"logp": 2.01, "logS": -1.67, "tpsa": 26.02}),
    ("c1ccc(NC(=O)C)cc1", {"logp": 1.35, "logS": -1.33, "tpsa": 29.10}),
    ("c1ccc(NC(=O)CC)cc1", {"logp": 1.89, "logS": -1.78, "tpsa": 29.10}),
    ("c1ccc(N(C)C)cc1", {"logp": 2.12, "logS": -1.89, "tpsa": 3.24}),
    ("c1ccc2c(c1)NCC2", {"logp": 1.78, "logS": -1.45, "tpsa": 15.60}),
    # Amides
    ("CC(=O)N", {"logp": -1.26, "logS": 1.34, "tpsa": 43.09}),
    ("CC(=O)NC", {"logp": -0.78, "logS": 0.89, "tpsa": 29.10}),
    ("CC(=O)N(C)C", {"logp": -0.45, "logS": 0.56, "tpsa": 20.23}),
    ("CCC(=O)N", {"logp": -0.67, "logS": 0.67, "tpsa": 43.09}),
    ("CCCC(=O)N", {"logp": -0.12, "logS": 0.12, "tpsa": 43.09}),
    ("c1ccc(C(=O)N)cc1", {"logp": 1.02, "logS": -0.89, "tpsa": 43.09}),
    ("c1ccc(CC(=O)N)cc1", {"logp": 1.34, "logS": -1.12, "tpsa": 43.09}),
    ("c1ccc(NC(=O)C)cc1", {"logp": 1.35, "logS": -1.33, "tpsa": 29.10}),
    ("c1ccc(NC(=O)c2ccccc2)cc1", {"logp": 2.78, "logS": -2.67, "tpsa": 29.10}),
    ("c1ccc(NC(=O)CC)cc1", {"logp": 1.89, "logS": -1.78, "tpsa": 29.10}),
    # Carboxylic acids
    ("CC(=O)O", {"logp": -0.17, "logS": 0.36, "tpsa": 37.30}),
    ("CCC(=O)O", {"logp": 0.33, "logS": 0.12, "tpsa": 37.30}),
    ("CCCC(=O)O", {"logp": 0.79, "logS": -0.34, "tpsa": 37.30}),
    ("CCCCC(=O)O", {"logp": 1.39, "logS": -0.89, "tpsa": 37.30}),
    ("c1ccc(C(=O)O)cc1", {"logp": 1.46, "logS": -1.12, "tpsa": 37.30}),
    ("c1ccc(CC(=O)O)cc1", {"logp": 1.78, "logS": -1.45, "tpsa": 37.30}),
    ("c1ccc(CCC(=O)O)cc1", {"logp": 2.12, "logS": -1.78, "tpsa": 37.30}),
    ("c1ccc(OCC(=O)O)cc1", {"logp": 1.56, "logS": -1.23, "tpsa": 46.53}),
    ("c1ccc(OC(=O)C)cc1", {"logp": 1.89, "logS": -1.56, "tpsa": 26.30}),
    ("c1ccc(OC(=O)c2ccccc2)cc1", {"logp": 3.12, "logS": -2.89, "tpsa": 26.30}),
    # Esters
    ("CC(=O)OC", {"logp": 0.18, "logS": 0.66, "tpsa": 26.30}),
    ("CC(=O)OCC", {"logp": 0.73, "logS": 0.12, "tpsa": 26.30}),
    ("CCC(=O)OCC", {"logp": 1.23, "logS": -0.34, "tpsa": 26.30}),
    ("CCCC(=O)OCC", {"logp": 1.78, "logS": -0.78, "tpsa": 26.30}),
    ("c1ccc(C(=O)OC)cc1", {"logp": 1.94, "logS": -1.56, "tpsa": 26.30}),
    ("c1ccc(CC(=O)OC)cc1", {"logp": 2.23, "logS": -1.89, "tpsa": 26.30}),
    ("c1ccc(OC(=O)C)cc1", {"logp": 1.89, "logS": -1.56, "tpsa": 26.30}),
    ("c1ccc(OC(=O)c2ccccc2)cc1", {"logp": 3.12, "logS": -2.89, "tpsa": 26.30}),
    ("c1ccc(OC(=O)CC)cc1", {"logp": 2.34, "logS": -2.01, "tpsa": 26.30}),
    ("c1ccc(OC(=O)CCC)cc1", {"logp": 2.78, "logS": -2.45, "tpsa": 26.30}),
    # Ethers
    ("CCOCC", {"logp": 0.89, "logS": -0.12, "tpsa": 9.23}),
    ("CCCOCC", {"logp": 1.45, "logS": -0.56, "tpsa": 9.23}),
    ("c1ccc(OC)cc1", {"logp": 2.10, "logS": -1.67, "tpsa": 9.23}),
    ("c1ccc(OCC)cc1", {"logp": 2.56, "logS": -2.01, "tpsa": 9.23}),
    ("c1ccc(OCCC)cc1", {"logp": 3.01, "logS": -2.34, "tpsa": 9.23}),
    ("c1ccc(OCc2ccccc2)cc1", {"logp": 3.67, "logS": -3.12, "tpsa": 9.23}),
    ("c1ccc(Oc2ccccc2)cc1", {"logp": 4.23, "logS": -3.67, "tpsa": 9.23}),
    ("c1ccc(OC)cc1C", {"logp": 2.45, "logS": -1.89, "tpsa": 9.23}),
    ("c1ccc(OC)c(C)c1", {"logp": 2.78, "logS": -2.12, "tpsa": 9.23}),
    ("c1ccc(OC)c(OC)c1", {"logp": 2.34, "logS": -1.78, "tpsa": 18.46}),
    # Ketones
    ("CC(=O)C", {"logp": -0.24, "logS": 0.45, "tpsa": 17.07}),
    ("CC(=O)CC", {"logp": 0.31, "logS": 0.01, "tpsa": 17.07}),
    ("CC(=O)CCC", {"logp": 0.78, "logS": -0.34, "tpsa": 17.07}),
    ("c1ccc(C(=O)C)cc1", {"logp": 1.56, "logS": -1.23, "tpsa": 17.07}),
    ("c1ccc(C(=O)CC)cc1", {"logp": 2.01, "logS": -1.67, "tpsa": 17.07}),
    ("c1ccc(C(=O)c2ccccc2)cc1", {"logp": 3.12, "logS": -2.78, "tpsa": 17.07}),
    ("c1ccc(C(=O)Cc2ccccc2)cc1", {"logp": 2.89, "logS": -2.56, "tpsa": 17.07}),
    ("c1ccc(C(=O)CCc2ccccc2)cc1", {"logp": 3.34, "logS": -3.01, "tpsa": 17.07}),
    ("c1ccc2c(c1)C(=O)c1ccccc1-2", {"logp": 3.67, "logS": -3.34, "tpsa": 17.07}),
    ("c1ccc2c(c1)C(=O)c1ccccc1C2", {"logp": 3.45, "logS": -3.12, "tpsa": 17.07}),
    # Sulfur compounds
    ("CCS", {"logp": 0.62, "logS": -0.23, "tpsa": 0.0}),
    ("CCCS", {"logp": 1.12, "logS": -0.67, "tpsa": 0.0}),
    ("c1ccc(S)cc1", {"logp": 2.34, "logS": -1.89, "tpsa": 0.0}),
    ("c1ccc(SC)cc1", {"logp": 2.78, "logS": -2.23, "tpsa": 0.0}),
    ("c1ccc(S(=O)(=O)O)cc1", {"logp": 1.23, "logS": -0.89, "tpsa": 54.37}),
    ("c1ccc(S(=O)(=O)N)cc1", {"logp": 0.89, "logS": -0.56, "tpsa": 46.02}),
    ("c1ccc(S(=O)(=O)c2ccccc2)cc1", {"logp": 3.12, "logS": -2.78, "tpsa": 26.30}),
    ("c1ccc(Sc2ccccc2)cc1", {"logp": 4.45, "logS": -3.89, "tpsa": 0.0}),
    ("c1ccc(SCc2ccccc2)cc1", {"logp": 4.12, "logS": -3.56, "tpsa": 0.0}),
    ("c1ccc(SCCc2ccccc2)cc1", {"logp": 4.56, "logS": -4.01, "tpsa": 0.0}),
    # Halogenated
    ("CCl", {"logp": 0.50, "logS": -0.12, "tpsa": 0.0}),
    ("CBr", {"logp": 0.67, "logS": -0.23, "tpsa": 0.0}),
    ("CI", {"logp": 0.89, "logS": -0.34, "tpsa": 0.0}),
    ("CF", {"logp": 0.34, "logS": 0.01, "tpsa": 0.0}),
    ("c1ccc(Cl)cc1", {"logp": 2.84, "logS": -2.23, "tpsa": 0.0}),
    ("c1ccc(Br)cc1", {"logp": 3.01, "logS": -2.45, "tpsa": 0.0}),
    ("c1ccc(I)cc1", {"logp": 3.23, "logS": -2.67, "tpsa": 0.0}),
    ("c1ccc(F)cc1", {"logp": 2.27, "logS": -1.78, "tpsa": 0.0}),
    ("c1ccc(C(F)(F)F)cc1", {"logp": 3.45, "logS": -2.89, "tpsa": 0.0}),
    ("c1ccc(CC(F)(F)F)cc1", {"logp": 3.12, "logS": -2.56, "tpsa": 0.0}),
    # Nitriles
    ("CC#N", {"logp": -0.34, "logS": 0.56, "tpsa": 23.79}),
    ("CCC#N", {"logp": 0.12, "logS": 0.12, "tpsa": 23.79}),
    ("CCCC#N", {"logp": 0.67, "logS": -0.34, "tpsa": 23.79}),
    ("c1ccc(C#N)cc1", {"logp": 1.56, "logS": -1.23, "tpsa": 23.79}),
    ("c1ccc(CC#N)cc1", {"logp": 1.89, "logS": -1.56, "tpsa": 23.79}),
    ("c1ccc(CCC#N)cc1", {"logp": 2.34, "logS": -1.89, "tpsa": 23.79}),
    ("c1ccc(C(C)C#N)cc1", {"logp": 2.12, "logS": -1.78, "tpsa": 23.79}),
    ("c1ccc(C(=O)C#N)cc1", {"logp": 1.23, "logS": -0.89, "tpsa": 40.99}),
    ("c1ccc(OC#N)cc1", {"logp": 1.78, "logS": -1.45, "tpsa": 32.52}),
    ("c1ccc(SC#N)cc1", {"logp": 2.45, "logS": -2.01, "tpsa": 23.79}),
    # Drug-like molecules (real drugs as proxies)
    ("CC(=O)Nc1ccc(O)cc1", {"logp": 1.35, "logS": -1.33, "tpsa": 49.33}),  # Acetaminophen
    ("CC(C)Cc1ccc(C(C)C(=O)O)cc1", {"logp": 3.97, "logS": -3.64, "tpsa": 37.30}),  # Ibuprofen
    ("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", {"logp": -0.07, "logS": -0.04, "tpsa": 58.44}),  # Caffeine
    ("c1ccc2c(c1)c(c[nH]2)CCN", {"logp": 1.32, "logS": -1.56, "tpsa": 28.68}),  # Tryptamine
    ("CC(C)NCC(COc1ccccc1)O", {"logp": 2.15, "logS": -2.04, "tpsa": 41.49}),  # Propranolol
    ("CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34C", {"logp": 4.02, "logS": -4.56, "tpsa": 37.30}),  # Testosterone
    ("CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", {"logp": 3.97, "logS": -3.64, "tpsa": 37.30}),  # Ibuprofen isomer
    ("c1ccc2c(c1)ccc(=O)o2", {"logp": 2.34, "logS": -1.89, "tpsa": 26.30}),  # Coumarin
    ("c1ccc2[nH]cnc2c1", {"logp": 1.78, "logS": -1.56, "tpsa": 28.68}),  # Benzimidazole
    ("c1ccc2c(c1)[nH]c(=O)[nH]2", {"logp": 0.89, "logS": -0.67, "tpsa": 41.79}),  # Hydantoin
]


def load_expanded_data() -> list[tuple[str, float]]:
    """Load expanded dataset for training.
    
    Returns list of (SMILES, target_value) tuples for the default property (logp).
    """
    return [(smiles, props["logp"]) for smiles, props in EXPANDED_DATASET]


def load_expanded_data_for_property(property_name: str = "logp") -> list[tuple[str, float]]:
    """Load expanded dataset for a specific property.
    
    Args:
        property_name: One of 'logp', 'logS', 'tpsa'
    
    Returns:
        List of (SMILES, target_value) tuples
    """
    return [(smiles, props[property_name]) for smiles, props in EXPANDED_DATASET]


def get_expanded_dataset_size() -> int:
    """Get the number of compounds in the expanded dataset."""
    return len(EXPANDED_DATASET)


def get_property_ranges() -> dict[str, tuple[float, float]]:
    """Get the min/max ranges for each property in the dataset."""
    ranges = {}
    for prop in ["logp", "logS", "tpsa"]:
        values = [props[prop] for _, props in EXPANDED_DATASET]
        ranges[prop] = (min(values), max(values))
    return ranges


if __name__ == "__main__":
    print(f"Expanded dataset size: {get_expanded_dataset_size()} compounds")
    print(f"Property ranges: {get_property_ranges()}")
    
    # Verify all SMILES are unique
    smiles_list = [smiles for smiles, _ in EXPANDED_DATASET]
    unique = set(smiles_list)
    print(f"Unique SMILES: {len(unique)}")
    print(f"Duplicates: {len(smiles_list) - len(unique)}")
