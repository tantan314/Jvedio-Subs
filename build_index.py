import os
import json

SUBTITLES_DIR = 'subtitles'
OUTPUT_FILE = 'index.json'

def main():
    if not os.path.exists(SUBTITLES_DIR):
        os.makedirs(SUBTITLES_DIR)
        print(f"Directory '{SUBTITLES_DIR}' created.")
        
    index_dict = {}
    valid_extensions = ('.srt', '.ass', '.vtt', '.ssa')
    
    # 诊断探针初始化
    collisions = []
    skipped_files = []
    
    for filename in os.listdir(SUBTITLES_DIR):
        # 排除误入的文件夹
        if not os.path.isfile(os.path.join(SUBTITLES_DIR, filename)):
            continue

        if filename.lower().endswith(valid_extensions):
            base_name = os.path.splitext(filename)[0]
            vid_key = base_name.upper()
            
            relative_path = f"{SUBTITLES_DIR}/{filename}"
            
            # 探针 1：检测 Key 是否已经存在（拦截覆盖动作）
            if vid_key in index_dict:
                collisions.append({
                    "key": vid_key,
                    "old_file": index_dict[vid_key],
                    "new_file": relative_path
                })
                
            index_dict[vid_key] = relative_path
        else:
            # 探针 2：记录所有因为后缀名不符被拦截的文件
            skipped_files.append(filename)
            
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_dict, f, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
        
    # ==========================================
    # 输出格式化诊断日志 (供 Github Actions 抓取)
    # ==========================================
    print("\n" + "=" * 50)
    print(f"[执行报告] 物理目录总文件数: {len(os.listdir(SUBTITLES_DIR))}")
    print(f"[执行报告] 成功生成索引条目: {len(index_dict)}")
    print("=" * 50)
    
    if collisions:
        print(f"\n[数据碰撞预警] 发现 {len(collisions)} 次键值覆盖！")
        print("说明: 以下文件拥有相同的番号，字典字典已保留后者，丢弃前者。")
        for c in collisions:
            print(f"  [冲突 Key]: {c['key']}")
            print(f"    - 被覆盖丢弃: {c['old_file']}")
            print(f"    - 最终被保留: {c['new_file']}")
            print("-" * 30)
            
    if skipped_files:
        print(f"\n[格式拦截预警] 发现 {len(skipped_files)} 个被规则剔除的文件！")
        print("说明: 后缀名非法或为系统隐藏文件。")
        for s in skipped_files:
            print(f"  [已跳过] -> {s}")
            
    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()
