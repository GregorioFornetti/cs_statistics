
import type { LoadError, Venue, YearRange, UniversityPublicationsCount, Institution, InstitutionsByCountryIsoCode, VenuePublicationsCountByYearAndInstitution, PublicationsCountByUniversityInput } from '@/types/data'
import { fetchJson } from '@/data_loading/general'
import { BASE_URL } from '@/types/constants'


const venueTypeToFolderMap: Record<string, string> = {
    'conference': 'conf_count_by_uni',
    'journal': 'journals_count_by_uni',
}

export async function loadPublicationsCountByUniversity(input: PublicationsCountByUniversityInput): Promise<
  | { data: UniversityPublicationsCount[]; errors?: never }
  | { errors: LoadError[]; data?: never }
> {

    const { countries, yearRange, venues } = input
    
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

    const institutionsByCountryIsoCode = values[0] as InstitutionsByCountryIsoCode
    const institutions = values[1] as Institution
    const venuePublicationsCountByYearAndInstitutionList = values.slice(2) as VenuePublicationsCountByYearAndInstitution[]

    // Create a set of institution IDs to process based on the provided countries
    const institutionsIdsToProcess = new Set<string>()
    countries.forEach((countryIsoCode) => {
      const institutionsInCountry = institutionsByCountryIsoCode[countryIsoCode]
      if (institutionsInCountry) {
        institutionsInCountry.forEach((institutionId) => {
          institutionsIdsToProcess.add(institutionId)
        })
      }
    })

    // Create a map to hold the aggregated publication counts
    const aggregatedCounts: Record<string, number> = {}
    for (const venuePublicationsCountByYearAndInstitution of venuePublicationsCountByYearAndInstitutionList) {
      for (const yearStr in venuePublicationsCountByYearAndInstitution) {
        const year = parseInt(yearStr, 10)
        if (year >= yearRange.start && year <= yearRange.end) {
          for (const institutionId in venuePublicationsCountByYearAndInstitution[yearStr]) {
            if (institutionsIdsToProcess.has(institutionId)) {
              const count = venuePublicationsCountByYearAndInstitution[yearStr][institutionId]
              if (!aggregatedCounts[institutionId]) {
                aggregatedCounts[institutionId] = 0
              }
              aggregatedCounts[institutionId] += count || 0
            }
          }
        }
      }
    }

    // Create the final result array
    const result: UniversityPublicationsCount[] = []
    institutionsIdsToProcess.forEach((institutionId) => {
      const institution = institutions[institutionId]
      if (institution) {
        result.push({
          institutionId,
          name: institution.name,
          publicationsCount: aggregatedCounts[institutionId] || 0,
          country: institution.country,
          countryIsoCode: institution.countryIsoCode,
        })
      }
    })
    result.sort((a, b) => b.publicationsCount - a.publicationsCount)

    return { data: result }
}