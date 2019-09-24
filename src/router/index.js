import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import login from '@/components/login'
import head from '@/components/head'
import user from '@/components/user'
import task from '@/components/task'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: task
    },
    {
      path: '/task',
      component: task
    },
    {
      path: '/user',
      component: user
    },
    {
      path: '/list',
      component: HelloWorld
    },
    {
      path: '/login',
      component: login
    }
  ]
})
