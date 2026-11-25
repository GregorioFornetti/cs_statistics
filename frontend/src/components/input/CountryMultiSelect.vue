<script setup lang="ts">
import { computed } from 'vue'
import type { CountriesByContinent } from '@/types/data'

const props = defineProps<{
  modelValue: string[]
  countriesByContinent: CountriesByContinent
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string[]]
}>()

const allCountries = computed(() =>
  Object.values(props.countriesByContinent).flat(),
)

const allCodes = computed(() =>
  allCountries.value.map(country => country.iso_code),
)

const selectedCount = computed(() => props.modelValue.length)

const allSelected = computed(() =>
  allCodes.value.length > 0 &&
  allCodes.value.every(code => props.modelValue.includes(code)),
)

function continentSelected(continent: string) {
  const countries = props.countriesByContinent[continent] ?? []

  return countries.length > 0 &&
    countries.every(country =>
      props.modelValue.includes(country.iso_code),
    )
}

function toggleCountry(code: string) {
  const selected = new Set(props.modelValue)

  if (selected.has(code)) {
    selected.delete(code)
  } else {
    selected.add(code)
  }

  emit('update:modelValue', [...selected])
}

function toggleContinent(continent: string) {
  const countries = props.countriesByContinent[continent] ?? []
  const codes = countries.map(country => country.iso_code)
  const selected = new Set(props.modelValue)

  if (continentSelected(continent)) {
    codes.forEach(code => selected.delete(code))
  } else {
    codes.forEach(code => selected.add(code))
  }

  emit('update:modelValue', [...selected])
}

function toggleAll() {
  emit('update:modelValue', allSelected.value ? [] : [...allCodes.value])
}

function flagUrl(isoCode: string) {
  return `https://flagcdn.com/w40/${isoCode.toLowerCase()}.png`
}
</script>

<template>
  <section class="space-y-3">
    <div class="flex items-center justify-between">
      <label class="text-sm font-semibold text-gray-800 dark:text-gray-200">
        Countries
      </label>

      <span class="text-xs text-gray-500 dark:text-gray-400">
        {{ selectedCount }} / {{ allCodes.length }} selected
      </span>
    </div>

    <div class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700">
      <!-- Select all -->
      <label
        class="flex cursor-pointer items-center gap-3 border-b border-gray-200
               bg-gray-50 px-4 py-3 dark:border-gray-700 dark:bg-gray-800/70"
      >
        <input
          type="checkbox"
          :checked="allSelected"
          @change="toggleAll"
          class="h-4 w-4 rounded accent-blue-600"
        />

        <span class="text-sm font-semibold">
          Select all countries
        </span>
      </label>

      <!-- Continents -->
      <div class="max-h-80 overflow-y-auto">
        <details
          v-for="(countries, continent) in countriesByContinent"
          :key="continent"
          class="border-b border-gray-100 last:border-0 dark:border-gray-800"
        >
          <summary
            class="flex cursor-pointer list-none items-center gap-3 px-4 py-3
                   transition hover:bg-gray-50 dark:hover:bg-gray-800/50"
          >
            <input
              type="checkbox"
              :checked="continentSelected(continent)"
              @click.stop
              @change="toggleContinent(continent)"
              class="h-4 w-4 rounded accent-blue-600"
            />

            <span class="flex-1 text-sm font-medium">
              {{ continent }}
            </span>

            <span class="text-xs text-gray-500 dark:text-gray-400">
              {{ countries.filter(c => modelValue.includes(c.iso_code)).length }}
              / {{ countries.length }}
            </span>

            <span class="text-xs text-gray-400">▼</span>
          </summary>

          <div class="space-y-1 bg-gray-50/70 px-4 py-2 dark:bg-gray-900/40">
            <label
              v-for="country in countries"
              :key="country.iso_code"
              class="flex cursor-pointer items-center gap-3 rounded-lg px-3 py-2
                     transition hover:bg-white dark:hover:bg-gray-800"
            >
              <input
                type="checkbox"
                :checked="modelValue.includes(country.iso_code)"
                @change="toggleCountry(country.iso_code)"
                class="h-4 w-4 rounded accent-blue-600"
              />

              <img
                :src="flagUrl(country.iso_code)"
                :alt="`${country.name} flag`"
                class="h-auto w-6 rounded-sm object-cover shadow-sm"
                loading="lazy"
              />

              <span class="text-sm text-gray-700 dark:text-gray-300">
                {{ country.name }}
              </span>
            </label>
          </div>
        </details>
      </div>
    </div>
  </section>
</template>