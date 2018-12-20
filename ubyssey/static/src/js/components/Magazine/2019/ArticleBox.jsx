import React from 'react'

class ArticleBox extends React.Component {
  render() {
    const background = this.props.image === null ? null: {'background-image': `url(${ this.props.image})`}
    const boxStyle = Object.assign({}, {'animation-delay': `${this.props.index*.125}s`}, background)
    return (
      <div className={`article-grid article-grid--${ this.props.index % 4 }`}>
        <a className={`o-article-box o-article-box--grid o-article-box--${ this.props.subsection }`} 
          href={ this.props.url } 
          style={boxStyle}>
          <h2>{ this.props.headline }</h2>
        </a>
      </div>
    ) 
  }
}

export default ArticleBox
