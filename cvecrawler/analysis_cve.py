import pandas as pd
import json
from collections import defaultdict


def analyze_cve_data(excel_path):
    # 读取Excel文件，确保列名与你的实际文件一致
    # 假设Excel列名为："CVE ID", "VFC SHA", "VIC SHA"
    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        print(f"读取Excel文件失败：{e}")
        return

    # 过滤无效数据（空值）
    df = df.dropna(subset=["VFC SHA", "VIC SHA", "CVE ID"])
    total_records = len(df)
    print(f"有效数据记录数：{total_records}\n")

    # 1. 检查是否有VFC SHA作为VIC SHA出现
    vfc_list = df["VFC SHA"].unique()
    vic_list = df["VIC SHA"].unique()
    vfc_as_vic = [vfc for vfc in vfc_list if vfc in vic_list]
    has_vfc_as_vic = len(vfc_as_vic) > 0

    print("=== 分析结果1：VFC SHA作为VIC SHA出现情况 ===")
    print(f"是否存在VFC SHA作为VIC SHA出现：{has_vfc_as_vic}")
    if has_vfc_as_vic:
        print(f"具体重复的SHA值：{', '.join(vfc_as_vic)}\n")
    else:
        print("未发现VFC SHA作为VIC SHA出现的情况\n")

    # 2. 统计重复出现的VFC SHA
    vfc_counts = df["VFC SHA"].value_counts()
    repeated_vfc = vfc_counts[vfc_counts > 1].to_dict()  # 仅保留出现次数>1的VFC
    repeated_vfc_result = {
        "total_repeated_vfc": len(repeated_vfc),  # 重复出现的VFC数量
        "vfc_sha_counts": repeated_vfc  # 每个VFC的出现次数
    }

    # 保存重复VFC结果到JSON
    with open("repeated_vfc_analysis.json", "w", encoding="utf-8") as f:
        json.dump(repeated_vfc_result, f, ensure_ascii=False, indent=2)

    print("=== 分析结果2：重复VFC SHA统计 ===")
    print(f"重复出现的VFC SHA总数：{repeated_vfc_result['total_repeated_vfc']}")
    print("重复VFC详情已保存到 repeated_vfc_analysis.json\n")

    # 3. 分析一个VIC对应多个VFC的情况（去重处理）
    vic_mapping = defaultdict(lambda: {"VFC SHA": set(), "CVE ID": set()})

    for _, row in df.iterrows():
        vic_sha = row["VIC SHA"]
        vfc_sha = row["VFC SHA"]
        cve_id = row["CVE ID"]

        # 收集对应关系（自动去重）
        vic_mapping[vic_sha]["VFC SHA"].add(vfc_sha)
        vic_mapping[vic_sha]["CVE ID"].add(cve_id)

    # 转换集合为列表（JSON序列化需要）
    vic_mapping_result = {
        vic: {
            "VFC SHA": list(vfcs),
            "CVE ID": list(cves),
            "vfc_count": len(vfcs)  # 标记该VIC对应的VFC数量
        }
        for vic, (vfcs, cves) in [(k, (v["VFC SHA"], v["CVE ID"])) for k, v in vic_mapping.items()]
    }

    # 保存VIC映射结果到JSON
    with open("vic_to_vfc_analysis.json", "w", encoding="utf-8") as f:
        json.dump(vic_mapping_result, f, ensure_ascii=False, indent=2)

    print("=== 分析结果3：VIC对应多个VFC情况 ===")
    multi_vfc_vic_count = sum(1 for item in vic_mapping_result.values() if item["vfc_count"] >= 2)
    print(f"存在一个VIC对应多个VFC的情况总数：{multi_vfc_vic_count}")
    print("VIC与VFC映射详情已保存到 vic_to_vfc_analysis.json")


if __name__ == "__main__":
    # 替换为你的Excel文件路径
    excel_file_path = "C:\\Users\\84525\\Desktop\\testdata\\源文件\\cve_info.xlsx"  # 例如："cve_info.xlsx"
    analyze_cve_data(excel_file_path)