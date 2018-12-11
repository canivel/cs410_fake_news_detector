import React, { Component } from "react";
import FakeNewsEvaluate from "./FakeNewsEvaluate";

export class App extends Component {
  render() {
    return (
      <div className="ui container">
        <div
          className="middle align row"
          style={{ marginTop: "30px", textAlign: "center" }}
        >
          <h1>Fake News Realiability Rating</h1>
          <FakeNewsEvaluate />
        </div>
      </div>
    );
  }
}

export default App;
