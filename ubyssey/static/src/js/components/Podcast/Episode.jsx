import React from 'react'
import DispatchAPI from '../../api/dispatch'

class Episode extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open:false,
    }
  }

  componentDidMount() {
    console.log(React.version)
  }

  handleClick() {
    this.setState(prevstate => ({
      open: !prevstate.open
    }))
  }

  render() {
    return (
      <div className="c-podcast-audio" >
        <div className="c-podcast-dropdown-button" onClick={() => this.handleClick()}>
          <i className="fa fa-caret-down"></i>
        </div>
        {this.state.open &&       
          <audio controls>
            <source src={this.props.file} />
          </audio>
        }
      </div>
    )
  }
}

export default Episode
