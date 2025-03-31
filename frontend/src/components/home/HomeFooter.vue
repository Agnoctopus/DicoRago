<template>
  <footer class="bg-gray-800">
    <div class="max-w-6xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <!-- Organisation en deux zones : copyright et liens -->
      <div class="flex flex-col md:flex-row justify-between items-center">
        <!-- Copyright -->
        <div class="mb-4 md:mb-0 text-center md:text-left">
          <p class="text-sm text-gray-400">&copy; 2025 DicoRago. All rights reserved.</p>
        </div>
        <!-- Liens de navigation, contact et réseaux sociaux avec icônes -->
        <div class="flex flex-wrap justify-center items-center gap-x-4 gap-y-2">
          <a
            href="/privacy"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiLock" />
            </svg>
            Privacy
          </a>
          <a
            href="/support"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiLifebuoy" />
            </svg>
            Support
          </a>
          <a
            href="mailto:contact@dicorago.com"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiEmailOutline" />
            </svg>
            Email
          </a>
          <a
            href="https://x.com/dicorago"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiTwitter" />
            </svg>
            Twitter
          </a>
          <a
            href="https://www.threads.net/@dicorago"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiInstagram" />
            </svg>
            Threads
          </a>
          <a
            href="https://github.com/Agnoctopus/DicoRago"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiGithub" />
            </svg>
            GitHub
          </a>
          <a
            href="/changelog"
            class="flex items-center text-sm text-gray-300 hover:text-white transition-colors"
          >
            <svg class="w-5 h-5 mr-1 text-gray-400" viewBox="0 0 24 24" fill="currentColor">
              <path :d="mdiHistory" />
            </svg>
            Changelog
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { mdiLock, mdiLifebuoy, mdiEmailOutline, mdiTwitter, mdiInstagram, mdiGithub, mdiHistory } from '@mdi/js';
</script>

<style scoped>
</style>
