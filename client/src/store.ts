import { createStore } from 'vuex'
import VuexPersist from "vuex-persist";

const vuexPersist = new VuexPersist({
  key: "Admin",
  storage: localStorage,
});

// Create a new store instance.
export default createStore({
  state () {
    return {
      count: 0,
      auth: {
        user: null,
        token: null,
      },
    }
  },
  mutations: {
    // auth
    setToken(state:any, token) {
      state.auth.token = token;
    },
    clearToken(state) {
      state.auth.token = null;
    },
    // user
    setUser(state, user) {
      state.auth.user = user;
    },
    clearUser(state) {
      state.auth.user = null;
    },
  },
  getters: {
    token: (state) => {
      return state.auth.token;
    },
    user: (state) => {
      return state.auth.user;
    },
  },
  plugins: [vuexPersist.plugin],
})