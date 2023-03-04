import {post} from "./_api";


export const postMessage = async (message) => {
  const payload = {message: message};
  try {
    return await post("/chat", payload);;
  } catch (err) {
    console.error(err);
  }
};