import re
def split_text_safe(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        # 如果不是最后一个chunk，尝试在一个完整的单词处结束
        if end < text_length:
            # 向后查找最近的空白字符，但最多查找100个字符
            for i in range(min(100, chunk_size)):
                if end - i > start and text[end - i].isspace():
                    end = end - i
                    break
        
        chunk = text[start:end].strip()
        if chunk:  # 只添加非空的chunk
            chunks.append(chunk)
        
        start = end
        if len(chunks) % 100 == 0:
            print(f"Processed {len(chunks)} chunks")

    return chunks

# 使用新函数重新分割文本
import time

start_time = time.time()
with open(r"E:\DataT\v1_cleaned.txt", 'r', encoding='utf-8') as file:
    text = file.read()

new_chunks = split_text_safe(text)
print(f"Total chunks created: {len(new_chunks)}")

# 检查chunk大小
chunk_sizes = [len(chunk) for chunk in new_chunks]
print(f"Average chunk size: {sum(chunk_sizes) / len(chunk_sizes):.2f}")
print(f"Min chunk size: {min(chunk_sizes)}")
print(f"Max chunk size: {max(chunk_sizes)}")

# 保存新的分割结果
with open(r"E:\DataT\chunked_text_new.txt", 'w', encoding='utf-8') as file:
    for i, chunk in enumerate(new_chunks):
        file.write(f"Chunk {i}:\n{chunk}\n{'='*50}\n")

# 验证总字符数
total_chars = sum(chunk_sizes)
print(f"Total characters in all chunks: {total_chars}")
print(f"Original text length: {len(text)}")
print(f"Time taken: {time.time() - start_time:.2f} seconds")
