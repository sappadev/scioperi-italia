"""Costanti per Scioperi Italia."""

DOMAIN = "scioperi_italia"
CONF_RSS_URL = "rss_url"
CONF_REGION_FILTER = "region_filter"
CONF_SECTOR_FILTER = "sector_filter"

DEFAULT_RSS_URL = "https://scioperi.mit.gov.it/mit2/public/scioperi/rss"

# Update intervals
UPDATE_INTERVAL_HOURS = 6
UPDATE_INTERVAL_SECONDS = UPDATE_INTERVAL_HOURS * 3600

# Settori (dal feed RSS reale)
SECTORS = [
    "Trasporto pubblico locale",
    "Aereo",
    "Ferroviario",
    "Trasporto merci e logistica",
    "Marittimo",
    "Tutti"
]

# Rilevanza
RELEVANCE_TYPES = [
    "Nazionale",
    "Regionale", 
    "Provinciale",
    "Locale",
    "Territoriale",
    "Interregionale"
]

# Regioni italiane
REGIONS = [
    "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna",
    "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche",
    "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana",
    "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto", "Italia", "Tutte"
]

# Sensor types
SENSOR_TYPE_COUNT = "count"
SENSOR_TYPE_NEXT = "next"
SENSOR_TYPE_TODAY = "today"

# Attributes
ATTR_STRIKES = "strikes"
ATTR_SECTOR = "sector"
ATTR_REGION = "region"
ATTR_PROVINCE = "province"
ATTR_START_DATE = "start_date"
ATTR_END_DATE = "end_date"
ATTR_RELEVANCE = "relevance"
ATTR_MODALITY = "modality"
ATTR_UNIONS = "unions"
ATTR_CATEGORY = "category"
ATTR_PROCLAMATION_DATE = "proclamation_date"