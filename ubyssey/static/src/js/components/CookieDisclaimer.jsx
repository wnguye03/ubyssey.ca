import React from 'react'
import Cookies from 'js-cookie'

class CookieDisclaimer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      showCookieDisclaimer: true,
    }
  }
  getCookieName() {
    return 'cookie_disclaimer'
  }

  getCookie(field) {
    let cookie = Cookies.get(this.getCookieName())
    if (typeof cookie === 'string' && cookie !== '') {
      cookie = JSON.parse(cookie)
      if (field) {
        return cookie[field]
      }
      return cookie
    }
    return cookie
  }

  setCookie(value) {
    Cookies.set(
      this.getCookieName(),
      {'accepted': value},
      { path: '/' }
    )
  }

  disableCookieDisclaimer() {
    this.setCookie(true)
    this.setState({
      showCookieDisclaimer: false
    })
  }

  componentDidMount() {
    const accepted = this.getCookie('accepted')

    if (!navigator.cookieEnabled || accepted) {
      this.setState({
        showCookieDisclaimer: false
      })
    }
  }

  render() {
    return (
      <div>
        { this.state.showCookieDisclaimer &&
          <div className='cookie-disclaimer-wrapper'>
            <div className='cookie-disclaimer-container'>
              <h3>Cookies on the Ubyssey website</h3>
              <div className='c-row'>
                <p>
                  This website uses cookies to give you the best experience possible.
                  Using this website means you accept our use of cookies. You can disable cookies in your browser settings.
                  We respect your privacy and you can read more about our cookie policy <em><a href={'https://www.ubyssey.ca/cookie-policy-2018/'}>here</a></em>.
                </p>
                <button
                  className='c-button c-button--small'
                  onClick={() => {this.disableCookieDisclaimer()}}
                  >Continue</button>
              </div>
            </div>
          </div>
        }
      </div>
    )
  }
}

export default CookieDisclaimer
