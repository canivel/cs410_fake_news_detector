import React from "react";
import { connect } from "react-redux";
import { isFakeNews } from "../actions";
import FakeNewsForm from "./FakeNewsForm";

class FakeNewsEvaluate extends React.Component {
  onSubmit = formValues => {
    this.props.isFakeNews(formValues);
  };

  renderResult() {
    if (!this.props.fakeness.fakeNews.prediction) {
      return "Wainting for news...";
    } else {
      return (
        <div>
          <h2>{this.props.fakeness.fakeNews.prediction}</h2>
          <h2>{this.props.fakeness.fakeNews.fake_rate}</h2>
        </div>
      );
    }
  }

  render() {
    return (
      <div className="ui segment">
        <div className="ui two column stackable center aligned grid">
          <div className="ui vertical divider">IS</div>
          <div className="middle aligned row">
            <div className="left column">
              <h3>Evaluate News</h3>
              <FakeNewsForm onSubmit={this.onSubmit} />
            </div>
            <div className="column">
              <div>{this.renderResult()}</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = state => {
  return { fakeness: state };
};

export default connect(
  mapStateToProps,
  { isFakeNews }
)(FakeNewsEvaluate);
