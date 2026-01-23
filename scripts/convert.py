import requests
import os

# --- 配置区：在此定义链接、目录和自定义文件名 ---
SOURCE_URLS = [
    {
        "url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/cdn-domain.list", 
        "category": "Apple", 
        "rename": "Apple_CDN.list"  # 自定义文件名
    },
    {
        "url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/domain.list", 
        "category": "Apple", 
        "rename": "Apple_CN.list"    # 自定义文件名
    },
    {
        "url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/no-cn-cdn-domain.list", 
        "category": "Apple", 
        "rename": "Apple_No_CN_CDN.list"    # 自定义文件名
    },
    {
        "url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/api-domain.list", 
        "category": "Apple", 
        "rename": "Apple_Api.list"    # 自定义文件名
    },
    {
        "url": "https://ruleset.skk.moe/List/non_ip/ai.conf", 
        "category": "AI", 
        "rename": "AI.list"      # 自定义文件名
    },
]

BASE_DIR = "QuantumultX"
# --------------------------------------------

def convert_all():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    mapping = {
        "DOMAIN-SUFFIX": "HOST-SUFFIX",
        "DOMAIN": "HOST",
        "DOMAIN-KEYWORD": "HOST-KEYWORD",
        "IP-CIDR": "IP-CIDR",
        "IP-CIDR6": "IP-CIDR6",
        "USER-AGENT": "USER-AGENT"
    }

    for item in SOURCE_URLS:
        url = item["url"]
        category = item["category"]
        # 核心修改：如果定义了 rename 则使用它，否则从 URL 提取
        target_filename = item.get("rename") or url.split('/')[-1]
        
        try:
            target_dir = os.path.join(BASE_DIR, category)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            print(f"正在转换 [{category}] -> {target_filename}...")
            
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            
            lines = resp.text.splitlines()
            qx_rules = []

            for line in lines:
                line = line.strip()
                if not line or line.startswith(("#", ";", "[")):
                    qx_rules.append(line)
                    continue
                
                parts = line.split(',')
                rule_type = parts[0].strip().upper()
                
                if rule_type in mapping:
                    new_type = mapping[rule_type]
                    val = parts[1].strip()
                    new_line = f"{new_type},{val}"
                    
                    if "no-resolve" in line.lower():
                        new_line += ",no-resolve"
                    qx_rules.append(new_line)
                else:
                    qx_rules.append(line)

            output_path = os.path.join(target_dir, target_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(qx_rules))
            print(f"✅ 成功保存: {output_path}")

        except Exception as e:
            print(f"❌ 转换失败 {url}: {e}")

if __name__ == "__main__":
    convert_all()
