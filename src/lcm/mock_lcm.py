from typing import List, Dict, Any
import yaml
from .interface import LCMInterface

class MockLCM(LCMInterface):
    """Simple keyword-based tagger for public demo only."""
    def __init__(self, taxonomy_path: str):
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            self.tax = yaml.safe_load(f)
        self.rules = []
        for dom in self.tax.get("domains", []):
            for c in dom.get("concepts", []):
                kws = [k.lower() for k in c.get("keywords", [])]
                self.rules.append({"concept_id": c["id"], "keywords": kws})

    def tag_record(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = " ".join(str(v).lower() for v in record.values())
        tags = []
        for rule in self.rules:
            hits = [kw for kw in rule["keywords"] if kw in text]
            if hits:
                tags.append({
                    "concept_id": rule["concept_id"],
                    "evidence": ",".join(hits),
                    "score": min(1.0, 0.3 + 0.1 * len(hits))
                })
        return tags
