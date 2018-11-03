import React from 'react'

class Mvp extends React.Component {

  render() {
    const {player, primaryColor} = this.props
    const secondaryColor = primaryColor + 'ce'
    const playerImage = {backgroundImage: 'url("' + player.image.medium + '")'}
    const ribbonPrimary = {backgroundColor: primaryColor}
    const ribbonAfter = {borderColor: secondaryColor, borderRightColor: 'transparent'}
    const ribbonBefore = {borderColor: secondaryColor, borderLeftColor: 'transparent'}
    
    
    const mvpStyle={backgroundColor: primaryColor + '70'}
    return(
      <div className='c-n-mvp' style={mvpStyle}>
        
        <div className='c-n-headshot'>
          <div className='c-n-headshot--image-container'>
            <div className='c-n-headshot--image'
              style={playerImage}>
            </div>
          </div>
          <div className="non-semantic-protector" style={{width: '138%'}}> 
            <span className="ribbon-before" style={ribbonBefore}></span>
            <span className="ribbon" style={ribbonPrimary}>
              <strong className="ribbon-content" >{player.name}</strong>
            </span>
            <span className="ribbon-after" style={ribbonAfter}></span>
          </div>
        </div>

        {player.content.map((paragraph) => {
          return(<p>{paragraph}</p>)
        })}
      </div>

    )
  }


}

export default Mvp;