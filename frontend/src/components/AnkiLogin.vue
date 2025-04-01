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
  <div class="max-w-md mx-auto mt-8 text-center font-sans">
    <h2 class="text-2xl font-bold mb-4">Login with Google or Apple</h2>

    <div class="space-y-2">
      <h4 class="text-lg font-bold mb-2">Sign-in</h4>

      <!-- Invisible container for the Google button rendered by the SDK.
             Using display: none to hide it. -->
      <div ref="googleButtonInvisible" style="display: none"></div>

      <!-- Custom visible button that triggers a click on the invisible Google button -->
      <button
        @click="triggerGoogleSignIn"
        class="w-full relative bg-white border border-gray-300 rounded-sm py-2 hover:bg-gray-50"
      >
        <img
          src="@/assets/google-brand.svg"
          alt="Google Logo"
          class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2"
        />
        <span class="block text-center w-full">Sign in with Google</span>
      </button>

      <!-- Apple sign-in button -->
      <button
        @click="handleAppleSignIn"
        class="w-full relative bg-black border border-black text-white rounded-sm py-2 hover:bg-gray-800"
      >
        <img
          src="@/assets/apple-brand.svg"
          alt="Apple Logo"
          class="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2"
        />
        <span class="block text-center w-full">Sign in with Apple</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles can be added here.
   Tailwind CSS is used for styling. */
</style>
