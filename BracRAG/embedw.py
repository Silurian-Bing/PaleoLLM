import weaviate
from weaviate.util import generate_uuid5

# 连接到 Weaviate
client = weaviate.Client("http://localhost:6000")

# 定义 schema
schema = {
    "class": "TextChunk",
    "vectorizer": "none",  # 我们将手动添加向量
    "vectorIndexType": "hnsw",
    "properties": [
        {
            "name": "content",
            "dataType": ["text"],
        },
        {
            "name": "chunk_id",
            "dataType": ["int"],
        }
    ]
}

# 创建 schema
client.schema.create_class(schema)