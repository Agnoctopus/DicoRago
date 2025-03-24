import axios from 'axios'
import type { Analysis, Example, User, VocStatus, ServerLearnedWord, Word } from '@/types'

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
 * @param language - Language to fetch for vocabulary.
 * @returns A Promise resolving to an Analysis object.
 */
export const analyzeText = async (text: string, language: string): Promise<Analysis> => {
  const response = await api.post<Analysis>('/analyze', { text, language })
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
 * Fetches words by their written form from the server.
 * Optionally includes associated senses.
 *
 * @param written - The written form to search for.
 * @param senses - Whether to include the associated senses (default: true).
 * @param language - Language to use for sense translations.
 * @returns A Promise that resolves to an array of Word objects.
 */
export const getWordsFromWritten = async (
  written: string,
  senses: boolean = true,
  language: string = "en_US"
): Promise<Word[]> => {
  const response = await api.get<Word[]>(`/written/${written}/words`, {
    params: { senses, language },
  })
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

/**
 * Updates the learning status of a vocabulary word for the current user.
 *
 * @param written - Written form.
 * @param learned - New learning status (true if learned, false otherwise).
 * @param updated_at - Ttimestamp of the update.
 * @returns A Promise resolving to the previous VocStatus object.
 */
export const updateUserVoc = async (
  written: string,
  learned: boolean,
  updated_at: Date,
): Promise<VocStatus> => {
  const response = await api.put<VocStatus>(`/user/voc`, {
    written: written,
    learned: learned,
    updated_at: updated_at.toISOString(),
  })
  const ret = response.data
  ret.last_update = new Date(`${ret.last_update}Z`)
  return ret
}

/**
 * Updates the learning status for multiple vocabulary words for the current user.
 *
 * @param updates - An array of objects, each containing:
 *    - written: the word's written form,
 *    - learned: the new learning status (true if learned, false otherwise),
 *    - updated_at: the timestamp of the update.
 * @returns A Promise resolving to the previous VocStatus object.
 */
export const updateUserVocs = async (
  updates: { written: string; learned: boolean; updated_at: Date }[],
): Promise<VocStatus> => {
  // Convert each update's timestamp to an ISO string.
  const payload = updates.map(({ written, learned, updated_at }) => ({
    written,
    learned,
    updated_at: updated_at.toISOString(),
  }))

  // Upload the batch of updates.
  const response = await api.put<VocStatus>(`/user/voc/batch`, payload)
  const ret = response.data
  ret.last_update = new Date(`${ret.last_update}Z`)
  return ret
}

/**
 * Retrieves vocabulary words that have been updated since a given date.
 *
 * @param since - Starting date for retrieving.
 * @returns A Promise resolving to an array of LearnedWord objects.
 */
export const getVocSince = async (since: Date): Promise<ServerLearnedWord[]> => {
  const response = await api.get<ServerLearnedWord[]>(`/user/voc/change/${since.toISOString()}`)
  const ret = response.data

  ret.forEach((word) => {
    word.updated_at = new Date(`${word.updated_at}Z`)
  })
  return ret
}

/**
 * Retrieves the current user's vocabulary status.
 *
 * @returns A Promise resolving to a VocStatus object.
 */
export const getStatusVoc = async (): Promise<VocStatus> => {
  const response = await api.get<VocStatus>(`/user/voc/status`)
  const ret = response.data

  ret.last_update = new Date(`${ret.last_update}Z`)

  return ret
}

/**
 * Retrieves all vocabulary words for the current user.
 *
 * @returns A Promise resolving to an array of LearnedWord objects.
 */
export const getVoc = async (): Promise<ServerLearnedWord[]> => {
  const response = await api.get<ServerLearnedWord[]>(`/user/voc`)
  const ret = response.data

  ret.forEach((word) => {
    word.updated_at = new Date(`${word.updated_at}Z`)
  })

  return ret
}

/**
 * Clears all vocabulary words for the current user.
 *
 * @returns A Promise that resolves when the vocabulary has been cleared.
 */
export const clearUserVoc = async (): Promise<void> => {
  await api.delete('/user/voc')
}
