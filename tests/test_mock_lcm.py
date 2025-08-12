from src.lcm.mock_lcm import MockLCM

def test_basic_tagging(tmp_path):
    taxonomy = tmp_path / "tax.yaml"
    taxonomy.write_text("""
domains:
  - id: D1
    name: Test
    concepts:
      - id: C.Person
        keywords: [name, email]
""")
    lcm = MockLCM(str(taxonomy))
    rec = {"foo": "Name: Alice", "bar": ""}
    tags = lcm.tag_record(rec)
    assert any(t["concept_id"] == "C.Person" for t in tags)
