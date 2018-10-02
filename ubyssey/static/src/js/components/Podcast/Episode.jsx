import React from 'react'
import DispatchAPI from '../../api/dispatch'

class Episode extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: window.location ? window.location.hash.includes(props.title) : false,
      playing: false
    }
  }

  handleClick() {
    this.setState(prevstate => ({
      open: !prevstate.open
    }))
  }

  handlePlayPause(e) {
    console.log(e)
    this.setState(prevstate => ({
      playing: !prevstate.playing
    }))
  }

  render() {
    const {author, description, file, image, publishedAt, title} = this.props
    const openStyle = this.state.open ? {flexDirection: 'column'} : {flexDirection: 'row'}
    return (
      <div className="c-episode-container" >
        <a name={title} ></a> 
        <div onClick={() => this.handleClick()}>
          <div className='c-episode-flex-wrapper-top'>
              <h3>{title}</h3>
              <h4>{publishedAt}</h4>
          </div>
          <div className={this.state.open ? 'c-episode-flex-wrapper-mid-col' : 'c-episode-flex-wrapper-mid-row'}>
              
              <div className='description'>
                  {description}
              </div>
          </div>
        </div>
        <div className='c-episode-obscure'>
          { this.state.open &&  
              <div className='c-episode-flex-wrapper-bottom'>
                <div className='image' style={{backgroundImage: "url(" + image + ")"}} ></div>
                <audio controls >
                  <source src={file} />
                </audio>
              </div>
          } { !this.state.open &&
            <div className='c-episode-flex-wrapper-bottom'>
              <div className='image'/>
              <audio controls>
              </audio>
            </div>
          }
        </div>
      </div>

    )
  }
}

export default Episode
