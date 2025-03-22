<script setup lang="ts">
import NavigationBar from '@/components/NavigationBar.vue'
import DictionaryTable from '@/components/DictionaryTable.vue'
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <NavigationBar />

    <!-- Main content area -->
    <div class="p-4 flex flex-col items-center">
      <DictionaryTable />
    </div>
  </div>
</template>
