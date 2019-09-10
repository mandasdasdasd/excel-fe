import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import login from '@/components/login'
import head from '@/components/head'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: login
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
