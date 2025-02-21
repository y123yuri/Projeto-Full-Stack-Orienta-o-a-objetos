"""Adicionando telefone à tabela restaurantes

Revision ID: 7aa5609b6bfe
Revises: d600e311783d
Create Date: 2025-02-20 22:40:12.986303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aa5609b6bfe'
down_revision = 'd600e311783d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comentarios_fake',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('restaurante_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurante_id'], ['restaurantes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('restaurantes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('telefone', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('descricao', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('link_maps', sa.String(length=300), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('restaurantes', schema=None) as batch_op:
        batch_op.drop_column('link_maps')
        batch_op.drop_column('descricao')
        batch_op.drop_column('telefone')

    op.drop_table('comentarios_fake')
    # ### end Alembic commands ###
