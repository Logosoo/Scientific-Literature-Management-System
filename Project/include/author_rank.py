import json
import os
import heapq
from collections import defaultdict
import time

def count_articles(data_folder):
    article_count = defaultdict(int)
    for i in range(1024):
        file_path = os.path.join(data_folder, f"{i}.jsonl")
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                author = data.get("author")
                titles = data.get("titles", [])
                if author and len(titles) > 10 and len(author) > 4:  #文章数最少有10篇才计入，可以节省排序时间；有的作者名字很诡异，就一两个字母，故省略
                    article_count[author] += len(titles)
    return article_count

def get_top_authors(article_count, top_n=100):
    start_time = time.time()
    top_list = heapq.nlargest(top_n, article_count.items(), key=lambda x: x[1])
    result = [{"num": idx + 1, "val": author} for idx, (author, _) in enumerate(top_list)]
    end_time = time.time()
    s_time = round(end_time - start_time, 6)
    return result, s_time

