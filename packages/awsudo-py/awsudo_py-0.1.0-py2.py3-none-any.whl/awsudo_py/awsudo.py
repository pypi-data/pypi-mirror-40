#!/usr/bin/env python3
"""
Set AWS environment variables using profiles. This is useful for something like
Terraform, which has poor support for AWS MFA.
"""
import argparse
from pathlib import Path
from typing import List, Optional
import os
import sys

from botocore import credentials
from botocore.session import Session
import boto3


def run_program(executable: str, args: List[str], env: dict):
    """
    We exec the included variable
    """
    os.execlpe(executable, executable, *args, env)


def get_credentials(profile: str = "default", environment: Optional[dict] = None):
    """
    Use session cache so users don't need to use MFA while there are valid
    session tokens. This is the behavior of the AWSCLI and what we are trying to
    emulate.

    Modified from:
    https://github.com/boto/botocore/pull/1338/#issuecomment-368472031
    """
    # By default the cache path is ~/.aws/boto/cache
    cli_cache = (Path.home() / ".aws" / "cli" / "cache").absolute()

    # Construct botocore session with cache
    session = Session(profile=profile)
    session.get_component("credential_provider").get_provider(
        "assume-role"
    ).cache = credentials.JSONFileCache(cli_cache)

    # return credentials from session
    creds = boto3.Session(
        botocore_session=session, profile_name=profile
    ).get_credentials()

    return {
        "AWS_ACCESS_KEY_ID": creds.access_key,
        "AWS_SECRET_ACCESS_KEY": creds.secret_key,
        "AWS_SESSION_TOKEN": creds.token,
    }


def get_environment(credentials: dict) -> dict:
    """Return environment updated with credentials"""
    for key, value in credentials.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    return os.environ


def main():
    parser = argparse.ArgumentParser(
        description="Set environment variables using profile"
    )
    parser.add_argument("-p", "--profile",help="AWS Profile to assume", default="default")
    parser.add_argument(
        "executable", help="executable to run", nargs=1, metavar="PROG"
    )
    parser.add_argument(
        "args", help="args to run with program", nargs="*", metavar="ARG"
    )
    if len(sys.argv) < 2:
        parser.print_help()
        parser.exit(2)
    parsed = parser.parse_args()
    executable, profile = parsed.executable[0], parsed.profile
    credentials = get_credentials(profile)
    print(credentials)
    environment = get_environment(credentials)
    run_program(executable, parsed.args, env=environment)


if __name__ == "__main__":
    main()
