from src.retriever import PageRetriever
from src.llm_client import NvidiaLLM

class RAGPipeline:
    def __init__(self, index_path):
        self.retriever = PageRetriever(index_path)
        self.llm = NvidiaLLM()
    
    def create_context(self, chunks):
        """Format retrieved chunks into context"""
        context = ""
        for i, chunk in enumerate(chunks, 1):
            context += f"\n[Source {i}: {chunk['doc_name']}, Page {chunk['page']}, Para {chunk['paragraph']}]\n"
            context += chunk['text']
            context += "\n---\n"
        return context
    
    def query(self, question, top_k=3):
        """Main RAG query function"""
        # Step 1: Retrieve relevant chunks
        print(f"Searching for: {question}")
        chunks = self.retriever.keyword_search(question, top_k=top_k)
        
        if not chunks:
            return "No relevant information found in the documents."
        
        # Step 2: Create context from chunks
        context = self.create_context(chunks)
        
        # Step 3: Create prompt
        prompt = f"""Based on the following information, answer the question.

Context:
{context}

Question: {question}

Answer (cite the sources by page number):"""
        
        # Step 4: Generate response
        print("Generating response...")
        response = self.llm.generate_response(prompt)
        
        return {
            'answer': response,
            'sources': chunks
        }