<template>
  <section class="py-12 bg-gray-100">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <h3 class="text-3xl font-bold text-center text-gray-800">Key Features</h3>
      <div class="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <FeatureEntry
          title="Vocabulary Analysis"
          description="Paste any Korean text and get an immediate breakdown with translations."
          :icon="mdiBookOpenVariant"
        />
        <FeatureEntry
          title="Color-Coded Recognition"
          description="Easily identify known and unknown words for a more efficient learning process."
          :icon="mdiPalette"
        />
        <FeatureEntry
          title="Vocabulary Filtering"
          description="Hide words you already know and focus on new ones."
          :icon="mdiFilter"
        />
        <FeatureEntry
          title="In-Depth Word Exploration"
          description="Access multiple meanings, definitions, and example sentences."
          :icon="mdiMagnify"
        />
        <FeatureEntry
          title="Personal Vocabulary Management"
          description="Track your progress by saving new words to your vocabulary list."
          :icon="mdiNotebook"
        />
        <FeatureEntry
          title="Grammar Structure Analysis"
          description="Get word types and sentence constructions to improve comprehension."
          :icon="mdiFormatListBulleted"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import FeatureEntry from './FeatureEntry.vue'
import {
  mdiBookOpenVariant,
  mdiPalette,
  mdiFilter,
  mdiMagnify,
  mdiNotebook,
  mdiFormatListBulleted,
} from '@mdi/js'
</script>

<style scoped>
/* Styles spécifiques à ce composant */
</style>
