import React, { Component } from 'react'
import humanizeDateTime from '../modules/Dates'

class ArticlePreview extends Component{
  constructor(props) {
    super(props)
  }

  goToArticle() {
    window.location = this.props.url
  }

  render() {
    const msec = Date.parse(this.props.publishTime)
    const publishedDate = new Date(msec)
    const imageStyle = {backgroundImage: `url(${this.props.featuredImageUrl})`}

    return (
      <article
        id={'suggested-article-' + String(this.props.articleId)}
        className='o-article o-article--suggested'>
          {this.props.featuredImageUrl &&
            <a href={this.props.url}>
              <div
                className='o-article__image'
                style={imageStyle}></div>
            </a>}
          <div className='o-article__meta'>
            <h3 className='o-article__headline'>
              <a href={this.props.url}>{this.props.headline}</a>
            </h3>
            <div className='o-article__byline'>
              <span className='o-article__author'>{this.props.authors[0]}</span> &nbsp;&middot;&nbsp; <span className='o-article__published'>{publishedDate.toDateString().slice(4)}</span>
            </div>
          </div>
      </article>
    )
  }
}

export default ArticlePreview;
