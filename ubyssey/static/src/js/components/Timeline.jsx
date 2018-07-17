import React, { Component } from 'react'

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

  componentDidMount() {

  }


  renderNode(node) {
    // const data = this.getArticleData(node[0])
    let date = new Date(Date.parse(node[1].timeline_date))
    return (
      <div className='timeline-node'>
        {this.state.selectedNode === node[0] && <div className='timeline-node-solid'></div>}
        <div className='timeline-node-hover'>
          <div className='timeline-node-solid--small'></div>
          <div className='timeline-node-info'>
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
          </div>
        </div>
        <div className='timeline-node-date'>{date.toDateString()}</div>
      </div>
    )
  }

  render() {
    return (
      <div className='timeline-container'>
        <h1 class='o-headline'>The Galloway Case</h1>
        <div className='timeline-tree'>
          {this.state.nodes.map((node) => {
            return this.renderNode(node)
          })}
        </div>

      </div>
    )
  }
}

export default Timeline
