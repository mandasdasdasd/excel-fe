<template>

<div>
      <vxe-pager
          align="left"
          :current-page.sync="page1.currentPage"
          :page-size.sync="page1.pageSize"
          :total="page1.totalResult"
          :layouts="['JumpNumber']">
     </vxe-pager>
</div>

</template>
<script>
   export default {
          data () {
            return {
              page1: {
                currentPage: 1,
                pageSize: 10,
                totalResult: 200
              }
              }
              }
              }
</script>
