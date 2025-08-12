# Base Zero — Public Demo (Safe Share)

This repository demonstrates the **shape** of the Syntropy/Base Zero concept-intelligence pipeline **without** exposing core IP.  
It ships with **synthetic data**, a **mock LCM**, and a **pluggable adapter** pattern so you can run end-to-end locally and show value on GitHub/LinkedIn.

> ⚠️ **IP Safety**: This repo excludes proprietary taxonomies, rules, prompts, embeddings, and any client-specific schemas. All examples and outputs are synthetic.

---

## What this shows
- Ingestion from a pluggable **adapter** (CSV in this demo; swap for Databricks in private)
- A **Mock LCM** that performs rule-based concept tagging (replace with your private LCM)
- Unified outputs to **vector-like** JSONL & simple **graph edge list**
- **Governance trace**: run metadata + audit log to illustrate explainability

---

## Quickstart
```bash
# 1) Create and activate a venv (recommended)
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install
pip install -r requirements.txt

# 3) Run demo (uses synthetic CSV adapter + mock LCM)
python -m src.pipeline.run --config src/pipeline/config.yaml

Outputs are written to ./outputs/:
	•	concept_tags.jsonl — row-level concept tags
	•	vector_records.jsonl — toy vector-like output (no real embeddings)
	•	graph_edges.csv — simple subject→object edges for visualization
	•	audit_log.jsonl — governance/audit trail of the run
## Architecture (public-safe)
```mermaid
flowchart LR
  A[Data Adapter (CSV)] -->|tables, rows| B[Parsing & Normalization]
  B --> C[Mock LCM (keywords/rules)]
  C --> D[Concept Tags]
  C --> E[Vector-like Records (JSONL)]
  D --> F[Graph Edge List]
  A --> G[Governance/Audit]
  C --> G
```
Swap **A** for a private Databricks adapter and **C** for your private LCM logic in your internal repo.

## Replace points (private-only)
- `src/lcm/mock_lcm.py` → replace with real LCM interface implementation
- `examples/taxonomy/base_zero_public.yaml` → keep synthetic; real taxonomy lives privately
- `src/pipeline/config.yaml` → adapt adapters + output sinks privately

## License
Default is **Business Source License 1.1 (BSL)** to deter commercial reuse. Choose your preference.
