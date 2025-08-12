from typing import List, Dict, Any

class LCMInterface:
    def tag_record(self, record: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Return concept tags for a single normalized record.
        Each tag is a dict like:
        {"concept_id": str, "evidence": str, "score": float}
        """
        raise NotImplementedError
