# -*- coding: utf-8 -*-
#
################################################################################
#
#   Copyright 2017-2018 ElevenPaths
#
#   Neto is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


import os
import re
import timeout_decorator


REGEXPS = {
    "possible_obfuscation":  [
        b"eval\(",
        b"encode",
        b"base64",
        b"base58",
        b"atob"
    ],
    "possible_payments":  [
        b"visa",
        b"VISA",
        b"[Mm]aster[Cc]ard",
        b"MASTERCARD",
        b"[Aa]merican_?[Ee]xpress",
        b"AMERICAN_?EXPRESS",
        b"[Pp]aypal"
    ],
    "pattern_recognition":  [
        b"pattern",
        b"regex",
        b"regularexpression"
    ],
    "external_connections": [
        b"XMLHttpRequest",
        b"GET",
        b"POST",
        b"PUT"
    ]
}


#@timeout_decorator.timeout(30, timeout_exception=StopIteration)
def runAnalysis(**kwargs):
    """
    Method that runs an analysis

    This method is dinamically loaded by neto.lib.extensions.Extension objects
    to conduct an analysis. The analyst can choose to perform the analysis on
    kwargs["extensionFile"] or on kwargs["unzippedFiles"]. It SHOULD return a
    dictionary with the results of the analysis that will be updated to the
    features property of the Extension.

    Args:
    -----
        kwargs: It currently contain:
            - extensionFile: A string to the local path of the extension.
            - unzippedFiles: A dictionary where the key is the relative path to
                the file and the the value the absolute path to the extension.
                {
                    "manifest.json": "/tmp/extension/manifest.json"
                    …
                }
    Returns:
    --------
        A dictionary where the key is the name given to the analysis and the
            value is the result of the analysis. This result can be of any
            format.
    """
    results = {}


    # Iterate through all the regexps
    for e, valuesRe in REGEXPS.items():
        results[e] = []
        # Iterate through all the files in the folder
        for f, realPath in kwargs["unzippedFiles"].items():
            if os.path.isfile(realPath):
                fileType = f.split(".")[-1].lower()
                
                # Extract matching strings from text files
                if fileType in ["js", "html", "htm", "css", "txt"]:
                    # Read the data
                    raw_data = open(realPath, "rb").read()
                    for exp in valuesRe:
                        values = re.findall(exp, raw_data)
                        for v in values:
                            # TODO: properly handle:
                            #   UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 29: unexpected end of data
                            try:
                                aux = {
                                    "value": v.decode("utf-8"),
                                    "path": f
                                }

                                results[e].append(aux)
                            except:
                                pass

    return {"suspicious": results}
