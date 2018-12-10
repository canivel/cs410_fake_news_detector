import React, { Component } from "react";
import { connect } from "react-redux";

class FakeNewsForm extends Component {
  onSubmitSearch = event => {
    event.preventDefault();
  };

  render() {
    return (
      <div className="ui segment">
        <form className="ui form" onSubmit={this.onSubmitSearch}>
          <div className="field">
            <label>Evaluate News</label>
            <input
              type="text"
              value={this.state.term}
              onChange={e => this.setState({ term: e.target.value })}
            />
          </div>
        </form>
        <div>{this.state.term}</div>
      </div>
    );
  }
}

export default SearchBar;
