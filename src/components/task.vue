<template>
    <div class="container-fluid">
        <headd></headd>
        <vxe-toolbar style="margin-top:20px">
          <template v-slot:buttons>
            <vxe-button v-if="xx" @click="getInsertEvent()">保存</vxe-button>
            <vxe-button  v-if="xx" @click="insertEvent()">新增</vxe-button>
             <vxe-button>
              <template>{{year}}</template>
              <template v-slot:dropdowns>
                <vxe-button @click="gettaskbyyear(year)" v-for="year in years">{{year}}</vxe-button>
              </template>
            </vxe-button>
          </template>
        </vxe-toolbar>

       
     <vxe-table
	  resizable
          border
          ref="xTable"
          class="mytable-style"
          :header-cell-class-name="headerCellClassName"
          :cell-class-name="cellClassName"
          :row-class-name="rowClassName"
          :data="tableData"
          :edit-render={}

          @cell-dblclick='insertevent'
          :edit-config="{trigger: 'click', mode: 'row'}">

          <vxe-table-column field="id" width="40" title="id"></vxe-table-column>
          <vxe-table-column field="task" title="任务" :edit-render="{name: 'textarea'}"></vxe-table-column>
          <vxe-table-column field="user" title="用户"  width="10%" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="priority" title="优先级" width="10%" sortable :edit-render="{name: 'select',  options: priority_list}"></vxe-table-column>
          <vxe-table-column field="status" title="状态"  width="10%" sortable :edit-render="{name: 'select', options: sex_list}"></vxe-table-column>
          <vxe-table-column field="create_time" title="创建时间"  width="15%" sortable></vxe-table-column>

          <vxe-table-column title="操作" width="15%"  v-if="save">
            <template v-slot="{ row }">
              <template v-if="$refs.xTable.hasActiveRow(row)">
                <vxe-button @click="saveRowEvent(row)">保存</vxe-button>
                <vxe-button @click="cancelRowEvent(row)">取消</vxe-button>
              </template>
              <template v-else>
                <vxe-button @click="editRowEvent(row)">编辑</vxe-button>
              </template>
            </template>
          </vxe-table-column>
            </vxe-table>
          <vxe-pager
          align="center"
          :current-page.sync="page.currentPage"
          :page-size.sync="page.pageSize"
          :total="page.totalResult"
          :layouts="['JumpNumber']"
          @page-change="handlePageChange"
          >
        </vxe-pager>    

        </div>
</template>

<script>
import headd from '@/components/head'
     export default {
	inject:['reload'],
        data () {
            return {
		xx: true,
                role_sale: true,
                page: {
                    currentPage: sessionStorage.getItem('currentPage'),
                    pageSize: 8,
                    totalResult: 50
                },
                tableData: [],
                year: sessionStorage.getItem('year'),
                years: [2018, 2019, 2020],
                pnumber: '',
                save: true,
                priority_list: [
                    {
                    'label': '高',
                    'value': '2'
                    },
                    {
                    'label': '中',
                    'value': '1'
                    },
                    {
                    'label': '低',
                    'value': '0'
                    }
                    ],
                sex_list: [
                    {
                    'label': '已完成',
                    'value': '1'
                    },
                    {
                    'label': '进行中',
                    'value': '0'
                    }
                    ]
            }
          },
        components: {
            headd
        },
        mounted: function () {   //页面初始化方法
            const exp= sessionStorage.getItem('year')
            if (!exp && typeof(exp) != "undefined" && exp!=0) {
                	this.year=2019
                } else {
                }
            this.init()
        },

        methods: {
            editRowEvent (row) {
		this.xx=false
              this.$refs.xTable.setActiveRow(row)
            },
            saveRowEvent (row) {
              this.update(row)
              this.cancelRowEvent()
            },
            cancelRowEvent (row) {
              this.$refs.xTable.clearActived()
            },
            init () {
		const cpage = sessionStorage.getItem('currentPage')
            	if (cpage === "null") {
                	this.page.currentPage=1
                	} else {
                	};
                const role = this.$cookies.get("role")
                if (role === "11") {
                    this.role_sale = false
                }; 
                if (role === "1" || role === "11") {
                    } else {
                        this.$router.push({
                            path:'/login',
                            query:{
                                id:this.id ,
                            }
                         })
                    };
		this.gettask(this.page.currentPage)
            }, 

            handlePageChange () {
		sessionStorage.setItem('currentPage', this.page.currentPage)
                this.init()
            },

	    gettask (cpage) {
                this.$http.get('/init/gettask', {params: { page: cpage, pageSize: this.page.pageSize, year: this.year}}).then(response => {
                    this.tableData = response.data.data
                    this.page.totalResult = response.data.total_page
                })
		},

	    gettaskbyyear (cyear) {
		sessionStorage.setItem('year', cyear)
		this.year = cyear
		this.gettask(this.page.currentPage)
		},

            insertEvent (row, event) {
                this.save = false;
                let record = {
               		status: "0",
			priority: "1"
              }
		 this.$refs.xTable.insertAt(record, row)
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'status'))
            },

            update (row) {
              let insertRecords = this.$refs.xTable.getInsertRecords()
                 this.$http.get('/init/updatetask', {params: {data: row, year: this.year}}).then(response => {
			this.$XModal.message({ message: '更新成功', status: 'success' })
                })
            },
            	
            cellClassName ({ row, column}) {
		if (column.property === 'status') {
                	if (row.status === "1") {
                    		return 'col-green'
                    }
            	}
		if (column.property === 'priority') {
                	if (row.priority === "2") {
                    		return 'col-red'
                    }
            	}
            },

            getInsertEvent () {
                let insertRecords = this.$refs.xTable.getInsertRecords()
		console.log(insertRecords)
                 this.$http.get('/init/addtask', {params: {data: JSON.stringify(insertRecords), year: this.year}}).then(response => {
			this.$XModal.message({ message: '保存成功', status: 'success' })
			this.reload()
                })
            }
          }
        }
</script>
<style >
.vxe-table .vxe-body--column.col-green {
  background-color: green;
  color: #fff;
}
.vxe-table .vxe-body--column.col-red {
  background-color: red;
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
