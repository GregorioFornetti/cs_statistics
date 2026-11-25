
import { ref, shallowRef } from 'vue'
import type { Conferences, CountriesByContinent, Journals, Metadata, LoadError, Venue, YearRange, UniversityPublicationsCount } from '@/types/data'
import { fetchJson } from '@/data_loading/general'
import { BASE_URL } from '@/types/constants'


const venueTypeToFolderMap: Record<string, string> = {
    'conference': 'conf_count_by_uni',
    'journal': 'journals_count_by_uni',
}

export async function loadPublicationsCountByUniversity(countries: string[], yearRange: YearRange, venues: Venue[]): Promise<{ errors?: LoadError[], data?: UniversityPublicationsCount[] }> {

    const resources = [
        `${BASE_URL}/institutions_by_country_iso_codes.json`,
        `${BASE_URL}/institutions.json`,
        ...venues.map(venue => `${BASE_URL}/${venueTypeToFolderMap[venue.type]}/${venue.id}.json`)
    ]

    const results = await Promise.allSettled(
      resources.map((resource) => fetchJson(resource)),
    )

    const errors: LoadError[] = []

    results.forEach((result, index) => {
      if (result.status === 'rejected') {
        errors.push({
          file: resources[index]!,
          message:
            result.reason instanceof Error
              ? result.reason.message
              : 'Unknown error',
        })
      }
    })

    if (errors.length > 0) {
      return { errors }
    }

    const values = results.map(
      (result) =>
        (result as PromiseFulfilledResult<unknown>).value,
    )

    // TODO PROCESS THE DATA

    return { data: values as UniversityPublicationsCount[] }
}