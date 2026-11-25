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