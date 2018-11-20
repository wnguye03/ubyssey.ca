import React from 'react'
import Map from './Map.jsx'
import { desktopSize } from '../../utils'

class FoodInsecurity extends React.Component {
  constructor(props){
    super(props)

    this.state = {
      currentPoint: null
    }
  }

  selectPoint(point) {
    const element = document.getElementsByClassName('food-insecurity')
    console.log(element[0].getBoundingClientRect().top + document.documentElement.scrollTop)
    const topOffset = element[0].getBoundingClientRect().top + document.documentElement.scrollTop
    window.scroll({
      top: topOffset - 48,
      left: 0,
      behavior: 'smooth'
    });
    if (this.state.currentPoint && this.state.currentPoint.name === this.props.pointData[point].name) {
      point = null
    }
    this.setState({
      currentPoint: this.props.pointData[point]
    })
  }

  render() {
    const isDesktop = window.innerWidth > desktopSize ? true: false
    return (
      <div className={'c-i-container'}>
        <h1>Campus Food Resources</h1>
        { isDesktop && 
          <div className='c-i-desktop'>
            <Map pointData={this.props.pointData} 
              mapImage={this.props.map}
              currentPoint={this.state.currentPoint}
              selectPoint={(point) => this.selectPoint(point)}/> 
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


