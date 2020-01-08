<template>
  <div class="home">
    <el-row>
      <el-col :span="4">
        <div style="height:250px" id="echartDemo1"></div>
      </el-col>
      <el-col :span="2">
        <div class="assetCount">
          <ul>
            <li v-for="item,index in this.estate.assetShowData" :key="index">
              <span :style="{'border-left':'4px solid '+ item.itemStyle.color}">
                {{item.name}}&nbsp;&nbsp;&nbsp;&nbsp;
                <span style="float: right">{{item.value}}</span>
              </span>
            </li>
          </ul>
        </div>
      </el-col>
      <el-col :span="6">
        <div style="height:250px" id="echartDemo2"></div>
      </el-col>

    </el-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator'
import { State, namespace, Action } from 'vuex-class'
const etest = namespace('edemo')
@Component
export default class Table extends Vue {
  @etest.State(state => state) estate: any
  @etest.Action('getDemo1') getDemo1!: Function
  @etest.Action('getDemo2') getDemo2!: Function
  mounted() {
    let m1 = document.getElementById('echartDemo1')
    this.getDemo1(m1)
    let m2 = document.getElementById('echartDemo2')
    this.getDemo2(m2)
  }
}
</script>
