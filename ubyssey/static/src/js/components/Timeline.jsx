import React, { Component } from 'react'

const desktopSize = 960;

class Timeline extends Component {
  constructor(props){
    super(props)
    this.state = {
      selectedNodeId: props.id,
      selectedNodeIndex: 0,
      nodes: props.nodes.map((node)=>{
        return {'headline': node.headline, 'id': node.parent_id, 'slug': node.slug, 'template_data': JSON.parse(node.template_data)}
      }),
      mobileShow: false,
    }
  }

  componentDidMount() {
    this.state.nodes.map((node, index) => {
      if (node.id === this.props.id) {
        this.setState({
          selectedNodeIndex: index
        })
      }
    })
  }

  mobileHandle() {
    this.setState(prevState => ({
      mobileShow: !prevState.mobileShow
    }))
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

  renderNode(node, index) {
    const date = new Date(Date.parse(node.template_data.timeline_date))
    const dateStyle = window.innerWidth > desktopSize ? index % 2 === 0 ? {top:'-22px'} : {top: '22px'}: {top: '-2px', 'left': '35px'}
    const timelineNodeStyle = this.state.selectedNodeId === node.id ? 'timeline-node timeline-node-selected': 'timeline-node'
    
    return (
      <div className={timelineNodeStyle}>
        {this.state.selectedNodeId === node.id && <div className='timeline-node-solid'></div>}
        
        <div className='timeline-node-hover'>
          <div className='timeline-node-info'> 
            <div className='timeline-node-bar'></div>
            <svg className='timeline-svg' >
              <path className="timeline-svg-path" d="M 231 0 H 250 V 200 H 0 V 0 L 231 0 "/>
            </svg>
            <div className='timeline-node-info-text'>
              <h3 className='o-headline'>{node.headline}</h3>
              {this.prepareDescription(node.template_data.description)}
              <div style={{alignSelf: 'flex-end'}}><a href={this.prepareUrl(node.slug)}><div className='c-button c-button--small'>Go to article</div></a></div>
            </div>
          </div>
        </div>
        <div className='timeline-node-date' style={dateStyle}>{date.toDateString().slice(4)}</div>
      </div>
    )
  }

  render() {
    console.log(window.innerWidth)
    const winSize = window.innerWidth
    const mobileStyle = {
      width: (winSize > desktopSize ? winSize: 140), 
      marginLeft: (winSize > desktopSize ? 0: (this.state.mobileShow ? winSize - 140: winSize)),
      height: winSize > desktopSize ? 80: window.innerHeight - 54
    }
    return (
      <div className='timeline-container' 
        onClick={() => {this.mobileHandle(window.innerWidth)}} 
        style={mobileStyle}
        ref={'mobileRef'}>
        <h1 className='o-headline'>The Galloway Case</h1>
        <div className='timeline-tree-container'>
          <div className='timeline-tree'>
            {this.state.nodes.map((node, index) => {
              return this.renderNode(node, index)
            })}
          </div>
        </div>
      </div>
    )
  }
}

export default Timeline
