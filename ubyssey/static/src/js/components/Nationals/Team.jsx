import React from 'react'

class Team extends React.Component {
  render() {
    const { team } = this.props
    return (
      <div className = 'c-n-team'>
        <h1>{team.name}</h1>
        {team.content.map((paragraph) => {
          return(<p>{paragraph}</p>)
        })}
      </div>
    )
  }
}

export default Team;