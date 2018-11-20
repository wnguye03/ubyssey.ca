import React from 'react'

class Map extends React.Component {
  constructor(props){
    super(props)
  }

  resetMap() {
    this.props.resetMap()
  }

  handlePointClick(index) {
    console.log(index)
  }

  renderPoints(location, index) {
    let pointStyle = {top: location[0] + '%', left: location[1] + '%'}

    // if (this.props.selectedTeam && team.name === this.props.selectedTeam.name) {
    //   Object.assign(logoStyle, {height: '60%', top: '30%', left: '50%', zIndex: 10})
    // } else if (this.props.selectedTeam) {
    //   Object.assign(logoStyle, {zIndex: 0, top: team.location[0] + '%', left: team.location[1] + '%'})
    // } else {
    //   Object.assign(logoStyle, {top: team.location[0] + '%', left: team.location[1] + '%'})
    // }

    return(
      <div className='c-i-map__marker' 
        style={pointStyle}
        onClick={() => {this.handlePointClick(index)}}>
        <div className='c-i-map__marker-center'></div>
      </div>
    )
  }

  render() {
    return (
      <div className='c-i-map' >
        <div className='c-i-map__image-container'>
          <div className='c-i-map__image' style={{backgroundImage: 'url(' + this.props.mapImage + ')'}}>
          {this.props.pointData.map((point, index) => {
            return(this.renderPoints(point.location, index))
          })}
          </div>
        </div>
      </div>
    )
  }
}

export default Map


