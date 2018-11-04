import React from 'react'
import Ribbon from './Ribbon.jsx'

class Mvp extends React.Component {

  render() {
    const {player, primaryColor} = this.props
    const playerImage = {backgroundImage: 'url("' + player.image.medium + '")'}
    const mvpStyle={backgroundColor: primaryColor + '70'}
    return(
      <div className='c-n-mvp' style={mvpStyle}>
        <h1>Player To Watch</h1>
        <div className='c-n-headshot'>
          <div className='c-n-headshot--image-container'>
            <div className='c-n-headshot--image'
              style={playerImage}>
            </div>
          </div>
          <Ribbon html={player.name} 
            isDesktop={this.props.isDesktop} 
            primaryColor={primaryColor}/>
        </div>

        {player.content.map((paragraph) => {
          return(<p>{paragraph}</p>)
        })}
      </div>

    )
  }


}

export default Mvp;