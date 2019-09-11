<template >
    <div class="row" style="background-color:#f5f5f5">
        <div class="col-md-12" style="height:50px">
            <div class="col-md-11" style="padding-top:11px">
               <span style="font-size:22px"><strong>才华有限公司</strong></span>
               <span style="margin-left:15px">项目表</span>
               <span style="margin-left:15px">个人表</span>
            </div>
            <div class="col-md-1" style="padding-top:11px">
               <span>{{username}}</span>
               <span style="margin-left:15px" @click="logout()"><a>登出</a></span>
            </div>
        </div>
    </div>
</template>
<script>
     export default {
        data () {
            return {
                username: '请先登陆',
            }
          },

        mounted: function () {   //页面初始化方法
            this.username = this.$cookies.get("name")
                },
        methods: {
            logout () {
                this.username = this.$cookies.remove("role")
                this.username = this.$cookies.remove("name")
                this.$router.push({  //核心语句
                            path:'/login',   //跳转的路径
                            query:{           //路由传参时push和query搭配使用 ，作用时传递参数
                                id:this.id ,
                            }
                         })

            }
         }
         }
</script>

<style scoped>
span {
    font-size: 25px;
      font-family: 宋体;
}

