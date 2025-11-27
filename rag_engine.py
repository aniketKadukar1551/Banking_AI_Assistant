import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from pymilvus import MilvusClient
import numpy as np

class BankRAG:
    def __init__(self, collection_name="banking_docs", db_file="./milvus_demo.db"):
        self.collection_name = collection_name
        self.client = MilvusClient(db_file)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_dim = 384
        
        if self.client.has_collection(collection_name):
            self.client.drop_collection(collection_name)
            
        self.client.create_collection(
            collection_name=collection_name,
            dimension=self.vector_dim
        )

    def ingest_docs(self, pdf_paths):
        print("Ingesting documents...")
        all_splits = []
        for path in pdf_paths:
            loader = PyPDFLoader(path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            splits = text_splitter.split_documents(docs)
            all_splits.extend(splits)
            
        data = []
        for i, split in enumerate(all_splits):
            text = split.page_content
            vector = self.encoder.encode(text).tolist()
            data.append({"id": i, "vector": vector, "text": text, "source": split.metadata.get("source", "unknown")})
            
        self.client.insert(collection_name=self.collection_name, data=data)
        print(f"Ingested {len(data)} chunks into Milvus.")

    def retrieve(self, query, top_k=3):
        query_vector = self.encoder.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=top_k,
            output_fields=["text", "source"]
        )
        
        retrieved_texts = []
        for res in results[0]:
            retrieved_texts.append(f"[Source: {os.path.basename(res['entity']['source'])}]\n{res['entity']['text']}")
            
        return "\n\n".join(retrieved_texts)

if __name__ == "__main__":
    # Test run
    rag = BankRAG()
    rag.ingest_docs(["data/fee_schedule.pdf"])
    print(rag.retrieve("What is the overdraft fee?"))
