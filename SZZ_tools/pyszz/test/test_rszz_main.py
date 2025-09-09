import json
import logging as log
import os
import sys
from time import time as ts

import yaml

from szz.ag_szz import AGSZZ
from szz.b_szz import BaseSZZ
from szz.l_szz import LSZZ
from szz.ma_szz import MASZZ, DetectLineMoved
from szz.r_szz import RSZZ
from szz.ra_szz import RASZZ

log.basicConfig(level=log.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')
log.getLogger('pydriller').setLevel(log.WARNING)

# whitespace, merge, rename, change_size
result = ["d1f64fd5115978cd2a6cae8934a4fea40b4a0137",
          "d65a34f3f806e44c288866c29dc8ab845cc2aa4a",
          "09243608abbd5544f7ccc88f4d455a99e9297d59",
          "1cf1407297f274aec8d20573e4f0cfeaa9251c64",
          "06113d50ce706e8dd85003770a2587c789b7d928"]


def main(input_json: str, out_json: str, conf: dict(), repos_dir: str):
    with open(input_json, 'r') as in_file:
        bugfix_commits = json.loads(in_file.read())

    tot = len(bugfix_commits)
    for commit, oracle in zip(bugfix_commits, result):
        repo_name = commit['repo_name']
        repo_url = f'https://test:test@github.com/{repo_name}.git'
        fix_commit = commit['fix_commit_hash']

        log.info(f'{repo_name} {fix_commit}')

        szz_name = conf['szz_name']
        if szz_name == 'r':
            l_szz = RSZZ(repo_full_name=repo_name, repo_url=repo_url, repos_dir=repos_dir)
            imp_files = l_szz.get_impacted_files(fix_commit_hash=fix_commit, file_ext_to_parse=conf.get('file_ext_to_parse'), only_deleted_lines=conf.get('only_deleted_lines', True))
            bic_list = l_szz.find_bic(fix_commit_hash=fix_commit,
                                      impacted_files=imp_files,
                                      ignore_revs_file_path=conf.get('ignore_revs_file_path'),
                                      max_change_size=conf.get('max_change_size'),
                                      detect_move_from_other_files=DetectLineMoved(conf.get('detect_move_from_other_files')))
            log.info(bic_list)
        else:
            log.info(f'SZZ implementation not found: {szz_name}')
            exit(-3)

        assert [bic.hexsha for bic in bic_list][0] == oracle

    log.info("+++ DONE +++")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('USAGE: python main.py <bugfix_commits.json> <conf_file path> <repos_directory>')
        exit(-1)
    input_json = sys.argv[1]
    conf_file = sys.argv[2]
    repos_dir = sys.argv[3]

    if not os.path.isfile(input_json):
        log.error('invalid input json')
        exit(-2)
    if not os.path.isfile(conf_file):
        log.error('invalid conf file')
        exit(-2)

    with open(conf_file, 'r') as f:
        conf = yaml.safe_load(f)

    log.info(f"parsed conf yml: {conf}")
    szz_name = conf['szz_name']

    out_dir = 'out'
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_json = os.path.join(out_dir, f'bic_{szz_name}_{int(ts())}.json')

    if not szz_name:
        log.error('The configuration file does not define the SZZ name. Please, fix.')
        exit(-3)
    
    log.info(f'Launching {szz_name}-szz')

    main(input_json, out_json, conf, repos_dir)
