import React from 'react'
import { mapPath } from './utils'

const mapZoom = 3
const mapDefault = [820, 376]

class Map extends React.Component {
  constructor(props){
    super(props)
    this.mapViewBox = [0, 0, 820, 376]
  }

  resetMap() {
    this.props.resetMap()
  }

  renderLogos(team) {
    let logoStyle = {}

    if (this.props.selectedTeam && team.name !== this.props.selectedTeam.name) {
      Object.assign(logoStyle, {opacity: '0'})
    } 
    else if (this.props.selectedTeam) {
      Object.assign(logoStyle, {height: '200px', top: '0%', left: '50%'})
    } else {
      Object.assign(logoStyle, styles.logo, {top: team.location[0] + '%', left: team.location[1] + '%'})
    }

    

    return(
      <img className='c-nationals-map-marker'
        src={team.image.thumbnail} 
        onClick={() => {this.props.selectTeam(team)}}
        style={logoStyle}/>
    )
  }

  render() {
    return (
      <div id='c-nationals-map' style={styles.map}>
        <svg xmlns="http://www.w3.org/2000/svg" 
          style={styles.svgMap}
          viewBox={this.mapViewBox.join(' ')}
          onClick={() => {this.resetMap()}}
          dangerouslySetInnerHTML={{__html: mapPath}} />

        {this.props.teamData.map((team) => {
          return(this.renderLogos(team))
        })}
      </div>
    )
  }
}

var styles = {
  map: {
    position: 'relative',
    height: 'auto',
    width: '90vw',
    margin: '2rem auto',
  },
  logo: {
    top: '0',
    left: '50%',
    transform: 'translate(-50%, 0%)',
    transition: 'all .2s ease-out 0s'
  },
}

export default Map


