/**
 * Represents a single change entry.
 */
export interface Change {
  type: string // e.g., "Feature", "Enhancement", "Fix", "API", "Critical"
  desc: string // A short description of the change
}

/**
 * Represents a single version entry in the changelog.
 */
export interface ChangelogEntry {
  version: string // Version number (e.g., "2")
  releaseName: string // Release name (e.g., "Odeng")
  date: string // ISO date string (e.g., "2025-03-31")
  changes: Change[] // List of changes for this release
}

/**
 * Changelog data for version 2: "Odeng" and version 1: "Initial Release".
 */
export const changelog: ChangelogEntry[] = [
  {
    version: '2',
    releaseName: 'Odeng',
    date: '2025-03-25',
    changes: [
      { type: 'Feature', desc: 'Track learned words on Dictionary page.' },
      { type: 'Feature', desc: 'Redesigned navigation with separate views.' },
      { type: 'Feature', desc: 'Export vocabulary in CSV/JSON.' },
      { type: 'Feature', desc: 'Import vocabulary in CSV/JSON.' },
      { type: 'Feature', desc: 'Multilingual dictionary support (FR, EN, others).' },
      { type: 'Feature', desc: 'New dictionary view.' },
      { type: 'Feature', desc: 'New settings view.' },
      { type: 'Feature', desc: 'Added Zen/Underline reading mode.' },
      { type: 'Feature', desc: 'Updated app icon.' },
      { type: 'Feature', desc: 'Manual vocabulary deletion via settings.' },
      { type: 'Feature', desc: 'New editing settings.' },
      { type: 'Feature', desc: 'Language selector in settings.' },
      { type: 'Feature', desc: 'Apple login support.' },
      { type: 'Feature', desc: 'Google login support.' },
      { type: 'Feature', desc: 'Dictionary language selection.' },
      { type: 'Feature', desc: 'Create DicoRago account via Threads/X.' },
      { type: 'Feature', desc: 'New vocabulary sync system.' },
      { type: 'Enhancement', desc: 'Colorize only unknown words.' },
      { type: 'Enhancement', desc: 'Track history of added words.' },
      { type: 'Fix', desc: 'Show blank line when vocabulary is empty.' },
      { type: 'Critical', desc: 'Mandatory iOS update.' },
    ],
  },
  {
    version: '1',
    releaseName: 'Gimpbap',
    date: '2025-02-18',
    changes: [
      { type: 'Feature', desc: 'Text analysis: breakdown & translations.' },
      { type: 'Feature', desc: 'Color-coded word recognition.' },
      { type: 'Feature', desc: 'Vocabulary filtering.' },
      { type: 'Feature', desc: 'In-depth word exploration (meanings, examples).' },
      { type: 'Feature', desc: 'Personal dictionary management.' },
      { type: 'Feature', desc: 'Grammar structure analysis.' },
    ],
  },
]
