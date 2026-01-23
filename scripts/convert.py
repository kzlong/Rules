import requests
import os

# --- 配置区：定义链接及其归属目录 ---
SOURCE_URLS = [
    {"url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/api-domain.list", "category": "Apple"},
    {"url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/no-cn-cdn-domain.list", "category": "Apple"},
    {"url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/domain.list", "category": "Apple"},
    {"url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/cdn-domain.list", "category": "Apple"},
    {"url": "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/api-ip.list", "category": "Apple"},
    {"url": "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Loon/rule/AI.list", "category": "AI"},
    # 你可以继续按格式添加更多链接...
]

BASE_DIR = "QuantumultX"  # 根目录名称
# --------------------------------

def convert_all():
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
        
        try:
            filename = url.split('/')[-1]
            # 拼接完整路径：Quantumult X/Apple/文件名 或 Quantumult X/AI/文件名
            target_dir = os.path.join(BASE_DIR, category)
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            print(f"正在转换 [{category}]: {filename}...")
            
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
                    new_line = f"{new_type},{val}" # 不带策略名，由 QX force-policy 指定
                    
                    if "no-resolve" in line.lower():
                        new_line += ",no-resolve"
                    qx_rules.append(new_line)
                else:
                    qx_rules.append(line)

            output_path = os.path.join(target_dir, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(qx_rules))
            print(f"✅ 成功保存到 {output_path}")

        except Exception as e:
            print(f"❌ 转换 {url} 失败: {e}")

if __name__ == "__main__":
    convert_all()
