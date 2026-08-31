"""
MediCore Nexus - Clinical Pharmacy & Drug Safety (drug_safety) Domain Controller & Gateway
Integrates business workflows, database repository, schema transformations, and event publication.
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timezone
import logging
from backend.app.modules.drug_safety.repository import drug_safety_repository
from backend.app.modules.drug_safety.service_deep import drug_safety_domain_service
from backend.app.events import event_bus

logger = logging.getLogger("medicore.controller.drug_safety")


class SafetyCheckDomainController:
    """
    Enterprise Domain Controller orchestrating transactional operations for Clinical Pharmacy & Drug Safety.
    """

    def __init__(self):
        self.repository = drug_safety_repository
        self.domain_service = drug_safety_domain_service
        logger.info(f"Initialized SafetyCheckDomainController.")

    async def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve record with audit logging."""
        record = await self.repository.get_by_id(entity_id)
        if record:
            self.domain_service.record_audit("VIEW", entity_id, "CONTROLLER", "Retrieved entity detail")
        return record

    async def query_entities(
        self,
        skip: int = 0,
        limit: int = 50,
        filters: Optional[Dict[str, Any]] = None,
        sort_by: str = "created_at",
        descending: bool = True
    ) -> Dict[str, Any]:
        """Query collection with metadata pagination."""
        items, total = await self.repository.list_all(skip, limit, filters, sort_by, descending)
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "has_more": (skip + limit) < total,
            "domain": "drug_safety",
        }

    async def process_create(self, payload: Dict[str, Any], actor_id: str = "SYSTEM") -> Dict[str, Any]:
        """Validate, persist, audit, and publish lifecycle creation event."""
        # Domain validation
        is_valid, err = self.domain_service.validate_entity_state(payload, ["name"])
        if not is_valid and "name" not in payload:
            payload["name"] = f"SafetyCheck Entry #{datetime.now(timezone.utc).strftime('%H%M%S')}"

        created_record = await self.repository.create(payload, creator_id=actor_id)
        self.domain_service.record_audit("CREATE", created_record["id"], actor_id, "Created new entity record")
        
        # Publish domain event
        await event_bus.publish(f"SafetyCheckCreated", created_record)
        return created_record

    async def process_update(self, entity_id: str, updates: Dict[str, Any], actor_id: str = "SYSTEM") -> Optional[Dict[str, Any]]:
        """Validate, mutate, audit, and publish update event."""
        updated = await self.repository.update(entity_id, updates, updater_id=actor_id)
        if updated:
            self.domain_service.record_audit("UPDATE", entity_id, actor_id, f"Updated fields: {', '.join(updates.keys())}")
            await event_bus.publish(f"SafetyCheckUpdated", updated)
        return updated

    async def process_delete(self, entity_id: str, actor_id: str = "SYSTEM") -> bool:
        """Soft-delete entity with immutable audit trail."""
        success = await self.repository.soft_delete(entity_id, deleter_id=actor_id)
        if success:
            self.domain_service.record_audit("DELETE", entity_id, actor_id, "Soft-deleted entity record")
            await event_bus.publish(f"SafetyCheckDeleted", {"id": entity_id})
        return success

    async def execute_bulk_batch_action(self, action: str, entity_ids: List[str], actor_id: str = "SYSTEM") -> Dict[str, Any]:
        """Perform batch operations across multiple records."""
        success_count = 0
        failed_count = 0
        errors = []

        for eid in entity_ids:
            try:
                if action.upper() == "ACTIVATE":
                    await self.repository.update(eid, {"status": "Active"}, updater_id=actor_id)
                elif action.upper() == "ARCHIVE":
                    await self.repository.update(eid, {"status": "Archived"}, updater_id=actor_id)
                elif action.upper() == "DELETE":
                    await self.repository.soft_delete(eid, deleter_id=actor_id)
                success_count += 1
            except Exception as e:
                failed_count += 1
                errors.append({"id": eid, "error": str(e)})

        return {
            "action": action,
            "total_processed": len(entity_ids),
            "successful_count": success_count,
            "failed_count": failed_count,
            "errors": errors,
        }


# Singleton controller instance
drug_safety_domain_controller = SafetyCheckDomainController()
