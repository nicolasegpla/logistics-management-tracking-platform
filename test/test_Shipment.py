import pytest
from app.domain.shipment import Shipment, ShipmentStatus
from datetime import datetime

#happy path
def test_new_shipment_starts_in_created_status():
    shipment = Shipment()

    assert shipment.status is ShipmentStatus.CREATED

def test_new_shipment_has_no_delivery_date():
    shipment = Shipment()

    assert shipment.delivery_date is None

def test_shipment_can_move_from_created_to_in_transit():
    shipment = Shipment()
    shipment.mark_as_in_transit()
    assert shipment.status is ShipmentStatus.IN_TRANSIT

def test_shipment_can_move_from_in_transit_to_delivered():
    shipment = Shipment() #created
    
    shipment.mark_as_in_transit()

    shipment.mark_as_delivered()

    assert shipment.status is ShipmentStatus.DELIVERED
    assert isinstance(shipment.delivery_date, datetime)

#sad path
def test_shipment_cant_move_from_created_to_delivered():
    shipment = Shipment()

    with pytest.raises(ValueError, match="you can't move from CREATED to DELIVERED"):
        shipment.mark_as_delivered()

    assert shipment.status is ShipmentStatus.CREATED

def test_shipment_cant_move_from_delivered_to_in_transit():
    shipment = Shipment()

    shipment.mark_as_in_transit()

    shipment.mark_as_delivered()

    with pytest.raises(ValueError):
        shipment.mark_as_in_transit()

    assert shipment.status is ShipmentStatus.DELIVERED
    assert isinstance(shipment.delivery_date, datetime)

