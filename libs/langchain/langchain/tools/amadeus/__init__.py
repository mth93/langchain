"""Amadeus tools."""

from langchain.libs.langchain.langchain.tools.amadeus.closest_airport import AmadeusClosestAirport
from langchain.libs.langchain.langchain.tools.amadeus.flight_search import AmadeusFlightSearch

__all__ = [
    "AmadeusClosestAirport",
    "AmadeusFlightSearch",
]
