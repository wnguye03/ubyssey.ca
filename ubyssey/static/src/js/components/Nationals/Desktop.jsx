import React from 'react'
import Mvp from './Mvp.jsx'
import TeamContent from './TeamContent.jsx'

class Desktop extends React.Component {
  constructor(props){
    super(props)
  }
  
  render() {
    const {team, isDesktop} = this.props
    return (
      <div className='c-n-content-container'>
        {(team !== null) && 
          <div className='c-n-content'>
            <Mvp player={team.player} 
              primaryColor={team.colors[0]}
              isDesktop={isDesktop}/>
            <TeamContent team={team} isDesktop={isDesktop}/>
          </div>
        }
      </div>
    )
  }
}

export default Desktop


