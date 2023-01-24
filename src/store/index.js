import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    Authenticated: false,
    token: null,
    refreshtoken: null,
    baseURL: "http://127.0.0.1:5000",
  },
  getters: {
    getToken(state) {
      return state.token;
    },
    getRefreshToken(state) {
      return state.refreshtoken;
    },
    getAuthentication(state) {
      return state.Authenticated;
    },
    getBaseURL(state) {
      return state.baseURL;
    },
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setRefreshToken(state, token) {
      state.refreshtoken = token;
    },
    loginUser(state) {
      state.Authenticated = true;
    },
    logoutUser(state) {
      state.Authenticated = false;
      state.token = null;
      state.refreshtoken = null;
    },
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState()],
});
