import os
import json

SUBTITLES_DIR = 'subtitles'
OUTPUT_FILE = 'index.json'

def main():
    # 若目录不存在则自动创建，防止 Actions 首次运行报错
    if not os.path.exists(SUBTITLES_DIR):
        os.makedirs(SUBTITLES_DIR)
        print(f"Directory '{SUBTITLES_DIR}' created.")
        
    index_dict = {}
    valid_extensions = ('.srt', '.ass', '.vtt', '.ssa')
    
    # 遍历并构建索引
    for filename in os.listdir(SUBTITLES_DIR):
        if filename.lower().endswith(valid_extensions):
            # 仅剥离扩展名，保留绝对原始的文件名
            base_name = os.path.splitext(filename)[0]
            
            # 统一转为大写作为 Key，抹平大小写差异造成的比对失败
            vid_key = base_name.upper()
            
            # Value 记录相对路径
            index_dict[vid_key] = f"{SUBTITLES_DIR}/{filename}"
            
    # 落地为 JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_dict, f, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
        
    print(f"Success! Indexed {len(index_dict)} subtitle files.")

if __name__ == '__main__':
    main()
