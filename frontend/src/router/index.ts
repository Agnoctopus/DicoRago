import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import AnalyzeView from '../views/AnalyzeView.vue'
import DictionaryView from '../views/DictionaryView.vue'
import HomeView from '../views/HomeView.vue'
import ChangelogView from '../views/ChangelogView.vue'
import NotFoundView from '../views/NotFoundView.vue'
import AnkiView from '../views/AnkiView.vue'
import AnkiLoginView from '../views/AnkiLoginView.vue'

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
  {
    path: '/changelog',
    name: 'Changelog',
    component: ChangelogView,
  },
  {
    path: '/anki',
    name: 'AnkiView',
    component: AnkiView,
  },
  {
    path: '/anki/login',
    name: 'AnkiLoginView',
    component: AnkiLoginView,
  },
  // Catch-all route for handling 404 errors
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
  },
]

/** Create the app router */
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

/** Export the router instance */
export default router
