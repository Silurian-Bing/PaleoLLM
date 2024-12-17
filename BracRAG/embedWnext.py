from weaviate import Client
import json
import numpy as np

# 创建 Weaviate 客户端
client = Client("http://localhost:6000")  # 使用您设置的端口

def semantic_search(query, limit=5):
    try:
        # 这里我们需要将查询转换为向量
        # 由于我们没有直接访问原始模型，我们将使用一个随机向量作为示例
        # 在实际应用中，您应该使用与原始嵌入相同的模型来生成查询向量
        query_vector = np.random.rand(384).tolist()  # 假设原始向量维度为 384

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
query = "cardinal process"
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

# 检查是否有数据在 Weaviate 中
try:
    objects = client.data_object.get()
    print(f"\nNumber of objects in Weaviate: {len(objects['objects'])}")
except Exception as e:
    print(f"Error fetching objects: {str(e)}")