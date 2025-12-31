"""Data coordinator per Scioperi Italia."""
import logging
from datetime import timedelta, datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    UPDATE_INTERVAL_SECONDS,
    CONF_RSS_URL,
    CONF_REGION_FILTER,
    CONF_SECTOR_FILTER,
    DEFAULT_RSS_URL,
)
from .parser import ScioperoParser

_LOGGER = logging.getLogger(__name__)


class ScioperiCoordinator(DataUpdateCoordinator):
    """Coordinator per gestire aggiornamenti scioperi."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize coordinator."""
        self.entry = entry
        self.rss_url = entry.data.get(CONF_RSS_URL, DEFAULT_RSS_URL)
        self.region_filter = entry.data.get(CONF_REGION_FILTER, "Tutte")
        self.sector_filter = entry.data.get(CONF_SECTOR_FILTER, "Tutti")
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    def _filter_strikes(self, strikes: list[dict]) -> list[dict]:
        """Filter strikes based on user preferences."""
        filtered = strikes
        
        # Filter by region
        if self.region_filter and self.region_filter != "Tutte":
            filtered = [
                s for s in filtered
                if s.get("region", "").lower() == self.region_filter.lower()
                or s.get("region", "") == " Italia"
            ]
        
        # Filter by sector
        if self.sector_filter and self.sector_filter != "Tutti":
            filtered = [
                s for s in filtered
                if s.get("sector", "").lower() == self.sector_filter.lower()
            ]
        
        return filtered

    async def _async_update_data(self) -> dict:
        """Fetch data from RSS feed."""
        try:
            # Parse feed (runs in executor to avoid blocking)
            strikes = await self.hass.async_add_executor_job(
                ScioperoParser.parse_feed, self.rss_url
            )
            
            # Filter strikes
            filtered_strikes = self._filter_strikes(strikes)
            
            # Organize data
            now = datetime.now()
            
            # Future strikes only
            future_strikes = [
                s for s in filtered_strikes
                if s.get("start_date") and s["start_date"] >= now.replace(hour=0, minute=0, second=0, microsecond=0)
            ]
            
            # Today's strikes
            today_strikes = [
                s for s in future_strikes
                if s["start_date"].date() == now.date()
            ]
            
            # Group by sector
            by_sector = {}
            for strike in future_strikes:
                sector = strike.get("sector", "Altro")
                if sector not in by_sector:
                    by_sector[sector] = []
                by_sector[sector].append(strike)
            
            # Group by region
            by_region = {}
            for strike in future_strikes:
                region = strike.get("region", "Altro")
                if region not in by_region:
                    by_region[region] = []
                by_region[region].append(strike)
            
            return {
                "all_strikes": filtered_strikes,
                "future_strikes": future_strikes,
                "today_strikes": today_strikes,
                "by_sector": by_sector,
                "by_region": by_region,
                "last_update": now,
            }
            
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}")
    
    @property
    def strikes(self) -> list[dict]:
        """Return all future strikes."""
        return self.data.get("future_strikes", []) if self.data else []
    
    @property
    def today_strikes(self) -> list[dict]:
        """Return today's strikes."""
        return self.data.get("today_strikes", []) if self.data else []
    
    def get_strikes_by_sector(self, sector: str) -> list[dict]:
        """Get strikes for specific sector."""
        if not self.data:
            return []
        return self.data.get("by_sector", {}).get(sector, [])
    
    def get_next_strike(self) -> dict | None:
        """Get next upcoming strike."""
        if not self.strikes:
            return None
        return self.strikes[0] if self.strikes else None
