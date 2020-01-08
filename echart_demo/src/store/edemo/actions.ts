import { ActionTree } from 'vuex'
import { StateTypes } from './types'
import state from './state'
const actions: ActionTree<StateTypes, any> = {
  // 获取左侧资产信息数据
  getDemo1({ commit, state: StateTypes }, item:any) {
    commit('getDemo1', item)
  },
  // 获取在线信息
  getDemo2({ commit, state: StateTypes }, item:any) {
    commit('getDemo2', item)
  },
  // 获取评分信息
  MARKINFO({ commit, state: StateTypes }, item:any) {
    commit('MARKINFO', item)
  }
}
export default actions
