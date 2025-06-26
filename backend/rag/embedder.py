from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
load_dotenv()
import time
 

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model= SentenceTransformer(model_name)

    def generate_embeddings(self, text):
        embeddings =  self.model.encode(text, convert_to_numpy=True)
        if isinstance(embeddings, list):
            # If the input is a list of texts, return a list of embeddings
            return [self.model.encode(t, convert_to_numpy=True) for t in text]
        # elif isinstance(embeddings, str):
        #     # If the input is a single string, return its embedding
        #     return self.model.encode([text], convert_to_numpy=True)[0]
        return embeddings
    
    
if __name__ == "__main__":
    start_time = time.time()
    test_embedder = Embedder()
    text = "This is a sample text for embedding."
    embedding = test_embedder.generate_embeddings(text)
    print("Single text embedding:")
    print(len(embedding))
    end_time = time.time()
    print(f"Processing time: {end_time - start_time} seconds")