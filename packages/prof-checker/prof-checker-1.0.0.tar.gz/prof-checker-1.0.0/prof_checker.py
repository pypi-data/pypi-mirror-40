import re
import subprocess
import argparse
import click
from enum import Enum
from functools import partial
from tokenize import ENCODING, NEWLINE, NL, STRING, tokenize

__version__ = "1.0.0"

out = partial(click.secho, bold=True, err=True)


def fetch_strings(f, src, strings_found, infos):
    for tok in tokenize(f.readline):
        if tok.type == STRING:
            current_string = tok.string
            if '"""' == current_string[:3]:
                current_string = current_string[3: -3]
            else:
                current_string = current_string[1: -1]
            current_string = current_string.strip("\n")
            current_string = current_string.strip(" ")
            strings_found.append(current_string)
            infos.append((src, tok.start[0]))


def output_results(strings, infos, probability):
    assert (len(strings) == len(infos))
    if probability is None or not 0 < probability < 1:
        from profanity_check import predict
        predictions = predict(strings)
        probability = 0
    else:
        from profanity_check import predict_prob
        predictions = predict_prob(strings)

    results = list(filter(lambda x: predictions[x[0]] > probability, enumerate(infos)))

    if results:
        click.secho("Probable profanities found: ", err=True)
        for result in results:
            out("\tIn {} on line {}: {}".format(result[1][0], result[1][1], strings[result[0]]))
        return -1

    click.secho("No profanities found, yaay!")
    return 0


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "-P",
    "--probability",
    type=float,
    help="Instead of prediction, use probability threshold",
)
@click.version_option(version=__version__)
@click.argument(
    "src",
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True,
    ),
    is_eager=True,
)
@click.pass_context
def main(ctx, probability, src):
    """ Profanity checker wrapper for python scripts/services """
    if not src:
        out("No paths given, nothing to do...")
        return

    strings_found = []
    infos = []
    for fl in set(src):
        with open(fl, "rb") as f:
            fetch_strings(f, fl, strings_found, infos)

    output_results(strings_found, infos, probability)


if __name__ == "__main__":
    main()
