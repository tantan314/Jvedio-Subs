import os
import json
import re

# 基础配置
SUBTITLES_DIR = 'subtitles'
OUTPUT_FILE = 'index.json'

def clean_vid(filename):
    """
    番号深度清洗器：将各种乱七八糟的命名统一洗为绝对净番号
    """
    # 1. 剥离扩展名
    base_name = os.path.splitext(filename)[0]
    
    # 2. 核心匹配：秒杀 259LUXU, 001-ARA 以及后缀如 -C, _4k 等冗余信息
    match = re.search(r'([a-zA-Z][a-zA-Z0-9]{1,6}-\d{2,6})', base_name)
    if match:
        return match.group(1).upper()
        
    # --- 特殊番号兜底补丁 ---
    
    # 补丁 1: 纯数字开头的特例片商 (1PONDO, 10MUSUME)
    match_num_start = re.search(r'(1PONDO|10MUSUME)[-_]?(\d+)', base_name, re.IGNORECASE)
    if match_num_start:
        return f"{match_num_start.group(1).upper()}-{match_num_start.group(2)}"

    # 补丁 2: FC2 格式处理 (例如 FC2-PPV-123456, fc2_123456)
    match_fc2 = re.search(r'(FC2[-_]*(?:PPV)?[-_]*\d{5,7})', base_name, re.IGNORECASE)
    if match_fc2:
        # 再次提取出纯数字部分
        nums_match = re.search(r'(\d{5,7})', match_fc2.group(1))
        if nums_match:
            return f"FC2-PPV-{nums_match.group(1)}"

    # 如果所有正则都未命中，返回大写的原文件名（不含扩展名）作为最后兜底
    return base_name.upper()

def main():
    # 安全检查：如果目录不存在，自动创建（防止首次运行报错）
    if not os.path.exists(SUBTITLES_DIR):
        os.makedirs(SUBTITLES_DIR)
        print(f"Directory '{SUBTITLES_DIR}' created.")
        
    index_dict = {}
    valid_extensions = ('.srt', '.ass', '.vtt', '.ssa')
    
    # 遍历字幕文件夹
    for filename in os.listdir(SUBTITLES_DIR):
        if filename.lower().endswith(valid_extensions):
            # 获取清洗后的绝对净番号
            vid_key = clean_vid(filename)
            
            # Value 记录相对路径，供 C# 客户端拼接 jsDelivr 直链
            # 注意：此处强制使用正斜杠 '/' 保证 URL 路径规范
            relative_path = f"{SUBTITLES_DIR}/{filename}"
            index_dict[vid_key] = relative_path
            
    # 将字典持久化为 JSON 文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # ensure_ascii=False 保证中文字符不被转义
        # separators 压缩体积，去掉无用空格
        json.dump(index_dict, f, ensure_ascii=False, separators=(',', ':'))
        
    print(f"Success! Indexed {len(index_dict)} subtitle files.")
    print("Sample Output:")
    
    # 打印前 5 条作为 Actions 运行日志的检查项
    sample_items = list(index_dict.items())[:5]
    for k, v in sample_items:
        print(f"  {k} -> {v}")

if __name__ == '__main__':
    main()
