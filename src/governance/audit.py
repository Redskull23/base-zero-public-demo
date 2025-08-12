import json, os, time
from typing import Dict, Any

class Auditor:
    def __init__(self, output_dir: str):
        self.path = os.path.join(output_dir, "audit_log.jsonl")
        os.makedirs(output_dir, exist_ok=True)

    def log(self, event: Dict[str, Any]):
        event["ts"] = time.time()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
