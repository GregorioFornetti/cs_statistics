<script setup lang="ts">
import { computed, ref } from 'vue'

import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

import CountryMultiSelect from '@/components/input/CountryMultiSelect.vue'
import YearRangeInput from '@/components/input/YearRangeInput.vue'
import VenueSelector from '@/components/input/VenueSelector.vue'

import { appData } from '@/data_loading/appData'
import type { VenueSelection } from '@/types/data'

const countriesByContinent = computed(
  () => appData.value?.countriesByContinent ?? {},
)

const conferences = computed(
  () => appData.value?.conferences ?? {},
)

const journals = computed(
  () => appData.value?.journals ?? {},
)

// Form state
const selectedCountries = ref<string[]>([])

const currentYear = new Date().getFullYear()

const selectedYears = ref<[number, number]>([
  2000,
  currentYear,
])

const selectedVenues = ref<VenueSelection[]>([])

function generateStatistics() {
  const selection = {
    countries: selectedCountries.value,
    yearRange: {
      start: selectedYears.value[0],
      end: selectedYears.value[1],
    },
    venues: selectedVenues.value.map(venue => ({
      id: venue.id,
      name: venue.name,
      type: venue.type,
    })),
  }

  console.log('Generating publications statistics with:', selection)
}
</script>

<template>
  <div class="flex min-h-screen flex-col bg-white dark:bg-gray-950">
    <Header />

    <main class="mx-auto w-full max-w-5xl flex-1 px-6 py-12">
      <div class="mb-10">
        <p class="text-sm font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">
          Statistics
        </p>

        <h1 class="mt-2 text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
          Publications count by university
        </h1>

        <p class="mt-3 max-w-2xl text-gray-600 dark:text-gray-400">
          Configure the filters below to generate a ranking of universities
          based on their publication counts.
        </p>
      </div>

      <form class="space-y-10" @submit.prevent="generateStatistics">
        <!-- Countries -->
        <CountryMultiSelect
          v-model="selectedCountries"
          :countries-by-continent="countriesByContinent"
        />

        <!-- Years -->
        <YearRangeInput
          v-model="selectedYears"
          :min-year="1900"
          :max-year="currentYear"
        />

        <!-- Conferences and journals -->
        <VenueSelector
          v-model="selectedVenues"
          :conferences="conferences"
          :journals="journals"
        />

        <!-- Current selection summary -->
        <div
          class="rounded-xl border border-gray-200 bg-gray-50 p-5
                 dark:border-gray-700 dark:bg-gray-900"
        >
          <h2 class="text-sm font-semibold text-gray-900 dark:text-white">
            Current selection
          </h2>

          <div class="mt-3 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                Countries
              </p>
              <p class="mt-1 text-lg font-semibold">
                {{ selectedCountries.length }}
              </p>
            </div>

            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                Year range
              </p>
              <p class="mt-1 text-lg font-semibold">
                {{ selectedYears[0] }} – {{ selectedYears[1] }}
              </p>
            </div>

            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                Conferences / Journals
              </p>
              <p class="mt-1 text-lg font-semibold">
                {{ selectedVenues.length }}
              </p>
            </div>
          </div>
        </div>
        <div class="flex justify-end">
          <button
            type="submit"
            class="inline-flex items-center gap-2 rounded-lg bg-blue-600
                  px-6 py-3 text-sm font-semibold text-white shadow-sm
                  transition hover:bg-blue-700 active:scale-[0.98]
                  focus-visible:outline-2 focus-visible:outline-offset-2
                  focus-visible:outline-blue-600"
          >
            Generate statistics

            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
          </button>
        </div>
      </form>
    </main>

    <Footer />
  </div>
</template>