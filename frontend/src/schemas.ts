import { z } from 'zod'

// Schéma pour le type Sense
export const senseSchema = z.object({
  id: z.number(),
  translation: z.string(),
  definition: z.string(),
})

// Schéma pour le type Word
export const wordSchema = z.object({
  id: z.number(),
  written: z.string(),
  category: z.string(),
  senses: z.array(senseSchema),
})

// Schéma pour le type Example (si nécessaire)
export const exampleSchema = z.object({
  category: z.string(),
  example: z.string(),
})

// Schéma pour le type LearnedWord
export const learnedWordSchema = z.object({
  written: z.string(),
  // Utilisation de preprocess pour transformer une chaîne (ou autre) en Date.
  updated_at: z.preprocess((arg) => {
    if (typeof arg === 'string' || arg instanceof Date) {
      return new Date(arg)
    }
    return arg
  }, z.date()),
})

// Schéma pour valider un tableau de LearnedWord
export const learnedWordArraySchema = z.array(learnedWordSchema)
