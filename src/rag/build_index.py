"""Build the local Chroma index used by both Telegram bots."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_chunks(path: Path) -> list[dict]:
    """Validate JSONL and convert metadata to Chroma-compatible scalar values."""
    chunks = {}
    with path.open(encoding="utf-8") as source:
        for number, line in enumerate(source, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row.get("text"), str) or not row["text"].strip():
                raise ValueError(f"Line {number}: non-empty text is required")
            chunk_id = str(row.get("chunk_id") or number)
            metadata = {}
            for key, value in row.get("metadata", {}).items():
                if value is None:
                    continue
                metadata[key] = value if isinstance(value, (str, int, float, bool)) else json.dumps(value, ensure_ascii=False)
            metadata["chunk_id"] = chunk_id
            chunk = {"id": chunk_id, "text": row["text"], "metadata": metadata}
            if chunk_id in chunks and chunks[chunk_id] != chunk:
                raise ValueError(f"Line {number}: conflicting chunk_id {chunk_id}")
            chunks[chunk_id] = chunk
    if not chunks:
        raise ValueError("The corpus is empty")
    return list(chunks.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=ROOT / "data/mayakovsky-corpus.jsonl")
    parser.add_argument("--index-dir", type=Path, default=ROOT / "data/chroma_db_mayakovsky")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])
    args = parser.parse_args()
    chunks = load_chunks(args.corpus)

    from langchain_core.documents import Document
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3", model_kwargs={"device": args.device})
    documents = [Document(page_content=row["text"], metadata=row["metadata"]) for row in chunks]
    Chroma.from_documents(documents, embeddings, ids=[row["id"] for row in chunks],
                          persist_directory=str(args.index_dir))
    print(f"Indexed {len(chunks)} chunks in {args.index_dir}")


if __name__ == "__main__":
    main()
