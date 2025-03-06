<script setup lang="ts">
import { computed, defineEmits } from 'vue'
import { mdiPalette, mdiFilter, mdiCog } from '@mdi/js'
import { useSettingsStore } from '@/stores/settings'

const settingsStore = useSettingsStore()
const coloringEnabled = computed({
  get: () => settingsStore.coloringEnabled,
  set: (value: boolean) => settingsStore.setColoringEnabled(value),
})
const vocabularyEnabled = computed({
  get: () => settingsStore.vocabularyEnabled,
  set: (value: boolean) => settingsStore.setVocabularyEnabled(value),
})

defineProps<{ isTextTooLong: boolean }>()
defineEmits(['analyze', 'toggle-settings'])
</script>
<template>
  <div class="mt-2 flex items-center justify-between p-2 pl-4 bg-white rounded shadow">
    <!-- Left: Toggles for Coloring and Vocabulary -->
    <div class="flex sm:flex-row flex-col items-start gap-2 sm:gap-6">
      <!-- Coloring toggle -->
      <label class="flex items-center cursor-pointer">
        <input type="checkbox" v-model="coloringEnabled" class="form-checkbox h-5 w-5" />
        <svg class="ml-2 w-5 h-5" viewBox="0 0 24 24">
          <path :d="mdiPalette" fill="currentColor" />
        </svg>
        <span class="ml-1">Coloring</span>
      </label>
      <!-- Vocabulary filtering toggle -->
      <label class="flex items-center cursor-pointer">
        <input type="checkbox" v-model="vocabularyEnabled" class="form-checkbox h-5 w-5" />
        <svg class="ml-2 w-5 h-5" viewBox="0 0 24 24">
          <path :d="mdiFilter" fill="currentColor" />
        </svg>
        <span class="ml-1">Vocabulary</span>
      </label>
    </div>
    <!-- Right: Gear icon and Analyze button -->
    <div class="flex items-center gap-4">
      <!-- Gear icon button -->
      <button
        @click="$emit('toggle-settings')"
        class="flex items-center cursor-pointer focus:outline-none"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path :d="mdiCog" fill="currentColor" />
        </svg>
      </button>
      <button
        @click="$emit('analyze')"
        :disabled="isTextTooLong"
        class="bg-blue-500 text-white font-semibold py-2 px-4 rounded shadow hover:bg-blue-600 transition duration-200 disabled:bg-blue-300 disabled:cursor-not-allowed disabled:hover:bg-blue-300"
      >
        Analyze Text
      </button>
    </div>
  </div>
</template>
