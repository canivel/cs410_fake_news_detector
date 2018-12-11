import React from "react";
import { connect } from "react-redux";
import { isFakeNews } from "../actions";
import FakeNewsForm from "./FakeNewsForm";

class FakeNewsEvaluate extends React.Component {
  onSubmit = formValues => {
    this.props.isFakeNews(formValues);
  };

  render() {
    return (
      <div>
        <h3>Evaluate News</h3>
        <FakeNewsForm onSubmit={this.onSubmit} />
      </div>
    );
  }
}

export default connect(
  null,
  { isFakeNews }
)(FakeNewsEvaluate);
