<template >
    <div class="row" style="background-color:#f5f5f5">
        <div class="col-md-12" style="height:50px">
            <div class="col-md-11" style="padding-top:11px">
               <span style="font-size:22px"><strong>CNIC</strong></span>
               <span style="margin-left:15px">项目表</span>
               <span v-if="privilege" style="margin-left:15px"> <router-link :to="{path: '/user'}">用户表</router-link></span>
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
                privilege: false,
            }
          },

        mounted: function () {   //页面初始化方法
            this.username = this.$cookies.get("user")
            var cookie_privilege = this.$cookies.get("privilege")
            if (cookie_privilege === "admin") {
                this.privilege = true
                }
            else {
                this.privilege = false
                }
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
