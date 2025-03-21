<script setup lang="ts">
import { useRoute } from 'vue-router'

// Access the current route to determine which link is active
const route = useRoute()
</script>

<template>
  <nav class="w-full bg-white shadow p-2">
    <div class="max-w-2xl mx-auto flex justify-between items-center">
      <!-- App Title (acts as a link to the home page) -->
      <router-link to="/" class="text-2xl font-bold text-blue-600"> DicoRago </router-link>
      <!-- Navigation Links -->
      <div class="flex space-x-6">
        <router-link
          to="/"
          class="text-lg hover:text-blue-600"
          :class="route.path === '/' ? 'underline underline-offset-4' : ''"
          exact
        >
          Analyze
        </router-link>
        <router-link
          to="/dico"
          class="text-lg hover:text-blue-600"
          :class="route.path === '/dico' ? 'underline underline-offset-4' : ''"
        >
          Dictionary
        </router-link>
      </div>
    </div>
  </nav>
</template>
