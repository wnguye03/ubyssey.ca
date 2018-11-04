import React from 'react'
import Map from './Map.jsx'
import Desktop from './Desktop.jsx'
import Mobile from './Mobile.jsx'
import { desktopSize } from '../../utils'

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
    const isDesktop = window.innerWidth > desktopSize ? true: false
    return (
      <div className={'c-n-container'}>
        <h4>The Ubyssey Presents:</h4>
        <h1>The 2018 Canadian Soccer Nationals</h1>
        { isDesktop && 
          <div style={{position: 'relative'}}>
            <Map teamData={this.props.teamData} 
              resetMap={() => {this.resetTeam()}}
              selectedTeam={this.state.selectedTeam}
              selectTeam={(team) => this.selectTeam(team)}/> 
            <Desktop team={this.state.selectedTeam} 
              isDesktop={isDesktop}/>
          </div>
        }{ !isDesktop && 
          <Mobile selectedTeam={this.state.selectedTeam}
            teamData={this.props.teamData}
            isDesktop={isDesktop}
            selectTeam={(team) => this.selectTeam(team)}/> 
        }
      </div>
    )
  }
}


export default Nationals


