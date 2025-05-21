// 输入选项
function showInputSection(option) {
    const mainButtons = document.getElementById('main-buttons');
    const inputContainer = document.getElementById('input-container');
    const partialSearchContainer = document.getElementById('partial-search-container');
    const optionsContainer = document.getElementById('options');
    const statsButtons = document.getElementById('stats-buttons');
    const searchInput = document.querySelector('#search-input');

    mainButtons.style.display = 'none';
    inputContainer.style.display = 'none';
    partialSearchContainer.style.display = 'none';
    optionsContainer.style.display = 'none';
    statsButtons.style.display = 'none';

    if (option === 'basic-search') {
        inputContainer.style.display = 'block';
        optionsContainer.style.display = 'block';
        searchInput.value = '';
        document.querySelector('input[name="search-type"][value="author"]').checked = true;
        updateSearchPlaceholder('请输入作者名');
    } else if (option === 'partial-match-search') {
        partialSearchContainer.style.display = 'block';
    } else if (option === 'related-search') {
        inputContainer.style.display = 'block';
        updateSearchPlaceholder('请输入作者名');
    } else if (option === 'stats') {
        showStatsButtons();
    }
}

// 更新输入框提示文字
function updateSearchPlaceholder(placeholder) {
    document.querySelector('#search-input').setAttribute('placeholder', placeholder);
}

// 返回主按钮区域
function backToMainButtons() {
    const mainButtons = document.getElementById('main-buttons');
    const inputContainer = document.getElementById('input-container');
    const optionsContainer = document.getElementById('options');
    const statsButtons = document.getElementById('stats-buttons');
    const searchInput = document.querySelector('#search-input');

    document.getElementById('partial-search-container').style.display = 'none';

    mainButtons.style.display = 'flex';
    mainButtons.style.flexDirection = 'column';
    mainButtons.style.alignItems = 'center';

    inputContainer.style.display = 'none';
    optionsContainer.style.display = 'none';
    statsButtons.style.display = 'none';
    searchInput.value = '';
}

// 返回基本搜索
function backToBasicSearch() {
    const mainButtons = document.getElementById('main-buttons');
    const inputContainer = document.getElementById('input-container');
    const optionsContainer = document.getElementById('options');
    const searchInput = document.querySelector('#search-input');

    document.querySelector('.results-box').style.display = 'none';

    inputContainer.style.display = 'block';
    optionsContainer.style.display = 'block';
    searchInput.value = '';
    mainButtons.style.display = 'none';

    document.querySelector('input[name="search-type"][value="author"]').checked = true;
    updateSearchPlaceholder('请输入作者名');
}

// 搜索按钮
function performSearch() {
    const query = document.querySelector('#search-input').value;

    if (!query.trim()) {
        alert("未输入文字");
        return;
    }

    window.location.href = 'search-results.html?query=' + encodeURIComponent(query);
}

// 统计功能按钮
function showStatsButtons() {
    const statsButtons = document.getElementById('stats-buttons');
    const inputContainer = document.getElementById('input-container');

    statsButtons.style.display = 'flex';
    statsButtons.style.flexDirection = 'column';
    statsButtons.style.alignItems = 'center';
    inputContainer.style.display = 'none';
}

// 按钮主菜单点击
document.getElementById('basic-search-btn').addEventListener('click', function () {
    showInputSection('basic-search');
});
document.getElementById('partial-match-search-btn').addEventListener('click', function () {
    showInputSection('partial-match-search');
});
document.getElementById('stats-btn').addEventListener('click', function () {
    showInputSection('stats');
});

// 选择“作者”或“论文”
document.querySelectorAll('input[name="search-type"]').forEach(function (radio) {
    radio.addEventListener('change', function () {
        if (this.value === 'author') {
            updateSearchPlaceholder('请输入作者名');
        } else if (this.value === 'paper') {
            updateSearchPlaceholder('请输入论文题目');
        }
    });
});

window.addEventListener('DOMContentLoaded', () => {
    const hasResults = document.querySelector('.results-box');
    if (hasResults) {
        document.getElementById('main-buttons').style.display = 'none';
        document.getElementById('input-container').style.display = 'none';
        document.getElementById('stats-buttons').style.display = 'none';
    }
});

function showStatsInput(type) {
    const input = document.getElementById('stats-input');
    const form = document.getElementById('stats-form');
    const container = document.getElementById('stats-input-container');
    const groupInfo = document.getElementById('group-info');

    if (type === 'author') {
        input.placeholder = '请输入要统计的作者数量';
        form.action = '/author-stats';
        if (groupInfo) groupInfo.style.display = 'none';
    } else if (type === 'hotspot') {
        input.placeholder = '请输入要统计的热点关键词数量';
        form.action = '/hotspot-analysis';
        if (groupInfo) groupInfo.style.display = 'none';
    } else if (type === 'clique') {
        input.placeholder = '请输入要查看的聚团编号';
        form.action = '/clique-analysis';
        if (groupInfo) groupInfo.style.display = 'block';
    }

    container.style.display = 'block';
    document.getElementById('stats-buttons').style.display = 'none';
}

function backToStatsButtons() {
    const statsButtons = document.getElementById('stats-buttons');
    const statsInputContainer = document.getElementById('stats-input-container');
    const resultsBox = document.querySelector('.results-box');

    if (resultsBox) {
        resultsBox.style.display = 'none';
    }

    statsInputContainer.style.display = 'none';
    statsButtons.style.display = 'flex';
    statsButtons.style.flexDirection = 'column';
    statsButtons.style.alignItems = 'center';

    document.getElementById('stats-input').value = '';
}

function backToStatsSearchButtons() {
    const statsButtons = document.getElementById('stats-buttons');
    const statsInputContainer = document.getElementById('stats-input-container');
    const resultsBox = document.querySelector('.results-box');

    if (resultsBox) {
        resultsBox.style.display = 'none';
    }
    statsButtons.style.display = 'none';

    statsInputContainer.style.display = 'block';

    document.getElementById('stats-input').value = '';
}

function backToPartialSearch() {
    const resultsBox = document.querySelector('.results-box');
    const partialSearchInput = document.getElementById('partial-search-container');
    const mainButtons = document.getElementById('main-buttons');

    if (resultsBox) resultsBox.style.display = 'none';
    if (partialSearchInput) partialSearchInput.style.display = 'block';
    if (mainButtons) mainButtons.style.display = 'none';
}
