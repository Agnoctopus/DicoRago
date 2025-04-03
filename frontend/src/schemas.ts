import { z } from 'zod'

// Schéma pour le type Sense
export const SenseSchema = z.object({
  id: z.number(),
  translation: z.string(),
  definition: z.string(),
})

// Schéma pour le type Word
export const WordSchema = z.object({
  id: z.number(),
  written: z.string(),
  category: z.string(),
  senses: z.array(SenseSchema),
})

// Schéma pour le type Example (si nécessaire)
export const ExampleSchema = z.object({
  category: z.string(),
  example: z.string(),
})

// Schéma pour le type VocabWord
export const VocabWordSchema = z.object({
  written: z.string(),
  status: z.string(),
  // Utilisation de preprocess pour transformer une chaîne (ou autre) en Date.
  updated_at: z.preprocess((arg) => {
    if (typeof arg === 'string' || arg instanceof Date) {
      return new Date(arg)
    }
    return arg
  }, z.date()),
})

// Schéma pour valider un tableau de VocabWord
export const VocabWordArraySchema = z.array(VocabWordSchema)
