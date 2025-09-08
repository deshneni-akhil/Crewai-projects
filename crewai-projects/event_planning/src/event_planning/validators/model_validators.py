from pydantic import BaseModel


class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    booking_status: str
