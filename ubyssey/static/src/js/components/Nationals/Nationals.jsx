import React from 'react'
import Map from './Map.jsx'
import Desktop from './Desktop.jsx'
import Mobile from './Mobile.jsx'
import { desktopSize } from '../../utils'
import { mapPath } from './utils'

const mapZoom = 3
const mapDefault = [820, 376]

class Nationals extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      selectedTeam: null
    }
  }
  

  selectTeam(team) {
    if (this.state.selectedTeam && this.state.selectedTeam.name === team.name) {
      team = null
    }
    this.setState({
      selectedTeam: team
    })
  }
  resetTeam() {
    this.setState({
      selectedTeam: null
    })
  }

  render() {
    return (
      <div className={'c-nationals-container'}>
        { (window.innerWidth > desktopSize) && 
          <div>
            <Map teamData={this.props.teamData} 
              resetMap={() => {this.resetTeam()}}
              selectedTeam={this.state.selectedTeam}
              selectTeam={(team) => this.selectTeam(team)}/> 
            <Desktop team={this.state.selectedTeam} />
          </div>
        }{ (window.innerWidth <= desktopSize) && 
          <Mobile selectedTeam={this.state.selectedTeam}
            teamData={this.props.teamData}
            selectTeam={(team) => this.selectTeam(team)}/> 
        }
      </div>
    )
  }
}


export default Nationals


