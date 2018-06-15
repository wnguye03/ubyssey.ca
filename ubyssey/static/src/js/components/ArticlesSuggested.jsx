
import React, { Component } from 'react'
import LinkedList from '../modules/LinkedList'
import ArticlePreview from './ArticlePreview.jsx'
import DispatchAPI from '../api/dispatch'
class ArticlesSuggested extends Component{

  constructor(props) {
    super(props)

    var articles = props.articles
    articles.unshift(props.firstArticle.id)

    this.articlesTable = {};
    this.articlesTable[this.props.firstArticle.id] = 0;

    this.state = {
      active: new LinkedList(articles),
      articles: [props.firstArticle],
      loading: false
    }
  }

  componentDidMount() {
    for (let id in this.props.articles) {
      this.getArticle(id)
    }
  }

  getArticle(id) {
    DispatchAPI.articles.rendered(id)
    .then ( (response) => {
      const articles = [...this.state.articles, response]
      this.setState({articles})
    })
  }

  render() {
    const articles = this.state.articles.map((article, index) => {
      console.log(index, article)
      if (index !== 0 && index <= 3) {
        return (
          <ArticlePreview 
            articleId={article.id}
            headline={article.headline}
            url={article.url}
            key={index} />
        )
      }
    });

    return (
      <div className={'suggested-articles-container-outer'}>
        <h1>Suggested Articles</h1>
        <div className={'suggested-articles-container-inner'}>
          {articles}
        </div>
      </div>
    );
  }
}

export default ArticlesSuggested;
