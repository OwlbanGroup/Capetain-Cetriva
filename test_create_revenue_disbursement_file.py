"""Tests for CreateRevenueDisbursementFile.py."""

import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

os.environ["TESTING"] = "1"

from CreateRevenueDisbursementFile import DisbursementBatch, DisbursementRecord  # noqa: E402,E403


class TestDisbursementRecord(unittest.TestCase):
    """Tests for DisbursementRecord dataclass."""

    def test_record_defaults(self):
        """Test that a DisbursementRecord has correct defaults."""
        record = DisbursementRecord(
            recipient="Alice",
            account_number="123456789",
            routing_number="021000021",
            amount=100.0,
            description="Test payment",
        )
        self.assertEqual(record.recipient, "Alice")
        self.assertEqual(record.account_number, "123456789")
        self.assertEqual(record.routing_number, "021000021")
        self.assertEqual(record.amount, 100.0)
        self.assertEqual(record.description, "Test payment")
        self.assertEqual(record.status, "pending")
        self.assertIsNone(record.transaction_id)
        self.assertIsNone(record.asset_class)
        self.assertIsInstance(record.timestamp, datetime)

    def test_record_custom_values(self):
        """Test DisbursementRecord with all custom values."""
        record = DisbursementRecord(
            recipient="Bob",
            account_number="987654321",
            routing_number="021000089",
            amount=500.0,
            description="Custom payment",
            timestamp=datetime(2024, 1, 15, 10, 30, 0),
            transaction_id="TXN-001",
            status="completed",
            asset_class="Digital Assets",
        )
        self.assertEqual(record.transaction_id, "TXN-001")
        self.assertEqual(record.status, "completed")
                        self.assertEqual(record.asset_class, "Digital Assets")


class TestDisbursementBatchCreation(unittest.TestCase):
    """Tests for DisbursementBatch initialization."""

    def test_batch_creation(self):
        """Test that a DisbursementBatch is created correctly."""
        batch = DisbursementBatch(
            batch_id="BATCH-001",
            description="Q1 allocations",
        )
        self.assertEqual(batch.batch_id, "BATCH-001")
        self.assertEqual(batch.description, "Q1 allocations")
        self.assertEqual(batch.records, [])
        self.assertEqual(batch.total_amount, 0.0)
        self.assertEqual(batch.status, "created")
        self.assertIsInstance(batch.created_at, datetime)
        self.assertIsNone(batch.completed_at)

    def test_allocation_percentages_exist(self):
        """Test that ALLOCATION_PERCENTAGES has correct keys."""
        self.assertIn("Alternative Assets", DisbursementBatch.ALLOCATION_PERCENTAGES)
        self.assertIn("Public Equities", DisbursementBatch.ALLOCATION_PERCENTAGES)
        self.assertIn("Digital Assets", DisbursementBatch.ALLOCATION_PERCENTAGES)
        self.assertAlmostEqual(DisbursementBatch.ALLOCATION_PERCENTAGES["Alternative Assets"], 0.60)

    def test_disbursement_history_default(self):
        """Test that _disbursement_history defaults to empty list."""
        batch = DisbursementBatch(batch_id="BATCH-002", description="Test")
        self.assertEqual(batch._disbursement_history, [])

