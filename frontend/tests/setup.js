/**
 * Vitest setup file — runs before each test file.
 * Provides localStorage mock and global cleanup.
 */

// Provide a minimal localStorage mock if not available
if (typeof globalThis.localStorage === 'undefined' || !globalThis.localStorage?.clear) {
  const store = {}
  globalThis.localStorage = {
    getItem: (key) => store[key] ?? null,
    setItem: (key, value) => { store[key] = String(value) },
    removeItem: (key) => { delete store[key] },
    clear: () => { Object.keys(store).forEach((k) => delete store[k]) },
    get length() { return Object.keys(store).length },
    key: (i) => Object.keys(store)[i] ?? null,
  }
}

beforeEach(() => {
  localStorage.clear()
})
