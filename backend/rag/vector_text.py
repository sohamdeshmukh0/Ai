from qdrant_client import QdrantClient
from qdrant_client.models import PointIdsList
 
def show_all_documents(collection_name="project_chunks", host="localhost", port=6333, limit=100):
    
    client = QdrantClient(
    url="https://1cdab6f0-3a76-4029-809c-ec4670e88251.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.e9yAV2JBKIPkXfEesfvkMFoNbDphzS78fCG5bAgs-nU",
)
    scroll_result = client.scroll(
        collection_name=collection_name,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    for point in scroll_result[0]:
        print(f"ID: {point.id}")
        print(f"Text: {point.payload.get('text')}")
        print("-" * 40)
    if not scroll_result[0]:
        print("No documents found in the collection.")
   
def delete_all_vectors(collection_name="project_chunks", host="localhost", port=6333):
    client = QdrantClient(host=host, port=port)
    # Get all point IDs
    scroll_result = client.scroll(
        collection_name=collection_name,
        with_payload=False,
        with_vectors=False
    )
    point_ids = [point.id for point in scroll_result[0]]
    if point_ids:
        client.delete(
            collection_name=collection_name,
            points_selector=PointIdsList(points=point_ids)
        )
        print(f"All vectors deleted from collection '{collection_name}'.")
    else:
        print("No points to delete.")
 
if __name__ == "__main__":
    show_all_documents()
    # delete_all_vectors()
 