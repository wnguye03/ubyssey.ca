import React from 'react'
import {defs, base, roads, locations} from './mapPath.js'

class Map extends React.Component {
  constructor(props) {
    super(props)
    this.MAP_WIDTH = this.props.isDesktop ? 500 : (window.innerWidth - 32 || document.documentElement.clientWidth - 32)
    this.MAP_HEIGHT = this.props.isDesktop ? 640 : (640/500)*this.MAP_WIDTH
    this.viewBox = [0, 0, this.MAP_WIDTH/2, this.MAP_HEIGHT/2]
    this.myLatestTap = new Date().getTime();
    this.state = {
      viewBox: this.viewBox,
      zoom: false,
      scale: 4
    }
  }

  setScale(value) {
    this.setState({
      scale: value
    })
  }

  detectDoubleTap(e) {
    if(!this.props.isDesktop) {
      var now = new Date().getTime();
      var timesince = now - this.myLatestTap;
      if((timesince < 500) && (timesince > 0)){
        this.zoomMap(e)
      }
    
      this.myLatestTap = new Date().getTime();
    }
  }

  zoomMap(e) {
    e.preventDefault()
    const map = document.getElementById('interactive-map')
    const mX = e.clientX - map.getBoundingClientRect().left
    const mY = e.clientY - map.getBoundingClientRect().top

    // get difference between click point and center of map
    let zoomX = mX - this.MAP_WIDTH/2
    let zoomY = mY - this.MAP_HEIGHT/2

    //normalize click point to be centered in zoomed SVG
    zoomX = (zoomX + (this.state.scale - 1)*this.viewBox[2]/this.state.scale)/2 
    zoomY = (zoomY + (this.state.scale - 1)*this.viewBox[3]/this.state.scale)/2





    const newViewBox = [zoomX, zoomY, this.viewBox[2]/this.state.scale, this.viewBox[3]/this.state.scale]

    if (!this.state.zoom) {
      this.setState({
        viewBox: newViewBox,
        zoom: true
      })
    } else {
      this.setState({
        viewBox: [0, 0, this.viewBox[2], this.viewBox[3]],
        zoom: false
      })
    }
  }

  selectPoint(e, point) {
    e.persist()
    if(!this.state.zoom) {
      this.zoomMap(e)
    }
    this.props.selectPoint(point)
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
    const mobileContentStyle = currentPoint ? {transform: 'translate(0)', opacity: 1}:{transform: 'translate(75%)', opacity: 0}
    return (
      <div className='c-i-map' height={this.MAP_HEIGHT}>
        <div className='c-i-map__image-container' style={{backgroundColor: '#292b71'}}>
          {this.renderMap()}
          <div className='c-i-map__instructions'>Double {this.props.isDesktop ? 'Click': 'Tap' } to Zoom | {this.props.isDesktop ? 'Click': 'Tap' } to Select </div>
        </div>
        <div className='c-i-map__content-container' style={this.props.isDesktop ? desktopContentStyle : mobileContentStyle}>
          <div className='c-i-map__content'>
            <span className='c-i-map__content-title'>{currentPoint && currentPoint.name}</span>
            {currentPoint && currentPoint.content.map((paragraph) => {
              return <p>{paragraph}</p>
            })} 
            <i className={`fa ${this.props.isDesktop ? 'fa-arrow-left': 'fa-arrow-right'}`} onClick={() => this.props.resetPoint()}> Back </i>
          </div>
        </div>
      </div>
    )
  }
}

export default Map


