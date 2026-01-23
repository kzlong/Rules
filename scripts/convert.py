import requests
import re

# ================= 配置区 =================
# 1. Loon 规则的原始地址
SOURCE_URL = "https://raw.githubusercontent.com/Elysian-Realme/FuGfConfig/refs/heads/main/ConfigFile/Loon/Apple/api-domain.list"
# 2. 你想在 QX 中指定的默认策略组（如 Proxy, Direct 等）
# 如果你打算在 QX 引用时用 force-policy，这里可以留空
#POLICY_NAME = "Proxy" 
# ==========================================

def convert_loon_to_qx():
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        lines = response.text.splitlines()
    except Exception as e:
        print(f"下载失败: {e}")
        return

    qx_rules = []
    
    # 转换逻辑映射
    mapping = {
        "DOMAIN-SUFFIX": "HOST-SUFFIX",
        "DOMAIN": "HOST",
        "DOMAIN-KEYWORD": "HOST-KEYWORD",
        "IP-CIDR": "IP-CIDR",
        "IP-CIDR6": "IP-CIDR6",
        "USER-AGENT": "USER-AGENT"
    }

    for line in lines:
        line = line.strip()
        
        # 1. 保留注释和空行
        if not line or line.startswith("#") or line.startswith(";"):
            qx_rules.append(line)
            continue
        
        # 2. 移除 Loon 可能存在的策略部分（Loon 规则末尾有时带策略，QX 需要统一格式）
        # 比如把 "DOMAIN-SUFFIX,google.com,Proxy" 简化为关键部分
        parts = line.split(',')
        rule_type = parts[0].strip()
        
        if rule_type in mapping:
            new_type = mapping[rule_type]
            # 提取核心值（例如 google.com）
            core_value = parts[1].strip()
            
            # 3. 重新组装成 QX 格式: 类型,内容,策略
            # 注意：QX 也可以不带策略，但在分流规则里带上更稳妥
            new_line = f"{new_type},{core_value},{POLICY_NAME}"
            
            # 处理特殊的 no-resolve 标志（针对 IP-CIDR）
            if "no-resolve" in line.lower() and "IP-CIDR" in rule_type:
                new_line += ",no-resolve"
                
            qx_rules.append(new_line)
        else:
            # 无法识别的保持原样或跳过
            qx_rules.append(f"# Unrecognized: {line}")

    # 保存文件
    with open("qx_rule.list", "w", encoding="utf-8") as f:
        f.write("\n".join(qx_rules))
    print("转换完成！")

if __name__ == "__main__":
    convert_loon_to_qx()
