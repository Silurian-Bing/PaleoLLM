from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

# 加载模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 读取分割后的文本
def read_chunks(file_path):
    chunks = []
    with open(file_path, 'r', encoding='utf-8') as file:
        current_chunk = ""
        for line in file:
            if line.startswith("Chunk "):
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = ""
            elif line.startswith("=="):
                continue
            else:
                current_chunk += line
        if current_chunk:
            chunks.append(current_chunk.strip())
    return chunks

# 创建嵌入
def create_embeddings(chunks, batch_size=32):
    embeddings = []
    for i in tqdm(range(0, len(chunks), batch_size), desc="Creating embeddings"):
        batch = chunks[i:i+batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
    return np.array(embeddings)

# 主程序
if __name__ == "__main__":
    input_file = r"E:\DataT\chunked_text_new.txt"
    output_file = r"E:\DataT\chunk_embeddings.npy"

    print("Reading chunks...")
    chunks = read_chunks(input_file)
    print(f"Read {len(chunks)} chunks.")

    print("Creating embeddings...")
    embeddings = create_embeddings(chunks)

    print("Saving embeddings...")
    np.save(output_file, embeddings)

    print(f"Embeddings saved to {output_file}")
    print(f"Shape of embeddings: {embeddings.shape}")
