# import json
# import logging as log
# import os
# import sys
# import dateparser
# from time import time as ts
#
# import yaml
#
# from szz.ag_szz import AGSZZ
# from szz.b_szz import BaseSZZ
# from szz.l_szz import LSZZ
# from szz.ma_szz import MASZZ, DetectLineMoved
# from szz.r_szz import RSZZ
# from szz.ra_szz import RASZZ
# from szz.tc_szz import TCSZZ
#
# log.basicConfig(
#     level=log.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
# log.getLogger('pydriller').setLevel(log.WARNING)
#
#
# def main(input_json: str, out_json: str, conf: dict(), repos_dir: str):
#     with open(input_json, 'r') as in_file:
#         bugfix_commits = json.loads(in_file.read())
#
#     tot = len(bugfix_commits)
#     for i, commit in enumerate(bugfix_commits):
#         bug_introducing_commits = set()
#         repo_name = commit['repo_name']
#         # using test:test as git login to skip private repos during clone
#         repo_url = f'https://test:test@github.com/{repo_name}.git'
#         fix_commit = commit['fix_commit_hash']
#
#         log.info(f'{i + 1} of {tot}: {repo_name} {fix_commit}')
#
#         commit_issue_date = None
#         if conf.get('issue_date_filter', None):
#             commit_issue_date = (commit.get('earliest_issue_date', None) or commit.get(
#                 'best_scenario_issue_date', None))
#             commit_issue_date = dateparser.parse(commit_issue_date).timestamp()
#
#         szz_name = conf['szz_name']
#         if szz_name == 'b':
#             b_szz = BaseSZZ(repo_full_name=repo_name,
#                             repo_url=repo_url, repos_dir=repos_dir)
#             imp_files = b_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = b_szz.find_bic(fix_commit_hash=fix_commit,
#                                                      impacted_files=imp_files,
#                                                      ignore_revs_file_path=conf.get(
#                                                          'ignore_revs_file_path'),
#                                                      issue_date_filter=conf.get(
#                                                          'issue_date_filter'),
#                                                      issue_date=commit_issue_date)
#
#         elif szz_name == 'ag':
#             ag_szz = AGSZZ(repo_full_name=repo_name,
#                            repo_url=repo_url, repos_dir=repos_dir)
#             imp_files = ag_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = ag_szz.find_bic(fix_commit_hash=fix_commit,
#                                                       impacted_files=imp_files,
#                                                       ignore_revs_file_path=conf.get(
#                                                           'ignore_revs_file_path'),
#                                                       max_change_size=conf.get(
#                                                           'max_change_size'),
#                                                       issue_date_filter=conf.get(
#                                                           'issue_date_filter'),
#                                                       issue_date=commit_issue_date)
#
#         elif szz_name == 'ma':
#             ma_szz = MASZZ(repo_full_name=repo_name,
#                            repo_url=repo_url, repos_dir=repos_dir)
#             imp_files = ma_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = ma_szz.find_bic(fix_commit_hash=fix_commit,
#                                                       impacted_files=imp_files,
#                                                       ignore_revs_file_path=conf.get(
#                                                           'ignore_revs_file_path'),
#                                                       max_change_size=conf.get(
#                                                           'max_change_size'),
#                                                       detect_move_from_other_files=DetectLineMoved(
#                                                           conf.get('detect_move_from_other_files')),
#                                                       issue_date_filter=conf.get(
#                                                           'issue_date_filter'),
#                                                       issue_date=commit_issue_date)
#
#         elif szz_name == 'r':
#             r_szz = RSZZ(repo_full_name=repo_name,
#                          repo_url=repo_url, repos_dir=repos_dir)
#             imp_files = r_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = r_szz.find_bic(fix_commit_hash=fix_commit,
#                                                      impacted_files=imp_files,
#                                                      ignore_revs_file_path=conf.get(
#                                                          'ignore_revs_file_path'),
#                                                      max_change_size=conf.get(
#                                                          'max_change_size'),
#                                                      detect_move_from_other_files=DetectLineMoved(
#                                                          conf.get('detect_move_from_other_files')),
#                                                      issue_date_filter=conf.get(
#                                                          'issue_date_filter'),
#                                                      issue_date=commit_issue_date)
#
#         elif szz_name == 'tc':
#             tc_szz = TCSZZ(repo_full_name=repo_name,
#                            repo_url=repo_url,
#                            repos_dir=repos_dir,
#                            blame_times_target=conf.get('blame_times_target', -1),
#                            mode=conf.get('mode', 1))
#             imp_files = tc_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = tc_szz.find_bic(fix_commit_hash=fix_commit,
#                                                       impacted_files=imp_files,
#                                                       ignore_revs_file_path=conf.get(
#                                                           'ignore_revs_file_path'),
#                                                       max_change_size=conf.get(
#                                                           'max_change_size'),
#                                                       issue_date_filter=conf.get(
#                                                           'issue_date_filter'),
#                                                       issue_date=commit_issue_date)
#
#         elif szz_name == 'l':
#             l_szz = LSZZ(repo_full_name=repo_name,
#                          repo_url=repo_url, repos_dir=repos_dir)
#             imp_files = l_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = l_szz.find_bic(fix_commit_hash=fix_commit,
#                                                      impacted_files=imp_files,
#                                                      ignore_revs_file_path=conf.get(
#                                                          'ignore_revs_file_path'),
#                                                      max_change_size=conf.get(
#                                                          'max_change_size'),
#                                                      detect_move_from_other_files=DetectLineMoved(
#                                                          conf.get('detect_move_from_other_files')),
#                                                      issue_date_filter=conf.get(
#                                                          'issue_date_filter'),
#                                                      issue_date=commit_issue_date)
#
#         elif szz_name == 'ra':
#             ra_szz = RASZZ(repo_full_name=repo_name,
#                            repo_url=repo_url, repos_dir=repos_dir)
#             imp_files = ra_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get(
#                 'file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
#             bug_introducing_commits = ra_szz.find_bic(fix_commit_hash=fix_commit,
#                                                       impacted_files=imp_files,
#                                                       ignore_revs_file_path=conf.get(
#                                                           'ignore_revs_file_path'),
#                                                       max_change_size=conf.get(
#                                                           'max_change_size'),
#                                                       detect_move_from_other_files=DetectLineMoved(
#                                                           conf.get('detect_move_from_other_files')),
#                                                       issue_date_filter=conf.get(
#                                                           'issue_date_filter'),
#                                                       issue_date=commit_issue_date)
#         else:
#             log.info(f'SZZ implementation not found: {szz_name}')
#             exit(-3)
#
#         log.info(f"result: {bug_introducing_commits}")
#         inducing_commit_hashes = []
#         for bic in bug_introducing_commits:
#             if bic:  # 直接判断Commit对象是否存在
#                 inducing_commit_hashes.append(bic.hexsha)  # 直接获取Commit对象的哈希值
#         bugfix_commits[i]["inducing_commit_hash"] = inducing_commit_hashes  # 存储哈希列表
#
#     with open(out_json, 'w') as out:
#         json.dump(bugfix_commits, out)
#
#     log.info("+++ DONE +++")
#
#
# if __name__ == "__main__":
#     if (len(sys.argv) > 0 and '--help' in sys.argv[1]) or len(sys.argv) < 3:
#         print('USAGE: python main.py <bugfix_commits.json> <conf_file path> <repos_directory(optional)>')
#         print('If repos_directory is not set, pyszz will download each repository')
#         exit(-1)
#     input_json = sys.argv[1]
#     conf_file = sys.argv[2]
#     repos_dir = sys.argv[3] if len(sys.argv) > 3 else None
#
#     if not os.path.isfile(input_json):
#         log.error('invalid input json')
#         exit(-2)
#     if not os.path.isfile(conf_file):
#         log.error('invalid conf file')
#         exit(-2)
#
#     with open(conf_file, 'r') as f:
#         conf = yaml.safe_load(f)
#
#     log.info(f"parsed conf yml: {conf}")
#     szz_name = conf['szz_name']
#
#     out_dir = 'out'
#     if not os.path.isdir(out_dir):
#         os.makedirs(out_dir)
#     out_json = os.path.join(out_dir, f'bic_{szz_name}_{int(ts())}.json')
#
#     if not szz_name:
#         log.error(
#             'The configuration file does not define the SZZ name. Please, fix.')
#         exit(-3)
#
#     log.info(f'Launching {szz_name}-szz')
#
#     main(input_json, out_json, conf, repos_dir)
# import json
# import logging as log
# import os
# import sys
# import dateparser
# from time import time as ts
# import threading  # 引入线程模块
#
# import yaml
# from concurrent.futures import ThreadPoolExecutor  # 多线程池
#
# from szz.ag_szz import AGSZZ
# from szz.b_szz import BaseSZZ
# from szz.l_szz import LSZZ
# from szz.ma_szz import MASZZ, DetectLineMoved
# from szz.r_szz import RSZZ
# from szz.ra_szz import RASZZ
# from szz.tc_szz import TCSZZ
# from szz.v_szz import VSZZ
#
# log.basicConfig(
#     level=log.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
# log.getLogger('pydriller').setLevel(log.WARNING)
#
# # 全局线程锁：确保同一仓库在同一时间仅被一个线程操作（解决Git锁冲突）
# repo_locks = dict()  # 格式: {repo_name: threading.Lock()}
#
#
# def process_single_commit(commit, conf, repos_dir):
#     """单独处理一个提交的函数（供线程调用）"""
#     bug_introducing_commits = set()
#     repo_name = commit['repo_name']
#     repo_url = f'https://test:test@github.com/{repo_name}.git'
#     fix_commit = commit['fix_commit_hash']
#
#     # 获取当前仓库的专属锁（不存在则创建）
#     if repo_name not in repo_locks:
#         repo_locks[repo_name] = threading.Lock()
#     repo_lock = repo_locks[repo_name]
#
#     # 关键：同一仓库同一时间只允许一个线程操作（避免Git锁冲突）
#     with repo_lock:
#         log.info(f'Processing {repo_name} {fix_commit}')
#
#         commit_issue_date = None
#         if conf.get('issue_date_filter'):
#             commit_issue_date = (commit.get('earliest_issue_date') or commit.get('best_scenario_issue_date'))
#             commit_issue_date = dateparser.parse(commit_issue_date).timestamp()
#
#         szz_name = conf['szz_name']
#         try:
#             # 根据不同的SZZ类型处理
#             if szz_name == 'b':
#                 b_szz = BaseSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
#                 imp_files = b_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = b_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#
#             elif szz_name == 'ag':
#                 ag_szz = AGSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
#                 imp_files = ag_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = ag_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     max_change_size=conf.get('max_change_size'),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#
#             elif szz_name == 'ma':
#                 ma_szz = MASZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
#                 imp_files = ma_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = ma_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     max_change_size=conf.get('max_change_size'),
#                     detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#
#             elif szz_name == 'r':
#                 r_szz = RSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
#                 imp_files = r_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = r_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     max_change_size=conf.get('max_change_size'),
#                     detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#
#             elif szz_name == 'tc':
#                 tc_szz = TCSZZ(
#                     repo_full_name=repo_name,
#                     repo_url=repo_url,
#                     repos_dir=repos_dir,
#                     blame_times_target=conf.get('blame_times_target', -1),
#                     mode=conf.get('mode', 1)
#                 )
#                 imp_files = tc_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = tc_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     max_change_size=conf.get('max_change_size'),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#
#             elif szz_name == 'l':
#                 l_szz = LSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
#                 imp_files = l_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = l_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     max_change_size=conf.get('max_change_size'),
#                     detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#
#             elif szz_name == 'ra':
#                 ra_szz = RASZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
#                 imp_files = ra_szz.get_impacted_files(
#                     fix_commit_hash=fix_commit,
#                     file_ext_to_parse=conf.get('file_ext_to_parse'),
#                     only_deleted_lines=conf.get('only_deleted_lines', True)
#                 )
#                 bug_introducing_commits = ra_szz.find_bic(
#                     fix_commit_hash=fix_commit,
#                     impacted_files=imp_files,
#                     ignore_revs_file_path=conf.get('ignore_revs_file_path'),
#                     max_change_size=conf.get('max_change_size'),
#                     detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
#                     issue_date_filter=conf.get('issue_date_filter'),
#                     issue_date=commit_issue_date
#                 )
#             # elif szz_name == "v":
#             #     v_szz = VSZZ(repo_full_name=project, repo_url=repo_url, repos_dir=REPOS_DIR,
#             #                    use_temp_dir=use_temp_dir, ast_map_path=AST_MAP_PATH)
#             #     for commit in commits:
#             #         print('Fixing Commit:', commit)
#             #         imp_files = v_szz.get_impacted_files(fix_commit_hash=commit,
#             #                                               file_ext_to_parse=['c', 'java', 'cpp', 'h', 'hpp'],
#             #                                               only_deleted_lines=True)
#             #         bug_introducing_commits = v_szz.find_bic(fix_commit_hash=commit,
#             #                                                   impacted_files=imp_files,
#             #                                                   ignore_revs_file_path=None)
#             #         output[commit] = bug_introducing_commits
#             # else:
#             #     log.error(f'SZZ implementation not found: {szz_name}')
#             #     return None
#
#         except Exception as e:
#             log.error(f'Error processing {repo_name} {fix_commit}: {str(e)}')
#             return None
#
#         # 提取提交哈希
#         inducing_commit_hashes = []
#         for bic in bug_introducing_commits:
#             if bic:
#                 inducing_commit_hashes.append(bic.hexsha)
#         return {
#             'repo_name': repo_name,
#             'fix_commit_hash': fix_commit,
#             'inducing_commit_hash': inducing_commit_hashes
#         }
#
#
# def main(input_json: str, out_json: str, conf: dict, repos_dir: str):
#     with open(input_json, 'r') as in_file:
#         bugfix_commits = json.loads(in_file.read())
#
#     tot = len(bugfix_commits)
#     log.info(f'发现 {tot} 个修复提交，启动多线程处理...')
#
#     max_workers = min(16, tot)
#     results = []
#
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         futures = [
#             executor.submit(process_single_commit, commit, conf, repos_dir)
#             for commit in bugfix_commits
#         ]
#
#         for i, future in enumerate(futures):
#             try:
#                 result = future.result()
#                 if result:
#                     bugfix_commits[i]['inducing_commit_hash'] = result['inducing_commit_hash']
#             except Exception as e:
#                 log.error(f'第 {i+1} 个任务失败: {str(e)}')
#
#     # 保存结果（添加indent=2参数）
#     with open(out_json, 'w') as out:
#         json.dump(bugfix_commits, out, indent=2)
#
#     log.info("+++ 处理完成 +++")
#
#
# if __name__ == "__main__":
#     if (len(sys.argv) > 1 and '--help' in sys.argv[1]) or len(sys.argv) < 3:
#         print('用法: python main.py <bugfix_commits.json> <conf_file path> <repos_directory(可选)>')
#         print('如果未指定repos_directory，pyszz将自动下载仓库')
#         exit(-1)
#
#     input_json = sys.argv[1]
#     conf_file = sys.argv[2]
#     repos_dir = sys.argv[3] if len(sys.argv) > 3 else None
#
#     if not os.path.isfile(input_json):
#         log.error('无效的输入JSON文件')
#         exit(-2)
#     if not os.path.isfile(conf_file):
#         log.error('无效的配置文件')
#         exit(-2)
#
#     with open(conf_file, 'r') as f:
#         conf = yaml.safe_load(f)
#
#     log.info(f"解析配置: {conf}")
#     szz_name = conf['szz_name']
#
#     out_dir = 'out'
#     if not os.path.isdir(out_dir):
#         os.makedirs(out_dir)
#     out_json = os.path.join(out_dir, f'bic_{szz_name}_{int(ts())}.json')
#
#     if not szz_name:
#         log.error('配置文件未定义SZZ名称，请修复')
#         exit(-3)
#
#     log.info(f'启动 {szz_name}-szz 多线程处理')
#     main(input_json, out_json, conf, repos_dir)
import json
import logging as log
import os
import sys
import dateparser
from time import time as ts
import threading  # 引入线程模块

import yaml
from concurrent.futures import ThreadPoolExecutor  # 多线程池

from szz.ag_szz import AGSZZ
from szz.b_szz import BaseSZZ
from szz.l_szz import LSZZ
from szz.ma_szz import MASZZ, DetectLineMoved
from szz.r_szz import RSZZ
from szz.ra_szz import RASZZ
from szz.tc_szz import TCSZZ
from szz.v_szz import VSZZ

log.basicConfig(
    level=log.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
log.getLogger('pydriller').setLevel(log.WARNING)

# 全局线程锁：确保同一仓库在同一时间仅被一个线程操作（解决Git锁冲突）
repo_locks = dict()  # 格式: {repo_name: threading.Lock()}
repo_locks_lock = threading.Lock()  # 保护repo_locks的创建


def process_single_commit(commit, conf, repos_dir):
    """单独处理一个提交的函数（供线程调用）"""
    bug_introducing_commits = set()
    repo_name = commit['repo_name']
    repo_url = f'https://test:test@github.com/{repo_name}.git'
    fix_commit = commit['fix_commit_hash']

    # 获取当前仓库的专属锁（线程安全）
    with repo_locks_lock:
        if repo_name not in repo_locks:
            repo_locks[repo_name] = threading.Lock()
    repo_lock = repo_locks[repo_name]

    # 关键：同一仓库同一时间只允许一个线程操作（避免Git锁冲突）
    with repo_lock:
        log.info(f'Processing {repo_name} {fix_commit}')

        commit_issue_date = None
        if conf.get('issue_date_filter'):
            commit_issue_date = (commit.get('earliest_issue_date') or commit.get('best_scenario_issue_date'))
            commit_issue_date = dateparser.parse(commit_issue_date).timestamp()

        szz_name = conf['szz_name']
        try:
            # 根据不同的SZZ类型处理
            if szz_name == 'b':
                b_szz = BaseSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
                imp_files = b_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = b_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )

            elif szz_name == 'ag':
                ag_szz = AGSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
                imp_files = ag_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = ag_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    max_change_size=conf.get('max_change_size'),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )

            elif szz_name == 'ma':
                ma_szz = MASZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
                imp_files = ma_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = ma_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    max_change_size=conf.get('max_change_size'),
                    detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )

            elif szz_name == 'r':
                r_szz = RSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
                imp_files = r_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = r_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    max_change_size=conf.get('max_change_size'),
                    detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )

            elif szz_name == 'tc':
                tc_szz = TCSZZ(
                    repo_full_name=repo_name,
                    repo_url=repo_url,
                    repos_dir=repos_dir,
                    blame_times_target=conf.get('blame_times_target', -1),
                    mode=conf.get('mode', 1)
                )
                imp_files = tc_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = tc_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    max_change_size=conf.get('max_change_size'),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )

            elif szz_name == 'l':
                l_szz = LSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
                imp_files = l_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = l_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    max_change_size=conf.get('max_change_size'),
                    detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )

            elif szz_name == 'ra':
                ra_szz = RASZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
                imp_files = ra_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse'),
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = ra_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                    max_change_size=conf.get('max_change_size'),
                    detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')),
                    issue_date_filter=conf.get('issue_date_filter'),
                    issue_date=commit_issue_date
                )



            elif szz_name == "v":
                # 修复VSZZ分支的变量引用错误，移除AST相关参数
                v_szz = VSZZ(
                    repo_full_name=repo_name,  # 使用当前处理的仓库名
                    repo_url=repo_url,
                    repos_dir=repos_dir  # 仅传递3个必要参数，移除use_temp_dir和ast_map_path
                )
                # 获取受影响文件（仅处理C/C++）
                imp_files = v_szz.get_impacted_files(
                    fix_commit_hash=fix_commit,
                    file_ext_to_parse=conf.get('file_ext_to_parse', ['c', 'cpp']),  # 明确指定C/C++文件
                    only_deleted_lines=conf.get('only_deleted_lines', True)
                )
                bug_introducing_commits = v_szz.find_bic(
                    fix_commit_hash=fix_commit,
                    impacted_files=imp_files,
                    ignore_revs_file_path=conf.get('ignore_revs_file_path')
                )

            else:
                log.error(f'SZZ implementation not found: {szz_name}')
                return {
                    'repo_name': repo_name,
                    'fix_commit_hash': fix_commit,
                    'inducing_commit_hash': []  # 返回空列表而非None
                }

        except Exception as e:
            log.error(f'Error processing {repo_name} {fix_commit}: {str(e)}')
            # 确保无论如何都返回包含空结果的字典
            return {
                'repo_name': repo_name,
                'fix_commit_hash': fix_commit,
                'inducing_commit_hash': []
            }

        # 提取提交哈希
        inducing_commit_hashes = []
        for bic in bug_introducing_commits:
            if bic:
                inducing_commit_hashes.append(bic.hexsha)
        return {
            'repo_name': repo_name,
            'fix_commit_hash': fix_commit,
            'inducing_commit_hash': inducing_commit_hashes
        }


def main(input_json: str, out_json: str, conf: dict, repos_dir: str):
    # 配置检查
    if szz_name == "v" and conf.get('use_ast', False) and 'ast_map_path' not in conf:
        log.error('VSZZ requires "ast_map_path" in config')
        exit(-3)

    with open(input_json, 'r') as in_file:
        bugfix_commits = json.loads(in_file.read())

    tot = len(bugfix_commits)
    log.info(f'发现 {tot} 个修复提交，启动多线程处理...')

    # 优化线程数配置
    max_workers = conf.get('max_workers', min(os.cpu_count() * 2, tot))
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_commit, commit, conf, repos_dir)
            for commit in bugfix_commits
        ]

        # 确保所有提交都有结果（即使处理失败）
        for i, future in enumerate(futures):
            try:
                result = future.result()
                # 直接更新原始数据中的对应提交
                bugfix_commits[i]['inducing_commit_hash'] = result['inducing_commit_hash']
            except Exception as e:
                log.error(f'第 {i+1} 个任务失败: {str(e)}')
                # 确保失败的提交也有结果字段
                bugfix_commits[i]['inducing_commit_hash'] = []

    # 保存结果（添加indent=2参数使输出更易读）
    with open(out_json, 'w') as out:
        json.dump(bugfix_commits, out, indent=2)

    log.info("+++ 处理完成 +++")


if __name__ == "__main__":
    if (len(sys.argv) > 1 and '--help' in sys.argv[1]) or len(sys.argv) < 3:
        print('用法: python main.py <bugfix_commits.json> <conf_file path> <repos_directory(可选)>')
        print('如果未指定repos_directory，pyszz将自动下载仓库')
        exit(-1)

    input_json = sys.argv[1]
    conf_file = sys.argv[2]
    repos_dir = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.isfile(input_json):
        log.error('无效的输入JSON文件')
        exit(-2)
    if not os.path.isfile(conf_file):
        log.error('无效的配置文件')
        exit(-2)

    with open(conf_file, 'r', encoding='gbk') as f:
        conf = yaml.safe_load(f)

    log.info(f"解析配置: {conf}")
    szz_name = conf['szz_name']

    out_dir = 'out'
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_json = os.path.join(out_dir, f'bic_{szz_name}_{int(ts())}.json')

    if not szz_name:
        log.error('配置文件未定义SZZ名称，请修复')
        exit(-3)

    log.info(f'启动 {szz_name}-szz 多线程处理')
    main(input_json, out_json, conf, repos_dir)