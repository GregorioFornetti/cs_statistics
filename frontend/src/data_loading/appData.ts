
import { ref, shallowRef } from 'vue'
import type { AppData, Conferences, CountriesByContinent, Journals, Metadata, LoadError, AppStatus } from '@/types/data'
import { BASE_URL } from '@/types/constants'


const resources = [
  {
    key: 'conferences',
    file: 'conferences.json',
    url: `${BASE_URL}/conferences.json`,
  },
  {
    key: 'countriesByContinent',
    file: 'countries_by_continent.json',
    url: `${BASE_URL}/countries_by_continent.json`,
  },
  {
    key: 'journals',
    file: 'journals.json',
    url: `${BASE_URL}/journals.json`,
  },
  {
    key: 'metadata',
    file: 'metadata.json',
    url: `${BASE_URL}/metadata.json`,
  },
] as const

export const appStatus = ref<AppStatus>('idle')
export const appData = shallowRef<AppData | null>(null)
export const appLoadErrors = ref<LoadError[]>([])

let pendingRequest: Promise<void> | null = null

async function fetchJson(url: string): Promise<unknown> {
  const response = await fetch(url)

  if (!response.ok) {
    throw new Error(
      `HTTP ${response.status}: ${response.statusText}`,
    )
  }

  return response.json()
}

export async function loadAppData(): Promise<void> {
  // Avoid unnecessary requests if everything is already loaded.
  if (appStatus.value === 'ready') return

  // Avoid concurrent duplicate requests.
  if (pendingRequest) return pendingRequest

  appStatus.value = 'loading'
  appLoadErrors.value = []

  pendingRequest = (async () => {
    const results = await Promise.allSettled(
      resources.map((resource) => fetchJson(resource.url)),
    )

    const errors: LoadError[] = []

    results.forEach((result, index) => {
      if (result.status === 'rejected') {
        errors.push({
          file: resources[index]!.file,
          message:
            result.reason instanceof Error
              ? result.reason.message
              : 'Unknown error',
        })
      }
    })

    if (errors.length > 0) {
      appData.value = null
      appLoadErrors.value = errors
      appStatus.value = 'error'
      return
    }

    const values = results.map(
      (result) =>
        (result as PromiseFulfilledResult<unknown>).value,
    )

    appData.value = {
      conferences: values[0] as Conferences,
      countriesByContinent: values[1] as CountriesByContinent,
      journals: values[2] as Journals,
      metadata: values[3] as Metadata,
    }

    appStatus.value = 'ready'
  })().finally(() => {
    pendingRequest = null
  })

  return pendingRequest
}