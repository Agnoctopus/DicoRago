<script setup lang="ts">
import { computed } from 'vue'
import { mdiPalette, mdiFilter, mdiCog } from '@mdi/js'
import { useSettingsStore } from '@/stores/settings'
import { useUserStore } from '@/stores/user'

const settingsStore = useSettingsStore()
const userStore = useUserStore()

const coloringEnabled = computed({
  get: () => settingsStore.coloringEnabled,
  set: (value: boolean) => settingsStore.setColoringEnabled(value),
})
const vocabularyEnabled = computed({
  get: () => settingsStore.vocabularyEnabled,
  set: (value: boolean) => settingsStore.setVocabularyEnabled(value),
})

// Access the logged-in user from the store.
const user = computed(() => userStore.user)

// Compute initials if no picture is provided.
const initials = computed(() => {
  if (!user.value || !user.value.name) return ''
  const names = user.value.name.split(' ')
  return names.length === 1
    ? names[0].charAt(0).toUpperCase()
    : names[0].charAt(0).toUpperCase() + names[1].charAt(0).toUpperCase()
})

defineProps<{ isTextTooLong: boolean }>()
defineEmits(['analyze', 'toggle-settings'])
</script>

<template>
  <div class="mt-2 flex items-center justify-between p-2 sm:pl-4 bg-white rounded shadow">
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
    <!-- Right: Container for Avatar and Gear Icon -->
    <div class="flex items-center gap-3">
      <div
        class="flex items-center space-x-1 p-0.75 rounded-3xl transition-colors duration-300"
        :class="
          user ? 'bg-gray-100 border border-gray-400 cursor-pointer' : 'border border-transparent'
        "
        @click="user && $emit('toggle-settings')"
      >
        <!-- Fixed placeholder for the avatar -->
        <div class="w-8 h-8 relative flex-shrink-0">
          <transition name="fade">
            <!-- Using v-show ensures that the element remains in the DOM,
                 so the placeholder’s space is never lost -->
            <div v-show="!!user" class="absolute inset-0">
              <template v-if="user && user.picture">
                <img :src="user.picture" alt="" class="w-8 h-8 rounded-full" />
              </template>
              <template v-else-if="user">
                <div
                  class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center text-sm font-semibold"
                >
                  {{ initials }}
                </div>
              </template>
            </div>
          </transition>
        </div>
        <!-- Gear icon; if no user, add an independent click handler -->
        <svg
          class="w-5 h-5"
          :class="{ 'cursor-pointer': !user }"
          @click="!user && $emit('toggle-settings')"
          viewBox="0 0 24 24"
        >
          <path :d="mdiCog" fill="currentColor" />
        </svg>
      </div>
      <!-- Analyze button -->
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

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
