import axios from 'axios'
import type { Analysis, Example, User } from '@/types'

/** Base URL for the REST API */
export const restAPIBaseURL = 'http://localhost:8000'

/** Axios instance with the REST API base URL preset */
export const api = axios.create({
  baseURL: restAPIBaseURL,
  withCredentials: true,
})

/**
 * Analyzes the provided text.
 * @param text - Text to be analyzed.
 * @returns A Promise resolving to an Analysis object.
 */
export const analyzeText = async (text: string): Promise<Analysis> => {
  const response = await api.post<Analysis>('/analyze', { text })
  return response.data
}

/**
 * Retrieves examples for a given sense.
 * @param sense_id - Unique identifier of the sense.
 * @returns A Promise resolving to an array of Example objects.
 */
export const getExamples = async (sense_id: number): Promise<Example[]> => {
  const response = await api.get<Example[]>(`/senses/${sense_id}/examples`)
  return response.data
}

/**
 * Retrieves the current user's data.
 * @returns A Promise resolving to a User object or null if no user is authenticated.
 */
export const getUser = async (): Promise<User | null> => {
  const response = await api.get<User>('/user/me')
  return response.data
}
