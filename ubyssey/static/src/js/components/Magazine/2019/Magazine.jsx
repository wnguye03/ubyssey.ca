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
        <div className="article-grid-container">
          {this.state.subsection &&
            this.props.articles[this.state.subsection].map((box, index) => {
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
          {/* <img className="cover-photo" src={this.props.cover} /> */}
        </div>
      </div>
    )
  }

  render() {
    const show = this.state.show ? "show" : ""
    return (
      <div className={`magazine-container ${show}`}>
        {/* {this.renderVideo()} */}
        {this.renderCover()}

        {this.renderSubsection()}
      </div>
    )
  }
}

export default Magazine
