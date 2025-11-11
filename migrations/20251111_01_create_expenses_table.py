"""
Create expenses table

Author: Vlad
Created: 2025-11-10
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            event_name TEXT NOT NULL,
            category TEXT,
            description TEXT,
            amount NUMERIC(10, 2),
            date DATE NOT NULL,
            photo_urls TEXT[],
            created_at TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        DROP TABLE IF EXISTS expenses
        """
    )
]
