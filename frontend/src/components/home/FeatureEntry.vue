<template>
  <div class="bg-white p-6 rounded-lg shadow-lg flex items-center">
    <!-- Section icône -->
    <div
      class="flex-shrink-0 flex items-center justify-center mr-4 border-r pr-4 h-full border-gray-200"
    >
      <svg class="w-12 h-12 text-blue-600" viewBox="0 0 24 24">
        <path :d="icon" />
      </svg>
    </div>
    <!-- Section texte -->
    <div>
      <h4 class="text-xl font-bold text-blue-600">{{ title }}</h4>
      <p class="mt-2 text-gray-600">{{ description }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
  icon: { type: String, required: true },
})
</script>

<style scoped>
/* Ajoutez des styles spécifiques si nécessaire */
</style>
