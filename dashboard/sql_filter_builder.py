import math
from datetime import date
from typing import Dict, Any, Tuple, List

class SqlFilterBuilder:
    def __init__(self, filters: Dict[str, Any]):
        """
        Initialize the builder with user-selected filters.
        
        :param filters: Dictionary containing active filter values (e.g., from Streamlit)
        """
        self.filters = filters

    def build(self) -> Tuple[str, Dict[str, Any]]:
        """
        Main orchestration method. Resets state at the beginning.
        """
        # Reset the state every time build() is called
        self.sql_parts = []
        self.params = {}

        # Now internal methods can use 'self.sql_parts' directly 
        # without needing them as arguments
        self._build_date_range_filter()
        self._build_store_location_filter()

        additional_filters_sql = "\n".join(self.sql_parts)
        return additional_filters_sql, self.params

    def _build_date_range_filter(self):
        """Internal method to handle user-provided date range filter."""
        date_range = self.filters.get("open_date_range")
        if date_range and len(date_range) == 2:
            self.sql_parts.append("AND s.sale_date >= :time_from")
            self.sql_parts.append("AND s.sale_date < :time_to")
            if date_range[0]:
                self.params["time_from"] = date_range[0]
            if date_range[1]:
                self.params["time_to"] = date_range[1]

    def _build_store_location_filter(self):
        """Internal method to handle store_location filter where NULL equals 'Online'."""
        store_locations = self.filters.get("store_location")
        
        # Check if we have any selections at all
        if not store_locations:
            return

        # Create the physical locations tuple (excluding None and 'Online')
        # Using a list comprehension first for clarity, then converting to tuple
        physical_stores = tuple(
            x for x in store_locations 
            if x is not None and str(x).lower() != 'online'
        )
        
        # Determine if 'Online' (NULL in DB) was part of the user's selection
        online_selected = len(set(store_locations) - set(physical_stores)) > 0

        if physical_stores and online_selected:
            # Case: Both physical stores and Online requested
            self.sql_parts.append("AND (s.store_location IN :store_location OR s.store_location IS NULL)")
            self.params["store_location"] = physical_stores
        elif physical_stores:
            # Case: Only physical stores requested
            self.sql_parts.append("AND s.store_location IN :store_location")
            self.params["store_location"] = physical_stores
        elif online_selected:
            # Case: Only Online requested
            self.sql_parts.append("AND s.store_location IS NULL")