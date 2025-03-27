import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import AnalyzeView from '../views/AnalyzeView.vue'
import DictionaryView from '../views/DictionaryView.vue'
import HomeView from '../views/HomeView.vue'

/** Application routes definition */
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/Analyze',
    name: 'Analyze',
    component: AnalyzeView,
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
