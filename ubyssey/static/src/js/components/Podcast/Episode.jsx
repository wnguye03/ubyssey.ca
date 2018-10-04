import React from 'react'
import DispatchAPI from '../../api/dispatch'

class Episode extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // auto opens the episode when clicked directly
      open: window.location ? window.location.hash.includes(props.slug) : false,
      maxHeight: 1000
    }
  }

  handleClick() {
    // console.log('scroll to ', document.getElementById(this.props.slug).offsetTop)
    // document.getElementById('content-wrapper').scroll({
    //   top: document.getElementById(this.props.slug).offsetTop, 
    //   left: 0, 
    //   behavior: 'smooth' 
    // }); 
    this.setState(prevstate => ({
      open: !prevstate.open,
      maxHeight: document.getElementById(this.props.slug).clientHeight
    }))
  }

  render() {
    const {author, description, file, image, publishedAt, slug, title} = this.props
    const openStyle = this.state.open ? {maxHeight: this.state.maxHeight} : {maxHeight: '150px'}
    return (
      <div className="c-episode-container" style={openStyle}>
        <a name={slug} ></a> 
        <div id={this.props.slug}>
          <div className='c-episode-flex-wrapper-top'>
              <h3 onClick={() => this.handleClick()}>{title}</h3>
              <h4>{publishedAt}</h4>
          </div>
          <div className={this.state.open ? 'c-episode-flex-wrapper-mid-col' : 'c-episode-flex-wrapper-mid-row'}>
              <p className='description'>
                  {description}
              </p>
          </div>
          <div className='c-episode-content'>
            { this.state.open &&  
                <div className='c-episode-flex-wrapper-bottom'>
                  <div className='image' style={{backgroundImage: "url(" + image + ")"}} ></div>
                  <audio controls >
                    <source src={file} />
                  </audio>
                </div>
            } { // dummy objects to maintain same innerHeight
              !this.state.open &&
              <div className='c-episode-flex-wrapper-bottom'>
                <div className='image'/>
                <audio controls>
                </audio>
              </div>
            }
          </div>
        </div>
        <div className='c-episode-obscure' onClick={() => this.handleClick()}>
            <span>Show {this.state.open ? 'Less' : 'More'}</span>
        </div>
      </div>

    )
  }
}

export default Episode
