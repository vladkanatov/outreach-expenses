"""
Remove description column from expenses table

Author: Vlad
Created: 2025-11-11
"""

from yoyo import step

__depends__ = {'20251111_01_create_expenses_table'}

steps = [
    step(
        """
        ALTER TABLE expenses DROP COLUMN IF EXISTS description
        """,
        """
        ALTER TABLE expenses ADD COLUMN description TEXT
        """
    )
]
