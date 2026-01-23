import requests
import os

# --- 配置区：在此添加所有需要转换的 Loon 规则链接 ---
SOURCE_URLS = [
    "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/api-domain.list",
    "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/domain.list",
    "https://raw.githubusercontent.com/viewer12/OverseasAI.list/refs/heads/main/rule/Quantumult/OverseasAI/OverseasAI.list",
    # 你可以继续按格式添加更多链接...
]

OUTPUT_DIR = "Quantumult X"  # 输出文件夹名称
# ----------------------------------------------

def convert_all():
    # 确保输出目录存在
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    mapping = {
        "DOMAIN-SUFFIX": "HOST-SUFFIX",
        "DOMAIN": "HOST",
        "DOMAIN-KEYWORD": "HOST-KEYWORD",
        "IP-CIDR": "IP-CIDR",
        "IP-CIDR6": "IP-CIDR6",
        "USER-AGENT": "USER-AGENT"
    }

    for url in SOURCE_URLS:
        try:
            # 1. 自动提取原文件名
            filename = url.split('/')[-1]
            print(f"正在转换: {filename}...")

            # 2. 获取内容
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            
            lines = resp.text.splitlines()
            qx_rules = []

            for line in lines:
                line = line.strip()
                # 保留注释、空行和头部标签
                if not line or line.startswith(("#", ";", "[")):
                    qx_rules.append(line)
                    continue
                
                parts = line.split(',')
                rule_type = parts[0].strip().upper()
                
                if rule_type in mapping:
                    new_type = mapping[rule_type]
                    val = parts[1].strip()
                    # 按照你的要求：不加 POLICY_NAME，仅生成 核心类型,值
                    new_line = f"{new_type},{val}"
                    
                    if "no-resolve" in line.lower():
                        new_line += ",no-resolve"
                    qx_rules.append(new_line)
                else:
                    qx_rules.append(line)

            # 3. 保存文件
            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(qx_rules))
            print(f"✅ 已保存至 {output_path}")

        except Exception as e:
            print(f"❌ 转换 {url} 失败: {e}")

if __name__ == "__main__":
    convert_all()
