import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor
#logic：1 vic match 1 vfc,the earliset vfc is the Upstream commit

def configure_session():
    # 配置重试机制
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_cve_list(session):
    url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=linux+kernel"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
    }
    try:
        response = session.get(url, headers=header)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"获取 CVE 列表时出错: {e}")
        return None


def extract_cve_ids(html_content):
    if not html_content:
        return []
    # 调整正则表达式以适应可能的网页结构变化
    obj = re.compile(r'=CVE-(?P<id>\d{4}-\d+)')
    return [match.group("id") for match in obj.finditer(html_content)]


def fetch_cve_details(session, cve_id):
    dataurl = f"https://cveawg.mitre.org/api/cve/CVE-{cve_id}"
    try:
        response = session.get(dataurl)
        response.raise_for_status()
        return cve_id, response.text
    except requests.RequestException as e:
        print(f"获取 CVE {cve_id} 详情时出错: {e}")
        return cve_id, None


def extract_cve_info(cve_content):
    if not cve_content:
        return None, None

    # 提取引入哈希值（保持不变）
    objversion = re.compile(r'"version":"(?P<value>[a-fA-F0-9]{40})"')
    version_match = objversion.search(cve_content)
    introduced_hash = version_match.group("value") if version_match else "无"

    # 提取所有修复哈希值，并选择最早的提交（列表中的最后一个）
    objlessThan = re.compile(r'"lessThan":"(?P<lessThan>[a-fA-F0-9]{40})"')
    fixed_hashes = [match.group("lessThan") for match in objlessThan.finditer(cve_content)]

    # 选择最早的修复提交（最后一个元素）
    fixed_hash = fixed_hashes[-1] if fixed_hashes else "无"

    return introduced_hash, fixed_hash

def main():
    session = configure_session()
    html_content = fetch_cve_list(session)
    cve_ids = extract_cve_ids(html_content)

    # 创建一个新的工作簿和工作表
    wb = Workbook()
    ws = wb.active
    # 设置新表头：CVE ID、VIC SHA、VFC
    ws.append(['CVE ID', 'VIC SHA', 'VFC SHA'])

    # 使用线程池执行获取CVE详情的任务
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_cve_details, session, cve_id) for cve_id in cve_ids]
        for future in futures:
            cve_id, cve_content = future.result()
            print(f"处理 CVE-{cve_id}")
            introduced_hash, fixed_hash = extract_cve_info(cve_content)

            # 新增判断逻辑，若引入和修复哈希都是"无"则不记录
            if introduced_hash != "无" or fixed_hash != "无":
                # 将数据添加到工作表中
                ws.append([f'CVE-{cve_id}', introduced_hash, fixed_hash])

    # 保存工作簿
    wb.save('cve_info.xlsx')
    print("数据收集完成，已保存到 cve_info.xlsx")


if __name__ == "__main__":
    main()