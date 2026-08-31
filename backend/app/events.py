"""
MediCore Nexus - Domain Event Bus
Decoupled event publisher and subscriber system for cross-domain orchestration
"""

from typing import Callable, Dict, List, Any
import asyncio
import logging

logger = logging.getLogger("medicore.events")


class DomainEventBus:
    """In-memory and async event bus for domain events."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_name: str, handler: Callable):
        """Register an async or sync handler for a given event name."""
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []
        self._subscribers[event_name].append(handler)
        logger.info(f"Subscribed handler {handler.__name__} to event {event_name}")

    async def publish(self, event_name: str, payload: Dict[str, Any]):
        """Publish domain event and notify all registered handlers."""
        logger.info(f"[EVENT-BUS] Event Published: {event_name} | Payload: {payload.get('id', 'N/A')}")
        handlers = self._subscribers.get(event_name, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    asyncio.create_task(handler(payload))
                else:
                    handler(payload)
            except Exception as ex:
                logger.error(f"Error handling event {event_name} in {handler.__name__}: {str(ex)}")


event_bus = DomainEventBus()


# Event Name Constants
EVENT_PRESCRIPTION_CREATED = "PrescriptionCreated"
EVENT_PRESCRIPTION_VALIDATED = "PrescriptionValidated"
EVENT_MEDICINE_DISPENSED = "MedicineDispensed"
EVENT_MEDICINE_SOLD = "MedicineSold"
EVENT_STOCK_DEDUCTED = "StockDeducted"
EVENT_LOW_STOCK_DETECTED = "LowStockDetected"
EVENT_LAB_ORDER_CREATED = "LabOrderCreated"
EVENT_LAB_RESULT_VERIFIED = "LabResultVerified"
EVENT_APPOINTMENT_SCHEDULED = "AppointmentScheduled"
EVENT_APPOINTMENT_CHECKED_IN = "AppointmentCheckedIn"
EVENT_INSURANCE_CLAIM_SUBMITTED = "InsuranceClaimSubmitted"
EVENT_PATIENT_ADMITTED = "PatientAdmitted"
EVENT_CRITICAL_ALLERGY_ALERT = "CriticalAllergyAlert"
