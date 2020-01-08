import { MutationTree } from 'vuex'
import { StateTypes } from './types'
import * as echarts from 'echarts'
import state from './state'
const fn = (data: any, pid: any) => {
  let result: any = []
  let temp: any = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].pid === pid) {
      let obj:any = { 'label': data[i].name, 'value': data[i].id, 'id': data[i].id }
      temp = fn(data, data[i].id)
      if (temp.length > 0) {
        obj.children = temp
      }
      result.push(obj)
    }
  }
  return result
}
const fntype = (data: any, pid: any) => {
  data.forEach(function(item: any) {
    item.id = item.id.toString()
    item.pid = item.pid.toString()
    item.name = item.type_name
  })
  let result2: any = []
  let temp2: any = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].pid === pid) {
      let obj2:any = { 'label': data[i].type_name, 'id': data[i].id, 'value': data[i].id }
      temp2 = fntype(data, data[i].id)
      if (temp2.length > 0) {
        obj2.children = temp2
      }
      result2.push(obj2)
    }
  }
  return result2
}
const getpid = (arr:any, target: any, nArr: any) => {
  for (let i in arr) {
    if (arr[i].id === target) {
      nArr.unshift(arr[i].id)
      getpid(arr, arr[i].pid, nArr)
    }
  }
  return nArr
}

// 设置饼图数据格式
const foreachArr = (arr:any) => {
  let aarr = []
  for (let i = 0; i < arr.length; i++) {
    let obj = {
      name: arr[i].name,
      value: arr[i].value,
      children: [],
      itemStyle: {
        color: arr[i].color
      }
    }
    aarr.push(obj)
  }
  return aarr
}
// 遍历后端返回的数组
const aforEach = (data: any, pid: any) => {
  data.forEach(function(item: any) {
    item.id = item.id.toString()
    item.pid = item.pid.toString()
  })
  let result: any = []
  let temp: any = []
  for (let i = 0; i < data.length; i++) {
    if (data[i].pid === pid) {
      let obj:any = { 'name': data[i].name, 'id': data[i].id, 'value': data[i].value, 'color': state.colorGroup[i] }
      temp = aforEach(data, data[i].id)
      if (temp.length > 0) {
        obj.children = temp
      }
      result.push(obj)
    }
  }
  return result
}
const aList = [
  { name: '分组1', value: 40, id: 1, pid: '' },
  { name: '分组2', value: 10, id: 2, pid: '' },
  { name: '分组1-1', value: 36, id: 3, pid: '1' },
  { name: '分组1-2', value: 4, id: 4, pid: '1' },
  { name: '分组1-1-1', value: 6, id: 5, pid: '3' },
  { name: '分组1-1-2', value: 6, id: 6, pid: '3' },
  { name: '分组1-1-3', value: 8, id: 7, pid: '3' },
  { name: '分组1-1-4', value: 8, id: 8, pid: '3' },
  { name: '分组1-1-5', value: 8, id: 9, pid: '3' },
  { name: '分组2-1', value: 8, id: 10, pid: '2' },
  { name: '分组2-2', value: 2, id: 11, pid: '2' },
  { name: '分组1-2-1', value: 1, id: 12, pid: '4' },
  { name: '分组1-2-2', value: 1, id: 13, pid: '4' },
  { name: '分组1-2-3', value: 1, id: 14, pid: '4' },
  { name: '分组1-2-4', value: 1, id: 15, pid: '4' }
]
let totalarr = (arr:any) => {
  let sum = 0
  for (let i = 0; i < arr.length; i++) {
    sum += arr[i].value
  }
  return sum
}
let aLinfo = aforEach(aList, '')
const mutations: MutationTree<StateTypes> = {
  getDemo1(state: StateTypes, item: any) {
    let myChart0 = echarts.init(item)
    let data = foreachArr(aLinfo)
    let options: any = {
      graphic: [{// 环形图中间添加文字
        type: 'text', // 通过不同top值可以设置上下显示
        left: 'center',
        top: '40%',
        style: {
          text: totalarr(aLinfo),
          textAlign: 'center',
          fill: '#000', // 文字的颜色
          width: 30,
          height: 30,
          fontSize: 40,
          lineWidth: 2,
          color: '#4d4f5c',
          fontFamily: 'Microsoft YaHei'
        }
      }, {
        type: 'text',
        left: 'center',
        top: '55%',
        style: {
          text: '全部数据',
          textAlign: 'center',
          fill: '#000',
          width: 30,
          height: 30,
          fontSize: 18
        }
      }],
      series: {
        type: 'sunburst',
        highlightPolicy: 'ancestor',
        nodeClick: false,
        data: data,
        center: ['50%', '50%'],
        radius: [0, '95%'],
        sort: null,
        levels: [{
        }, {
          r0: '50%',
          r: '75%',
          itemStyle: {
            borderWidth: 0
          },
          label: {
            show: false
          }
        }, {
          r0: '50%',
          r: '85%',
          label: {
            show: false
          }
        }, {
          r0: '85%',
          r: '95%',
          label: {
            show: false
          },
          itemStyle: {
            borderWidth: 0
          }
        }]
      }
    }
    state.assetShowData = data
    myChart0.setOption(options)
    myChart0.on('click', function(params:any) {
      console.log(params)
      if (params.name === '分组1') {
        options.graphic = [{// 环形图中间添加文字
          type: 'text', // 通过不同top值可以设置上下显示
          left: 'center',
          top: '40%',
          style: {
            text: aLinfo[0].value,
            textAlign: 'center',
            fill: '#000', // 文字的颜色
            width: 30,
            height: 30,
            fontSize: 40,
            color: '#4d4f5c',
            fontFamily: 'Microsoft YaHei'
          }
        }, {
          type: 'text',
          left: 'center',
          top: '55%',
          style: {
            text: aLinfo[0].name,
            textAlign: 'center',
            fill: '#000',
            width: 30,
            height: 30,
            fontSize: 18
          }
        }]
        if (aLinfo[0].children) {
          params.data.children = foreachArr(aLinfo[0].children)
          data[0] = params.data
          state.assetShowData = params.data.children
        }
        data[1].children = []
        myChart0.setOption(options)
      } else if (params.name === '分组2') {
        options.graphic = [{// 环形图中间添加文字
          type: 'text', // 通过不同top值可以设置上下显示
          left: 'center',
          top: '40%',
          style: {
            text: aLinfo[1].value,
            textAlign: 'center',
            fill: '#000', // 文字的颜色
            width: 30,
            height: 30,
            fontSize: 40,
            color: '#4d4f5c',
            fontFamily: 'Microsoft YaHei'
          }
        }, {
          type: 'text',
          left: 'center',
          top: '55%',
          style: {
            text: aLinfo[1].name,
            textAlign: 'center',
            fill: '#000',
            width: 30,
            height: 30,
            fontSize: 18
          }
        }]
        if (aLinfo[1].children) {
          params.data.children = foreachArr(aLinfo[1].children)
          data[1] = params.data
          state.assetShowData = params.data.children
        }
        data[0].children = []
        myChart0.setOption(options)
      }
    })
    myChart0.on('click', function(params:any) {
      if (params.name === '分组1-1') {
        options.graphic = [{// 环形图中间添加文字
          type: 'text', // 通过不同top值可以设置上下显示
          left: 'center',
          top: '40%',
          style: {
            text: aLinfo[0].children[0].value,
            textAlign: 'center',
            fill: '#000', // 文字的颜色
            width: 30,
            height: 30,
            fontSize: 40,
            color: '#4d4f5c',
            fontFamily: 'Microsoft YaHei'
          }
        }, {
          type: 'text',
          left: 'center',
          top: '55%',
          style: {
            text: aLinfo[0].children[0].name,
            textAlign: 'center',
            fill: '#000',
            width: 30,
            height: 30,
            fontSize: 18
          }
        }]
        if (aLinfo[0].children[0].children) {
          params.data.children = foreachArr(aLinfo[0].children[0].children)
          let temp:any = data[0].children
          temp[0] = params.data
          temp[1].children = []
          state.assetShowData = params.data.children
        }
        myChart0.setOption(options)
      } else if (params.name === '分组1-2') {
        options.graphic = [{// 环形图中间添加文字
          type: 'text', // 通过不同top值可以设置上下显示
          left: 'center',
          top: '40%',
          style: {
            text: aLinfo[0].children[1].value,
            textAlign: 'center',
            fill: '#000', // 文字的颜色
            width: 30,
            height: 30,
            fontSize: 40,
            color: '#4d4f5c',
            fontFamily: 'Microsoft YaHei'
          }
        }, {
          type: 'text',
          left: 'center',
          top: '55%',
          style: {
            text: aLinfo[0].children[1].name,
            textAlign: 'center',
            fill: '#000',
            width: 30,
            height: 30,
            fontSize: 18
          }
        }]
        if (aLinfo[0].children[1].children) {
          params.data.children = foreachArr(aLinfo[0].children[1].children)
          let temp:any = data[0].children
          temp[1] = params.data
          temp[0].children = []
          state.assetShowData = params.data.children
        }
        myChart0.setOption(options)
      }
    })
    myChart0.on('click', function(params:any) {
      if (params.componentType === 'graphic') {
        let graphic0 = [{// 环形图中间添加文字
          type: 'text', // 通过不同top值可以设置上下显示
          left: 'center',
          top: '40%',
          style: {
            text: '40',
            textAlign: 'center',
            fill: '#000', // 文字的颜色
            width: 30,
            height: 30,
            fontSize: 40,
            color: '#4d4f5c',
            fontFamily: 'Microsoft YaHei'
          }
        }, {
          type: 'text',
          left: 'center',
          top: '55%',
          style: {
            text: '分组1',
            textAlign: 'center',
            fill: '#000',
            width: 30,
            height: 30,
            fontSize: 18
          }
        }]
        let graphic1 = [{// 环形图中间添加文字
          type: 'text', // 通过不同top值可以设置上下显示
          left: 'center',
          top: '40%',
          style: {
            text: '50',
            textAlign: 'center',
            fill: '#000', // 文字的颜色
            width: 30,
            height: 30,
            fontSize: 40,
            lineWidth: 2,
            color: '#4d4f5c',
            fontFamily: 'Microsoft YaHei'
          }
        }, {
          type: 'text',
          left: 'center',
          top: '55%',
          style: {
            text: '全部资产',
            textAlign: 'center',
            fill: '#000',
            width: 30,
            height: 30,
            fontSize: 18
          }
        }]
        if (options.graphic[1].style.text === '分组1-1') {
          options.graphic = graphic0
          let temp:any = options.series.data[0].children[0]
          if (temp.children) {
            temp.children = []
            state.assetShowData = options.series.data[0].children
          }
          myChart0.setOption(options)
        } else if (options.graphic[1].style.text === '分组1-2') {
          options.graphic = graphic0
          let temp:any = options.series.data[0].children[1]
          if (temp.children) {
            temp.children = []
            state.assetShowData = options.series.data[0].children
          }
          myChart0.setOption(options)
        } else if (params.componentType === 'graphic') {
          if (options.graphic[1].style.text === '分组1') {
            options.graphic = graphic1
            let temp:any = options.series.data[0]
            if (temp.children) {
              temp.children = []
              state.assetShowData = options.series.data
            }
            options.series.data[1].children = []
            myChart0.setOption(options)
          } else if (options.graphic[1].style.text === '分组2') {
            options.graphic = graphic1
            let temp:any = options.series.data[1]
            if (temp.children) {
              temp.children = []
              state.assetShowData = options.series.data
            }
            options.series.data[0].children = []
            myChart0.setOption(options)
          }
        }
      }
    })
  },
  getDemo2(state: StateTypes, item: any) {
    let myChart2 = echarts.init(item)
    let labelBottom = {
      normal: {
        color: '#ccc'
      }
    }
    let radius = [40, 55]
    let options: any = {
      tooltip: {
        trigger: 'item',
        formatter: '{b}: {c} ({d}%)'
      },
      toolbox: {
        show: false,
        right: 20,
        feature: {
          dataView: { show: true, readOnly: false },
          magicType: {
            show: true,
            type: ['pie', 'funnel'],
            option: {
              funnel: {
                width: '10%',
                height: '30%',
                itemStyle: {
                  normal: {
                    label: {
                      formatter: function(params: any) {
                        return 'other\n' + params.value + '%\n'
                      },
                      textStyle: {
                        baseline: 'middle'
                      }
                    }
                  }
                }
              }
            }
          },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
      // legend: {
      //   x: 'center',
      //   y: '85%',
      //   data: ['威胁告警', '漏洞告警', '异常告警'， '资产告警'],
      //   icon: 'square',
      //   itemWidth: 12,
      //   itemHeight: 12
      // },
      series: [
        {
          hoverAnimation: false,
          type: 'pie',
          center: ['25%', '25%'],
          radius: [45, 53],
          x: '0%',
          itemStyle: {
            normal: {
              label: {
                formatter: '{d|{d}%}\n{b|{b}}\n{c|{c}个}',
                position: 'center',
                rich: {
                  b: {
                    color: '#ccc'
                  },
                  c: {
                    color: '#ccc'
                  },
                  d: {
                    color: '#000',
                    lineHeight: 18
                  }
                }
              },
              color: 'rgb(240,72,68)'
            }
          },
          data: [
            {
              name: '未分组',
              value: 50,
              itemStyle: labelBottom,
              label: {
                show: false,
                position: 'inside'
              }
            },
            { name: '分组1', value: 1 }
          ]
        },
        {
          hoverAnimation: false,
          type: 'pie',
          center: ['75%', '25%'],
          radius: [45, 53],
          x: '20%',
          itemStyle: {
            normal: {
              label: {
                formatter: '{d|{d}%}\n{b|{b}}\n{c|{c}个}',
                position: 'center',
                rich: {
                  b: {
                    color: '#ccc'
                  },
                  c: {
                    color: '#ccc'
                  },
                  d: {
                    color: '#000',
                    lineHeight: 18
                  }
                }
              },
              color: 'rgb(255,168,71)'
            }
          },
          data: [
            {
              name: '未分组',
              value: 30,
              itemStyle: labelBottom,
              label: {
                show: false,
                position: 'inside'
              }
            },
            { name: '分组2', value: 20 }
          ]
        },
        {
          hoverAnimation: false,
          type: 'pie',
          center: ['-25%', '75%'],
          radius: [45, 53],
          x: '40%',
          itemStyle: {
            normal: {
              label: {
                formatter: '{d|{d}%}\n{b|{b}}\n{c|{c}个}',
                position: 'center',
                rich: {
                  b: {
                    color: '#ccc'
                  },
                  c: {
                    color: '#ccc'
                  },
                  d: {
                    color: '#000',
                    lineHeight: 18
                  }
                }
              },
              color: 'rgb(51,153,255)'
            }
          },
          data: [
            {
              name: '未分组',
              value: 20,
              itemStyle: labelBottom,
              label: {
                show: false,
                position: 'inside'
              }
            },
            { name: '分组3', value: 30 }
          ]
        },
        {
          hoverAnimation: false,
          type: 'pie',
          center: ['50%', '75%'],
          radius: [45, 53],
          x: '60%',
          itemStyle: {
            normal: {
              label: {
                formatter: '{d|{d}%}\n{b|{b}}\n{c|{c}个}',
                position: 'center',
                rich: {
                  b: {
                    color: '#ccc'
                  },
                  c: {
                    color: '#ccc'
                  },
                  d: {
                    color: '#000',
                    lineHeight: 18
                  }
                }
              },
              color: 'rgb(46,204,113)'
            }
          },
          data: [
            {
              name: '未分组',
              value: 10,
              itemStyle: labelBottom,
              label: {
                show: false,
                position: 'inside'
              }
            },
            { name: '分组4', value: 70 }
          ]
        }
      ]
    }
    myChart2.setOption(options)
  }
}
export default mutations
