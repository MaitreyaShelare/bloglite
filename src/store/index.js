import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    Authenticated: false,
    token: null,
    refreshtoken: null,
    currentUserID: null,
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
    getCurrentUserID(state) {
      return state.currentUserID;
    },
    getBaseURL(state) {
      return state.baseURL;
    },
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    setRefreshToken(state, refreshtoken) {
      state.refreshtoken = refreshtoken;
    },
    setCurrentUserID(state, id) {
      state.currentUserID = id;
    },
    loginUser(state) {
      state.Authenticated = true;
    },
    logoutUser(state) {
      state.Authenticated = false;
      state.token = null;
      state.refreshtoken = null;
      state.currentUserID = null;
    },
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState()],
});
