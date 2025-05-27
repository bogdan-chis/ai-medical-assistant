from datasets import load_dataset
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
import re
import multiprocessing
from functools import partial
from tqdm import tqdm
import time
from backend.data.postprocessing import extract_efficient_metadata
from backend.data.dataset_loader import load_dataset

dataset = load_dataset()

# Process documents in parallel
def process_document(item, idx):

    question = item['input']
    answer = item['output']
    content = f"Question: {question}\nAnswer: {answer}"
    
    # Extract metadata efficiently
    metadata = extract_efficient_metadata(question, answer)
    metadata["doc_id"] = idx

    return Document(page_content=content, metadata=metadata)


def process_dataset(dataset):
    print(f"Processing {len(dataset)} dialogues...")
    all_docs = []
    start = time.time()

    for idx, item in tqdm(enumerate(dataset), total=len(dataset), desc="Creating documents"):
        doc = process_document(item, idx)
        all_docs.append(doc)

    print(f"Done in {time.time() - start:.2f}s")
    return all_docs


def load_and_process_dataset():
    documents = process_dataset(dataset)
    return documents


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=150,
    separators=["\n\n", "\n", ". "]
)

def safe_split_document(doc):
    if len(doc.page_content) > 1500:
        return splitter.split_documents([doc])
    else:
        return [doc]
    

def create_split_documents():
    docs = load_and_process_dataset()
    split_documents = []
    for doc in docs:
        split_documents.extend(safe_split_document(doc))

    return split_documents