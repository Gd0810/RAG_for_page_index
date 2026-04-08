import json
import os
from PyPDF2 import PdfReader

class PageIndexer:
    def __init__(self, data_dir, index_path):
        self.data_dir = data_dir
        self.index_path = index_path
        self.index = []
    
    def extract_pdf(self, pdf_path):
        """Extract text from PDF with page numbers"""
        reader = PdfReader(pdf_path)
        doc_name = os.path.basename(pdf_path)
        
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            
            # Split into paragraphs (simple split by double newline)
            paragraphs = text.split('\n\n')
            
            for para_num, para in enumerate(paragraphs, start=1):
                if para.strip():  # Skip empty paragraphs
                    self.index.append({
                        'doc_name': doc_name,
                        'page': page_num,
                        'paragraph': para_num,
                        'text': para.strip(),
                        'id': f"{doc_name}_p{page_num}_par{para_num}"
                    })
    
    def extract_text_file(self, txt_path):
        """Extract text from .txt file with line numbers"""
        doc_name = os.path.basename(txt_path)
        
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into chunks (e.g., every 5 lines or by paragraphs)
        paragraphs = content.split('\n\n')
        
        for para_num, para in enumerate(paragraphs, start=1):
            if para.strip():
                self.index.append({
                    'doc_name': doc_name,
                    'page': 1,  # Text files don't have pages
                    'paragraph': para_num,
                    'text': para.strip(),
                    'id': f"{doc_name}_par{para_num}"
                })
    
    def build_index(self):
        """Build index from all documents in data directory"""
        print("Building page index...")
        
        for filename in os.listdir(self.data_dir):
            filepath = os.path.join(self.data_dir, filename)
            
            if filename.endswith('.pdf'):
                print(f"Indexing PDF: {filename}")
                self.extract_pdf(filepath)
            elif filename.endswith('.txt'):
                print(f"Indexing TXT: {filename}")
                self.extract_text_file(filepath)
        
        # Save index
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)
        
        print(f"Index built! Total chunks: {len(self.index)}")
        return self.index