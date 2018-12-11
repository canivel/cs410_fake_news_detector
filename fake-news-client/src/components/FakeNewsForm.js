import React, { Component } from "react";
import { Field, reduxForm } from "redux-form";

class FakeNewsForm extends Component {
  renderInput(formProps) {
    return (
      // <input
      //   onChange={formProps.input.onChange}
      //   value={formProps.input.value}
      // />
      //same thing as above
      <div className="field">
        <label>{formProps.label}</label>
        <input {...formProps.input} />
      </div>
    );
  }

  renderTextArea({ input, label }) {
    return (
      <div className="field">
        <label>{label}</label>
        <textarea {...input} />
      </div>
    );
  }

  onSubmitNews = formValues => {
    this.props.onSubmit(formValues);
    //return dispatch(isFakeNews(formValues.title, formValues.author, formValues.text));
  };

  render() {
    return (
      <div className="ui segment">
        <form
          className="ui form"
          onSubmit={this.props.handleSubmit(this.onSubmitNews)}
        >
          <Field
            name="author"
            component={this.renderInput}
            label="Enter Author"
            type="text"
          />
          <Field
            name="title"
            component={this.renderInput}
            label="Enter Title"
            type="text"
          />
          <Field
            name="text"
            component={this.renderTextArea}
            label="Enter News Body"
            type="textarea"
          />
          <button className="ui button primary">Evaluate News</button>
        </form>
      </div>
    );
  }
}

export default reduxForm({
  form: "fakeNews" // a unique identifier for this form
})(FakeNewsForm);
