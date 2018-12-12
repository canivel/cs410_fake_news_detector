import React, { Component } from "react";
import { Field, reduxForm } from "redux-form";

class FakeNewsForm extends Component {
  renderError({ error, touched }) {
    if (touched && error) {
      return (
        <div className="ui error message">
          <div className="header">{error}</div>
        </div>
      );
    }
  }

  renderInput = formProps => {
    const className = `field ${
      formProps.meta.error && formProps.meta.touched ? "error" : ""
    }`;
    return (
      // <input
      //   onChange={formProps.input.onChange}
      //   value={formProps.input.value}
      // />
      //same thing as above
      <div className={className}>
        <label>{formProps.label}</label>
        <input {...formProps.input} />
        {this.renderError(formProps.meta)}
      </div>
    );
  };

  renderTextArea = ({ input, label, meta }) => {
    const className = `field ${meta.error && meta.touched ? "error" : ""}`;
    return (
      <div className={className}>
        <label>{label}</label>
        <textarea {...input} />
        {this.renderError(meta)}
      </div>
    );
  };

  onSubmitNews = formValues => {
    this.props.onSubmit(formValues);
    //return dispatch(isFakeNews(formValues.title, formValues.author, formValues.text));
  };

  render() {
    return (
      <form
        className="ui form"
        onSubmit={this.props.handleSubmit(this.onSubmitNews)}
        className="ui form error"
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
    );
  }
}

const validate = formValues => {
  const errors = {};

  if (!formValues.author) {
    errors.author = "You must enter a author";
  }

  if (!formValues.title) {
    errors.title = "You must enter a title";
  }

  if (!formValues.text) {
    errors.text = "You must enter a news text ...";
  }

  return errors;
};

export default reduxForm({
  form: "fakeNews", // a unique identifier for this form
  validate
})(FakeNewsForm);
