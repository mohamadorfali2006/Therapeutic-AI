# HANDOFF — Therapeutic-AI

**Session date:** 2026-09-06

## What was accomplished
- Scaffolded `C:/Users/PCD/Therapeutic-AI` for an AI drug-discovery + FDA-cleared SaMD company.
- Created full **org design**: 84 roles across 9 functions (`org/README.md` + 9 role files in `org/roles/`).
- Created complete **documentation set** (`docs/00-INDEX.md` … `docs/10-CHANGELOG.md`): implementation plan, architecture (Mermaid, PCCP-first Regulated-AI pipeline), design (Global2Design), API reference, database/provenance model, user guide, how-to-run, integrations, testing, changelog.
- Created `AGENTS.md` project rules and `README.md`.
- `git init` + initial commit `d8460dd` (24 files, 741 insertions).
- Obsidian mirror created at `C:/Users/PCD/Documents/Obsidian Vault/Projects/Therapeutic-AI/` (docs + org + `_HOME.md`); created vault-level `_ALL-PROJECTS.md` index.

## Key decisions made on your behalf
1. **Dual-product company**: AI drug discovery (research/non-SaMD) + FDA-cleared SaMD clinical products.
2. **510(k)/De Novo** primary FDA path; EU MDR + EU AI Act run parallel.
3. **PCCP-first**: build adaptive-AI validation infrastructure from day one (Regulated-AI team = the backbone).
4. **Regulated-AI reports to Regulatory/Quality** (independent of shipping pressure).
5. **In-house wet lab** closes the design→build→test→learn loop.

## Current state
- **Planning/org-deliverable complete.** No application code yet (Phase 2 starts engineering).
- Git repo initialized locally on branch `master`, commit `d8460dd`.

## Blocker / unresolved
- **GitHub remote + push NOT done.** `gh` CLI is not installed and no `GH_TOKEN` is set.
  - To complete: install `gh` (`winget install GitHub.cli` or from GitHub releases), run `gh auth login`, then:
    - `gh repo create Therapeutic-AI --private --source=. --remote=origin --push`
    - or `git remote add origin <url>` then `git push -u origin master`
  - Do not attempt secret-bearing workarounds.

## Next steps
1. Authenticate GitHub (`gh auth login`) → create private repo → push (`<= 15 min`).
2. Begin **Phase 1** (Months 0–3): hire CEO-first leadership (CSO + CRQO together), stand up ISO 13485 QMS skeleton, file FDA Q-Submission strategy.
3. When engineering starts (Phase 2): build the CI/CD-backed **Regulated-AI validation pipeline first**, then platform.
4. After any docs update: re-sync Obsidian mirror per sync script / `AGENTS.md`.

## Failed approaches (do not retry)
- None — single-pass scaffold; no retry loops encountered. GitHub push skipped only due to missing auth tooling, not a code failure.