"""Add unique constraints to JobTag and Tag models

Revision ID: 7b735e1961a1
Revises: cd89ce4ab3f0
Create Date: 2025-05-27 18:42:23.901816

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7b735e1961a1"
down_revision: Union[str, None] = "cd89ce4ab3f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add unique constraint to job_tags table for (job_id, tag_id)
    op.create_unique_constraint("unique_job_tag", "job_tags", ["job_id", "tag_id"])

    # Remove the existing unique constraint on tags.name
    op.drop_index("ix_tags_name")

    # Add unique constraint to tags table for (name, category)
    op.create_unique_constraint("unique_name_category", "tags", ["name", "category"])

    # Recreate the index on tags.name (without unique constraint)
    op.create_index("ix_tags_name", "tags", ["name"])


def downgrade() -> None:
    # Remove the unique constraint from job_tags
    op.drop_constraint("unique_job_tag", "job_tags", type_="unique")

    # Remove the unique constraint from tags
    op.drop_constraint("unique_name_category", "tags", type_="unique")

    # Drop the non-unique index on tags.name
    op.drop_index("ix_tags_name")

    # Recreate the unique index on tags.name
    op.create_index("ix_tags_name", "tags", ["name"], unique=True)
