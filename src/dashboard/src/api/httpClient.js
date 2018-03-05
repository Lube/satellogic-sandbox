import axios from "axios";

const CLIENT_DEFAULTS = {
  baseURL: "http://localhost:5000",
  timeout: 6000
};

export default axios.create(CLIENT_DEFAULTS);
