from enum import Enum
from datetime import datetime

class ShipmentStatus(Enum):
    CREATED = "CREATED"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"

class Shipment:
    def __init__(self):
        self.status = ShipmentStatus.CREATED
        self.delivery_date = None

    def mark_as_in_transit(self):
        if self.status == ShipmentStatus.DELIVERED:
            raise ValueError("you can't move from DELIVERED to IN_TRANSIT")
        self.status = ShipmentStatus.IN_TRANSIT

    def mark_as_delivered(self):
        if self.status == ShipmentStatus.CREATED:
            raise ValueError("you can't move from CREATED to DELIVERED")
        self.status = ShipmentStatus.DELIVERED
        self.delivery_date = datetime.now()
        
