from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut

def reverse_geocode(lat: float, lon: float) -> str:
    try:
        geo = Nominatim(user_agent="sos_agent", timeout=5)
        loc = geo.reverse((lat, lon), exactly_one=True)
        if loc:
            return loc.address
    except (GeocoderUnavailable, GeocoderTimedOut):
        pass

    return f"Latitude {lat}, Longitude {lon}"
