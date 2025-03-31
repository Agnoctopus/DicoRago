<template>
  <div class="min-h-screen flex flex-col justify-center items-center bg-gray-100 p-4">
    <!-- Icon of the application -->
    <img :src="icon" alt="" class="w-56 h-56 mb-6 rounded-4xl border-2" />
    <h1 class="text-5xl font-bold text-gray-800 mb-4">404</h1>
    <p class="text-xl text-gray-700 mb-6 text-center">
      Oops! The page you are looking for doesn't exist.
    </p>
    <router-link to="/" class="text-blue-600 hover:underline"> Return to Home </router-link>
  </div>
</template>

<script setup lang="ts">
import icon from '@/assets/icon.png'
</script>

<style scoped></style>
