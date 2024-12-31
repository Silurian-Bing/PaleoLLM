# import_vectors.py
import numpy as np
from weaviate import Client

def import_data_to_weaviate():
    # 1. 加载向量和对应的文本数据
    vectors = np.load('chunk_embeddings.npy')
    
    # 2. 连接Weaviate
    client = Client("http://localhost:6000")
    
    # 3. 批量导入数据
    for i in range(len(vectors)):
        client.data_object.create({
            "class": "TextChunk",
            "vector": vectors[i].tolist(),
            "properties": {
                "content": texts[i],
                "chunk_id": i
            }
        })

if __name__ == "__main__":
    import_data_to_weaviate()