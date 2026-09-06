# AGENTS.md — Therapeutic-AI

Project rules for agents working in this repo. Global defaults in `C:/Users/PCD/.claude/CLAUDE.md` apply unless overridden here.

## Verification
Per global Verify Commands: detect stack by marker file; run build/lint/test after every change. **No app code exists yet** — verification for this planning repo = documentation/org consistency checks (file presence, internal links, markdown lint if configured).

## Documentation & Obsidian
- `/docs` reflects current state; update at end of every phase.
- Obsidian mirror: `C:/Users/PCD/Documents/Obsidian Vault/Projects/Therapeutic-AI/` (sync after each phase).

## Regulatory context (company-relevant for any agent touching docs/code)
- This is a **dual-track** company: drug-discovery research (non-SaMD) + FDA-cleared SaMD.
- **PCCP-first** posture: adaptive AI retraining must be pre-authorized and pipeline-validated.
- Never commit secrets/keys/PHI. Data provenance + train/test separation are non-negotiable design principles.

## Git
- Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`, etc.).
- Commit after every verified working change; push to GitHub when remote is configured.