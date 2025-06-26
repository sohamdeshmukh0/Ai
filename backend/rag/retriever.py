from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from typing import List, Any


class Retriever:

    def __init__(self, 
                 collection_name="project_chunks",
                 vector_size=384):
        
        self.collection_name = collection_name
        self.client = QdrantClient(
    url="https://1cdab6f0-3a76-4029-809c-ec4670e88251.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.e9yAV2JBKIPkXfEesfvkMFoNbDphzS78fCG5bAgs-nU"
)
        # Creating the collection if it doesn't exist
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )

    def insert_documents(self, documents: List[str], embeddings: List[Any]):
        points = [
            {"id": i, "vector": embedding, "payload": {"text": doc}}
            for i, (doc, embedding) in enumerate(zip(documents, embeddings))
        ]
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def retrieve(self, query_embedding, k=5):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k
        )
        filtered = [hit.payload["text"] for hit in results]
        return filtered

if __name__ == "__main__":
    docs = ["Random thing.", "I love apples.", "Document 3 about birds."]
    embeddings = [
        [0.1]*384,
        [0.2]*384,
        [0.3]*384,
    ]
    retriever = Retriever()
    retriever.insert_documents(docs, embeddings)
    query_embedding = [0.1]*384  # Replace with real embedding
    results = retriever.retrieve(query_embedding)
    print("Retrieved:", results)