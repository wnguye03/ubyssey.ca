/** @format */

import React from "react"

class Header extends React.Component {
  constructor(props) {
    super(props)
    // (this.scrollTop = 0),
    //   (this.state = {
    //     fixHeader: false,
    //   })
  }

  // componentDidMount() {
  //   document.addEventListener("scroll", () => {
  //     this.updateHeader()
  //   })
  // }

  // componentWillUnmount() {
  //   document.removeEventListener("scroll", () => {
  //     this.updateHeader()
  //   })
  // }

  updateHeader() {
    // this.scrollTop = $(window).scrollTop()
    // let element = $(".js-sticky")
    // const elementHeight = element.height(),
    //   elementOffset = $(window).height() - elementHeight,
    //   parentHeight = element.parent().height()
    // if (parentHeight <= elementHeight) {
    //   return
    // }
    // const shouldStick = this.scrollTop > elementOffset
    // if (shouldStick && !this.state.fixHeader) {
    //   this.setState({
    //     fixHeader: true,
    //   })
    // }
    // if (!shouldStick && this.state.fixHeader) {
    //   this.setState({
    //     fixHeader: false,
    //   })
    // }
  }

  renderSubsection(subsection) {
    return (
      <div
        className={`subsection ${this.props.selected === subsection ? "selected" : ""}`}
        onClick={() => this.props.selectSubsection(subsection)}>
        <span>{subsection}</span>
      </div>
    )
  }

  render() {
    const show =
      ((this.props.transition && !this.props.selected) || this.props.selected) && this.props.isDesktop ? "show" : ""
    const sticky = this.props.selected ? "js-sticky--fixed" : ""
    return (
      <div id="magazine-nav" className={sticky}>
        <div className={`item left ${show}`}>
          <a
            className="subsection"
            onClick={() => {
              this.props.selectSubsection()
            }}>
            The Ubyssey Magazine
          </a>
        </div>
        <div className={`item center ${show}`}>
          <h1>{this.props.title}</h1>
        </div>

        <div className={`item show ${show ? "right" : "center"}`}>
          {this.props.subsections.map((subsection) => {
            return this.renderSubsection(subsection)
          })}
        </div>
      </div>
    )
  }
}

export default Header
