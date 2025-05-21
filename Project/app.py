from flask import Flask, render_template, request, jsonify
from inc import *

app = Flask(__name__)

data_folder_au = '/root/autodl-tmp/data/data_au'
data_folder_ar = '/root/autodl-tmp/data/data2.0'
group_output = '/root/autodl-tmp/data/author_groups.jsonl'

trie_keywords = None
trie_partial = None
top_authors = None
sort_time = None

def load_data():
    print("Loading all data and building structures...\n")
    print("[1/5] Building Trie for hotspot keyword analysis...")
    trie_keywords = hotspot_build_trie(data_folder_ar)
    print("[2/5] Building Trie for partial matching search...")
    trie_partial = partial_build_trie(data_folder_ar)
    print("[3/5] Counting articles per author...")
    article_count = count_articles(data_folder_au)
    top_authors, sort_time = get_top_authors(article_count)
    print("[4/5] Building author groups using union-find...")
    uf = build_groups(data_folder_au)
    groups = group_members(uf)
    save_groups(groups, group_output)
    print("[5/5] Counting total number of articles and authors...\n")
    count_authors_and_articles(data_folder_au, data_folder_ar)
    print("\n✅ All data loaded successfully!\n")
    
    return trie_keywords, trie_partial, top_authors , sort_time

@app.route('/')
def index():
    return render_template('index.html')

# 基本搜索功能
@app.route('/search', methods=['POST'])
def search():
    search_type = request.form['search-type']
    query = request.form['query']
    if search_type == 'author':
        results = search_by_author(query)
    else:
        results = search_by_article(query)
    return render_template('index.html', results=results,search_type=search_type)

# 部分匹配搜索功能
@app.route('/partial-match', methods=['POST'])
def partial_match():
    keywords = request.form['keywords'].split()
    results = partial_search(trie_partial, keywords)
    return render_template(
        'index.html',
        results=results,
        search_type='partial'
    )

# 作者统计功能
@app.route('/author-stats')
def author_stats():
    n = int(request.args.get('n', 10))
    top_n = top_authors[:n]
    result = []
    for idx, item in enumerate(top_n, 1):
        result.append({
            "num": idx,
            "val": item["val"]
        })
    return render_template('index.html', results=result, search_type='stats',search_time=sort_time)

# 热点分析功能
@app.route('/hotspot-analysis')
def hotspot_analysis():
    n = int(request.args.get('n', 10))
    top_keywords,search_time = output_top_keywords(trie_keywords, top_n=n)
    return render_template('index.html', results=top_keywords, search_type='stats',search_time=search_time)

# 聚团分析功能
@app.route('/clique-analysis')
def clique_analysis():
    n = int(request.args.get('n', 2)) 
    groups = load_groups(group_output)
    group_total = len(groups)
    results, search_time, group_total = query_group(group_output, n)
    return render_template(
        'index.html',
        results=results,
        search_type='stats',
        search_time=search_time,
        group_total=group_total
    )

if __name__ == '__main__':
    print("Loading all data and building structures...\n")
    trie_keywords, trie_partial, top_authors, sort_time = load_data()
    app.run(debug=True, use_reloader=False)

