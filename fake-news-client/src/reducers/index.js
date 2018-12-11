import { combineReducers } from "redux";
import { reducer as formReducer } from "redux-form";
import isFakeNewsReducer from "./isFakeNewsReducer";

export default combineReducers({
  fakeNews: isFakeNewsReducer,
  form: formReducer
});
