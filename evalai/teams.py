import click
import sys
import validators

from click import echo, style

from evalai.utils.teams import create_team, display_teams


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--host", "-h", is_flag=True, help="View your host teams.")
@click.option(
    "--participant", "-p", is_flag=True, help="View your host teams."
)
def teams(ctx, host, participant):
    """
    List all the participant/host teams of a user.
    """
    """
    Invoked by running `evalai teams`
    """
    if ctx.invoked_subcommand is None:
        if host == participant:
            echo(
                style("Sorry, wrong flag. Please pass either one of the flags "
                      "{} {} {}.", bold=True, fg="red").format(
                    style("--participant", bold=True, fg="yellow"),
                    style("or", bold=True, fg="red"),
                    style("--host", bold=True, fg="yellow"),
                )
            )
            sys.exit(1)

        display_teams(host)


@teams.command()
@click.argument("TEAM", type=str)
def create(team):
    """
    Create a participant or host team.
    """
    """
    Invoked by running `evalai teams create`
    """
    is_host = False
    if team not in ("host", "participant"):
        echo(
            style("Sorry, wrong argument. Please choose either "
                  "{} {} {}.", bold=True, fg="red").format(
                style("participant", bold=True, fg="yellow"),
                style("or", bold=True, fg="red"),
                style("host", bold=True, fg="yellow"),
            )
        )
        sys.exit(1)

    team_name = click.prompt(
        style("Enter team name", bold=True, fg="cyan"), type=str)
    if click.confirm(
        style("Please confirm the team name - {}".format(team_name), bold=True, fg="cyan"), abort=True
    ):
        team_url = ""
        if click.confirm(
            style("Do you want to enter the Team URL".format(
                team_name), bold=True, fg="cyan")
        ):
            team_url = click.prompt(
                style("Team URL", bold=True, fg="cyan"), type=str)
            while not (
                validators.url(team_url) or validators.domain(team_url)
            ):
                echo(
                    style("Sorry, please enter a valid link.",
                          bold=True,
                          fg="red",
                          )
                )
                team_url = click.prompt(
                    style("Team URL", bold=True, fg="cyan"), type=str)

        is_host = team == "host"
        create_team(team_name, team_url, is_host)
