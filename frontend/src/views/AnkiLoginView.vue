<script setup lang="ts">
import { ref } from 'vue'

const googleButtonInvisible = ref<HTMLElement | null>(null) // Invisible container for the Google button

function triggerGoogleSignIn() {
  // Initialize the Google SDK.
  if (window.google && window.google.accounts) {
    window.google.accounts.id.initialize({
      client_id: '738555358973-8t65bo2j79olfbr86l84m7fhr6ckob7v.apps.googleusercontent.com',
      context: 'signin',
      ux_mode: 'redirect',
      login_uri: 'https://agno.re/api/auth/google/anki',
    })
    // Render the Google button in the invisible container.
    if (googleButtonInvisible.value) {
      window.google.accounts.id.renderButton(googleButtonInvisible.value, {
        type: 'icon',
        theme: 'outline',
        size: 'large',
        shape: 'rectangular',
        logo_alignment: 'left',
      })
    }
  }

  if (googleButtonInvisible.value) {
    // Fallback: query for a child div with role="button"
    const div = googleButtonInvisible.value.querySelector(
      'div[role="button"]',
    ) as HTMLElement | null
    if (div) {
      div.click()
    }
  }
}

// Function to trigger Apple sign-in.
function handleAppleSignIn() {
  // Initialize the Apple ID SDK.
  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.init({
      clientId: 'com.DicoRago.webapp',
      scope: 'name email',
      redirectURI: 'https://agno.re/api/auth/apple/anki',
      usePopup: false,
    })
  }

  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.signIn()
  }
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-500 to-indigo-600 p-4"
  >
    <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
      <!-- Logo de l'application et message d'accueil -->
      <div class="flex flex-col items-center mb-6">
        <img
          src="@/assets/icon.png"
          alt=""
          class="w-48 h-48 rounded-full border-2 shadow-lg mb-4"
        />
        <h2 class="text-3xl font-bold text-center text-gray-800 mb-2">Welcome to Dicorago</h2>
        <p class="text-gray-600 text-center">
          Sign in to sync your vocabulary with Anki and manage your decks
        </p>
      </div>

      <div class="space-y-4">
        <!-- Invisible container for the Google button rendered by the SDK -->
        <div ref="googleButtonInvisible" class="hidden"></div>

        <!-- Bouton personnalisé pour déclencher la connexion Google -->
        <button
          @click="triggerGoogleSignIn"
          class="w-full relative flex items-center justify-center px-4 py-3 bg-white border border-gray-300 rounded-sm shadow hover:bg-gray-50 transition"
        >
          <img src="@/assets/google-brand.svg" alt="Google Logo" class="w-6 h-6 absolute left-4" />
          <span class="font-medium text-gray-700 whitespace-nowrap">Sign in with Google</span>
        </button>

        <!-- Bouton de connexion Apple -->
        <button
          @click="handleAppleSignIn"
          class="w-full relative flex items-center justify-center px-4 py-3 bg-black border border-black rounded-sm shadow hover:bg-gray-800 transition"
        >
          <img src="@/assets/apple-brand.svg" alt="Apple Logo" class="w-6 h-6 absolute left-4" />
          <span class="font-medium text-white whitespace-nowrap">Sign in with Apple</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Vous pouvez ajouter des styles personnalisés supplémentaires ici si nécessaire */
</style>
