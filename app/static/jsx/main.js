

var App = React.createClass({
  getInitialState: function() {
    return {
      questionData: [{prompt: q.prompt, answers: ["a","b","c","d"], correct: 2}, {prompt: "Question 2", answers: ["a","b","c","d"], correct: 0}],
      progress: 0,
      score: 0
    };
  },
  checkAnswer: function(index) {
    var correct = this.state.questionData[this.state.progress].correct;
    var newScore = 0, newProgress = 0;
    if (correct === index) {
      newScore = this.state.score + 1;
      this.setState({score: newScore});
      newProgress = this.state.progress + 1;
      this.setState({progress: newProgress});
    } else {
      newProgress = this.state.progress + 1;
      this.setState({progress: newProgress});
    }
  },
  resetQuiz: function() {
    this.setState({score: 0, progress: 0});
  },
  render: function() {
    var questionDatum = this.state.questionData[this.state.progress];
    if(this.state.questionData.length > this.state.progress) {
    return (
     <div>
       <Questions questionDatum={questionDatum} />
       <AnswerList answers={questionDatum.answers} answerCallback={this.checkAnswer} />
       <Score score={this.state.score} />
       <Progress progress={this.state.progress} />
     </div>
    );
    } else {
      return (
        <div>
          <p>Quiz Finished!</p>
          <span>Your <Score score={this.state.score} /></span>
          <button type="button" onClick={this.resetQuiz}>Reset Quiz</button>
        </div>
      );
    }
  }
});

var Score = React.createClass({
  render: function() {
    return (
      <span>Score: {this.props.score}</span>
    )
  }
});

var Progress = React.createClass({
  render: function() {
    return (
      <p>Question {this.props.progress + 1}</p>
    )
  }
});

var Questions = React.createClass({
  render: function() {
    return (
      <p>{this.props.questionDatum.prompt}</p>
    )
  }
});

var AnswerList = React.createClass({
  render: function() {
    return (
      <ul>
        {this.props.answers.map(function(answer, index) {
         return (
          <ListItem answerItem={answer} answerCallback={this.props.answerCallback} index={index} />
         )
        },this)}
      </ul>
    );
  }
});

var ListItem = React.createClass({
  onClickAnswer: function() {
    this.props.answerCallback(this.props.index);
  },
  render: function() {
    return (
      <li onClick={this.onClickAnswer}>{this.props.answerItem}</li>
    );
  }
});
ReactDOM.render(
  <App />,
  document.getElementById("app")
);