import React from 'react'

class Ribbon extends React.Component {

  render() {
    const secondaryColor = this.props.primaryColor + 'ce'
    const ribbonPrimary = {backgroundColor: this.props.primaryColor}
    const ribbonAfter = {borderColor: secondaryColor, borderRightColor: 'transparent'}
    const ribbonBefore = {borderColor: secondaryColor, borderLeftColor: 'transparent'}
    
    return(
      <div className="non-semantic-protector" style={this.props.style}> 
        <span className="ribbon-before" style={ribbonBefore}></span>
        <span className="ribbon" style={ribbonPrimary}>
          <strong className="ribbon-content" dangerouslySetInnerHTML={{__html: this.props.html}}></strong>
        </span>
        <span className="ribbon-after" style={ribbonAfter}></span>
      </div>
    )
  }
}

export default Ribbon;