import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DictionaryView from '../views/DictionaryView.vue'

/** Application routes definition */
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/dico',
    name: 'Dictionary',
    component: DictionaryView,
  },
]

/** Create the app router */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

/** Export the router instance */
export default router
