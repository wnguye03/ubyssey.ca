/** @format */

import React from "react"
import ArticleBox from "./ArticleBox.jsx"
import Header from "./Header.jsx"

const fadeDelay = 500

class Magazine extends React.Component {
  constructor(props) {
    super(props)
    this.subsections = Object.keys(this.props.articles)
    this.state = {
      subsection: null,
      nextSubsection: null,
      transition: false,
    }
  }

  selectSubsection(subsection) {
    this.setState(
      {
        transition: true, //hide
        nextSubsection: subsection,
      },
      () => {
        setTimeout(() => {
          this.setState(
            {
              subsection: this.state.nextSubsection,
            },
            () => {
              setTimeout(() => {
                this.setState({
                  transition: false, //show
                })
              }, 10)
            }
          )
        }, fadeDelay)
      }
    )
  }

  renderSubsection() {
    return (
      <div className="article-grid-container">
        {this.state.subsection &&
          this.props.articles[this.state.subsection].map((box, index) => {
            return (
              <ArticleBox
                color={box.color}
                index={index}
                subsection={this.state.subsection}
                transition={this.state.transition}
                url={box.url}
                image={box.featured_image}
                headline={box.headline}
              />
            )
          })}
      </div>
    )
  }

  renderMagazineLanding() {
    return (
      <div className={`cover-photo-container ${!this.state.transition ? "show" : ""}`}>
        <h1 className="c-cover__logo">Presence</h1>
        <img className="cover-photo" src={this.props.cover} />
      </div>
    )
  }

  render() {
    return (
      <div className="magazine-container">
        <Header
          subsections={this.subsections}
          selected={this.state.subsection}
          selectSubsection={(subsection) => this.selectSubsection(subsection)}
        />

        <div style={{ width: "100%" }}>
          {this.state.subsection && this.renderSubsection()}
          {!this.state.subsection && this.renderMagazineLanding()}
        </div>
      </div>
    )
  }
}

export default Magazine
