/** @format */

import React from "react"

class Header extends React.Component {
  renderSubsection(subsection) {
    return (
      <div
        className={`subsection ${
          this.props.selected === subsection ? "selected" : ""
        }`}
        onClick={() => this.props.selectSubsection(subsection)}>
        <span>{subsection}</span>
      </div>
    )
  }

  render() {
    return (
      <div className="magazine-header">
        <div className="item left">
          <a
            className="subsection"
            onClick={() => {
              this.props.selectSubsection()
            }}>
            The Ubyssey Magazine
          </a>
        </div>

        <div className="item center">
          <h1>Presence</h1>
        </div>

        <div className="item right">
          {this.props.subsections.map((subsection) => {
            return this.renderSubsection(subsection)
          })}
        </div>
      </div>
    )
  }
}

export default Header
