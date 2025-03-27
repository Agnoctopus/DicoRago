import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { getUser } from '@/api'
import type { User } from '@/types'

// User store to manage authentication state.
export const useUserStore = defineStore('user', () => {
  // Reactive state: user data and fetch status.
  const user = ref<User | null>(null)
  const isFetched = ref(false)

  /**
   * Fetch user data from the API if not already fetched.
   */
  async function fetchUser() {
    if (isFetched.value) return
    try {
      user.value = await getUser()
    } catch (error: unknown) {
      let message = 'Unknown error'
      if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail
        if (detail) {
          console.info("Couldn't fetch the user:", detail)
        } else {
          message = error.message
          console.error('Error fetching user:', message)
        }
      } else if (error instanceof Error) {
        message = error.message
        console.error('Error fetching user:', message)
      }
      user.value = null
    }
    isFetched.value = true
  }

  /**
   * Refresh user data from the API.
   */
  async function refreshUser() {
    try {
      user.value = await getUser()
    } catch (error: unknown) {
      let message = 'Unknown error'
      if (axios.isAxiosError(error)) {
        message = error.response?.data?.detail || error.message
      } else if (error instanceof Error) {
        message = error.message
      }
      console.error('Error refreshing user:', message)
      user.value = null
    }
  }

  return { user, isFetched, fetchUser, refreshUser }
})
