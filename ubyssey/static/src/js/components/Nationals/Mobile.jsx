import React from 'react'
import Mvp from './Mvp.jsx'

class Mobile extends React.Component {
  constructor(props){
    super(props)
  }

  renderTeamHeader(team) {
    return(
      <div className='c-n-team-header'
        style={{backgroundColor: team.colors[0]}}
        onClick={() => {this.props.selectTeam(team)}}>
        <div className='c-n-image-container'>
          <div className='c-n-image' style={{backgroundImage: 'url("' + team.image.thumbnail + '")'}} />
        </div> 
        <span className='c-n-title'>{team.name}</span>
      </div>
    )
  }

  renderTeamContent(team) {
    return(
      <div className='c-n-team-content'>
        <h4>
          <span className='c-n-team-stat'>Wins: {team.stats[0]}</span>
          <span className='c-n-team-stat'>Losses: {team.stats[1]}</span>
          <span className='c-n-team-stat'>Ties: {team.stats[2]}</span>  
        </h4>
        {team.content.map((paragraph) => {
          return(<p>{paragraph}</p>)
        })}
        <Mvp player={team.player}/>
      </div>
    )
  }

  render() {
    const {selectedTeam, teamData} = this.props
    return (
      <div className='c-n-mobile-container'>
        {teamData.map((team) => {
          if (selectedTeam && team.name === selectedTeam.name) {
            return(
              <div className='c-n-team-container' >
                {this.renderTeamHeader(team)}
                {this.renderTeamContent(team)}
              </div>
            )
          } else {
            return(
              <div className='c-n-team-container'>
                {this.renderTeamHeader(team)}
              </div>
            )
          }
          return
        })}
      </div>
    )
  }
}

var styles = {
  map: {
    position: 'relative',
    // maxHeight: '75vh',
    height: 'auto',
    width: '90vw',
    margin: '2rem auto',
  },
  logo: {
    top: '0',
    left: '0',
    transform: 'translate(-50%, 0%)',
    transition: 'all 0.1s ease-out 0s'
  },
  title: {
    fontSize: '1.8rem',
    fontWeight: 400,
    fontFamily: "'Roboto', Helvetica, Arial, sans-serif",
    textAlign: 'center'
  }
}

export default Mobile


