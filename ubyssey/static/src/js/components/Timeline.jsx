import React, { Component } from 'react'
// import ReactDOM from 'react-dom'

const desktopSize = 960;

class Timeline extends Component {
  constructor(props){
    super(props)
    this.state = {
      selectedNodeId: props.id,
      selectedNodeIndex: 0,
      nodes: props.nodes.map((node)=>{
        return {'headline': node.headline, 'id': node.parent_id, 'slug': node.slug, 'template_data': JSON.parse(node.template_data), 'featured_image': node.featured_image}
      }),
      isMobile: false,
      mobileShow: false,
      loaded: false,
      openNode: -1,
    }
  }

  componentDidMount() {
    // console.log(ReactDOM.findDOMNode(this.refs.myRef))
    const isMobile = window.innerWidth < desktopSize
    this.state.nodes.map((node, index) => {
      if (node.id === this.props.id) {
        this.setState({
          selectedNodeIndex: index,
          isMobile: isMobile,
          loaded: true
        })
      }
    })
  }

  mobileHandle() {
    this.setState(prevState => ({
      mobileShow: !prevState.mobileShow
    }))
  }

  prepareHeadline (headline) {
    if (headline) {
      return headline.length > 35 ? headline.slice(0, 32).concat('...') : headline
    }
    return ''
  }

  prepareDescription(description) {
    if (description) {
      if (description.length > 250) {
        return description.slice(0, 250).concat('...')
      } else {
        return description
      }
    } else {
      return ''
    }
  }

  prepareUrl(slug) {
    
    return window.location.origin + window.location.pathname.replace(this.state.nodes[this.state.selectedNodeIndex].slug, slug)
  }

  renderButton(slug) {
    const mobileStyle = this.state.isMobile ? {left: '-35px'}: {alignSelf: 'flex-end'}
    return (
      <div style={mobileStyle}>
        <a href={this.prepareUrl(slug)}>
          <div className='c-button c-button--small'>
            Read More
          </div>
        </a>
      </div>
    )
  }

  renderDesktopNode(node, index) {
    const date = new Date(Date.parse(node.template_data.timeline_date))
    const dateStyle = index % 2 === 0 ? {top:'-20px'} : {top: '26px'}
    const timelineNodeStyle = this.state.selectedNodeId === node.id ? 't-node-container t-node-selected': 't-node-container'
    
    return (
      <div className={timelineNodeStyle}>
        
        <div ref='myRef' className='t-node'>{ this.state.selectedNodeId === node.id && <div className='t-node-solid'></div>}</div>
        <div className='t-node-hover'>
          <div className='t-node-info'> 
            <div className='t-node-info-text' style={{right: index == this.state.nodes.length - 1 ? 0: 'auto'}}>
              <div className='t-node-info-carret'> </div>
              <h3 className='o-headline'>{node.headline}</h3>
              {this.prepareDescription(node.template_data.description)}
              {this.renderButton(node.slug)}
            </div>
          </div>
        </div>
        <div className='t-node-date' style={dateStyle}>{date.toDateString().slice(4).replace(' 0', ' ')}</div>
      </div>
    )
  }

  renderMobileNode(node, index) {
    const date = new Date(Date.parse(node.template_data.timeline_date))
    const timelineNodeStyle = this.state.selectedNodeId === node.id ? 't-node-container t-node-selected': 't-node-container'
    // const backgroundColor = index % 2 === 0 ? 'rgba(255, 255, 255, .9)' : 'rgba(255, 255, 255, 1)'
    const color = index % 2 === 0 ? 'black': 'black'

    // const isClicked = this.state.openNode === index ? {height: '100px', display: 'block'} : {height: 0, display: 'none'}
    return (
      <div className={timelineNodeStyle}
        onClick={() => { console.log(index); this.setState(prevState => ({openNode: prevState.openNode !== index ? index: -1}))}}
        // style={{backgroundColor: backgroundColor, color: color}}
        >
        <div className='t-node-mobile-box'>
          <div className='t-node-date' >{date.toDateString().slice(4)}</div>
          <div className='t-node-info'>
            <h3 className='o-headline'>{node.headline}</h3>
          </div>
        </div>
        <div className='t-node-mobile-box'>
          <div style={{width: '100%', height: '100%', backgroundImage: 'url(' + node.featured_image + ')', backgroundSize: 'cover'}}/>
        </div>
        <div className='t-node-mobile-box'>
          <a href={this.prepareUrl(node.slug)}><span>Read More</span></a>
        </div>
      </div>
    )
  }

  render() {
    const winWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    const winHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    const mobileStyle = {
      width: winWidth, 
      overflow: this.state.mobileShow ? 'scroll': 'visible',
      marginTop: (this.state.isMobile ? (this.state.mobileShow ? 0 : winHeight-54-54) : 0),
      height: this.state.isMobile ? window.innerHeight - 54 : 80
    }
    return (
      <div style={{width: '100%'}}>
        {this.state.loaded && 
          <div className='t-container' style={mobileStyle} >
            <div className='t-title' onClick={() => {this.mobileHandle(window.innerWidth)}} >
              { this.state.isMobile && 
                <i className="fa fa-bars" style={{fontSize: '20px', padding: '0 25px'}}></i>
              }
              <h1 className='o-headline'>The Galloway Case {this.state.isMobile && 'Timeline'}</h1>
            </div>
            <div className='t-tree-container'>
              {!this.state.isMobile && <div className='t-tree-branch'/>}
              {!this.state.isMobile && 
                <div className='t-tree'>
                  {this.state.nodes.map((node, index) => {
                    return this.renderDesktopNode(node, index)
                  })}
                </div>
              }
              {this.state.isMobile && 
                this.state.nodes.map((node, index) => {
                  return this.renderMobileNode(node, index)
                })
              }
            </div>
          </div>}
      </div>
    )
  }
}

export default Timeline
