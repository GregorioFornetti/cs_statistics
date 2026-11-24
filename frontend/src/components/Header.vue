
<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useTheme } from '../composables/useTheme'

const { theme, toggleTheme } = useTheme()
</script>

<template>
  <header
    class="sticky top-0 z-50 border-b border-gray-200
           bg-white/90 backdrop-blur-md
           dark:border-gray-800 dark:bg-gray-950/90"
  >
    <nav
      class="mx-auto flex h-16 max-w-7xl items-center
             justify-between px-6"
    >
      <RouterLink
        to="/"
        class="flex items-center gap-2 rounded-lg px-3 py-2
               text-sm font-semibold transition-colors
               hover:bg-gray-100 hover:text-blue-600
               dark:hover:bg-gray-800 dark:hover:text-blue-400"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="m3 10 9-7 9 7" />
          <path d="M5 9v12h14V9" />
          <path d="M9 21v-8h6v8" />
        </svg>
        Home
      </RouterLink>

      <button
        type="button"
        @click="toggleTheme"
        :aria-label="theme === 'light'
          ? 'Switch to dark mode'
          : 'Switch to light mode'"
        class="flex h-10 w-10 items-center justify-center
               rounded-full text-gray-600 transition-all
               hover:bg-gray-100 hover:text-gray-900
               dark:text-gray-300 dark:hover:bg-gray-800
               dark:hover:text-white"
      >
        <!-- Moon -->
        <svg
          v-if="theme === 'light'"
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M20.9 13A9 9 0 0 1 11 3.1
                   9 9 0 1 0 20.9 13Z" />
        </svg>

        <!-- Sun -->
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="12" cy="12" r="4" />
          <path d="M12 2v2" />
          <path d="M12 20v2" />
          <path d="m4.93 4.93 1.42 1.42" />
          <path d="m17.65 17.65 1.42 1.42" />
          <path d="M2 12h2" />
          <path d="M20 12h2" />
          <path d="m6.35 17.65-1.42 1.42" />
          <path d="m19.07 4.93-1.42 1.42" />
        </svg>
      </button>
    </nav>
  </header>
</template>
