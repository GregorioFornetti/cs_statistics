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

export interface Conferences {
  [id: string]: {
    name: string
  }
}

export interface Journals {
  [id: string]: {
    name: string
  }
}

export interface CountriesByContinent {
  [continent: string]: {
    name: string
    iso_code: string
  }[]
}

export type VenueType = 'conference' | 'journal'

export interface VenueSelection {
  id: string
  name: string
  type: VenueType
}

export interface AppData {
  conferences: Conferences
  countriesByContinent: CountriesByContinent
  journals: Journals
  metadata: Metadata
}



export interface LoadError {
  file: string
  message: string
}

export type AppStatus = 'idle' | 'loading' | 'ready' | 'error'

export interface YearRange {
  start: number
  end: number
}

export interface Venue {
  id: string
  name: string
  type: VenueType
}




export interface Institution {
  [institutionId: string]: {
    name: string,
    country?: string,
    countryIsoCode?: string
    state?: string
    city?: string
  }
}

export interface InstitutionsByCountryIsoCode {
  [countryIsoCode: string]: string[]
}

export interface VenuePublicationsCountByYearAndInstitution {
  [year: string]: {
    [institutionId: string]: number
  }
}


export interface UniversityPublicationsCount {
  institutionId: string
  publicationsCount: number
  name: string
  country?: string
  countryIsoCode?: string
}

export interface PublicationsCountByUniversityInput {
  countries: string[]
  yearRange: YearRange
  venues: Venue[]
}