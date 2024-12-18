import inspect
import re
from pprint import pformat
from typing import get_args, get_origin

import click
from typing_extensions import Any, Union

from .client import TorBox
from .services import (
    IntegrationsServices,
    RSSService,
    StatsService,
    TorrentsService,
    UsenetService,
    UserService,
    WebDLService,
)


class TorBoxCLI:
    def __init__(self):
        self.services = {
            "integrations": IntegrationsServices,
            "rss": RSSService,
            "stats": StatsService,
            "torrents": TorrentsService,
            "usenet": UsenetService,
            "user": UserService,
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
                name=service_name, help=f"Run {service_name} operations"
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
                            required = param.default == inspect._empty
                            param_help = ""

                            # Handle Union types
                            if get_origin(param_type) is Union:
                                param_type = get_args(param_type)[0]

                            # Handle list types
                            is_list = False
                            if get_origin(param_type) is list:
                                is_list = True
                                param_type = get_args(param_type)[0]

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
                                    multiple=is_list,
                                    help=param_help,
                                )
                            )

                    def make_callback(service_name, cmd_func, _):
                        @click.pass_context
                        def callback(ctx, **kwargs):
                            service = getattr(ctx.obj["client"], service_name)

                            for key, value in kwargs.items():
                                if isinstance(value, tuple):
                                    if key == "torrent_hashes":
                                        kwargs[key] = ",".join(value)
                                    else:
                                        kwargs[key] = list(value)

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
