# Brachiopods Semantic Search System

A comprehensive system for processing brachiopods text data and enabling semantic search capabilities using modern NLP techniques and vector databases.

## System Components

### 1. Text Processing Pipeline
- **text_preprocessor.py**: Cleans and formats raw text data, removing artifacts and normalizing content.
- **text_chunker.py**: Splits processed text into manageable chunks with configurable size and overlap.

### 2. Embedding Generation
- **embeddings_generator.py**: Generates text embeddings using the all-MiniLM-L6-v2 model from sentence-transformers.

### 3. Vector Database Integration
- **weaviate_schema_setup.py**: Initializes Weaviate database schema for storing text chunks and their embeddings.
- **weaviate_data_loader.py**: Loads generated embeddings and corresponding text chunks into Weaviate.
- **semantic_search.py**: Implements semantic search functionality using the embedded vectors.

## Prerequisites
- Python 3.7+
- sentence-transformers
- Weaviate
- numpy
- tqdm

## Installation
1. Clone this repository
2. Install required packages:
```bash
pip install sentence-transformers weaviate-client numpy tqdm
