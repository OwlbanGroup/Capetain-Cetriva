"""
Revenue Disbursement Module

This module provides comprehensive revenue disbursement capabilities for the
Capetain Cetriva AI Hybrid Fund.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional

from banking_utils import BankingUtils

if TYPE_CHECKING:
    from oscar_compensation import OscarCompensation  # noqa: F401

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
    """Represents a batch of disbursements.

    Integrates with OscarCompensation for founder compensation disbursement.
    """

    # Investment thesis allocation percentages (from corporate_breakdown.md)
    ALLOCATION_PERCENTAGES: ClassVar[Dict[str, float]] = {
        "Alternative Assets": 0.60,
        "Public Equities": 0.30,
        "Digital Assets": 0.10,
    }

    batch_id: str
    description: str
    records: List[DisbursementRecord] = field(default_factory=list)
    total_amount: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = "created"
    _disbursement_history: List[DisbursementRecord] = field(default_factory=list)
    banking_utils: BankingUtils = field(default_factory=BankingUtils)

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

    def disburse_to_stakeholder(
        self,
        recipient: str,
        amount: float,
        description: str,
        asset_class: Optional[str] = None,
        routing_number: str = "021000021",
    ) -> Optional[DisbursementRecord]:
        """Disburse funds to a stakeholder via ACH payment."""
        try:
            account_number = self.banking_utils.generate_account()
            if account_number is None:
                logger.error(
                    "Failed to generate account number for %s", recipient
                )
                return None
            response = self.banking_utils.create_ach_payment(
                account_number, routing_number, amount, description
            )
            record = DisbursementRecord(
                recipient=recipient,
                account_number=account_number,
                routing_number=routing_number,
                amount=amount,
                description=description,
                transaction_id=(response.get("transaction_id") if response else None),
                status="completed" if response else "failed",
                asset_class=asset_class,
            )
            self._disbursement_history.append(record)
            return record
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Error disbursing to %s: %s", recipient, e)
            return None

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

    def allocate_oscar_compensation(
        self,
        aum: float,
        returns: float,
        description: str = "Oscar Broome Annual Compensation",
        period: str = "annual",
    ) -> Optional[Dict[str, Any]]:
        """Calculate and disburse Oscar Broome's compensation.

        Uses OscarCompensation to determine the management fee (2% of AUM)
        and performance fee (20% of returns above 8% hurdle), then processes
        an ACH payment via BankingUtils.

        Args:
            aum: Assets under management.
            returns: Total returns for the period.
            description: Payment description.
            period: Description of the compensation period.

        Returns:
            Oscar Broome ACH payment response dict, or None on failure.
        """
        from oscar_compensation import OscarCompensation  # noqa: F811

        oscar_comp = OscarCompensation(
            banking_utils=self.banking_utils,
            aum=aum,
        )
        return oscar_comp.process_compensation(
            aum=aum,
            returns=returns,
            description=description,
            period=period,
        )

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
