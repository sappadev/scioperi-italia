"""Parser RSS per Scioperi Italia."""
import logging
import re
from datetime import datetime
from typing import Any
import feedparser

_LOGGER = logging.getLogger(__name__)


class ScioperoParser:
    """Parser per feed RSS scioperi."""

    @staticmethod
    def parse_date(date_str: str) -> datetime | None:
        """Parse date in format DD/MM/YYYY."""
        try:
            return datetime.strptime(date_str.strip(), "%d/%m/%Y")
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def extract_field(description: str, field_name: str) -> str:
        """Extract field from description."""
        pattern = rf"{field_name}:\s*([^<\n]+)"
        match = re.search(pattern, description)
        return match.group(1).strip() if match else ""

    @staticmethod
    def parse_title(title: str) -> dict[str, str]:
        """Parse title to extract initial data."""
        data = {}
        
        # Extract start date
        date_match = re.search(r"Data inizio:\s*(\d{2}/\d{2}/\d{4})", title)
        if date_match:
            data["start_date_str"] = date_match.group(1)
        
        # Extract sector
        sector_match = re.search(r"Settore:\s*([^-]+)", title)
        if sector_match:
            data["sector"] = sector_match.group(1).strip()
        
        # Extract relevance
        relevance_match = re.search(r"Rilevanza:\s*([^-]+)", title)
        if relevance_match:
            data["relevance"] = relevance_match.group(1).strip()
        
        # Extract region
        region_match = re.search(r"Regione:\s*([^-]+)", title)
        if region_match:
            data["region"] = region_match.group(1).strip()
        
        # Extract province
        province_match = re.search(r"Provincia:\s*(.+)$", title)
        if province_match:
            data["province"] = province_match.group(1).strip()
        
        return data

    @classmethod
    def parse_strike(cls, item: Any) -> dict[str, Any] | None:
        """Parse single strike from RSS item."""
        try:
            strike = {}
            
            # Parse title
            title_data = cls.parse_title(item.title)
            strike.update(title_data)
            
            # Parse description
            description = item.description
            
            # Extract all fields
            strike["modality"] = cls.extract_field(description, "modalità")
            strike["end_date_str"] = cls.extract_field(description, "Data fine")
            strike["unions"] = cls.extract_field(description, "Sindacati")
            strike["category"] = cls.extract_field(description, "Categoria interessata")
            strike["proclamation_date_str"] = cls.extract_field(description, "Data proclamazione")
            
            # Parse dates
            if "start_date_str" in strike:
                strike["start_date"] = cls.parse_date(strike["start_date_str"])
            if strike.get("end_date_str"):
                strike["end_date"] = cls.parse_date(strike["end_date_str"])
            if strike.get("proclamation_date_str"):
                strike["proclamation_date"] = cls.parse_date(strike["proclamation_date_str"])
            
            # Add metadata
            strike["guid"] = item.get("guid", "")
            strike["link"] = item.get("link", "")
            strike["pub_date"] = item.get("published", "")
            
            # Only return valid strikes with start date
            if strike.get("start_date"):
                return strike
            
            return None
            
        except Exception as e:
            _LOGGER.error("Error parsing strike: %s", e)
            return None

    @classmethod
    def parse_feed(cls, url: str) -> list[dict[str, Any]]:
        """Parse RSS feed and return list of strikes."""
        try:
            feed = feedparser.parse(url)
            
            if feed.bozo:
                _LOGGER.warning("Feed parsing warning: %s", feed.bozo_exception)
            
            strikes = []
            for item in feed.entries:
                strike = cls.parse_strike(item)
                if strike:
                    strikes.append(strike)
            
            # Sort by start date
            strikes.sort(key=lambda x: x.get("start_date", datetime.min))
            
            _LOGGER.info("Parsed %d strikes from feed", len(strikes))
            return strikes
            
        except Exception as e:
            _LOGGER.error("Error parsing feed: %s", e)
            return []
