from weaviate import Client
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 创建 Weaviate 客户端
client = Client("http://localhost:6000")

# 加载与embed.py相同的模型
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_search(query, limit=5):
    try:
        # 使用模型将查询文本转换为向量
        query_vector = model.encode(query).tolist()

        result = (
            client.query
            .get("TextChunk", ["content", "chunk_id"])
            .with_near_vector({
                "vector": query_vector
            })
            .with_limit(limit)
            .do()
        )
        
        print("Raw API response:")
        print(json.dumps(result, indent=2))  # 打印完整的 API 响应
        
        if "data" in result and "Get" in result["data"] and "TextChunk" in result["data"]["Get"]:
            return result["data"]["Get"]["TextChunk"]
        else:
            print("Unexpected response structure.")
            return result
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# 测试检索
query = "cardinal process"  # 您可以修改这个查询文本
results = semantic_search(query)

if results is not None:
    if isinstance(results, list):
        print(f"\nQuery: {query}")
        for i, result in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Chunk ID: {result.get('chunk_id', 'N/A')}")
            print(f"Content: {result.get('content', 'N/A')[:200]}...")
    else:
        print("Unexpected result format. Raw result:")
        print(json.dumps(results, indent=2))
else:
    print("No results returned.")

# 检查数据库中的对象数量
try:
    objects = client.data_object.get()
    print(f"\nNumber of objects in Weaviate: {len(objects['objects'])}")
except Exception as e:
    print(f"Error fetching objects: {str(e)}")

# 展示一些样本数据
def show_sample_data(limit=3):
    try:
        print("\nShowing sample data from database:")
        result = (
            client.query
            .get("TextChunk", ["content", "chunk_id"])
            .with_limit(limit)
            .do()
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error fetching sample data: {str(e)}")

show_sample_data()