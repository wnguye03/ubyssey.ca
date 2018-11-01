import React from 'react'
import Mvp from './Mvp.jsx'
import Team from './Team.jsx'

class Desktop extends React.Component {
  constructor(props){
    super(props)
  }

  render() {
    const {team} = this.props
    console.log(team)
    return (
      <div  >
        {(this.props.team !== null) && 
          <div className='c-n-content'>
            <Mvp player={team.player} />
            <Team team={team} />
          </div>
        }
      </div>
    )
  }
}

export default Desktop


