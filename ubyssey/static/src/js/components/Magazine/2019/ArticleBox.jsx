/** @format */

import React from "react"

class ArticleBox extends React.Component {
  render() {
    const background =
      this.props.image === null
        ? null
        : { "background-image": `url(${this.props.image})` }
    const transition = { transitionDelay: `${this.props.index * 0.125}s` }
    const boxStyle = Object.assign({}, background, transition)
    return (
      <div className={`article-grid ${this.props.subsection}`}>
        <a
          className={`o-article-box o-article-box--grid ${
            !this.props.transition ? "show" : ""
          }`}
          href={this.props.url}
          style={boxStyle}>
          <h2>{this.props.headline}</h2>
        </a>
      </div>
    )
  }
}

export default ArticleBox
