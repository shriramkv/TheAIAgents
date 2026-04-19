import random
from datetime import datetime, timedelta

def get_mock_flights(origin: str, destination: str, date: str):
    """
    Generates a list of mock flights for testing.
    """
    airlines = ["SkyLink", "Oceanic Air", "StarFlier", "GlobalJet", "WindRider"]
    flights = []
    
    for _ in range(10):
        # Random price between 3000 and 15000
        price = random.randint(3000, 15000)
        
        # Random duration between 2 and 12 hours
        duration_hours = random.randint(2, 12)
        duration_minutes = random.choice([0, 15, 30, 45])
        duration = f"{duration_hours}h {duration_minutes}m"
        
        # Random layovers between 0 and 2
        layovers = random.randint(0, 2)
        
        # Random departure time
        hour = random.randint(0, 23)
        minute = random.choice([0, 15, 30, 45])
        departure = f"{hour:02d}:{minute:02d}"
        
        # Arrival time (mock calculation)
        arrival_hour = (hour + duration_hours) % 24
        arrival = f"{arrival_hour:02d}:{minute:02d}"
        
        flights.append({
            "airline": random.choice(airlines),
            "price": price,
            "duration": duration,
            "layovers": layovers,
            "departure": departure,
            "arrival": arrival,
            "origin": origin,
            "destination": destination,
            "date": date
        })
        
    return flights
