"""Oscar Broome Compensation Module.

This module calculates and processes compensation for Oscar Broome,
the founder and owner of Owlban Group and Capetain Cetriva.

Compensation is based on the fund fee structure:
  - Management Fee: 2% of Assets Under Management (AUM)
  - Performance Fee (Incentive Fee): 20% of returns above an 8% hurdle rate
  - Oscar's ownership percentage determines his share of total fees

The module integrates with BankingUtils to process ACH payments to
Oscar's bank account at Capetain Private AI Bank (routing 021000021).
"""

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from banking_utils import BankingUtils

logger = logging.getLogger(__name__)


# -- Configuration constants --

MANAGEMENT_FEE_RATE = 0.02       # 2% annual management fee
PERFORMANCE_FEE_RATE = 0.20     # 20% performance fee
HURDLE_RATE = 0.08              # 8% annual hurdle rate
OSCAR_OWNERSHIP_PERCENTAGE = 1.00  # 100% - Oscar owns both Owlban Group and Capetain Cetriva

DEFAULT_ROUTING_NUMBER = "021000021"    # Capetain Private AI Bank
DEFAULT_AUM = 150_000_000                # $150M current AUM (Q2 2024)


@dataclass
class CompensationBreakdown:
    """Detailed breakdown of Oscar Broome's compensation for a period."""

    period: str
    aum: float
    gross_management_fee: float
    gross_performance_fee: float
    returns: float
    oscar_ownership_pct: float
    net_management_fee: float
    net_performance_fee: float
    total_compensation: float
    timestamp: datetime = field(default_factory=datetime.now)


class OscarCompensation:
    """Calculate and process Oscar Broome's compensation.

    Compensation = Oscar ownership % x (management fee + performance fee)
    where:
      - management fee  = 2% x AUM
      - performance fee = 20% x max(0, returns - 8% x AUM)
    """

    def __init__(
        self,
        banking_utils: Optional["BankingUtils"] = None,
        aum: float = DEFAULT_AUM,
        ownership_pct: float = OSCAR_OWNERSHIP_PERCENTAGE,
        routing_number: str = DEFAULT_ROUTING_NUMBER,
    ) -> None:
        """Initialize the compensation calculator.

        Args:
            banking_utils: Optional BankingUtils instance for ACH payments.
                If None, a new instance is created (lazy import to avoid
                importing heavy dependencies like torch at import time).
            aum: Assets under management for fee calculation.
            ownership_pct: Oscar's ownership percentage of the fee pool.
            routing_number: Routing number for ACH payments.
        """
        if banking_utils is None:
            from banking_utils import BankingUtils
            banking_utils = BankingUtils()
        self.banking_utils: "BankingUtils" = banking_utils
        self.aum = aum
        self.ownership_pct = ownership_pct
        self.routing_number = routing_number
        self.history: List[CompensationBreakdown] = []

    # -- Calculation methods --

    def calculate_management_fee(self, aum: float) -> float:
        """Calculate the gross management fee (2% of AUM).

        Args:
            aum: Assets under management.

        Returns:
            Gross management fee for the period.
        """
        fee = aum * MANAGEMENT_FEE_RATE
        logger.info(
            "Management fee: %.2f%% of $%.2f = $%.2f",
            MANAGEMENT_FEE_RATE * 100, aum, fee,
        )
        return fee

    def calculate_performance_fee(self, aum: float, returns: float) -> float:
        """Calculate the gross performance fee.

        Performance fee = 20% of returns above the 8% hurdle rate.
        If returns are at or below the hurdle, no performance fee is charged.

        Args:
            aum: Assets under management.
            returns: Total returns for the period.

        Returns:
            Gross performance fee (zero if returns <= hurdle).
        """
        hurdle_amount = aum * HURDLE_RATE
        if returns <= hurdle_amount:
            logger.info(
                "Returns $%.2f <= hurdle $%.2f -- no performance fee",
                returns, hurdle_amount,
            )
            return 0.0

        excess_returns = returns - hurdle_amount
        fee = excess_returns * PERFORMANCE_FEE_RATE
        logger.info(
            "Performance fee: 20%% of excess $%.2f (hurdle $%.2f) = $%.2f",
            excess_returns, hurdle_amount, fee,
        )
        return fee

    def calculate_compensation(
        self,
        aum: float,
        returns: float,
        period: str = "annual",
    ) -> CompensationBreakdown:
        """Calculate Oscar Broome's total compensation for a period.

        Args:
            aum: Assets under management.
            returns: Total returns for the period.
            period: Description of the period (e.g. "annual", "Q1 2024").

        Returns:
            CompensationBreakdown with full detail.
        """
        gross_mgmt = self.calculate_management_fee(aum)
        gross_perf = self.calculate_performance_fee(aum, returns)

        net_mgmt = gross_mgmt * self.ownership_pct
        net_perf = gross_perf * self.ownership_pct
        total = net_mgmt + net_perf

        breakdown = CompensationBreakdown(
            period=period,
            aum=aum,
            gross_management_fee=gross_mgmt,
            gross_performance_fee=gross_perf,
            returns=returns,
            oscar_ownership_pct=self.ownership_pct,
            net_management_fee=net_mgmt,
            net_performance_fee=net_perf,
            total_compensation=total,
        )
        self.history.append(breakdown)
        logger.info(
            "Oscar Broome %s compensation: $%.2f (mgmt $%.2f + perf $%.2f)",
            period, total, net_mgmt, net_perf,
        )
        return breakdown

        # -- Payment processing --

    def _get_or_generate_account(self, provided: Optional[str]) -> str:
        """Return a provided account number or generate a new valid one."""
        if provided:
            return provided
        account_number = self.banking_utils.generate_account()
        if account_number is None:
            raise ValueError(
                "Failed to generate a valid account number for Oscar Broome."
            )
        return account_number

    def process_compensation(
        self,
        aum: float,
        returns: float,
        description: str = "",
        account_number: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Calculate Oscar's compensation and issue an ACH payment.

        Integrates with BankingUtils.spend_profits_for_oscar() to handle
        routing number selection and account number generation.

        Args:
            aum: Assets under management.
            returns: Total returns for the period.
            description: Optional payment description.
            account_number: Oscar's bank account number.
                If None, BankingUtils generates a valid account number.

        Returns:
            ACH payment response dict, or None if payment creation fails.
        """
        breakdown = self.calculate_compensation(aum, returns)
        if description:
            description = (
                f"{description} - Oscar Broome Compensation ({breakdown.period})"
            )
        else:
            description = f"Oscar Broome Compensation ({breakdown.period})"

        # Use BankingUtils.spend_profits_for_oscar which handles routing
        # number (021000021) and account number generation internally
        response = self.banking_utils.spend_profits_for_oscar(
            breakdown.total_compensation,
            description=description,
            account_number=account_number,
        )
        logger.info("Oscar Broome compensation payment processed: %s", response)
        return response

    # -- History and reporting --

    def get_compensation_history(self) -> List[CompensationBreakdown]:
        """Return the history of all compensation calculations."""
        return list(self.history)

    def summary(self, period_filter: Optional[str] = None) -> str:
        """Return a human-readable summary of compensation history.

        Args:
            period_filter: Optional period string to filter by.

        Returns:
            Multi-line summary string.
        """
        records = (
            [r for r in self.history if r.period == period_filter]
            if period_filter
            else self.history
        )
        if not records:
            return "No compensation records found."

        lines = ["Oscar Broome Compensation Summary"]
        lines.append("-" * 50)
        total_all = 0.0
        for r in records:
            lines.append(
                f"  {r.period}: AUM=${r.aum:,.0f}, "
                f"Mgmt=${r.net_management_fee:,.2f}, "
                f"Perf=${r.net_performance_fee:,.2f}, "
                f"Total=${r.total_compensation:,.2f}"
            )
            total_all += r.total_compensation
        lines.append("-" * 50)
        lines.append(f"  Total: ${total_all:,.2f}")
        return "\n".join(lines)

    @classmethod
    def create_default(cls) -> "OscarCompensation":
        """Factory method to create a compensation instance with defaults from env."""
        aum = float(os.getenv("DEFAULT_AUM", DEFAULT_AUM))
        ownership = float(
            os.getenv("OSCAR_OWNERSHIP_PCT", OSCAR_OWNERSHIP_PERCENTAGE)
        )
        routing = os.getenv("ROUTING_NUMBER", DEFAULT_ROUTING_NUMBER)
        return cls(aum=aum, ownership_pct=ownership, routing_number=routing)


if __name__ == "__main__":
    # Example: Calculate and process annual compensation
    comp = OscarCompensation.create_default()
    aum = float(os.getenv("DEFAULT_AUM", DEFAULT_AUM))
    returns = aum * 0.15  # Assume 15% annual returns

    breakdown = comp.calculate_compensation(aum, returns, period="2024 Annual")
    print(comp.summary())
    print(f"\nGross Management Fee: ${breakdown.gross_management_fee:,.2f}")
    print(f"Gross Performance Fee: ${breakdown.gross_performance_fee:,.2f}")
    print(f"Oscar's Net Mgmt Fee: ${breakdown.net_management_fee:,.2f}")
    print(f"Oscar's Net Perf Fee: ${breakdown.net_performance_fee:,.2f}")
    print(f"Total Compensation: ${breakdown.total_compensation:,.2f}")
