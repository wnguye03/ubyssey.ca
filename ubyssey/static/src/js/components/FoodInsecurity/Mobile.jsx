import React from 'react'

class Mobile extends React.Component {
  constructor(props) {
    super(props)
  }

  renderMap() {

    return(
      <svg xmlns="http://www.w3.org/2000/svg" 
        className='c-i-map'
        width={this.MAP_WIDTH}
        height={this.MAP_HEIGHT}
        id='interactive-map'
        viewBox={this.state.viewBox.join(' ')}
        onClick={(e)=> this.detectDoubleTap(e)}
        onDoubleClick={(e) => this.zoomMap(e)}>
        <defs dangerouslySetInnerHTML={{__html: defs}}></defs>
        <title>UBC Map</title>
        <g id="Ocean">
          <rect className="cls-1" width={this.state.viewBox[2]} height={this.state.viewBox[3]}/>
        </g>
        <g id="Base" dangerouslySetInnerHTML={{__html: base}}></g>
        <g id="Roads" dangerouslySetInnerHTML={{__html: roads}}></g>
        <g id="Locations">
          {Object.keys(locations).map((name) => {
            let point = null
            this.props.pointData.map((data) => {
              if(data.name.split(' ').join('').toLowerCase() === name) {
                point = data
              }
            })
            return(
              <svg xmlns="http://www.w3.org/2000/svg" 
                style={{overflow: 'auto'}}>
                <title style={{textTransform: 'capitalize'}}>{point.name}</title>
                <polygon className='cls-5' 
                  id={name}
                  points={locations[name]} 
                  onClick={(e) => {this.selectPoint(e, point)}}/>
              </svg>
            )
          })}
        </g>
      </svg>
    )
  }

  render() {
    const currentPoint = this.props.currentPoint
    const desktopContentStyle = currentPoint ? {transform: 'translate(0)', width: '350px', opacity: 1}:{transform: 'translate(-350px)', width: 0, opacity: 0}
    const mobileContentStyle = currentPoint ? {transform: 'translateY(-350px)', opacity: 1}:{transform: 'translateY(0)'}
    return (
      <div className='c-i-map' height={this.MAP_HEIGHT}>
        <div className='c-i-map__image-container' style={{backgroundColor: '#292b71'}}>
          {this.renderMap()}
          <div className='c-i-map__instructions'>Double {this.props.isDesktop ? 'Click': 'Tap' } to Zoom | {this.props.isDesktop ? 'Click': 'Tap' } to Select </div>
        </div>
        <div className='c-i-map__content-container' style={this.props.isDesktop ? desktopContentStyle : mobileContentStyle}>
          <div className='c-i-map__content'>
            <div className='c-i-map__content-header'>
              <span className='c-i-map__content-title'>{currentPoint && currentPoint.name}</span> 
              {!this.props.isDesktop && <span> <i className='fa fa-arrow-down' onClick={() => this.props.resetPoint()}> Back </i> </span>}
            </div>
            {currentPoint && currentPoint.content.map((paragraph) => {
              return <p>{paragraph}</p>
            })} 
            {this.props.isDesktop && <i className='fa fa-arrow-left' onClick={() => this.props.resetPoint()}> Back </i> }
          </div>
        </div>
      </div>
    )
  }
}

export default Mobile


