import React, { Component } from 'react'
import DispatchAPI from '../api/dispatch'

import Cookies from 'js-cookie';
 
const COLOR_OPACITY = .8

class Poll extends Component {
  constructor(props){
    super(props);
    this.state = {
      answers: [],
      answer_ids: [],
      votes: [],
      checkedAnswers: [],
      hasVoted: false,
      pollQuestion: '',
      loading: true,
      totalVotes: 0,
      showResults: false,
      pollOpen: false,
    }
  }

  componentDidMount() {
    //initialize poll with results if user already voted
    console.log('cookie', Cookies.get(this.pollCookie()))
    let answer_id = Number(this.getCookie('answer_id'))
    this.update(answer_id)
  }

  pollCookie() {
    return 'poll_id_' + String(this.props.id)
  }

  getCookie(field){
    let cookie = Cookies.get(this.pollCookie())
    if(typeof cookie === 'string' && cookie !== ''){
      cookie = JSON.parse(cookie)
      return cookie[field]
    }
    return null
  }

  update(answer_id) {
    DispatchAPI.polls.getResults(this.props.id)
      .then((response)=> {
        console.log(response)
        let answers = []
        let votes = []
        let answer_ids = []
        let vote_id = Number(this.getCookie('vote_id'))
        for(let answer of response.answers){
          answers.push(answer['name'])
          votes.push(answer['vote_count'])
          answer_ids.push(answer['id'])
        }
        let totalVotes = votes.reduce((acc, val) => { return acc + val; })
        this.setState({
          answers: answers,
          answer_ids: answer_ids,
          votes: votes,
          vote_id: vote_id,
          pollQuestion: response.question,
          loading: false,
          totalVotes: totalVotes,
          showResults: response.show_results,
          pollOpen: response.is_open
        }, () => {
          if(answer_id){
            let checkedAnswers = this.state.checkedAnswers.concat(this.state.answer_ids.indexOf(answer_id))
            this.setState({
              hasVoted: true,
              checkedAnswers: checkedAnswers
            })
          }
        })
      })
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
      }, () => {
        for(let index of this.state.checkedAnswers){
          let payload = {'answer_id': this.state.answer_ids[index]}
          DispatchAPI.polls.vote(payload).then(response => {
            Cookies.set(this.pollCookie(), {pole_id: this.props.id, vote_id: response.id, answer_id: this.state.answer_ids[index]}, { path: '/' })
            this.update()
          })
        }
      })
  }

  editVote() {
    this.setState({
      hasVoted: false
    })
  }

  getPollResult(index) {
    let total = this.state.votes.reduce((acc, val) => { return acc + val; })
    let width = 0
    if(total !== 0){
      width = String((100*this.state.votes[index]/total).toFixed(0)) + '%'
    }
    return width
  }

  render() {
    const pollStyle = this.state.hasVoted ? 'poll-results' : 'poll-voting'
    const buttonStyle = this.state.hasVoted ? 'poll-button-voted': 'poll-button-no-vote'
    const showResult = this.state.showResults ? (this.state.hasVoted ? COLOR_OPACITY : 0) : 0
    const notShowResult = this.state.showResults ? (this.state.hasVoted ? 0 : COLOR_OPACITY) : COLOR_OPACITY
    return (
      <div>
        {!this.state.loading && 
          <div className={['poll-container', pollStyle].join(' ')}>
          <h1>{this.state.pollQuestion}</h1>
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
                let buttonSelected = this.state.checkedAnswers.includes(index) ? 'poll-button-selected' : 'poll-button-not-selected'
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
                      <span className={['poll-button-inner', buttonSelected].join(' ')} ></span>
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
          { (this.state.hasVoted && this.state.showResults) &&
            <div>
              <i style={{position: 'relative', top: '-5px'}}>Total Votes: {this.state.totalVotes}</i>
              <br/>
              <button className={'poll-edit-button'} onClick={() => this.editVote()}>Change Vote</button>
            </div>
          }
          { (this.state.hasVoted && !this.state.showResults) && 
            <div>
              <p>Poll results hidden from public</p>
              <h3>Thank you for your opinion</h3>
            </div>
          }
          { !this.state.pollOpen &&
            <h3>This poll is currently closed</h3>
          }
        </div>
        }
        {this.state.loading && 'Loading Poll...'}
      </div>
    );
  }
}

export default Poll
