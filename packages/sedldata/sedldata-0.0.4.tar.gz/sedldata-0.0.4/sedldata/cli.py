import os
import click
import datetime
import pprint

import alembic.config

from sedldata.lib import Session


@click.group()
def cli():
    pass


@cli.command()
def upgrade():
    session = Session()
    session.db.upgrade()


@cli.command()
@click.argument('infile')
@click.argument('outfile')
@click.option('--collection', default=None)
def load(infile, outfile, collection):
    session = Session()
    session.load_xlsx(collection, infile, outfile)

@cli.command()
def collections():
    # Dump the datatable
    click.echo("Dump\n")

    session = Session()
    results = session.get_results('''select * from collection_summary''')
    for row in results['data']:
        pprint.pprint(dict(row))
