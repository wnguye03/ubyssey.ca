import React from 'react'
import Map from './Map.jsx'
import { desktopSize } from '../../utils'

class FoodInsecurity extends React.Component {
  constructor(props){
    super(props)

    this.mapViewBox = [0, 0, 820, 376]
    this.state = {
      selectedTeam: null
    }
  }

  selectPoint(team) {
    if (this.state.selectedTeam && this.state.selectedTeam.name === team.name) {
      team = null
    }
    this.setState({
      selectedTeam: team
    })
  }
  
  resetPoints() {
    this.setState({
      selectedTeam: null
    })
  }

  render() {
    const isDesktop = window.innerWidth > desktopSize ? true: false
    return (
      <div className={'c-i-container'}>
        { isDesktop && 
          <div className='c-i-desktop'>
            <Map pointData={this.props.pointData} 
              resetMap={() => {this.resetPoints()}}
              selectedTeam={this.state.selectedTeam}
              mapViewBox={this.mapViewBox}
              mapImage={this.props.map}
              selectPoint={(team) => this.selectPoint(team)}/> 
          </div>
        }{ !isDesktop && 
          <div>
            mobile render
          </div>
        }
      </div>
    )
  }
}


export default FoodInsecurity


