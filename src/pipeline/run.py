import argparse, os, json, csv, yaml
from typing import Dict, Any
from ..adapters.local_csv_adapter import LocalCSVAdapter
from ..lcm.mock_lcm import MockLCM
from ..governance.audit import Auditor

def main(config_path: str):
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # Adapter
    if cfg["adapter"]["type"] != "local_csv":
        raise ValueError("Public demo only supports local_csv adapter")
    adapter = LocalCSVAdapter(cfg["adapter"]["options"]["tables"])

    # LCM
    lcm = MockLCM(cfg["taxonomy_path"])

    # Outputs
    out_dir = cfg["outputs"]["dir"]
    os.makedirs(out_dir, exist_ok=True)
    auditor = Auditor(out_dir)

    concept_fp = open(os.path.join(out_dir, "concept_tags.jsonl"), "w", encoding="utf-8")         if cfg["outputs"].get("write_concept_tags") else None
    vector_fp = open(os.path.join(out_dir, "vector_records.jsonl"), "w", encoding="utf-8")         if cfg["outputs"].get("write_vector_like") else None
    graph_fp = open(os.path.join(out_dir, "graph_edges.csv"), "w", encoding="utf-8", newline="")         if cfg["outputs"].get("write_graph_edges") else None

    if graph_fp:
        gw = csv.writer(graph_fp)
        gw.writerow(["subject", "relation", "object", "evidence"])

    # Process
    for row in adapter.rows():
        tags = lcm.tag_record(row)
        auditor.log({"event": "tagged", "table": row.get("__table__"), "tags_count": len(tags)})

        if concept_fp:
            concept_fp.write(json.dumps({"table": row.get("__table__"), "row": row, "tags": tags}) + "\n")

        # Vector-like: turn concept_ids into stable ints (toy; no real embeddings)
        if vector_fp and tags:
            concept_ids = sorted(t["concept_id"] for t in tags)
            toy_vec = [hash(cid) % 1000 / 1000.0 for cid in concept_ids]
            vector_fp.write(json.dumps({
                "table": row.get("__table__"),
                "row_id": hash(json.dumps(row, sort_keys=True)) % 10_000_000,
                "concept_ids": concept_ids,
                "vector": toy_vec
            }) + "\n")

        # Graph edges example: employee manages department, transaction belongs_to employee
        if graph_fp:
            if row.get("department"):
                gw.writerow([row.get("email"), "belongs_to", row.get("department"), "department field"])
            if row.get("description") and row.get("employee_id"):
                gw.writerow([row.get("employee_id"), "pays", row.get("description"), "txn description"])

    if concept_fp: concept_fp.close()
    if vector_fp: vector_fp.close()
    if graph_fp: graph_fp.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=str, required=True)
    args = ap.parse_args()
    main(args.config)
