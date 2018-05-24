import React, { Component } from 'react'

class Poll extends Component {
  constructor(props){
    super(props);
    this.state = {
      answers: ['Yes', 'No', 'Maybe'],
      votes: [0, 0, 0],
      checkedAnswers: [],
      hasVoted: false,
    }
  }

  changeAnswers(e, index){
    if(!this.state.hasVoted){

      let deselect = false
      let newCheckedAnswers = this.state.checkedAnswers

      if(this.state.checkedAnswers.includes(index)) {
        newCheckedAnswers.splice(this.state.checkedAnswers.indexOf(index), 1)
        deselect = true
      }

      else if(!this.props.many){
        newCheckedAnswers = []
        newCheckedAnswers.push(index)      
      }

      else if(this.props.many){
        newCheckedAnswers.push(index)
      }

      this.setState({
        checkedAnswers: newCheckedAnswers,
      }, () => {
        if(!deselect){
          if(this.props.many){
            //wait for vote submit
          }else{
            this.onVote();
          }
        }
      })
    }
  }

  onVote() {
    let newVotes = this.state.votes
    for(let i = 0; i < this.state.checkedAnswers.length; i++) {
      newVotes[this.state.checkedAnswers[i]]++;
    }
    this.setState({
      votes: newVotes,
      hasVoted: true
    })
  }

  editVote() {
    this.setState({
      hasVoted: false
    })
  }

  getPollResult(index) {
    let total = this.state.votes.reduce((acc, val) => { return acc + val; })
    let width = String((100*this.state.votes[index]/total).toFixed(0)) + '%'
    return width
  }

  render() {
    const pollStyle = this.state.hasVoted ? 'poll-results' : 'poll-voting'
    const buttonStyle = this.state.hasVoted ? 'poll-button-voted': 'poll-button-no-vote'
    const showResult = this.state.hasVoted ? 1 : 0
    const notShowResult = this.state.hasVoted ? 0 : 1
    return (
      <div className={['poll-container', pollStyle].join(' ')}>
        <h1>This is a poll</h1>
        <form className={'poll-answer-form'}>
          {this.state.answers.map((answer, index) =>{
            if(this.props.many){
              let selected = this.state.checkedAnswers.includes(index) ? 'selected' : ''
              return (
                <label className={['block', buttonStyle].join(' ')}>
                  <input className={['poll-button', selected].join(' ')} 
                    name={answer} 
                    type={'radio'} 
                    value={answer}
                    checked={this.state.checkedAnswers.includes(index)}
                    onChange={(e) => this.changeAnswers(e, index)}>
                    {answer}
                  </input>
                  <div className={'poll-result-bar'} style={{width: this.getPollResult(index)}}> </div>
                </label>
              )
            }else{
              let isSelected = this.state.checkedAnswers.includes(index) ? 'poll-selected' : 'poll-not-selected'
              return (
                <label className={['poll-button-label', buttonStyle].join(' ')}>
                  
                  <input className={'poll-input'} 
                    name={'answer'} 
                    type={'radio'} 
                    value={answer}
                    checked={this.state.checkedAnswers.includes(index)}
                    onChange={(e) => this.changeAnswers(e, index)}>
                      <span className={'poll-answer-text'}>{answer}</span>
                  </input>

                  <span className={'poll-button'}
                    style={{opacity: notShowResult}}>
                    <span className={'poll-button-inner'}></span>
                  </span>

                  <span className={'poll-percentage'}
                    style={{opacity: showResult}}>
                    {this.getPollResult(index)}
                  </span>

                  <div className={'poll-result-bar'} 
                    style={{width: this.getPollResult(index), opacity: showResult}}>
                      <div className={isSelected}>                      
                        <span className={'poll-checkmark'}></span>
                      </div>
                  </div>

                </label>
              )
            }
          })}
        </form>
        {this.state.hasVoted && <button className={'poll-edit-button'} onClick={() => this.editVote()}>Edit Vote</button>}
      </div>
    );
  }
}

const PollElement = <Poll many={false}/>

React.render(PollElement, document.getElementById("react-poll"))
