# © 2015 James R. Barlow: github.com/jbarlow83
#
# This file is part of OCRmyPDF.
#
# OCRmyPDF is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OCRmyPDF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OCRmyPDF.  If not, see <http://www.gnu.org/licenses/>.

# unpaper documentation:
# https://github.com/Flameeyes/unpaper/blob/master/doc/basic-concepts.md

import os
import sys
from functools import lru_cache
from subprocess import STDOUT, CalledProcessError, check_output
from tempfile import NamedTemporaryFile

from . import get_version
from ..exceptions import MissingDependencyError

try:
    from PIL import Image
except ImportError:
    print("Could not find Python3 imaging library", file=sys.stderr)
    raise


@lru_cache(maxsize=1)
def version():
    return get_version('unpaper')


def run(input_file, output_file, dpi, log, mode_args):
    args_unpaper = ['unpaper', '-v', '--dpi', str(dpi)] + mode_args

    SUFFIXES = {'1': '.pbm', 'L': '.pgm', 'RGB': '.ppm'}

    im = Image.open(input_file)
    if im.mode not in SUFFIXES.keys():
        log.info("Converting image to other colorspace")
        try:
            if im.mode == 'P' and len(im.getcolors()) == 2:
                im = im.convert(mode='1')
            else:
                im = im.convert(mode='RGB')
        except IOError as e:
            log.error("Could not convert image with type " + im.mode)
            im.close()
            raise MissingDependencyError() from e

    try:
        suffix = SUFFIXES[im.mode]
    except KeyError:
        log.error("Failed to convert image to a supported format.")
        im.close()
        raise MissingDependencyError() from e

    with NamedTemporaryFile(suffix=suffix) as input_pnm, NamedTemporaryFile(
        suffix=suffix, mode="r+b"
    ) as output_pnm:
        im.save(input_pnm, format='PPM')
        im.close()

        os.unlink(output_pnm.name)

        args_unpaper.extend([input_pnm.name, output_pnm.name])
        try:
            stdout = check_output(
                args_unpaper, close_fds=True, universal_newlines=True, stderr=STDOUT
            )
        except CalledProcessError as e:
            log.debug(e.output)
            raise e from e
        else:
            log.debug(stdout)
            # unpaper sets dpi to 72
            Image.open(output_pnm.name).save(output_file, dpi=(dpi, dpi))


def clean(input_file, output_file, dpi, log):
    run(
        input_file,
        output_file,
        dpi,
        log,
        [
            '--layout',
            'none',
            '--mask-scan-size',
            '100',  # don't blank out narrow columns
            '--no-border-align',  # don't align visible content to borders
            '--no-mask-center',  # don't center visible content within page
            '--no-grayfilter',  # don't remove light gray areas
            '--no-blackfilter',  # don't remove solid black areas
            '--no-deskew',  # don't deskew
        ],
    )
