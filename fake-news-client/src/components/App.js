import React, { Component } from "react";
import FakeNewsEvaluate from "./FakeNewsEvaluate";

export class App extends Component {
  render() {
    return (
      <div className="ui container">
        <h1>Fake News Realiability Rating</h1>
        <FakeNewsEvaluate />
      </div>
    );
  }
}

export default App;
