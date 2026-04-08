import json
import re

class PageRetriever:
    def __init__(self, index_path):
        self.index_path = index_path
        self.load_index()
    
    def load_index(self):
        """Load the page index"""
        with open(self.index_path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)
    
    def keyword_search(self, query, top_k=3):
        """Simple keyword-based search"""
        query_words = set(query.lower().split())
        results = []
        
        for chunk in self.index:
            text_lower = chunk['text'].lower()
            
            # Count matching words
            matches = sum(1 for word in query_words if word in text_lower)
            
            if matches > 0:
                results.append({
                    'chunk': chunk,
                    'score': matches
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return [r['chunk'] for r in results[:top_k]]
    
    def search_by_page(self, doc_name, page_num):
        """Retrieve all content from a specific page"""
        results = []
        for chunk in self.index:
            if chunk['doc_name'] == doc_name and chunk['page'] == page_num:
                results.append(chunk)
        return results
    
    def search_by_doc(self, doc_name, top_k=5):
        """Get first top_k chunks from a document"""
        results = []
        for chunk in self.index:
            if chunk['doc_name'] == doc_name:
                results.append(chunk)
                if len(results) >= top_k:
                    break
        return results