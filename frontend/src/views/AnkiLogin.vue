<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'

const token = ref<string | null>(null)
const redirectUri = ref('')
const googleButtonInvisible = ref<HTMLElement | null>(null) // Invisible container for the Google button

function triggerGoogleSignIn() {
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

// Utility function to load an external script.
function loadScript(src: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.defer = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Error loading script: ${src}`))
    document.head.appendChild(script)
  })
}

// Function to trigger Apple sign-in.
function handleAppleSignIn() {
  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.signIn()
  }
}

onMounted(() => {
  // Retrieve the redirect_uri parameter from the URL.
  const params = new URLSearchParams(window.location.search)
  redirectUri.value = params.get('redirect_uri') || window.location.origin

  // If a token is already present, redirect immediately.
  const urlToken = params.get('token')
  if (urlToken) {
    token.value = urlToken
    const redirectUrl = new URL(redirectUri.value)
    redirectUrl.searchParams.append('token', urlToken)
    window.location.href = redirectUrl.toString()
  }

  Promise.all([
    loadScript('https://accounts.google.com/gsi/client'),
    loadScript(
      'https://appleid.cdn-apple.com/appleauth/static/jsapi/appleid/1/en_US/appleid.auth.js',
    ),
  ])
    .then(() => {
      // Initialize the Google SDK.
      if (window.google && window.google.accounts) {
        window.google.accounts.id.initialize({
          client_id: '738555358973-8t65bo2j79olfbr86l84m7fhr6ckob7v.apps.googleusercontent.com',
          context: 'signin',
          ux_mode: 'redirect',
          login_uri: 'https://agno.re/api/auth/google/anki',
        })
        // Render the Google button in the invisible container.
        nextTick(() => {
          console.log(googleButtonInvisible.value)
          if (googleButtonInvisible.value) {
            window.google.accounts.id.renderButton(googleButtonInvisible.value, {
              type: 'icon',
              theme: 'outline',
              size: 'large',
              shape: 'rectangular',
              logo_alignment: 'left',
            })
          }
        })
      }
      // Initialize the Apple ID SDK.
      if (window.AppleID && window.AppleID.auth) {
        window.AppleID.auth.init({
          clientId: 'com.DicoRago.webapp',
          scope: 'name email',
          redirectURI: 'https://agno.re/api/auth/apple/anki',
          usePopup: false,
        })
      }
    })
    .catch((error) => {
      console.error(error.message)
    })
})
</script>

<template>
  <div class="max-w-md mx-auto mt-8 text-center font-sans">
    <h2 class="text-2xl font-bold mb-4">Login with Google or Apple</h2>
    <!-- If a token is present, show a success message -->
    <div v-if="token">
      <p class="text-green-500">Authentication successful. Redirecting…</p>
    </div>
    <!-- Otherwise, display the sign-in buttons -->
    <div v-else>
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
  </div>
</template>

<style scoped>
/* Additional custom styles can be added here.
   Tailwind CSS is used for styling. */
</style>
