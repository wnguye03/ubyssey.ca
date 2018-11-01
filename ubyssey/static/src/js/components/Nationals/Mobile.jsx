import React from 'react'
import Mvp from 'Mvp.jsx'

class Mobile extends React.Component {
  constructor(props){
    super(props)
  }

  renderTeamHeader(name, image) {
    return(
      <div>
        <div className={}style={{backgroundImage: 'url("' + image + '")'}} />
        <h1>{name}</h1>
        {content.map((paragraph) => {
          return(<p>{paragraph}</p>)
        })}
      </div>
    )
  }

  logoStyle(team) {
    let logoStyle = {}
    if (this.state.selectedTeam && team.name !== this.state.selectedTeam) {
      Object.assign(logoStyle, {display: 'none'})
    } else if(this.state.selectedTeam) {
      return(Object.assign(logoStyle, {height: '200px', top: '0', left: '50%'}))
    }
    return(Object.assign(logoStyle, styles.logo, {top: team.location[0] + '%', left: team.location[1] + '%'}))
  }

  render() {
    return (
      <div>
        <div id='c-nationals-map' style={styles.map}>
          <svg xmlns="http://www.w3.org/2000/svg" 
            style={styles.svgMap}
            viewBox={this.state.mapViewBox.join(' ')}
            onClick={() => {this.resetMap()}}
            dangerouslySetInnerHTML={{__html: mapPath}} />
          {this.props.teamData.map((team) => {
            return(
              <img className='c-nationals-map-marker'
                src={team.image.thumbnail} 
                onClick={() => {this.selectTeam(team)}}
                style={this.logoStyle(team)}/>
            )
          })}
        </div>
        {this.state.selectedTeam && this.props.teamData.map((team) => {
          if (team.name === this.state.selectedTeam) {
            return(
              <div className='c-nationals-team-container' >
                {this.renderTeam(team.name, team.content)}
                {this.renderPlayer(team.player)}
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


