import Vue from 'vue'
import Vuex from 'vuex'
const str = window.localStorage

Vue.use(Vuex);  

const state={
        year : 2019
    }

const store = new Vuex.Store({
    state,
    mutations: {
        increment (state, payload) {
           state.year = payload.amount
    }
  }
})
export default store;
