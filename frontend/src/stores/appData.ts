import { ref, shallowRef } from 'vue'

export type AppStatus = 'idle' | 'loading' | 'ready' | 'error'

export interface Metadata {
  creators: number
  publications: number
  streams: number
  institutions: number
  identifiers: number
  signatures: number
  affiliations: number
  locations: number
  versionrels: number
  triples: number
  externalURIs: number
  raw_data_origin: string
  download_date: string
}

export interface AppData {
  conferences: unknown
  countriesByContinent: unknown
  journals: unknown
  metadata: Metadata
}

export interface LoadError {
  file: string
  message: string
}

const BASE_URL =
  'https://raw.githubusercontent.com/GregorioFornetti/cs_statistics/main/data/processed'

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
          file: resources[index].file,
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
      conferences: values[0],
      countriesByContinent: values[1],
      journals: values[2],
      metadata: values[3],
    }

    appStatus.value = 'ready'
  })().finally(() => {
    pendingRequest = null
  })

  return pendingRequest
}