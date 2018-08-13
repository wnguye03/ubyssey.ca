import React from 'react';

const COLOR_OPACITY = .8

class PollAnswer extends React.Component {
  constructor(props){
    super(props)
  }
  render(){
    const { index, answer, hasVoted, showResults, checkedAnswers, answerPercentage } = this.props
    const buttonStyle = hasVoted ? 'poll-button-voted': 'poll-button-no-vote'
    const showResult = showResults ? (hasVoted ? COLOR_OPACITY : 0) : 0
    const notShowResult = showResults ? (hasVoted ? 0 : COLOR_OPACITY) : COLOR_OPACITY
    let isSelected = checkedAnswers.includes(index) ? 'poll-selected' : 'poll-not-selected'
    let buttonSelected = checkedAnswers.includes(index) ? 'poll-button-selected' : 'poll-button-not-selected'
    return(
      <label className={['poll-button-label', buttonStyle].join(' ')}>
        <input className={'poll-input'}
          name={'answer'}
          type={'radio'}
          value={answer}
          checked={this.props.checkedAnswers.includes(index)}
          onChange={(e) => this.props.changeAnswers(e, index)}>
            <span className={'poll-answer-text'}>{answer}</span>
            <div className={isSelected}>
              <span className={'poll-checkmark'}></span>
            </div>
        </input>

        <span className={'poll-button'}
          style={{opacity: notShowResult}}>
          <span className={['poll-button-inner', buttonSelected].join(' ')} ></span>
        </span>

        <span className={'poll-percentage'}
          style={{opacity: showResult}}>
          {answerPercentage}
        </span>

        <div className={'poll-result-bar'} style={{width: answerPercentage, opacity: showResult}}>
        </div>
        
      </label>
    )
  }
}

export default PollAnswer;
