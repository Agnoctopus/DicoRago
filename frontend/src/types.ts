/**
 * Represents a morpheme.
 */
export interface Morph {
  /** Lexeme. */
  lex: string
  /** Grammatical tag. */
  tag: string
}

/**
 * Represents an analysed linguistic unit.
 */
export interface Unit {
  /** Word form. */
  word: string
  /** Optional vocabulary form. */
  vocabulary?: string
  /** Surface form. */
  surface: string
  /** Associated morphemes. */
  morphs: Morph[]
}

/**
 * Represents the complete analysis result.
 */
export interface Analysis {
  /** Analyzed units. */
  units: Unit[]
  /** Vocabulary from analysis. */
  vocab: Word[]
}

/**
 * Represents an example usage of a sense.
 */
export interface Example {
  /** Example category. */
  category: string
  /** Example text. */
  example: string
}

/**
 * Represents a sense of a word.
 */
export interface Sense {
  /** Unique identifier. */
  id: number
  /** Translation written form. */
  translation: string
  /** Translation definition. */
  definition: string
}

/**
 * Represents a word.
 */
export interface Word {
  /** Unique identifier. */
  id: number
  /** Written form. */
  written: string
  /** Word category. */
  category: string
  /** Associated senses. */
  senses: Sense[]
}

/**
 * Represents a user.
 */
export interface User {
  /** Username. */
  name: string
  /** E-mail. */
  email: string
  /** Link to avatar picture. */
  picture?: string
}

/**
 * Represents the vocabulary status.
 */
export interface VocStatus {
  /** Total number of words learned. */
  learned_count: number
  /** Timestamp of the most recent vocabulary update. */
  last_update: Date
}

/**
 * Represents a local learned word.
 */
export interface LearnedWord {
  /** Written form. */
  written: string
  /** Timestamp of the last update. */
  updated_at: Date
}

/**
 * Represents a learned word from server.
 */
export interface ServerLearnedWord {
  /** Written form. */
  written: string
  /** Whether the word is learned. */
  learned: boolean
  /** Timestamp of the last update. */
  updated_at: Date
}
