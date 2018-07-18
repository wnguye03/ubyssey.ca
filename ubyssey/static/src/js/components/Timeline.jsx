import React, { Component } from 'react'

const desktopSize = 960;

class Timeline extends Component {
  constructor(props){
    super(props)
    this.state = {
      selectedNode: props.id,
      nodes: props.nodes.map((node)=>{
        console.log(node)
        return [node[0], JSON.parse(node[1])]
      }),
    }
  }

  renderNode(node, index) {
    // const data = this.getArticleData(node[0])
    let date = new Date(Date.parse(node[1].timeline_date))
    const dateStyle = window.innerWidth > desktopSize ? index % 2 === 0 ? {top:'-20px'} : {top: '20px'}: {top: '-2px'};

    return (
      <div className='timeline-node'>
        {this.state.selectedNode === node[0] && <div className='timeline-node-solid'></div>}
        <div className='timeline-node-hover'>
          <div className='timeline-node-solid--small'></div>
          <div className='timeline-node-info'>
            {node[1].description}
          </div>
        </div>
        <div className='timeline-node-date' style={dateStyle}>{date.toDateString().slice(4)}</div>
      </div>
    )
  }

  render() {
    const mobileStyle = {
      width: window.innerWidth > desktopSize ? window.innerWidth: window.innerWidth*.3, 
      marginLeft: window.innerWidth > desktopSize ? 0: window.innerWidth*.7,
      height: window.innerWidth > desktopSize ? 80: window.innerHeight - 54
    }
    return (
      <div className='timeline-container' style={mobileStyle}>
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
