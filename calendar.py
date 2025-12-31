"""Calendar platform for Scioperi Italia."""
import logging
from datetime import datetime, timedelta

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import ScioperiCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Scioperi Italia calendar."""
    coordinator: ScioperiCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ScioperiCalendar(coordinator)])


class ScioperiCalendar(CoordinatorEntity, CalendarEntity):
    """Calendar entity for strikes."""

    def __init__(self, coordinator: ScioperiCoordinator) -> None:
        """Initialize calendar."""
        super().__init__(coordinator)
        self._attr_name = "Scioperi Italia"
        self._attr_unique_id = "scioperi_calendar"
        self._attr_icon = "mdi:calendar-alert"
        self._event = None

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        next_strike = self.coordinator.get_next_strike()
        if not next_strike:
            return None
        
        return self._strike_to_event(next_strike)

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        events = []
        
        for strike in self.coordinator.strikes:
            strike_start = strike.get("start_date")
            strike_end = strike.get("end_date")
            
            if not strike_start:
                continue
            
            # Check if strike is in range
            if strike_start.date() > end_date.date():
                break  # Strikes are sorted, stop here
            
            if strike_end and strike_end.date() < start_date.date():
                continue
            
            events.append(self._strike_to_event(strike))
        
        return events

    def _strike_to_event(self, strike: dict) -> CalendarEvent:
        """Convert strike to calendar event."""
        start = strike.get("start_date")
        end = strike.get("end_date", start)
        
        sector = strike.get("sector", "Sciopero")
        region = strike.get("region", "")
        province = strike.get("province", "")
        relevance = strike.get("relevance", "")
        
        # Build summary
        summary = f"{sector}"
        if region and region.strip():
            summary += f" - {region}"
        if province and province.strip() and province != "Tutte":
            summary += f" ({province})"
        
        # Build description
        description_parts = []
        if relevance:
            description_parts.append(f"Rilevanza: {relevance}")
        if strike.get("modality"):
            description_parts.append(f"Modalità: {strike['modality']}")
        if strike.get("unions"):
            description_parts.append(f"Sindacati: {strike['unions']}")
        if strike.get("category"):
            description_parts.append(f"Categoria: {strike['category']}")
        
        description = "\n".join(description_parts)
        
        return CalendarEvent(
            summary=summary,
            start=start,
            end=end,
            description=description,
            location=f"{region}, {province}" if province != "Tutte" else region,
        )
