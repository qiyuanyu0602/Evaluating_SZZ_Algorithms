# %%
import json
import os

# %%
dataset_a_baseline_results = []
with open('./dataset_a_baseline_results.json') as f:
    dataset_a_baseline_results = json.load(f)

# %%
print(len(dataset_a_baseline_results))

# %%
r_find_cids_map = {}
true_cnt = 0
b_find_cnt = 0
b_find_true_cnt = 0

ag_find_cnt = 0
ag_find_true_cnt = 0

ma_find_cnt = 0
ma_find_true_cnt = 0

r_find_cnt = 0
r_find_true_cnt = 0

l_find_cnt = 0
l_find_true_cnt = 0
for a_baseline_result in dataset_a_baseline_results:
    bug_commit_cids = a_baseline_result['info']['bug_commit_hash']
    true_cnt = true_cnt + len(bug_commit_cids)
    
    b_induce_cids = a_baseline_result['b_induce_cids']
    a_induce_cids = a_baseline_result['a_induce_cids']
    ma_induce_cids = a_baseline_result['ma_induce_cids']
    r_induce_cids = a_baseline_result['r_induce_cids']
    r_find_cids_map[bug_commit_cids[0]] = r_induce_cids
    if 'l_induce_cids' in a_baseline_result:
        l_induce_cids = a_baseline_result['l_induce_cids']
    else:
        l_induce_cids = []
    
    b_find_cnt = b_find_cnt + len(b_induce_cids)
    ag_find_cnt = ag_find_cnt + len(a_induce_cids)
    ma_find_cnt = ma_find_cnt + len(ma_induce_cids)
    r_find_cnt = r_find_cnt + 1
    l_find_cnt = l_find_cnt + 1
        
    for b_cid in b_induce_cids:
        if b_cid in bug_commit_cids:
            b_find_true_cnt = b_find_true_cnt + 1
                
                
    for a_cid in a_induce_cids:
        if a_cid in bug_commit_cids:
            ag_find_true_cnt = ag_find_true_cnt + 1
            
    for ma_cid in ma_induce_cids:
        if ma_cid in bug_commit_cids:
            ma_find_true_cnt = ma_find_true_cnt + 1
            
    for r_cid in r_induce_cids:
        if r_cid in bug_commit_cids:
            r_find_true_cnt = r_find_true_cnt + 1
    
    for l_cid in l_induce_cids:
        if l_cid in bug_commit_cids:
            l_find_true_cnt = l_find_true_cnt + 1

# %%
print(true_cnt)
print(b_find_cnt)
print(b_find_true_cnt)
print(ag_find_cnt)
print(ag_find_true_cnt)
print(ma_find_cnt)
print(ma_find_true_cnt)
print(r_find_cnt)
print(r_find_true_cnt)
print(l_find_cnt)
print(l_find_true_cnt)

# %%
dataset_d_results = []
with open('./dataset_d_results.json') as f:
    dataset_d_results = json.load(f)
print(len(dataset_d_results))

# %%
find_cnt= 0
find_true_cnt = 0
true_cnt = 0

for d_result in dataset_d_results:
    info = d_result['info']
    bug_commit_cids = info['bug_commit_hash']
    
    find_cids = d_result['find_cid']
    true_cnt = true_cnt + len(bug_commit_cids)
    find_cnt = find_cnt + len(find_cids)
    
    for cid1 in bug_commit_cids:
        for cid2 in find_cids:
            if cid1 == cid2:
                find_true_cnt = find_true_cnt + 1

print(find_cnt)
print(find_true_cnt)
print(true_cnt)

# %%
dataset_a_results = []
with open('./dataset_a_results.json') as f:
    dataset_a_results = json.load(f)
print(len(dataset_a_results))

# %%
find_cnt= 0
find_true_cnt = 0
true_cnt = 0

for a_result in dataset_a_results:
    info = a_result['info']
    bug_commit_cids = info['bug_commit_hash']
    
    find_cids = a_result['find_cid']
    if len(find_cids) == 0:
        find_cids = r_find_cids_map[bug_commit_cids[0]]
    true_cnt = true_cnt + len(bug_commit_cids)
    find_cnt = find_cnt + len(find_cids)
    
    for cid1 in bug_commit_cids:
        for cid2 in find_cids:
            if cid1 == cid2:
                find_true_cnt = find_true_cnt + 1

print(find_cnt)
print(find_true_cnt)
print(true_cnt)

# %%
dataset_fa_results = []
with open('./dataset_fa_results.json') as f:
    dataset_fa_results = json.load(f)
print(len(dataset_fa_results))

# %%
find_cnt= 0
find_true_cnt = 0
true_cnt = 0

for fa_result in dataset_fa_results:
    info = fa_result['info']
    bug_commit_cids = info['bug_commit_hash']
    
    find_cids = fa_result['find_cid']
    true_cnt = true_cnt + len(bug_commit_cids)
    find_cnt = find_cnt + len(find_cids)
    
    for cid1 in bug_commit_cids:
        for cid2 in find_cids:
            if cid1 == cid2:
                find_true_cnt = find_true_cnt + 1

print(find_cnt)
print(find_true_cnt)
print(true_cnt)


