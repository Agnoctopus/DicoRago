<template>
  <div class="max-w-3xl mx-auto p-4">
    <h1 class="text-4xl font-bold mb-8 text-center">Changelog</h1>

    <div v-if="changelogData.length">
      <div v-for="entry in changelogData" :key="entry.version" class="mb-8">
        <article class="border-l-4 pl-4 border-blue-500 shadow rounded p-4">
          <header class="mb-2">
            <div class="flex flex-col md:flex-row md:items-center md:justify-between">
              <div class="flex items-center space-x-4">
                <!-- Release name as the main title -->
                <h2 class="text-2xl font-bold text-blue-700">
                  {{ entry.releaseName }}
                </h2>
                <!-- Version number as a tag -->
                <span class="bg-gray-200 text-gray-800 text-sm font-medium px-2 py-0.5 rounded">
                  v{{ entry.version }}
                </span>
              </div>
              <time class="text-gray-500" :datetime="entry.date">
                {{ formatDate(entry.date) }}
              </time>
            </div>
          </header>
          <ul class="list-disc pl-5">
            <li v-for="(change, idx) in entry.changes" :key="idx">
              <span class="font-bold">{{ change.type }}: </span>
              {{ change.desc }}
            </li>
          </ul>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { changelog as changelogData } from '@/data/changelog'

/**
 * Formats the date in English.
 * @param dateStr - The date in ISO format.
 * @returns The formatted date.
 */
function formatDate(dateStr: string): string {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }
  return new Date(dateStr).toLocaleDateString('en-US', options)
}
</script>

<style scoped>
/* Additional styles can be added here if needed */
</style>
