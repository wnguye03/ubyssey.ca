import React, { Component } from 'react'
import DispatchAPI from '../api/dispatch'

import Cookies from 'js-cookie'
import PollAnswer from './PollAnswer.jsx'

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
    let init = true
    let answer_id = Number(this.getCookie('answer_id'))
    this.update(init, answer_id)
  }

  getCookieName() {
    return 'poll_id_' + String(this.props.id)
  }

  getCookie(field){
    let cookie = Cookies.get(this.getCookieName())
    if(typeof cookie === 'string' && cookie !== ''){
      cookie = JSON.parse(cookie)
      if(field){
        return cookie[field]
      }
      return cookie
    }
    return cookie
  }

  setCookie(vote_id, answer_id){
    console.log(vote_id, answer_id)
    Cookies.set(
      this.getCookieName(),
      {pole_id: this.props.id, vote_id: vote_id, answer_id: answer_id},
      { path: '/' }
    )
  }

  update(init, answer_id) {
    DispatchAPI.polls.getResults(this.props.id)
      .then((response)=> {
        console.log(response.answers)
        let answers = []
        let votes = []
        let answer_ids = []
        let vote_id = this.getCookie('vote_id')

        for(let answer of response.answers){
          answers.push(answer['name'])
          votes.push(answer['vote_count'])
          answer_ids.push(answer['id'])
        }

        if(init){
          // if the cookie or the answer_id is not set
          let cookie = this.getCookie()
          if(!cookie || !cookie.answer_id){
            this.setCookie(vote_id, answer_ids[0])
          }
        }

        let totalVotes = response.total_votes
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
    console.log(e, index)
    if(!this.state.hasVoted){
      let deselect = false
      let newCheckedAnswers = this.state.checkedAnswers

      if(this.state.checkedAnswers.includes(index)) {
        newCheckedAnswers.splice(this.state.checkedAnswers.indexOf(index), 1)
        deselect = true
      }

      if(!this.props.many){
        newCheckedAnswers = []
        newCheckedAnswers.push(index)
      }

      else if(this.props.many){
        newCheckedAnswers.push(index)
      }

      this.setState({
        checkedAnswers: newCheckedAnswers,
        hasVoted: true
      }, () => {
        if(!deselect){
          if(this.props.many){
            //wait for vote submit
          }else{
            console.log(this.state.checkedAnswers)
            this.onVote();
          }
        }
      })
    }
  }

  onVote() {
      for(let index of this.state.checkedAnswers){
        let payload = {poll_id: this.props.id, vote_id: this.state.vote_id, answer_id: this.state.answer_ids[this.state.checkedAnswers[0]]}
        console.log(this.state.answer_ids[index])
        DispatchAPI.polls.vote(payload).then(response => {
          this.setCookie(response.id, this.state.answer_ids[index])
          this.update()
        })
      }
  }

  editVote() {
    this.setState({
      hasVoted: false
    })
  }

  getPollResult(index) {
    if(this.state.showResults){
      let width = 0
      if(this.state.totalVotes !== 0){
        width = String((100*this.state.votes[index]/this.state.totalVotes).toFixed(0)) + '%'
      }
      return width
    }
  }

  render() {
    const { answers, checkedAnswers, hasVoted, pollQuestion,
      loading, totalVotes, showResults, pollOpen} = this.state

    const pollStyle = hasVoted ? 'poll-results' : 'poll-voting'
    const buttonStyle = hasVoted ? 'poll-button-voted': 'poll-button-no-vote'
    const showResult = showResults ? (hasVoted ? COLOR_OPACITY : 0) : 0
    const notShowResult = showResults ? (hasVoted ? 0 : COLOR_OPACITY) : COLOR_OPACITY
    return (
      <div>
        {!loading &&
          <div className={['poll-container', pollStyle].join(' ')}>
          <h1>{pollQuestion}</h1>
          <form className={'poll-answer-form'}>
            {answers.map((answer, index) =>{
              // if(this.props.many){
              //   let selected = checkedAnswers.includes(index) ? 'selected' : ''
              //   return (
              //     <label className={['block', buttonStyle].join(' ')}>
              //       <input className={['poll-button', selected].join(' ')}
              //         name={answer}
              //         type={'radio'}
              //         value={answer}
              //         checked={checkedAnswers.includes(index)}
              //         onChange={(e) => this.changeAnswers(e, index)}>
              //         {answer}
              //       </input>
              //       <div className={'poll-result-bar'} style={{width: this.getPollResult(index)}}> </div>
              //     </label>
              //   )
              // }else{
                let isSelected = checkedAnswers.includes(index) ? 'poll-selected' : 'poll-not-selected'
                let buttonSelected = checkedAnswers.includes(index) ? 'poll-button-selected' : 'poll-button-not-selected'
                let answerPercentage = this.getPollResult(index)
                return (
                  <PollAnswer
                    key={answer}
                    index={index}
                    answer={answer}
                    hasVoted={hasVoted}
                    showResults={showResults}
                    checkedAnswers={checkedAnswers}
                    answerPercentage={answerPercentage}
                    changeAnswers={(e) => this.changeAnswers(e, index)}
                    />
                )
            })}
          </form>
          { (hasVoted && showResults) &&
            <div>
              <i style={{position: 'relative', top: '-5px'}}>Total Votes: {totalVotes}</i>
              <br/>
              <button className={'poll-edit-button'} onClick={() => this.editVote()}>Change Vote</button>
            </div>
          }
          { (hasVoted && !showResults) &&
            <div>
              <p>Poll results hidden from public</p>
              <h3>Thank you for your opinion</h3>
            </div>
          }
          { !pollOpen &&
            <h3>This poll is currently closed</h3>
          }
        </div>
        }
        {loading && 'Loading Poll...'}
      </div>
    );
  }
}

export default Poll
