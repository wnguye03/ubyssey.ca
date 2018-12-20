import React from 'react'

class Header extends React.Component {
  render() {
    return (
      <div className='magazine-header'>
        <div className="item left">
          <a className="o-link">The Ubyssey Magazine</a>
        </div>
        
        <div className="item center">
          Presence
        </div>
        
        <div className="item right">
            <div className="item">
              <h3>{this.subsections[0]}</h3>
            </div>
            <div className="item">
              <h3>{this.subsections[1]}</h3>
            </div>
            <div className="item">
              <h3>{this.subsections[2]}</h3>
            </div>
        </div>
      </div>
    ) 
  }
}

export default Header