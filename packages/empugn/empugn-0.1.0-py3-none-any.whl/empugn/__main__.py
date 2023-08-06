import argparse
import os
import sys

from yattag import indent

from .input import PARSERS
from . import empugn


def get_parser():
    parser = argparse.ArgumentParser(
        description='Generate HTML or XML from YAML or JSON',
        prog='empugn',
    )
    parser.add_argument(
        'template_file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='The YAML or JSON template to process. If unspecified, the template is read from stdin.',
    )

    parser.add_argument(
        '--template-format',
        choices=PARSERS,
        default=None,
        help=(
            'Template format. If unspecified, attempted to be autodetected from the '
            'input filename (but defaults to YAML).'
        ),
    )
    parser.add_argument(
        '--output-file',
        '-o',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output file. If unspecified, the HTML/XML output is written into stdout.',
    )
    parser.add_argument(
        '--indent',
        '-i',
        type=str,
        default='  ',
        help=(
            'Indent output. If integer, this many spaces will be used. If string, will be used literally. '
            'To disable indentation, pass in the empty string.'
        )
    )
    parser.add_argument(
        '--doctype',
        type=str,
        default='html',
        help='The HTML/XML doctype for output. To disable, pass in the empty string.',
    )
    parser.add_argument(
        '--use-emrichen',
        '-r',
        action='store_true',
        default=False,
        help=(
            'Use Emrichen to process tags, making Empugn a full featured HTML template engine. '
            'Emrichen must be installed.'
        ),
    )
    parser.add_argument(
        '--var-file',
        '-f',
        dest='var_files',
        metavar='VAR_FILE',
        type=argparse.FileType('r'),
        action='append',
        default=[],
        help=(
            '(Implies --use-emrichen) A YAML file containing an object whose top-level keys will be defined as variables. '
            'May be specified multiple times.'
        ),
    )
    parser.add_argument(
        '--define',
        '-D',
        metavar='VAR=VALUE',
        action='append',
        default=[],
        help='(Implies --use-emrichen) Defines a single variable. May be specified multiple times.',
    )
    parser.add_argument(
        '--include-env',
        '-e',
        action='store_true',
        default=False,
        help='(Implies --use-emrichen) Expose process environment variables to the template.',
    )
    return parser


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = get_parser()
    args = parser.parse_args(args)

    if args.define or args.include_env or args.var_files:
        args.use_emrichen = True

    if args.use_emrichen:
        from emrichen import Context, Template

        override_variables = dict(item.split('=', 1) for item in args.define)

        variable_sources = list(args.var_files)
        if args.include_env:
            variable_sources.append(os.environ)

        context = Context(*variable_sources, **override_variables)
        template = Template.parse(args.template_file, format=args.template_format)
        input = template.enrich(context)
    else:
        from .input import parse
        input = parse(args.template_file, format=args.template_format)

    if len(input) != 1:
        raise TypeError('Input must have exactly one document. Multi-document YAML files are not supported.')

    output = empugn(input, doctype=args.doctype)

    if args.indent:
        try:
            indentation = ' ' * int(args.indent)
        except ValueError:
            indentation = args.indent

        output = indent(output, indentation=indentation)

    args.output_file.write(output)

if __name__ == '__main__':
    main()
