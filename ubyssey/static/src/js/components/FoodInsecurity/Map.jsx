import React from 'react'

class Map extends React.Component {
  constructor(props){
    super(props)
  }

  renderPoints(location, index, selected) {
    const pointStyle = {top: location[0] + '%', left: location[1] + '%', transform: `translate(-50%, -50%) scale(${selected ? '1.2': '1'})`}
    
    return(
      <div className='c-i-map__marker' 
        style={pointStyle}
        onClick={() => {this.props.selectPoint(index)}}>
        <div className='c-i-map__marker-center'></div>
      </div>
    )
  }

  render() {
    const currentPoint = this.props.currentPoint
    const contenStyle = currentPoint ? {transform: 'translate(0)', width: '350px', opacity: 1}:{transform: 'translate(-350px)', width: 0, opacity: 0}
    return (
      <div className='c-i-map' >
        <div className='c-i-map__image-container'>
          <div className='c-i-map__image' style={{backgroundImage: 'url(' + this.props.mapImage + ')'}}>
          {this.props.pointData.map((point, index) => {
            return(this.renderPoints(point.location, index, (currentPoint ? point.name == currentPoint.name: false)))
          })}
          </div>
        </div>
        <div className='c-i-map__content-container' style={contenStyle}>
          <div className='c-i-map__content'>
            <h2>{currentPoint && currentPoint.name}</h2>
            {currentPoint && currentPoint.content.map((paragraph) => {
              return <p>{paragraph}</p>
            })}  
          </div>
        </div>
      </div>
    )
  }
}

export default Map


