import React, { Component } from 'react';

class ArticlePreview extends Component{
  constructor(props) {
    super(props)
  }
  
  goToArticle() {
    console.log('go to article')
    window.location = this.props.url
  }

  render() {
    return (
      <div 
        onClick={() => this.goToArticle()}
        id={'suggested-article' + String(this.props.articleId)}
        className='article-preview'>
          <h3>{this.props.headline}</h3>
      </div>
    )
  }
}

export default ArticlePreview;