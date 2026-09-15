"""
Revenue Disbursement Module

This module provides comprehensive revenue disbursement capabilities for the
Capetain Cetriva AI Hybrid Fund.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from banking_utils import BankingUtils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class DisbursementRecord:
    """Represents a single disbursement transaction record."""
    recipient: str
    account_number: str
    routing_number: str
    amount: float
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
    transaction_id: Optional[str] = None
    status: str = "pending"
    asset_class: Optional[str] = None


@dataclass
class DisbursementBatch:
    """Represents a batch of disbursements."""
    batch_id: str
    description: str
    records: List[DisbursementRecord] = field(default_factory=list)
    total_amount: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = "created"

    def add_record(self, record: DisbursementRecord) -> None:
        """Add a disbursement record to the batch."""
        self.records.append(record)
        self.total_amount += record.amount

    @property
    def success_count(self) -> int:
        """Count of successful disbursements."""
        return sum(1 for r in self.records if r.status == "completed")

    @property
    def failed_count(self) -> int:
        """Count of failed disbursements."""
        return sum(1 for r in self.records if r.status == "failed")

    def allocate_and_disburse(
        self,
        total_amount: float,
        description: str = "Revenue allocation and disbursement",
    ) -> Dict[str, Optional[DisbursementRecord]]:
        """Allocate total revenue according to investment thesis and disburse."""
        if total_amount <= 0:
            logger.error("Total allocation amount must be greater than zero.")
            return {}

        results = {}
        for asset_class, percentage in self.ALLOCATION_PERCENTAGES.items():
            allocated_amount = total_amount * percentage
            record = self.disburse_to_stakeholder(
                recipient=f"{asset_class} Allocation",
                amount=allocated_amount,
                description=f"{description} - {asset_class}",
                asset_class=asset_class,
            )
            results[asset_class] = record
            if record:
                logger.info("Allocated $%.2f to %s", allocated_amount, asset_class)
            else:
                logger.warning("Failed to allocate to %s", asset_class)

        return results

    def get_disbursement_history(
        self,
        recipient: Optional[str] = None,
        asset_class: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
    ) -> List[DisbursementRecord]:
        """Query disbursement history with optional filters."""
        results = []
        for record in self._disbursement_history:
            if recipient and record.recipient != recipient:
                continue
            if asset_class and record.asset_class != asset_class:
                continue
            if start_date and record.timestamp < start_date:
                continue
            if end_date and record.timestamp > end_date:
                continue
            if status and record.status != status:
                continue
            results.append(record)
        return results
