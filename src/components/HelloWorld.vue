<template>
    <div>
        <vxe-toolbar>
          <template v-slot:buttons>
            <vxe-button @click="getInsertEvent">保存</vxe-button>
            <vxe-button @click="insertEvent(-1)">新增</vxe-button>
             <vxe-button>
              <template>{{year}}</template>
              <template v-slot:dropdowns>
                <vxe-button @click="xyear(x)" v-for="x in years">{{x}}</vxe-button>
              </template>
            </vxe-button>
          </template>
        </vxe-toolbar>
        
     <vxe-table
          border
          ref="xTable"
          class="mytable-style"
          :header-cell-class-name="headerCellClassName"
          :cell-class-name="cellClassName"
          :row-class-name="rowClassName"
          :data="tableData"
          :edit-config="{trigger: 'click', mode: 'cell'}">
          <vxe-table-column type="index" width="60"></vxe-table-column>
          <vxe-table-column field="year" title="年份"></vxe-table-column>
          <vxe-table-column field="vname" title="项目名称" sortable  :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="people" title="人员" sortable  :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="input" title="进价"  :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="output" title="卖价" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="discount" title="折扣" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="profit" title="利润"></vxe-table-column>
          <vxe-table-column field="number" title="数量" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="status" title="状态" sortable :edit-render="{name: 'input'}"></vxe-table-column>
        </vxe-table>

        </div>
</template>



<script>
import store from "./store.js"

     export default {
          data () {
            return {
              tableData: [],
              year: sessionStorage.getItem('year'),
              years: []
            }
          },

        mounted: function () {   //页面初始化方法
           this.$http.get('/init', {params: {year: this.year}}).then(response => {
                this.tableData = response.data
            }),
            this.$http.get('/init/year').then(response => {
                this.years = response.data;
            })

        },

          methods: {
            xyear (item) {
                this.year = item
                sessionStorage.setItem('year', item)
                this.$http.get('/init/yearsort', {params: {year: item}}).then(response => {
                    this.tableData = response.data
                })
            },

            insertEvent (row) {
              let record = {
                year: this.year
              }
              this.$refs.xTable.insertAt(record, row)
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'year'))
            },

            rowClassName ({ row, rowIndex}) {
                if (row.status === "完成") {
                    return 'row-green'
                    }
                else if (row.status === "紧急") {
                    return 'row-red'
                    }
                else if (row.status === "失效") {
                    return 'row-gray'
                    }
            },

            getInsertEvent () {
               alert()
              let insertRecords = this.$refs.xTable.getInsertRecords()
                 this.$http.get('/init/add', {params: {data: JSON.stringify(insertRecords), year: this.year}}).then(response => {
                    this.tableData = response.data
                })
            }

          }
        }
</script>
<style >
.vxe-table .vxe-body--row.row-green {
  background-color: green;
  color: #fff;
}
.vxe-table .vxe-body--row.row-red {
  background-color: red;
  color: #fff;
}
.vxe-table .vxe-body--row.row-gray {
  background-color: gray;
  color: #fff;
}
</style>
