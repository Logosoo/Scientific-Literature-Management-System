import hashlib
import json
import os
import time

# 标题哈希
def hash_string(title: str) -> int:
    if title is None:
        title = '' 
    return int(hashlib.md5(title.encode()).hexdigest(), 16) % 1024

# 标题搜索
def search_by_article(title: str):
    start_time = time.time()
    hash_value = hash_string(title)
    file_path = f"/root/autodl-tmp/data/data2.0/{hash_value}.jsonl"

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data["title"] == title:
                    end_time = time.time()
                    return [{
                        "title": data["title"],
                        "authors": data["authors"],
                        "year": data["year"],
                        "pages": data["pages"],
                        "urls": data["urls"],
                        "booktitle": data["booktitle"],
                        "ee": data.get("ee", ""),
                        "search_time": round(end_time - start_time, 6)
                    }]
    end_time = time.time()
    return [{   #没有就返回空
        "title": title,
        "authors": '无',
        "year": '无',
        "pages": '无',
        "urls": '无',
        "booktitle": '无',
        "ee": '无',
        "search_time": round(end_time - start_time, 6)
        }]

    
# 作者名搜索
def search_by_author(author: str):
    start_time = time.time()
    hash_value = hash_string(author)
    file_path = f"/root/autodl-tmp/data/data_au/{hash_value}.jsonl"

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data["author"] == author:
                    end_time = time.time()
                    return [{
                        "author": data["author"],
                        "titles": [t for t in data["titles"] if t],
                        "cos": [co for co in data["cos"] if co],
                        "search_time": round(end_time - start_time, 6)
                    }]
    end_time = time.time()
    return [{   #没有就返回空
        "author": author,
        "titles": '无',
        "cos": '无',
        "search_time": round(end_time - start_time, 6)
    }]
