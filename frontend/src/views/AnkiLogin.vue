<script setup lang="ts">
import { ref, onMounted } from 'vue'

const token = ref<string | null>(null)
const redirectUri = ref('')

// Interface for Google Credential Response.
interface GoogleCredentialResponse {
  credential: string
}

// Callback to be invoked by Google SDK upon successful login.
function handleGoogleCredentialResponse(response: GoogleCredentialResponse) {
  const t = response.credential
  token.value = t
  // Build the redirect URL by appending the token as a query parameter.
  const redirectUrl = new URL(redirectUri.value)
  redirectUrl.searchParams.append('token', t)
  window.location.href = redirectUrl.toString()
}

// Trigger Google sign-in prompt if the SDK is available.
function handleGoogleSignIn() {
  if (window.google && window.google.accounts) {
    window.google.accounts.id.prompt()
  }
}

// Trigger Apple sign-in if the SDK is available.
function handleAppleSignIn() {
  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.signIn()
  }
}

onMounted(() => {
  // Retrieve the redirect_uri parameter from the URL.
  const params = new URLSearchParams(window.location.search)
  redirectUri.value = params.get('redirect_uri') || window.location.origin

  // If a token is already present (from a previous redirect), redirect immediately.
  const urlToken = params.get('token')
  if (urlToken) {
    token.value = urlToken
    const redirectUrl = new URL(redirectUri.value)
    redirectUrl.searchParams.append('token', urlToken)
    window.location.href = redirectUrl.toString()
  }

  // Initialize Google SDK in redirect mode.
  if (window.google && window.google.accounts) {
    window.google.accounts.id.initialize({
      client_id: '738555358973-8t65bo2j79olfbr86l84m7fhr6ckob7v.apps.googleusercontent.com',
      context: 'signin',
      ux_mode: 'redirect',
      login_uri: 'https://dicorago.com/api/auth/anki/google',
      callback: handleGoogleCredentialResponse,
    })
  }

  // Initialize Apple ID SDK if available.
  if (window.AppleID && window.AppleID.auth) {
    window.AppleID.auth.init({
      clientId: 'com.DicoRago.webapp',
      scope: 'name email',
      redirectURI: 'https://dicorago.com/api/auth/anki/apple',
      usePopup: false,
    })
  }
})
</script>

<template>
  <div class="max-w-md mx-auto mt-8 text-center font-sans">
    <h2 class="text-2xl font-bold mb-4">Login with Google or Apple</h2>
    <!-- If token is present, show success message -->
    <div v-if="token">
      <p class="text-green-500">Authentication successful. Redirecting...</p>
    </div>
    <!-- Otherwise, show sign-in buttons -->
    <div v-else>
      <div class="space-y-4">
        <button
          @click="handleGoogleSignIn"
          class="w-full relative bg-white border border-gray-300 rounded-sm py-2 hover:bg-gray-50 flex items-center justify-center"
        >
          <img src="@/assets/google-brand.svg" alt="Google Logo" class="w-5 h-5 mr-2" />
          <span>Sign in with Google</span>
        </button>
        <button
          @click="handleAppleSignIn"
          class="w-full relative bg-black border border-black text-white rounded-sm py-2 hover:bg-gray-800 flex items-center justify-center"
        >
          <img src="@/assets/apple-brand.svg" alt="Apple Logo" class="w-5 h-5 mr-2" />
          <span>Sign in with Apple</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Tailwind CSS is used for styling; add any additional custom styles here if needed. */
</style>
