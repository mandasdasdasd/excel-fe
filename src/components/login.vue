<template>
<div class="container" style="margin-top:200px">
<div class="row">
<div class="col-md-6 col-md-offset-3">
<div class="col-md-10 col-md-offset-1">
<form class="form-horizontal" role="form">
	<div class="form-group">
		<label for="firstname" class="col-sm-2 control-label">用户名</label>
		<div class="col-sm-10">
			<input type="text" class="form-control" id="firstname"  ref="user"
				   placeholder="请输入用户名">
		</div>
	</div>
	<div class="form-group">
		<label for="lastname" class="col-sm-2 control-label">密码</label>
		<div class="col-sm-10">
			<input type="password" class="form-control" id="lastname" ref="pwd" 
				   placeholder="请输入密码">
		</div>
	</div>
	<div class="form-group">
		<div class="col-sm-offset-2 col-sm-10">
			<div class="checkbox">
				<label>
					<input type="checkbox"> 请记住我
				</label>
			</div>
		</div>
	</div>
	<div class="form-group">
		<div class="col-sm-offset-2 col-sm-10">
			<button @click="login()" @click.prevent="handleSubmit" class="btn btn-default">登录</button>
		</div>
	</div>
</form>
</div>
</div>
</div>
</div>
</template>

<script>
     export default {
        data () {
            return {
            }
          },
       methods: {
            login () {
                this.$http.get('/init/login', {params: {user: this.$refs.user.value, pwd: this.$refs.pwd.value}}).then(response => {
                if (response.data === 1) {
                    alert("登陆成功")
                        this.$router.push({  //核心语句
                            path:'/task',   //跳转的路径
                            query:{           //路由传参时push和query搭配使用 ，作用时传递参数
                                id:this.id ,
                            }
                         })
                    } else {
                    alert("登陆失败")
                    }
                })
            },
        }
        }
</script>
