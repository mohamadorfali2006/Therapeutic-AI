# CDD Standard Operating Procedures

> Repeatable procedures for defining targets, curating seed data, and reviewing domain plausibility.

---

## SOP-1: Define a Demo Target

**Owner:** Head of CDD (cdd-1)
**Trigger:** New predictive task requested for DDE, or periodic review of existing targets.

### Steps

1. **Identify the task.** State the property or score the model should predict. Write one sentence on why it matters for drug discovery.

2. **Classify the task type.** Choose one:
   - `regression` — continuous numeric output (e.g., logP, solubility).
   - `classification` — discrete label output (e.g., feasible / not-feasible).
   - `ordinal` — ordered discrete scale (e.g., synthetic-accessibility 0-10).

3. **Define the target field.** Choose a snake_case field name that will appear in `seed_data.py` and `demo-targets.json`. Examples: `logP`, `solubility_logS`, `synth_score`.

4. **Set the plausible range.** Based on known chemistry or published benchmarks, define the expected output range. Include units or scale in the field description.

5. **Identify the data source.** Name the public dataset or computation method that provides ground-truth values. If computed (not experimental), state the method explicitly.

6. **Write the justification.** Two to four sentences covering: (a) what drug-discovery decision this property informs, (b) why it is appropriate for a demo, (c) what it does NOT predict.

7. **Add to demo-targets.json.** Append the new target entry with all required fields. Commit with message `feat(cdd): add demo target <name>`.

### Target entry schema

```json
{
  "name": "string — target display name",
  "task_type": "regression | classification | ordinal",
  "smiles_field": "smiles",
  "target_field": "string — field name in seed_data.py",
  "plausible_range": [min, max],
  "data_source": "string — dataset name or method",
  "justification": "string — 2-4 sentences",
  "demo_only": true
}
```

### Gate

Head of CDD (cdd-1) must approve the entry before it is committed. Approval means the plausible range is defensible and the justification is scientifically sound.

---

## SOP-2: Curate Seed Data

**Owner:** Computational Chemistry Agent (cdd-2), with Data Curation Agent (cdd-4) on provenance.
**Trigger:** Initial seed dataset creation, or update when a new target is added.

### Steps

1. **Source molecules.** Pull from public benchmark datasets (ESOL, Lipophilicity, MoleculeNet) or PubChem. Record the exact source name, version, and access date.

2. **Validate SMILES.** Every SMILES string must:
   - Be parseable by a SMILES parser (default RDKit; fallback: `deepchem` or manual regex check for well-formedness).
   - Represent a neutral, non-salt, non-counterion molecule where possible.
   - Contain no undefined stereochemistry markers (`[?]`) or exotic atoms outside {C, N, O, S, P, F, Cl, Br, I, H}.
   - Failures are either fixed (remove salt, pick canonical form) or excluded with a logged reason.

3. **Populate target fields.** For each molecule, fill every field defined in `demo-targets.json`:
   - If a public benchmark provides the value, use it directly and tag `source` with the dataset name.
   - If the field requires computation (e.g., `synth_score`), apply the designated rule-based method and tag `source` as `"computed-<method>"`.
   - No field may be left empty or set to a placeholder (null, 0, -1 unless those are valid values).

4. **Check diversity.** Sort molecules by Murcko scaffold (or nearest-neighbor fingerprint clustering). No single scaffold class should exceed 20% of the dataset. If it does, substitute molecules from underrepresented classes.

5. **Check for duplicates.** Canonicalize all SMILES and remove exact duplicates. Log the number removed.

6. **Write seed_data.py.** Output a Python file containing a single list-of-dicts constant. No external file reads. The file must be importable without side effects.

7. **Run provenance report.** cdd-4 produces a companion report documenting source, version, access date, total count, duplicates removed, and validation failures.

### Gate

- cdd-4 reviews provenance before the PR.
- cdd-1 (Head) approves the final seed_data.py.

---

## SOP-3: Review Domain Plausibility of Predictions

**Owner:** Structural Biology Agent (cdd-3)
**Trigger:** After any model training run or prediction batch is delivered by AI Research.

### Steps

1. **Collect predictions.** Retrieve the prediction output for every molecule in the seed set (or a new input batch).

2. **Range check.** For each target, verify that every predicted value falls within the `plausible_range` from `demo-targets.json`. Flag any outlier.

3. **Structural sanity check.** For flagged outliers:
   - Confirm the input SMILES is chemically valid.
   - Check if the molecule's functional groups are consistent with the predicted property (e.g., a highly polar molecule should not have a logP > 5).
   - If the outlier is chemically explainable (e.g., a perfluorinated chain with high logP), mark it as "expected outlier" with rationale.
   - If the outlier is not explainable, mark it as "model error" and escalate to AI Research.

4. **Distribution review.** Compare the predicted-value distribution to the known training-data distribution. Large shifts (> 2 std from training mean) across the batch suggest model drift or data mismatch.

5. **Write the plausibility report.** Include:
   - Total molecules reviewed.
   - Outliers found, categorized as expected or model-error.
   - Distribution summary (mean, std, range of predictions vs. training data).
   - Pass / fail recommendation.

6. **Escalate failures.** If any prediction batch fails (unexplained outliers > 5% of molecules), cdd-3 reports to cdd-1, who escalates to AI Research for retraining or investigation.

### Gate

cdd-1 signs the plausibility report before it enters the validation record.

---

## SOP Summary Table

| SOP | Owner | Inputs | Key outputs | Gate approver |
|---|---|---|---|---|
| Define Target | cdd-1 | Task request, chemistry knowledge | `demo-targets.json` entry, justification | cdd-1 (self) |
| Curate Seed Data | cdd-2 + cdd-4 | Public datasets, target spec | `seed_data.py`, provenance report | cdd-1 |
| Plausibility Review | cdd-3 | Model predictions, seed data, target ranges | Plausibility report | cdd-1 |
