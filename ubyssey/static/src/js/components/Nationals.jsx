import React from 'react'
import { desktopSize } from '../utils'

class Nationals extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      isMobile: window.innerWidth < desktopSize
    }
  }

  componentDidMount() {
    console.log(this.props)
    this.props.teamData.map((team) => {
      console.log(team)
    })
  }

  renderTeam(name, content) {
    return(
      <div>
        <h1>{name}</h1>
        {content.map((paragraph) => {
          <p>{paragraph}</p>
        })}
      </div>
    )

  }

  renderPlayer(player) {
    return (
      <div>
        <h3>{player.name}</h3>
        <img src={player.image.medium}></img>
        {player.content.map((paragraph) => {
          <p>{paragraph}</p>
        })}
      </div>
    )
  }

  render() {
    const mapStyle = {
      backgroundImage: "url(" + this.props.map + ")",
      height: '480px',
      width: '640px'
    }
    return (
      <div className={'c-nationals-container'}>
        <div className='c-nationals-map'
            style={mapStyle}>
            {this.props.teamData.map((team) => {
              <img src={team.image.thumbnail}
                style={{position: 'relative', top: team.location[0], left: team.location[1]}}></img>
            })}
        </div>
        {this.props.teamData.map((team) => {
          <div className='c-nationals-team-container'>
            {this.renderTeam(team.name, team.content)}
            {this.renderPlayer(team.player)}
          </div>
        })}
      </div>
    )
  }
}

export default Nationals
