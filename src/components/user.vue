<template>
<div>
    <headd></headd>
        <vxe-toolbar>
          <template v-slot:buttons>
            <vxe-button @click="insertEvent()">在第1行插入</vxe-button>
            <vxe-button @click="getInsertEvent">保存</vxe-button>
          </template>
        </vxe-toolbar>

        <vxe-table
          border
          show-overflow
          ref="xTable"
          :data="tableData"
          :edit-config="{trigger: 'click', mode: 'cell'}">
          <vxe-table-column type="index" width="60"></vxe-table-column>
          <vxe-table-column field="name" title="姓名" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="user" title="账号" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="pwd" title="密码" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="tele" title="手机号" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="role" title="权限" sortable :edit-render="{name: 'select', options: role_list}"></vxe-table-column>
          <vxe-table-column field="status" title="状态" sortable :edit-render="{name: 'select', options: status_list}"></vxe-table-column>
          <vxe-table-column field="sex" title="性别" sortable :edit-render="{name: 'select', options: sex_list}"></vxe-table-column>
          <vxe-table-column v-if="createtime" field="create_time" title="创建时间" sortable :edit-render="{name: 'input'}"></vxe-table-column>
        </vxe-table>

</div>
</template>
<script>
import headd from '@/components/head'


        export default {
          data () {
            return {
                createtime: true,
              tableData: [],
              role_list: [
                    {
                    'label': '1级',
                    'value': '1'
                    },
                    {
                    'label': '2级',
                    'value': '0'
                    }
                    ],
              status_list: [
                    {
                    'label': '在职',
                    'value': '1'
                    },
                    {
                    'label': '离职',
                    'value': '0'
                    }
                    ],
              sex_list: [
                    {
                    'label': '男',
                    'value': '1'
                    },
                    {
                    'label': '女',
                    'value': '0'
                    }
                    ],
            }
          },
         components: {
            headd
        },

          mounted: function () {
             this.$http.get('/init/getuser').then(response => {
                    this.tableData = response.data
                })
          },
          methods: {
            insertEvent (row) {
                this.createtime=false;
                 let record = {
                status: '1',
                sex: '1',
                role: '1'
              }
              this.$refs.xTable.insertAt(record, row)
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'status'))
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'sex'))
            },
            getInsertEvent () {
              let insertRecords = this.$refs.xTable.getInsertRecords()
                this.$http.get('/init/useradd', {params: {data: JSON.stringify(insertRecords)}}).then(response => {
                    alert(response.data.message)
                    this.tableData.data = response.data.data
                })
            }
          }
        }
</script>
