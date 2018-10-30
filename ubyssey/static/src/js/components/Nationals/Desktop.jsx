import React from 'react'

class Desktop extends React.Component {
  constructor(props){
    super(props)
  }

  render() {
    const {team} = this.props
    console.log(team)
    return (
      <div className='c-nationals-team-container' >
        {(this.props.team !== null) && 
          <div>
            <h1>{team.name}</h1>
            {team.content.map((paragraph) => {
              return(<p>{paragraph}</p>)
            })}
            
            <h3>{team.player.name}</h3>
            <img src={team.player.image.medium}></img>
            {team.player.content.map((paragraph) => {
              return(<p>{paragraph}</p>)
            })}
          </div>
        }
      </div>
    )
  }
}

export default Desktop


