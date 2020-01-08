import Vue from 'vue'
import Vuex from 'vuex'
import edemo from './store/edemo/index'

Vue.use(Vuex)
export default new Vuex.Store({
  modules: {
    edemo: edemo
  }
})