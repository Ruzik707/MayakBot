import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("build_index", Path(__file__).resolve().parents[1] / "src/rag/build_index.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class IndexInputTests(unittest.TestCase):
    def load(self, rows):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "corpus.jsonl"
            path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")
            return builder.load_chunks(path)

    def test_list_metadata_and_duplicate_ids(self):
        row = {"chunk_id": "poem_1", "text": "Фрагмент", "metadata": {"tags": ["тема"], "unused": None}}
        result = self.load([row, row])
        self.assertEqual(len(result), 1)
        self.assertEqual(json.loads(result[0]["metadata"]["tags"]), ["тема"])
        self.assertNotIn("unused", result[0]["metadata"])

    def test_conflicting_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            self.load([{"chunk_id": "same", "text": "A"}, {"chunk_id": "same", "text": "B"}])

    def test_empty_text_and_empty_corpus_are_rejected(self):
        for rows in [[], [{"text": " "}]]:
            with self.assertRaises(ValueError):
                self.load(rows)


if __name__ == "__main__":
    unittest.main()
