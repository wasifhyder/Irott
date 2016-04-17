(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);throw new Error("Cannot find module '"+o+"'")}var f=n[o]={exports:{}};t[o][0].call(f.exports,function(e){var n=t[o][1][e];return s(n?n:e)},f,f.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){


var App = React.createClass({displayName: "App",
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
     React.createElement("div", null, 
       React.createElement(Questions, {questionDatum: questionDatum}), 
       React.createElement(AnswerList, {answers: questionDatum.answers, answerCallback: this.checkAnswer}), 
       React.createElement(Score, {score: this.state.score}), 
       React.createElement(Progress, {progress: this.state.progress})
     )
    );
    } else {
      return (
        React.createElement("div", null, 
          React.createElement("p", null, "Quiz Finished!"), 
          React.createElement("span", null, "Your ", React.createElement(Score, {score: this.state.score})), 
          React.createElement("button", {type: "button", onClick: this.resetQuiz}, "Reset Quiz")
        )
      );
    }
  }
});

var Score = React.createClass({displayName: "Score",
  render: function() {
    return (
      React.createElement("span", null, "Score: ", this.props.score)
    )
  }
});

var Progress = React.createClass({displayName: "Progress",
  render: function() {
    return (
      React.createElement("p", null, "Question ", this.props.progress + 1)
    )
  }
});

var Questions = React.createClass({displayName: "Questions",
  render: function() {
    return (
      React.createElement("p", null, this.props.questionDatum.prompt)
    )
  }
});

var AnswerList = React.createClass({displayName: "AnswerList",
  render: function() {
    return (
      React.createElement("ul", null, 
        this.props.answers.map(function(answer, index) {
         return (
          React.createElement(ListItem, {answerItem: answer, answerCallback: this.props.answerCallback, index: index})
         )
        },this)
      )
    );
  }
});

var ListItem = React.createClass({displayName: "ListItem",
  onClickAnswer: function() {
    this.props.answerCallback(this.props.index);
  },
  render: function() {
    return (
      React.createElement("li", {onClick: this.onClickAnswer}, this.props.answerItem)
    );
  }
});
ReactDOM.render(
  React.createElement(App, null),
  document.getElementById("app")
);

},{}]},{},[1])