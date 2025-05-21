import os
import json
import time

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):  # 查找
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  #路径压缩
        return self.parent[x]

    def union(self, x, y):  #合并
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x

def build_groups(data_folder):
    uf = UnionFind()
    for file_num in range(1024):
        file_path = f"{data_folder}/{file_num}.jsonl"
        if not os.path.exists(file_path):
            continue
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                author_data = json.loads(line)
                author = author_data.get("author")
                coauthors = author_data.get("cos", [])
                for coauthor in coauthors:
                    uf.union(author, coauthor)
    return uf

def group_members(uf):
    groups = {}
    for author in uf.parent:
        root = uf.find(author)
        if root not in groups:
            groups[root] = set()
        groups[root].add(author)
    return groups

def save_groups(groups, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (root, members) in enumerate(groups.items(), 1):
            json.dump({
                "group_num": i,
                "group_member": list(members),
                "member_count": len(members)
            }, f, ensure_ascii=False)
            f.write('\n')

def load_groups(file):
    groups = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            groups.append(json.loads(line))
    return groups

def query_group(file, group_index):
    start_time = time.time()
    groups = load_groups(file)
    group_total = len(groups)
    if group_index <= 0 or group_index > group_total:
        return [{'num': 0, 'val': '无效的聚团编号'}], 0, group_total

    group = groups[group_index - 1]
    results = [{'num': i + 1, 'val': author} for i, author in enumerate(group['group_member'])]

    end_time = time.time()
    search_time = round(end_time - start_time, 6)

    return results, search_time, group_total