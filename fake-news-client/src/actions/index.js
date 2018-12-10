import fakeNewsApi from "../apis/fakeNewsCanivel";

export const isFakeNews = (title, author, text) => {
  return async dispatch => {
    const response = await fakeNewsApi.post(
      "/isfakenews",
      {
        title: title,
        author: author,
        text: text
      },
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      }
    );

    dispatch({
      type: "IS_FAKE_NEWS",
      payload: response.data
    });
  };
};
