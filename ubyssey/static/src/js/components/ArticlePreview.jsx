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
            {this.props.featuredImageUrl && 
              <div
                className='sa-thumbnail-image'
                style={{backgroundImage: 'url(' + this.props.featuredImageUrl + ')'}}></div>
            }
            {!this.props.featuredImageUrl && 
              <div className='sa-thumbnail-image'>
                No image
              </div>
            }
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