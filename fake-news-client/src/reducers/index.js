import { combineReducers } from "redux";
import isFakeNewsReducer from "./postsReducer";

export default combineReducers({
  fakeNews: isFakeNewsReducer
});
