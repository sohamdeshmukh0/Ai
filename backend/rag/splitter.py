from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import time

class Splitter:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=0,
            length_function=len,
            separators=["\n\n", "\n", " ", "",]
        )

    # Yeh List dega (of chunks)
    def chunks(self, text):
        return self.text_splitter.split_text(text)
    
if __name__ == "__main__":
    start_time = time.time()
    splitter = Splitter()
    text = open("oms.txt", "r", encoding="utf-8").read()
    chunks = splitter.chunks(text)
    end_time = time.time()
    print(f"Processing time: {end_time - start_time} seconds")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")
    print(f"Total chunks: {len(chunks)}")