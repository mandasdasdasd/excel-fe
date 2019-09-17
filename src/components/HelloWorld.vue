<template>
    <div class="container-fluid">
        <headd></headd>
        <vxe-toolbar style="margin-top:20px">
          <template v-slot:buttons>
            <vxe-button @click="getInsertEvent()">保存</vxe-button>
            <vxe-button @click="insertEvent()">新增</vxe-button>
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
          :edit-render={}

          @cell-dblclick='insertevent'
          :edit-config="{trigger: 'click', mode: 'row'}">

          <vxe-table-column field="id" width="40" title="id"></vxe-table-column>
          <vxe-table-column field="project_time" title="立项时间" sortable  :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="project_number" title="编号" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="area" title="区域" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="billing_information" title="开票信息" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="contact" title="联系人" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="tele" title="电话" :edit-render="{name: 'input'}" ></vxe-table-column>
          <vxe-table-column field="project_sort" title="项目类别" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="order_content" title="订单内容" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="norm" title="规格" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="supplier" title="供应商" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="purchase_number" title="采购量" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="original_price" title="原价" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="discount" title="折扣（%）" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="total_price" title="总价" sortable ></vxe-table-column>
          <vxe-table-column field="sell_number" title="售货量" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="sell_price" title="售价" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="sell_total_price" title="总价" sortable ></vxe-table-column>
          <vxe-table-column field="tax" title="税率（%）" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="price_after_tax" title="税后价" sortable></vxe-table-column>
          <vxe-table-column field="other_price" title="其他费用" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column v-if="role_sale" field="profit" title="利润" sortable ></vxe-table-column>
          <vxe-table-column field="billing" title="发票" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="back_money" title="回款"  :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="billing_money" title="支票现金" :edit-render="{name: 'select', options: sexList}"></vxe-table-column>
          <vxe-table-column field="task_man" title="业务员" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="exe_man" title="执行人员" sortable :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="common" title="备注" :edit-render="{name: 'input'}"></vxe-table-column>
          <vxe-table-column field="update_number" title="编辑次数"></vxe-table-column>
          <vxe-table-column field="create_time" title="创建时间" sortable></vxe-table-column>

          <vxe-table-column title="操作" v-if="save">
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
        data () {
            return {
                role_sale: true,
                page: {
                    currentPage: 1,
                    pageSize: 8,
                    totalResult: 50
                },
                tableData: [],
                year: sessionStorage.getItem('year'),
                years: [],
                pnumber: '',
                save: true,
                sexList: [
                    {
                    'label': '现金',
                    'value': '1'
                    },
                    {
                    'label': '支票',
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
            if (!exp && typeof exp!="undefined" && exp!=0) {
                this.year=2019
                } else {
                }
            this.init(),
            this.$http.get('/init/year').then(response => {
                this.years = response.data;
            })
        },

        methods: {
            al () {
                alert(12)
            },
            editRowEvent (row) {
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
                    }

                this.$http.get('/init', {params: {year: this.year, page: this.page.currentPage, pageSize: this.page.pageSize}}).then(response => {
                    this.tableData = response.data.data
                    this.page.totalResult = response.data.total_page
                })
            }, 

            handlePageChange () {
                this.init()
            },

            xyear (item) {
                this.year = item
                sessionStorage.setItem('year', item)
                this.$http.get('/init/yearsort', {params: {year: item, pageSize: this.page.pageSize}}).then(response => {
                    this.tableData = response.data
                })
            },

            insertEvent (row, event) {
                this.save = false;
                let record = {
                year:this.year,
                profit: "不可编辑",
                create_time: "不可编辑",
                total_price: "不可编辑",
                sell_total_price: "不可编辑",
                price_after_tax: "不可编辑",
              }
              this.$refs.xTable.insertAt(record, row)
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'year'))
            },

            insertevent ({row}, event) {
                this.save = false;
              let record = {
                profit: "不可编辑",
                create_time: "不可编辑",
                total_price: "不可编辑",
                sell_total_price: "不可编辑",
                price_after_tax: "不可编辑",
                project_number: row.project_number,
                project_time: row.project_time,
                area: row.area
              }
              this.$refs.xTable.insertAt(record, row)
                .then(({ row }) => this.$refs.xTable.setActiveCell(row, 'year'))
            },

            update (row) {
              let insertRecords = this.$refs.xTable.getInsertRecords()
                 this.$http.get('/init/update', {params: {data: row, year: this.year}}).then(response => {
                    alert(response.data.message)
                })
            },
            	
            rowClassName ({ row, rowIndex}) {
                if (row.profit > 1000) {
                    return 'row-green'
                    }
            },

            getInsertEvent () {
                let insertRecords = this.$refs.xTable.getInsertRecords()
                 this.$http.get('/init/add', {params: {data: JSON.stringify(insertRecords), year: this.year}}).then(response => {
                    alert(response.data.message)
                    this.tableData.data = response.data.data
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
