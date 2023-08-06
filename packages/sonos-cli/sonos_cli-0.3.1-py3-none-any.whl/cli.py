import click

from sonos.commands import login, logout, get, set, play, pause, play_next, play_prev, get_status, control_volume


@click.group()
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(get)
cli.add_command(set)
cli.add_command(play_next)
cli.add_command(pause)
cli.add_command(play)
cli.add_command(play_prev)
cli.add_command(get_status)
cli.add_command(control_volume)

if __name__ == '__main__':
    cli()
