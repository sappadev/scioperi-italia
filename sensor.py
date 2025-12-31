"""Sensor platform for Scioperi Italia."""
import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    SECTORS,
    ATTR_STRIKES,
    ATTR_SECTOR,
    ATTR_REGION,
    ATTR_START_DATE,
    ATTR_END_DATE,
    ATTR_MODALITY,
    ATTR_RELEVANCE,
)
from .coordinator import ScioperiCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Scioperi Italia sensors."""
    coordinator: ScioperiCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []
    
    # Main sensors
    sensors.append(ScioperiCountSensor(coordinator))
    sensors.append(ScioperiTodaySensor(coordinator))
    sensors.append(ScioperiNextSensor(coordinator))
    
    # Sector-specific sensors
    for sector in SECTORS:
        if sector != "Tutti":
            sensors.append(ScioperiSectorSensor(coordinator, sector))
    
    async_add_entities(sensors)


class ScioperiBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for Scioperi Italia sensors."""

    def __init__(self, coordinator: ScioperiCoordinator, name: str, icon: str) -> None:
        """Initialize base sensor."""
        super().__init__(coordinator)
        self._attr_name = f"Scioperi {name}"
        self._attr_icon = icon
        self._attr_unique_id = f"scioperi_{name.lower().replace(' ', '_')}"


class ScioperiCountSensor(ScioperiBaseSensor):
    """Sensor for total strike count."""

    def __init__(self, coordinator: ScioperiCoordinator) -> None:
        """Initialize sensor."""
        super().__init__(coordinator, "Totali", "mdi:alert-circle")

    @property
    def native_value(self) -> int:
        """Return the state."""
        return len(self.coordinator.strikes)

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        strikes = self.coordinator.strikes[:10]  # Limit to 10 for attributes
        
        return {
            ATTR_STRIKES: [
                {
                    "sector": s.get(ATTR_SECTOR, ""),
                    "region": s.get(ATTR_REGION, ""),
                    "start_date": s.get("start_date_str", ""),
                    "relevance": s.get(ATTR_RELEVANCE, ""),
                }
                for s in strikes
            ],
            "last_update": self.coordinator.data.get("last_update"),
        }


class ScioperiTodaySensor(ScioperiBaseSensor):
    """Sensor for today's strikes."""

    def __init__(self, coordinator: ScioperiCoordinator) -> None:
        """Initialize sensor."""
        super().__init__(coordinator, "Oggi", "mdi:calendar-today")

    @property
    def native_value(self) -> int:
        """Return the state."""
        return len(self.coordinator.today_strikes)

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        strikes = self.coordinator.today_strikes
        
        return {
            ATTR_STRIKES: [
                {
                    "sector": s.get(ATTR_SECTOR, ""),
                    "region": s.get(ATTR_REGION, ""),
                    "modality": s.get(ATTR_MODALITY, ""),
                    "unions": s.get("unions", ""),
                    "category": s.get("category", ""),
                }
                for s in strikes
            ]
        }


class ScioperiNextSensor(ScioperiBaseSensor):
    """Sensor for next upcoming strike."""

    def __init__(self, coordinator: ScioperiCoordinator) -> None:
        """Initialize sensor."""
        super().__init__(coordinator, "Prossimo", "mdi:calendar-clock")

    @property
    def native_value(self) -> str:
        """Return the state."""
        next_strike = self.coordinator.get_next_strike()
        if not next_strike:
            return "Nessuno"
        
        start = next_strike.get("start_date")
        if start:
            return start.strftime("%d/%m/%Y")
        return "Sconosciuto"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        next_strike = self.coordinator.get_next_strike()
        if not next_strike:
            return {}
        
        return {
            ATTR_SECTOR: next_strike.get(ATTR_SECTOR, ""),
            ATTR_REGION: next_strike.get(ATTR_REGION, ""),
            "province": next_strike.get("province", ""),
            ATTR_START_DATE: next_strike.get("start_date_str", ""),
            ATTR_END_DATE: next_strike.get("end_date_str", ""),
            ATTR_MODALITY: next_strike.get(ATTR_MODALITY, ""),
            ATTR_RELEVANCE: next_strike.get(ATTR_RELEVANCE, ""),
            "unions": next_strike.get("unions", ""),
            "category": next_strike.get("category", ""),
            "guid": next_strike.get("guid", ""),
        }


class ScioperiSectorSensor(ScioperiBaseSensor):
    """Sensor for specific sector strikes."""

    def __init__(self, coordinator: ScioperiCoordinator, sector: str) -> None:
        """Initialize sector sensor."""
        self.sector = sector
        super().__init__(
            coordinator, 
            sector.replace("Trasporto pubblico locale", "TPL"),
            self._get_sector_icon(sector)
        )

    @staticmethod
    def _get_sector_icon(sector: str) -> str:
        """Get icon for sector."""
        icons = {
            "Trasporto pubblico locale": "mdi:bus",
            "Aereo": "mdi:airplane",
            "Ferroviario": "mdi:train",
            "Trasporto merci e logistica": "mdi:truck",
            "Marittimo": "mdi:ferry",
        }
        return icons.get(sector, "mdi:alert")

    @property
    def native_value(self) -> int:
        """Return the state."""
        return len(self.coordinator.get_strikes_by_sector(self.sector))

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        strikes = self.coordinator.get_strikes_by_sector(self.sector)[:5]
        
        return {
            ATTR_SECTOR: self.sector,
            ATTR_STRIKES: [
                {
                    "region": s.get(ATTR_REGION, ""),
                    "start_date": s.get("start_date_str", ""),
                    "modality": s.get(ATTR_MODALITY, ""),
                }
                for s in strikes
            ]
        }
