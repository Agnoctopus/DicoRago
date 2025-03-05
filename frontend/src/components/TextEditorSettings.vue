<script setup lang="ts">
import { computed, defineEmits } from 'vue'
import ToggleSwitch from '@/components/ToggleSwitch.vue'
import { mdiPalette } from '@mdi/js'
import { useSettingsStore } from '@/stores/settings'

// Emit a 'close' event when the settings overlay should be closed.
defineEmits<{ (e: 'close'): void }>()

const settingsStore = useSettingsStore()

// Computed proxy for onlyUnknownColoring using the store.
const onlyUnknown = computed({
  get: () => settingsStore.onlyUnknownColoring,
  set: (value: boolean) => settingsStore.setOnlyUnknownColoring(value),
})
</script>

<template>
  <!-- Full-screen overlay with backdrop blur. Clicking outside closes the panel. -->
  <div
    class="fixed top-0 left-0 w-screen h-screen flex items-center justify-center backdrop-blur-sm z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white p-6 border border-gray-300 rounded-md shadow-lg w-11/12 max-w-md">
      <!-- Header with title and close button -->
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-xl font-bold m-0">Settings</h3>
        <button
          class="bg-transparent border-0 text-2xl leading-none cursor-pointer focus:outline-none"
          @click="$emit('close')"
        >
          ×
        </button>
      </div>
      <hr class="border-t border-gray-300 mb-4" />
      <!-- Option: Toggle for coloring only unknown words -->
      <div class="space-y-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <!-- Palette icon -->
            <svg class="w-6 h-6 mr-2" viewBox="0 0 24 24">
              <path :d="mdiPalette" fill="currentColor" />
            </svg>
            <span>Color only unknown words</span>
          </div>
          <!-- Toggle switch bound to onlyUnknown -->
          <ToggleSwitch v-model="onlyUnknown" />
        </div>
      </div>
    </div>
  </div>
</template>
