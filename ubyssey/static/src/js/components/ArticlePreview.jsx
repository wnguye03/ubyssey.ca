import React, { Component } from 'react';

class ArticlePreview extends Component{
  constructor(props) {
    super(props)
  }
  
  goToArticle() {
    window.location = this.props.url
  }

  render() {
    return (
      <div 
        onClick={() => this.goToArticle()}
        id={'suggested-article-' + String(this.props.articleId)}
        className='article-preview'>
          <div className='sa-content'>
            <img 
              className='sa-thumbnail-image' 
              src={this.props.featuredImageUrl}>
              </img>
            <h3>{this.props.headline}</h3>
          </div>
          <div className='sa-subtitle'>
            <span className='sa-date'>{this.props.publishTime}</span>
            <span className='sa-author'><em>{this.props.authors[0]}</em></span>
          </div>
      </div>
    )
  }
}

export default ArticlePreview;