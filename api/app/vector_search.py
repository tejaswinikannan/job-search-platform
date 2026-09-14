import chromadb
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-mpnet-base-v2")
_client = chromadb.PersistentClient(path="./chroma_db")
_collection = _client.get_or_create_collection("jobs", metadata={"hnsw:space": "cosine"})


def index_jobs(jobs: list) -> None:
    texts = [f"{job.title}. {job.description}" for job in jobs]
    ids = [str(job.id) for job in jobs]
    embeddings = _model.encode(texts).tolist()
    _collection.upsert(ids=ids, documents=texts, embeddings=embeddings)


def semantic_search(query: str, top_k: int = 10) -> list[tuple[int, float]]:
    query_embedding = _model.encode([query]).tolist()
    results = _collection.query(query_embeddings=query_embedding, n_results=top_k)
    return [
        (int(job_id), distance)
        for job_id, distance in zip(results["ids"][0], results["distances"][0])
    ]
