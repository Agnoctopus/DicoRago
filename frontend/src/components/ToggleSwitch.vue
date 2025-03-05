<!-- ToggleSwitch.vue -->
<template>
  <!-- Toggle switch with hidden checkbox and styled slider -->
  <label class="switch relative inline-block w-10 h-6">
    <input type="checkbox" v-model="model" :disabled="disabled" class="opacity-0 w-0 h-0" />
    <span
      class="slider absolute cursor-pointer top-0 left-0 right-0 bottom-0 bg-gray-300 transition-all duration-300 rounded-full"
    ></span>
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Define props for v-model and disabled state.
const props = defineProps<{
  modelValue: boolean
  disabled?: boolean
}>()

// Emit update event for v-model binding.
const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

// Computed property to simplify v-model usage.
const model = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit('update:modelValue', value),
})
</script>

<style scoped>
.switch input:checked + .slider {
  background-color: #4ade80;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.2s;
  border-radius: 1000px;
}

.slider:before {
  position: absolute;
  content: '';
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

.switch input:checked + .slider:before {
  transform: translateX(16px);
}
</style>
