import json
import os
import nltk
from collections import defaultdict
import heapq
import time
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
custom_stop_words = {
    'learning.','data.','via','new','using', 'based', 'learning', 'data', 'analysis', 'system', 'model', 'design', 'detection', 'research','networks.','systems.','approach','control','-','information','neural','performance','method','study','towards'
}
stop_words.update(custom_stop_words)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.weight = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.weight += 1  # 每次插入时，增加节点计数，作为单词出现频率

    def get_top_keywords(self, top_n=10):
        result = []
        def dfs(node, current_word):
            if node.weight > 0:
                result.append((current_word, node.weight))
            for char, child_node in node.children.items():
                dfs(child_node, current_word + char)
        dfs(self.root, '')
        return heapq.nlargest(top_n, result, key=lambda x: x[1]) # 同样使用堆排序

def hotspot_build_trie(data_folder):
    trie = Trie()
    for file_num in range(1024):
        file_path = f"{data_folder}/{file_num}.jsonl"
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                title = data.get("title")
 
                if title and isinstance(title, str):
                    words = title.split()
                    for word in words:
                        word = word.lower()
                        if word not in stop_words:  
                            trie.insert(word)
    return trie

def output_top_keywords(trie, top_n=10):
    start_time = time.time()  
    top_keywords = trie.get_top_keywords(top_n)
    end_time = time.time()
    s_time = round(end_time - start_time, 6)
    result = []
    for idx, (keyword, _) in enumerate(top_keywords, 1):
        result.append({
            "num": idx,
            "val": keyword,
        })

    return result, s_time
