<script setup lang="ts">
import HomeHeader from '@/components/home/HomeHeader.vue'
import HeroSection from '@/components/home/HeroSection.vue'
import Features from '@/components/home/HomeFeatures.vue'
import HomeFooter from '@/components/home/HomeFooter.vue'
</script>

<style scoped>
/* Global component-specific styles can be added here if needed */
</style>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <main class="flex-grow">
      <HomeHeader />
      <HeroSection />
      <Features />
    </main>

    <HomeFooter />
  </div>
</template>
