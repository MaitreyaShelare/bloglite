import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    Authenticated: false,
    token: null,
  },
  getters: {
    getToken(state) {
      return state.token;
    },
    getAuthentication(state) {
      return state.Authenticated;
    },
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
    },
    loginUser(state) {
      state.Authenticated = true;
    },
    logoutUser(state) {
      state.Authenticated = false;
      state.token = null;
    },
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState()],
});
