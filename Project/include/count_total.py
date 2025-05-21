import os
import json

def count_lines_in_jsonl(folder_path):
    total = 0
    for file_num in range(1024):
        file_path = os.path.join(folder_path, f"{file_num}.jsonl")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = sum(1 for _ in f)
            total += lines
    return total

def count_authors_and_articles(data_authors, data_articles):
    print("Counting total number of articles and authors...\n")
    article_count = count_lines_in_jsonl(data_articles)
    author_count = count_lines_in_jsonl(data_authors)
    print(f"Total number of articles: {article_count}")
    print(f"Total number of authors : {author_count}")

