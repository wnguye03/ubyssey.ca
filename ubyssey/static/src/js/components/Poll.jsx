import React, { Component } from 'react'

class Poll extends Component {
  constructor(props){
    super(props);
    this.state = {
      answers: ['yes', 'no'],
      votes: [0, 0],
      checkedAnswers: [],
    }
  }

  changeAnswers(e, index){
    console.log(index)
    let newCheckedAnswers = this.state.checkedAnswers
    //always remove the index if its checked before click
    if(this.state.checkedAnswers.includes(index)) {
      newCheckedAnswers.splice(this.state.checkedAnswers.indexOf(index), 1)
    }
    //if only one is allowed
    else if(!this.props.many){
      //remove other indexs before adding new index
      newCheckedAnswers = []
      newCheckedAnswers.push(index)      
    }
    //otherwise multiple are allowed, add the index
    else if(this.props.many){
      newCheckedAnswers.push(index)
    }
    this.setState({
      checkedAnswers: newCheckedAnswers
    }, () => {
      if(this.props.many){
        //wait for vote submit
      }else{
        this.onVote();
      }
    })

  }
  onVote() {
    let newVotes = this.state.votes
    for(let i = 0; i < this.state.checkedAnswers.length; i++) {
      newVotes[this.state.checkedAnswers[i]]++;
    }
    this.setState({
      votes: newVotes
    })
  }

  render() {
    return (
      <div>
        <h1>This is a poll</h1>
        <form className={'poll-answer-form'}>
          {this.state.answers.map((answer, index) =>{
            if(this.props.many){
              return (
                <label className='block'>
                  <input className={'poll-button'} 
                    name={answer} 
                    type={'radio'} 
                    value={answer}
                    checked={this.state.checkedAnswers.includes(index)}
                    onChange={(e)=>this.changeAnswers(e, index)}>
                    {answer}
                  </input>
                </label>
              )
            }else{
              return (
                <label className='block'>
                  <input className={'poll-button'} 
                    name={'answer'} 
                    type={'radio'} 
                    value={answer}
                    checked={this.state.checkedAnswers.includes(index)}
                    onChange={(e)=>this.changeAnswers(e, index)}>
                    {answer}
                  </input>
                </label>
              )
            }
          })}
        </form>
      </div>
    );
  }
}

const PollElement = <Poll many={false}/>

React.render(PollElement, document.getElementById("react-poll"))
