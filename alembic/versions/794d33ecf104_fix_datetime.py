"""fix datetime

Revision ID: 794d33ecf104
Revises: 3e846cc615a4
Create Date: 2025-10-19 11:05:02.343325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '794d33ecf104'
down_revision: Union[str, Sequence[str], None] = '3e846cc615a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Изменяем колонки на TIMESTAMP WITH TIME ZONE
    op.alter_column('projects', 'created_at',
                    existing_type=sa.DateTime(),
                    type_=sa.DateTime(timezone=True),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')

    op.alter_column('projects', 'updated_at',
                    existing_type=sa.DateTime(),
                    type_=sa.DateTime(timezone=True),
                    postgresql_using='updated_at AT TIME ZONE \'UTC\'')

    op.alter_column('users', 'created_at',
                    existing_type=sa.DateTime(),
                    type_=sa.DateTime(timezone=True),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')

    op.alter_column('documents', 'created_at',
                    existing_type=sa.DateTime(),
                    type_=sa.DateTime(timezone=True),
                    postgresql_using='created_at AT TIME ZONE \'UTC\'')

    op.alter_column('documents', 'updated_at',
                    existing_type=sa.DateTime(),
                    type_=sa.DateTime(timezone=True),
                    postgresql_using='updated_at AT TIME ZONE \'UTC\'')


def downgrade() -> None:
    """Downgrade schema."""
    # Возвращаем обратно на WITHOUT TIME ZONE
    op.alter_column('documents', 'updated_at',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.DateTime())

    op.alter_column('documents', 'created_at',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.DateTime())

    op.alter_column('users', 'created_at',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.DateTime())

    op.alter_column('projects', 'updated_at',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.DateTime())

    op.alter_column('projects', 'created_at',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.DateTime())
