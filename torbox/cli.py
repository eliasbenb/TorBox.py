import inspect
import re
from pprint import pformat

import click
from typing_extensions import Any, Union

from .client import TorBox
from .services import (
    # IntegrationsServices,
    RSSService,
    TorrentsService,
    UsenetService,
    WebDLService,
)


class TorBoxCLI:
    def __init__(self):
        self.services = {
            # "integrations": IntegrationsServices,
            "rss": RSSService,
            "torrents": TorrentsService,
            "usenet": UsenetService,
            "webdl": WebDLService,
        }

    def generate_commands(self):
        @click.group()
        @click.option("--api-key", "-k", required=True, help="TorBox API key")
        @click.option(
            "--base-url",
            help="TorBox API base URL",
            required=False,
            default="https://api.torbox.app/v1",
        )
        @click.option(
            "--pretty",
            "-p",
            is_flag=True,
            help="Pretty print object output",
        )
        @click.pass_context
        def cli(ctx, api_key, base_url, pretty):
            """TorBox CLI - Manage your TorBox services"""
            ctx.ensure_object(dict)
            ctx.obj = {
                "client": TorBox(api_key=api_key, base_url=base_url),
                "pretty": pretty,
            }

        for service_name, service_class in self.services.items():
            service_group = click.Group(
                name=service_name, help=f"Manage {service_name} operations"
            )

            for name, func in inspect.getmembers(
                service_class, predicate=inspect.isfunction
            ):
                if not name.startswith("_"):
                    params = inspect.signature(func).parameters
                    command_options = []
                    doc_string = inspect.getdoc(func) or ""

                    for param_name, param in params.items():
                        if param_name not in ["self"]:
                            param_type = (
                                param.annotation
                                if param.annotation != inspect._empty
                                else Any
                            )
                            if (
                                hasattr(param_type, "__origin__")
                                and param_type.__origin__ is Union
                            ):
                                param_type = param_type.__args__[
                                    0
                                ]  # Use the first type from Union
                            required = param.default == inspect._empty
                            param_help = ""

                            if doc_string:
                                param_pattern = rf"\s+{param_name}\s*\((.*?)\):"
                                param_match = re.search(param_pattern, doc_string)
                                if param_match:
                                    param_help = param_match.group(1)

                            command_options.append(
                                click.Option(
                                    ["--" + param_name],
                                    required=required,
                                    type=param_type,
                                    help=param_help,
                                )
                            )

                    def make_callback(service_name, cmd_func, _):
                        @click.pass_context
                        def callback(ctx, **kwargs):
                            service = getattr(ctx.obj["client"], service_name)
                            result = cmd_func(service, **kwargs)
                            if ctx.obj["pretty"]:
                                click.echo(click.style(pformat(result), fg="green"))
                            else:
                                click.echo(str(result))

                        return callback

                    command = click.Command(
                        name=name,
                        callback=make_callback(service_name, func, name),
                        params=command_options,
                        help=doc_string,
                    )
                    service_group.add_command(command)
            cli.add_command(service_group)

        return cli


def main():
    cli = TorBoxCLI().generate_commands()
    cli()


if __name__ == "__main__":
    main()
