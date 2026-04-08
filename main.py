
import os
from src.indexer import PageIndexer
from src.rag_pipeline import RAGPipeline

def main():
    # Paths
    DATA_DIR = 'data/documents'
    INDEX_PATH = 'indexed_data/index.json'
    
    # Create directories if they don't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check if index exists, if not build it
    if not os.path.exists(INDEX_PATH):
        print("Index not found. Building index...")
        indexer = PageIndexer(DATA_DIR, INDEX_PATH)
        indexer.build_index()
    else:
        print("Index found. Loading...")
    
    # Initialize RAG pipeline
    rag = RAGPipeline(INDEX_PATH)
    
    # Interactive query loop
    print("\n=== RAG System Ready ===")
    print("Commands:")
    print("  - Ask any question")
    print("  - Type 'reindex' to rebuild the index")
    print("  - Type 'quit' to exit\n")
    
    while True:
        question = input("Your question: ").strip()
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'reindex':
            indexer = PageIndexer(DATA_DIR, INDEX_PATH)
            indexer.build_index()
            rag = RAGPipeline(INDEX_PATH)
            continue
        elif not question:
            continue
        
        # Get answer
        result = rag.query(question, top_k=3)
        
        print("\n" + "="*50)
        print("ANSWER:")
        print(result['answer'])
        print("\n" + "="*50)
        print("SOURCES:")
        for source in result['sources']:
            print(f"  - {source['doc_name']}, Page {source['page']}, Paragraph {source['paragraph']}")
        print("="*50 + "\n")

if __name__ == "__main__":
    main()

