export default (state = [], action) => {
  switch (action.type) {
    case "IS_FAKE_NEWS":
      return action.payload;
    default:
      return state;
  }
};
