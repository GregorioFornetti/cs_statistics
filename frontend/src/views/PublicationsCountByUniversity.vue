<script setup lang="ts">
import { computed, ref } from 'vue'

import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

import CountryMultiSelect from '@/components/input/CountryMultiSelect.vue'
import YearRangeInput from '@/components/input/YearRangeInput.vue'
import VenueSelector from '@/components/input/VenueSelector.vue'

import { appData } from '@/stores/appData'
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

      <form class="space-y-10" @submit.prevent>
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
      </form>
    </main>

    <Footer />
  </div>
</template>