import React from 'react'
import Mvp from './Mvp.jsx'
import TeamContent from './TeamContent.jsx'

class Desktop extends React.Component {
  constructor(props){
    super(props)
  }
  
  render() {
    // const {team, isDesktop} = this.props
    // return (
    //   <div className='c-n-content-container'>
    //     {(team !== null) && 
    //       <div className='c-n-content'>
    //         <Mvp player={team.player} 
    //           primaryColor={team.colors[0]}
    //           isDesktop={isDesktop}/>
    //         <TeamContent team={team} isDesktop={isDesktop}/>
    //       </div>
    //     }
    //   </div>
    // )
    const {teamData, isDesktop, selectedTeam} = this.props
    
    return (
      <div>
        {teamData.map((team) => {
          const isSelected = selectedTeam ? selectedTeam.name === team.name: selectedTeam
          return(
            <div className='c-n-content-container'>
              <div className='c-n-content'>
                <Mvp player={team.player} 
                  primaryColor={team.colors[0]}
                  isDesktop={isDesktop}
                  isSelected={isSelected}/>
                <TeamContent team={team} 
                  isDesktop={isDesktop}
                  isSelected={isSelected}/>
              </div>
            </div>
          )

        })}
      </div>

    )
  }
}

export default Desktop


