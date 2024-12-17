import re

def clean_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    skip_next = False
    short_line_count = 0
    max_line_length = 0
    line_lengths = []

    # 第一遍遍历，找出正常单栏行的最大字符长度
    for line in lines:
        line = line.strip()
        if len(line) > 10 and len(line) < 120:  # 扩大范围到120
            max_line_length = max(max_line_length, len(line))
            line_lengths.append(len(line))

    # 输出调试信息
    print(f"检测到的最大行长度: {max_line_length}")
    print(f"行长度分布: 最小 {min(line_lengths)}, 最大 {max(line_lengths)}, 平均 {sum(line_lengths)/len(line_lengths):.2f}")

    # 设定长度阈值，使用0.9作为系数
    length_threshold = int(max_line_length * 0.9)
    print(f"设定的长度阈值: {length_threshold}")

    for i, line in enumerate(lines):
        line = line.strip()
        
        # 跳过页面分隔符及其上下行
        if '----页面分隔----' in line or skip_next:
            skip_next = False
            continue
        if i < len(lines) - 1 and '----页面分隔----' in lines[i+1]:
            continue
        
        # 跳过特定内容
        if re.search(r'\d{4}\s+University\s+of\s+Kansas', line):
            continue
        
        # 跳过只包含一个数字的行（可能是页码）
        if re.match(r'^\d+$', line):
            continue
        
        # 跳过疑似跨列内容的行
        if re.search(r'\w+\s+\w+\s+\w+\s+\w+\s+\w+', line) and len(set(line.split())) > 10:
            print(f"跳过疑似跨列内容 ({len(line)} 字符): {line[:50]}...")
            continue
        
        # 跳过长行，但保留看起来像完整句子的内容
        if len(line) > length_threshold and not line[0].isupper() and not line[-1] in '.!?':
            print(f"跳过长行 ({len(line)} 字符): {line[:50]}...")
            continue
        
        # 处理短行
        if len(line) <= 15:  # 假设15个字符或更少为短行
            short_line_count += 1
        else:
            if short_line_count >= 2:  # 如果之前有连续两行或以上的短行，跳过它们
                cleaned_lines = cleaned_lines[:-short_line_count]
            short_line_count = 0
        
        cleaned_lines.append(line)

    # 处理文件末尾的短行
    if short_line_count >= 2:
        cleaned_lines = cleaned_lines[:-short_line_count]

    # 写入清理后的文本
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n')

    print(f"原始行数: {len(lines)}")
    print(f"清理后行数: {len(cleaned_lines)}")

# 使用示例
input_file = r"E:\DataT\v1_extracted_columns.txt"
output_file = r"E:\DataT\v1_cleaned.txt"
clean_text(input_file, output_file)

print(f"文本已清理并保存到 {output_file}")