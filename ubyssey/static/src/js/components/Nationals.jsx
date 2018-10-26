import React from 'react'

const desktopSize = 960;

class Nationals extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      isMobile: window.innerWidth < desktopSize
    }
  }

  componentDidMount() {
    console.log(this.props)
  }

  prepareDescription(description) {
    if (description) {
      if (description.length > 500) {
        return <p> {description.slice(0, 500).concat('...')} </p>
      } else {
        return <p> {description} </p>
      }
    } else {
      return ''
    }
  }

  render() {
    // const winWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    // const winHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    // const mobileStyle = {
    //   width: winWidth,
    //   overflow: this.state.mobileShow ? 'scroll': 'visible',
    //   marginTop: (this.state.isMobile ? (this.state.mobileShow ? 0 : winHeight-54-54) : -80),
    //   height: this.state.isMobile ? window.innerHeight - 54 : 80
    // }

    return (
      <div className={'c-nationals-container'}>
        This is the nationals component
      </div>
    )
  }
}

export default Nationals
