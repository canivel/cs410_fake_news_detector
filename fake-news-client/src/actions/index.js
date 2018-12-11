import fakeNewsApi from "../apis/fakeNewsCanivel";

export const isFakeNews = formValues => {
  return async dispatch => {
    const response = await fakeNewsApi.post(
      "/isfakenews",
      { ...formValues },
      {
        headers: {
          "Content-Type": "application/json"
        }
      }
    );

    console.log(response);

    dispatch({
      type: "IS_FAKE_NEWS",
      payload: response.data
    });
  };
};
