import os
import hashlib
import json
import xml.etree.ElementTree as ET
from lxml import etree

def hash_string(title: str) -> int:
    if title is None:
        title = ''  # 如果值为 None，使用空字符串
    return int(hashlib.md5(title.encode()).hexdigest(), 16) % 1024

def save_to_jsonl(data, filename):
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")  

# 提取作者数据
def update_author(authors, title):
    for author in authors:
        author_hash = hash_string(author)
        author_file_path = f"/root/SJJG/Code/pythonCode/data_au/{author_hash}.jsonl"

        if os.path.exists(author_file_path): # 如果文件存在
            with open(author_file_path, 'r+', encoding='utf-8') as f:
                existing_data = []
                for line in f:
                    existing_data.append(json.loads(line))

                author_data = next((entry for entry in existing_data if entry['author'] == author), None)
                if author_data: # 作者已经在文件中的情况
                    if title not in author_data['titles']:
                        author_data['titles'].append(title)

                    for coauthor in authors:
                        if coauthor != author and coauthor not in author_data['cos']:
                            author_data['cos'].append(coauthor)
                else: # 作者原先不在文件中
                    new_data = {
                        "author": author,
                        "titles": [title],
                        "cos": [coauthor for coauthor in authors if coauthor != author]
                    }
                    existing_data.append(new_data)
                    
                f.seek(0)  
                f.truncate()  
                for entry in existing_data:
                    json.dump(entry, f, ensure_ascii=False)
                    f.write("\n")

        else: # 文件不存在，直接存
            print('New author ',author)
            new_data = {
                "author": author,
                "titles": [title],
                "cos": [coauthor for coauthor in authors if coauthor != author]
            }
            save_to_jsonl(new_data, author_file_path)

# 提取文章信息
def parse_xml(filename):
    tree = etree.parse(filename, parser=etree.XMLParser(resolve_entities=False))
    root = tree.getroot()
    cnt = 0  

    with open(filename, 'rb') as file:
        for event, element in etree.iterparse(file, events=("start", "end")):
            if event == "start" and element.tag in ['www', 'inproceedings', 'incollection']:    # 文章可能有很多个标签

                title = element.find('title').text if element.find('title') is not None else ''
                if title=='Home Page' or title == '' or title == 'None':    # 根据分析，有非常多文章题目叫Home Page，所以都略去
                    continue
                authors = [author.text for author in element.findall('author')] if element.findall('author') else []
                editors = [editor.text for editor in element.findall('editor')] if element.findall('editor') else []
                authors_all = authors + editors  # 作者标签可能为authors或editors
                year = element.find('year').text if element.find('year') is not None else ''
                pages = element.find('pages').text if element.find('pages') is not None else ''
                urls = [url.text for url in element.findall('url')] if element.findall('url') else []
                ee = element.find('ee').text if element.find('ee') is not None else ''
                booktitle = element.find('booktitle').text if element.find('booktitle') is not None else ''

                data = {
                    "title": title,
                    "authors": authors_all,
                    "year": year,
                    "pages": pages,
                    "urls": urls,
                    "booktitle": booktitle,
                    "ee": ee
                }
                hash_value = hash_string(title)
                file_path = f"/root/SJJG/Code/pythonCode/data2.0/{hash_value}.jsonl"
                save_to_jsonl(data, file_path)
                update_author(authors_all, title)

            element.clear()

if __name__ == "__main__":
    parse_xml('/root/SJJG/Code/dblp.xml') 
