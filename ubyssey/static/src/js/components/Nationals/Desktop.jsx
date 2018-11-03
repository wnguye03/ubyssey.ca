import React from 'react'
import Mvp from './Mvp.jsx'

class Desktop extends React.Component {
  constructor(props){
    super(props)
  }

  render() {
    const {team} = this.props
    return (
      <div className='c-n-content-container'>
        {(team !== null) && 
          <div className='c-n-content'>
            <Mvp player={team.player} primaryColor={team.colors[0]}/>
            <div className = 'c-n-team'>
              <h1>{team.name}</h1>
              {team.content.map((paragraph) => {
                return(<p>{paragraph}</p>)
              })}
            </div>
          </div>
        }
      </div>
    )
  }
}

export default Desktop


