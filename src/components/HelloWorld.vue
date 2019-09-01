<template>
    <div>
        <vxe-toolbar>
          <template v-slot:buttons>
            <!-- 
            <vxe-button @click="insertEvent()">在第1行插入</vxe-button>
            <vxe-button @click="insertEvent(tableData[2])">在第3行插入并激活 Sex 单元格</vxe-button>
            -->
            <vxe-button @click="getInsertEvent">获取新增</vxe-button>
            <vxe-button @click="insertEvent(-1)">在最后行插入</vxe-button>
          </template>
        </vxe-toolbar>

        <vxe-table
          border
          show-overflow
          ref="xTable"
          max-height="400"
          :data="tableData"
          :edit-config="{trigger: 'click', mode: 'cell'}">
          <vxe-table-column type="index" width="60"></vxe-table-column>
          <vxe-table-column field="sex" title="Sex" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="name" title="Name" :edit-render="{name: 'input'}"> </vxe-table-column>
          <vxe-table-column field="age" title="Age" :edit-render="{name: 'input'}"> </vxe-table-column>
        </vxe-table>
        </div>
</template>
<script>
     export default {
          data () {
            return {
              tableData: [],
              asdasd: []
            }
          },

        mounted: function () {   //页面初始化方法
            this.$http.get('/init').then(response => {
                this.tableData = response.data
            })
        },

          methods: {
            insertEvent (row) {
              let record = {
              sex : "1"
              }
              this.$refs.xTable.insertAt(record, row)
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'sex'))
            },
            getInsertEvent () {
              let insertRecords = this.$refs.xTable.getInsertRecords()
                 //this.$http.get('/init/add', {params: {data: JSON.stringify(insertRecords[0])}}).then(response => {
                 this.$http.get('/init/add', {params: {data: JSON.stringify(insertRecords)}}).then(response => {
                    alert("success")
                })
            }
          }
        }
</script>
