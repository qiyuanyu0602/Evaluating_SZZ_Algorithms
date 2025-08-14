import re
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openpyxl import Workbook
from concurrent.futures import ThreadPoolExecutor


# 验证SHA-1哈希值（40位十六进制字符）
def is_valid_sha(sha_str):
    if not sha_str or len(sha_str) != 40:
        return False
    # 匹配十六进制字符（0-9, a-f, A-F）
    return bool(re.fullmatch(r'^[0-9a-fA-F]{40}$', sha_str))


def configure_session():
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
    obj = re.compile(r'=CVE-(?P<id>\d{4}-\d+)')
    return [match.group("id") for match in obj.finditer(html_content)]


def fetch_cve_details(session, cve_id):
    dataurl = f"https://cveawg.mitre.org/api/cve/CVE-{cve_id}"
    try:
        response = session.get(dataurl)
        response.raise_for_status()
        return cve_id, response.json()
    except requests.RequestException as e:
        print(f"获取 CVE {cve_id} 详情时出错: {e}")
        return cve_id, None
    except ValueError as e:
        print(f"解析 CVE {cve_id} JSON 时出错: {e}")
        return cve_id, None


def extract_cve_info(cve_json):
    if not cve_json:
        return "无", "无"

    introduced_hashes = []
    fixed_hashes = []

    try:
        # 定位版本信息核心区域
        containers = cve_json.get('containers', {})
        cna = containers.get('cna', {})
        affected_list = cna.get('affected', [])

        # 遍历所有受影响产品的版本信息
        for affected in affected_list:
            versions = affected.get('versions', [])
            for version_info in versions:
                # 只处理git类型的版本信息
                if version_info.get('versionType') != 'git':
                    continue  # 跳过非git版本类型（过滤版本号等噪声）

                version = version_info.get('version', '').strip()
                less_than = version_info.get('lessThan', '').strip()

                # 收集有效的VIC SHA（必须是40位十六进制且包含lessThan字段）
                if version and less_than and is_valid_sha(version):
                    introduced_hashes.append(version)

                # 收集有效的VFC SHA（必须是40位十六进制）
                if less_than and is_valid_sha(less_than):
                    fixed_hashes.append(less_than)

        # 确定最终VIC SHA（取最后一个有效引入提交）
        introduced_hash = introduced_hashes[-1] if introduced_hashes else "无"
        # 确定最终VFC SHA（取最后一个有效修复提交）
        fixed_hash = fixed_hashes[-1] if fixed_hashes else "无"

        return introduced_hash, fixed_hash

    except (KeyError, IndexError) as e:
        print(f"提取CVE信息时发生结构错误: {e}")
        return "无", "无"


def main():
    session = configure_session()
    html_content = fetch_cve_list(session)
    cve_ids = extract_cve_ids(html_content)

    wb = Workbook()
    ws = wb.active
    ws.append(['CVE ID', 'VIC SHA', 'VFC SHA'])

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_cve_details, session, cve_id) for cve_id in cve_ids]
        for future in futures:
            cve_id, cve_json = future.result()
            print(f"处理 CVE-{cve_id}")
            introduced_hash, fixed_hash = extract_cve_info(cve_json)

            if introduced_hash != "无" or fixed_hash != "无":
                ws.append([f'CVE-{cve_id}', introduced_hash, fixed_hash])

    wb.save('cve_info.xlsx')
    print("数据收集完成，已保存到 cve_info.xlsx")


if __name__ == "__main__":
    main()