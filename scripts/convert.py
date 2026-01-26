import requests
import os

# --- 配置区：按需修改链接、分类目录和重命名 ---
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
    # 你可以在这里增加 {} 格式的配置
]

BASE_DIR = "QuantumultX"
# --------------------------------------------

def convert_all():
    # 定义 Loon 到 QX 的语法映射
    mapping = {
        "DOMAIN-SUFFIX": "HOST-SUFFIX",
        "DOMAIN": "HOST",
        "DOMAIN-KEYWORD": "HOST-KEYWORD",
        "IP-CIDR": "IP-CIDR",
        "IP-CIDR6": "IP-CIDR6",
        "USER-AGENT": "USER-AGENT"
    }

    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    for item in SOURCE_URLS:
        url = item["url"]
        category = item["category"]
        target_filename = item.get("rename") or url.split('/')[-1]
        
        try:
            # 准备输出路径
            target_dir = os.path.join(BASE_DIR, category)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            print(f"正在处理: {url} -> {category}/{target_filename}")
            
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            lines = resp.text.splitlines()
            
            qx_rules = []
            for line in lines:
                line = line.strip()
                
                # 1. 跳过或保留空行、注释、头部标签
                if not line or line.startswith(("#", ";", "[")):
                    qx_rules.append(line)
                    continue
                
                # 2. 分割规则行 (例如: DOMAIN-SUFFIX,google.com,Proxy)
                parts = line.split(',')
                if len(parts) < 2:
                    qx_rules.append(line)
                    continue

                rule_type = parts[0].strip().upper()
                
                # 3. 如果命中映射表，执行格式转换
                if rule_type in mapping:
                    new_type = mapping[rule_type]
                    # 只取第二部分（域名/IP），彻底丢弃后面的 Proxy 等策略名
                    core_value = parts[1].strip()
                    
                    # 重新组装成 QX 格式 (类型,值)
                    new_line = f"{new_type},{core_value}"
                    
                    # 特殊处理 no-resolve 标志
                    if "no-resolve" in line.lower():
                        new_line += ",no-resolve"
                        
                    qx_rules.append(new_line)
                else:
                    # 对于识别不了的行（如 FINAL），原样保留
                    qx_rules.append(line)

            # 保存文件
            output_path = os.path.join(target_dir, target_filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(qx_rules))
            print(f"✅ 转换成功: {output_path}")

        except Exception as e:
            print(f"❌ 处理 {url} 时出错: {e}")

if __name__ == "__main__":
    convert_all()
