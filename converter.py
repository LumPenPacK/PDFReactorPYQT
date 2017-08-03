#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os

# You can download the PDFreactor Web Service Python wrapper from:
# http://www.pdfreactor.com/download/get/?product=pdfreactor&type=webservice_clients&jre=false
from PDFreactor import *

# Create new PDFreactor instance
import self as self

pdfReactor = PDFreactor("http://localhost:9423/service/rest")

f = []


def get_html_files(input_dir):
    """ Get all html files within a directory. Also walk through sub folders recursively. """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                path = os.path.relpath(path, input_dir)
                f.append(path)

    for e in f:
        print("Found document " + e)


def convert_batch(input_dir, output_dir):
    get_html_files(input_dir)

    for e in f:

        path = os.path.join(output_dir, os.path.dirname(e))

        if not os.path.exists(path):
            os.makedirs(path)
        convert(os.path.join(input_dir, e), os.path.join(output_dir, os.path.splitext(e)[0] + ".pdf"))


def convert(input_f, output_f, remote=None):

    if not remote:
        config = {
            'document': "file:///" + input_f,
        }
    else:

        config = {
            'document': input_f,
        }


    # The resulting PDF
    result = None

    try:
        # Render document and save result
        result = pdfReactor.convertAsBinary(config)
    except Exception as e:
        # Not successful, print error and log
        print("Content-type: text/html\n\n")
        print("An Error Has Occurred")
        print(str(e))

    # Check if successful
    if result is not None:
        # Used to prevent newlines are converted to Windows newlines (\n --> \r\n)
        # when using Python on Windows systems
        if sys.platform == "win32":
            import msvcrt

            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        # Set the correct header for PDF output and echo PDF content
        print("Content-Type: application/pdf\n")

        print("input_f " + input_f)
        print("output_f " + output_f)

        write_pdf(output_f, result)


def write_pdf(output, stream):
    f = open(output, 'wb')
    f.write(stream)
    f.close()
