/** @format */

import React from "react"
import ArticleBox from "./ArticleBox.jsx"
import Header from "./Header.jsx"
import { editorial } from "./contents.js"

const fadeDelay = 500

class Magazine extends React.Component {
  constructor(props) {
    super(props)
    this.subsections = ["editorial"].concat(Object.keys(this.props.articles))
    this.state = {
      subsection: null,
      nextSubsection: null,
      transition: false,
      isDesktop: true,
      show: false,
    }
  }

  componentDidMount() {
    window.addEventListener("resize", () => {
      this.updateSize()
    })
    this.updateSize()
  }

  componentDidUpdate() {
    if (!this.state.show) {
      setTimeout(() => {
        this.setState({
          show: true,
        })
      }, 100)
    }
  }

  componentWillUnmount() {
    window.addEventListener("resize", () => {
      this.updateSize()
    })
  }

  updateSize() {
    this.setState({
      isDesktop: (window.screen.width || document.body.clientWidth) > 600,
    })
  }

  selectSubsection(subsection) {
    this.setState(
      {
        transition: true, //hide
        nextSubsection: subsection,
      },
      () => {
        if (!this.state.nextSubsection) {
          window.scrollTo(0, 0, "smooth")
        }
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
    const slideUp = (this.state.transition && !this.state.subsection) || this.state.subsection ? "slide-up" : " "
    return (
      <div className={`article-grid-wrapper ${slideUp}`}>
        <Header
          subsections={this.subsections}
          title={this.props.title}
          nextSubsection={this.state.nextSubsection}
          transition={this.state.transition}
          selected={this.state.subsection}
          isDesktop={this.state.isDesktop}
          selectSubsection={(subsection) => this.selectSubsection(subsection)}
        />

        {this.state.subsection && this.state.subsection == this.subsections[0] && (
          <div className="editorial-container">
            <div className="inside-cover" style={{ backgroundImage: `url(${this.props.insideCover})` }} />
            <div className="editorial-content">
              <div className="title">{editorial.title}</div>
              {editorial.paragraphs.map((paragraph) => {
                return <p>{paragraph}</p>
              })}
            </div>
          </div>
        )}
        {this.state.subsection && this.state.subsection != this.subsections[0] && (
          <div className="article-grid-container">
            {this.props.articles[this.state.subsection].map((box, index) => {
              return (
                <ArticleBox
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
        )}
      </div>
    )
  }

  renderVideo() {
    return (
      <video preload="yes" autoPlay="true" muted="true" loop="true" playsInline="true" id="magazine-video">
        <source src={`${this.props.video}.mp4`} type="video/mp4" />
        <source src={`${this.props.video}.ogg`} type="video/ogg" />
      </video>
    )
  }

  renderCover() {
    const background = { backgroundImage: `url(${this.props.cover})` }
    return (
      <div className="cover-photo-wrapper">
        <div className="cover-photo-container" style={background}>
          <div id="magazine-title">The Ubyssey Magazine</div>
          <h1 className="c-cover__logo">{this.props.title}</h1>
          <div className="c-cover__content">
            <h1>Editor-in-Chief</h1>
            <li>Lucy Fox</li>
            <h1>Written Content Editors</h1>
            <li>Charlotte Alden</li>
            <li>Mitchell Ballachay</li>
            <li>Andrew Ha</li>
            <li>Emma Livingstone</li>
            <li>Riya Talitha</li>
            <h1>Illustrations Editor</h1>
            <li>Kristine Ho</li>
            <h1>Design Editor</h1>
            <li>Claire Lloyd</li>
          </div>
        </div>
      </div>
    )
  }

  render() {
    const show = this.state.show ? "show" : ""
    return (
      <div className={`magazine-container ${show}`}>
        {this.renderCover()}
        {this.renderSubsection()}
      </div>
    )
  }
}

export default Magazine
