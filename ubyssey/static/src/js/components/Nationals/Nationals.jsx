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
        {/* <div className='c-n-title'>
          <div>U Sports Men’s Soccer Championship</div>
          <div style={{fontSize: '1.5rem', fontWeight: 600}}>Hosted by the UBC Thunderbirds: November 8-11</div>
        </div>  */}
        { isDesktop && 
          <div className='c-n-desktop'>
            <Map teamData={this.props.teamData} 
              resetMap={() => {this.resetTeam()}}
              selectedTeam={this.state.selectedTeam}
              selectTeam={(team) => this.selectTeam(team)}/> 
            <Desktop teamData={this.props.teamData} 
              isDesktop={isDesktop}
              selectedTeam={this.state.selectedTeam}/>
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


