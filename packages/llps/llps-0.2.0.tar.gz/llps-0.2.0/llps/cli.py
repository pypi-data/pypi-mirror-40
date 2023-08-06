
import click

from .project_schema import ProjectSchema
from .exceptions import InvalidLLPSException


@click.group()
def main():
    pass


@main.command('validate')
@click.argument('filepath')
def cli_validate_schema(filepath):
    """Validate a schema as a valid project schema."""
    try:
        ProjectSchema.from_file(filepath)
    except InvalidLLPSException as exc:
        click.echo(exc, err=True)


if __name__ == '__main__':
    main()
