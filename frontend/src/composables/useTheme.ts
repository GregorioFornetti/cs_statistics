
import { ref, watch } from 'vue'

export type Theme = 'light' | 'dark'

const savedTheme = localStorage.getItem('theme') as Theme | null

const theme = ref<Theme>(
  savedTheme === 'dark' || savedTheme === 'light'
    ? savedTheme
    : 'light'
)

watch(
  theme,
  (value) => {
    document.documentElement.classList.toggle('dark', value === 'dark')
    localStorage.setItem('theme', value)
  },
  { immediate: true }
)

export function useTheme() {
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
  }

  return {
    theme,
    toggleTheme,
  }
}
