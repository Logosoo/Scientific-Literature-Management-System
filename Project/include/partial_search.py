import os
import json
import time
import re

class TrieNode:
    def __init__(self):
        self.children = {}
        self.titles = []  # 存储包含该子串的文章标题

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, title: str):
        current_node = self.root
        for char in title:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
            current_node.titles.append(title)

    def title_search(self, keywords):
        all_titles = set()

        def node_search(node, current_word, titles_found): # 深度优先搜索遍历
            if len(current_word) >= len(keywords[0]) and current_word.endswith(keywords[0]):
                for title in node.titles:
                    if re.search(r'\b' + re.escape(keywords[0]) + r'\b', title):
                        titles_found.add(title)

            for child_char, child_node in node.children.items():
                node_search(child_node, current_word + child_char, titles_found)

        node_search(self.root, "", all_titles)
        for keyword in keywords[1:]:
            all_titles = {title for title in all_titles if re.search(r'\b' + re.escape(keyword) + r'\b', title)}
        return list(all_titles)

def partial_build_trie(data_folder):
    trie = Trie()
    for file_num in range(1024): 
        file_path = f"{data_folder}/{file_num}.jsonl"
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                title = json.loads(line).get('title')
                if title:
                    trie.insert(title)  # 插入字典树
    return trie

def partial_search(trie, keywords):
    ans = trie.title_search(keywords)
    return [{'title': title} for title in ans]


