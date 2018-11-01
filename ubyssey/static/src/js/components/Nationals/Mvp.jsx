import React from 'react'

class Mvp extends React.Component {

  render() {
    const {player} = this.props
    const playerImage = {backgroundImage: 'url("' + player.image.medium + '")'}
    return(
      <div className='c-n-mvp'>
        
        <div className='c-n-headshot'>
          <div className='c-n-headshot--image-container'>
            <div className='c-n-headshot--image'
              style={playerImage}>
            </div>
          </div>

          <span className='c-n-headshot--name'>{player.name}</span>
        </div>

        {player.content.map((paragraph) => {
          return(<p>{paragraph}</p>)
        })}
      </div>

    )
  }


}

export default Mvp;