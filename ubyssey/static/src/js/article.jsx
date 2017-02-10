import React from 'react';
import './modules/Youtube';
import ArticleList from './components/ArticleList.jsx';
import Search from './components/Search.jsx';

window.articleHeader = false;

if ($('main.article').length) {

    const $article = $('article');

    var articleId = $article.data('id');
    var articleHeadline = $article.data('headline');
    var articleURL = $article.data('url');

    var userId = $article.data('user-id');

    var articleIds = $article.data('list');
    var listName = $article.data('list-name');

    if(articleIds === parseInt(articleIds, 10)){
        articleIds = [articleIds];
    } else {
        articleIds = articleIds.split(',');
    }

    var firstArticle = {
        id: articleId,
        headline: articleHeadline,
        url: articleURL
    };

    var articleList = React.render(
        <ArticleList breakpoint={960} name={listName} firstArticle={firstArticle} articles={articleIds} userId={userId} />,
        document.getElementById('article-list')
    );
}

React.render(
    <Search />,
    document.getElementById('search-form')
);
