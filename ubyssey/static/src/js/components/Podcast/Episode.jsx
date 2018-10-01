import React from 'react'
import DispatchAPI from '../../api/dispatch'

class Episode extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <audio controls>
        <source src={this.props.file} />
      </audio>
    )
  }
}

export default Episode
