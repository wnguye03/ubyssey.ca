import React, { Component } from 'react'
import Cookies from 'js-cookie'

class AdblockSplash extends Component {
  constructor(props){
    super(props)
    this.state = {
      splashScreenEnable: true,
    }
  }
  getCookieName() {
    return 'ubyssey_site_visit'
  }

  getCookie(field) {
    let cookie = Cookies.get(this.getCookieName())
    if(typeof cookie === 'string' && cookie !== '') {
      cookie = JSON.parse(cookie)
      if(field) {
        return cookie[field]
      }
      return cookie
    }
    return cookie
  }

  setCookie(visitCount) {
    Cookies.set(
      this.getCookieName(),
      {'visitCount': visitCount},
      { path: '/' }
    )
  }

  componentDidMount() {
    let visitCount = this.getCookie('visitCount')
    if (typeof(visitCount) !== 'number') {
      this.setCookie(1)
    } else{
      this.setCookie(visitCount + 1)
    }
  }

  render() {
    console.log(this.getCookie('visitCount'))
    return (
      <div>
        {this.getCookie('visitCount') > 3 && this.state.splashScreenEnable && 
          <div className='adblock-container'>
            <div className='adblock-fullscreen' />
            <div className='adblock-content'>
              <h1>Enjoying the Ubyssey?</h1>
              <h3>Support your student newspaper</h3> 
              <h3>Disable your adblocker</h3>
              <p>The Ubyssey is a not for profit organization funded by advertisments and contributions from users like you.</p> 
              <p>Thank you!</p>
              <button 
                className='adblock-button' 
                onClick={() => this.setState({splashScreenEnable: false})}>
                Don't ask again
              </button>
            </div>
          </div>
        }
      </div>
    )
  }
}

export default AdblockSplash
