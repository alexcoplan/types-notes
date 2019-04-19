#!/usr/bin/env python3
#
# Render errata to LaTeX.

import yaml

with open("errata.yml", "r") as f:
  errata = yaml.safe_load(f)

tex_start = """
\\documentclass[10pt]{article}
\\usepackage{fullpage} % geometry
\\usepackage{bussproofs} % proof trees
\\usepackage{amssymb}
\\EnableBpAbbreviations
% \\usepackage{stmaryrd}

\\begin{document}
\\title{Types Errata (2018-2019)}
\\author{Alex Coplan}
\maketitle
"""

tex_end = """
\end{document}
"""

with open("errata.tex", "w") as f:
  f.write(tex_start)
  lectures = errata["lectures"]
  for lec in lectures:
    sec = "\\section*{Lecture %d: %s}\n" % (lec["lecture"], lec["title"])
    f.write(sec)
    f.write("\\begin{itemize}\n")
    for item in lec["errata"]:
      f.write("\\item Slide %d: %s\n" % (item["slide"], item["erratum"]))
    f.write("\\end{itemize}\n")
  f.write(tex_end)
