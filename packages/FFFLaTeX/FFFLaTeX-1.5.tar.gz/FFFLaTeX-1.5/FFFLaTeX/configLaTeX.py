def get_latex_for_element(name: str):
    if name in tagTex.keys():
        return tagTex[name]
    return ""


tagTex = {
    "documentHeader": """
\\documentclass{article}

\\usepackage[cp1252]{inputenc}
\\usepackage{graphicx}
\\usepackage{media9}
\\usepackage[OT1]{fontenc}
\\usepackage{tabularx}
\\usepackage{float}
\\usepackage{pgfplotstable}
\\usepackage[allbordercolors=white]{hyperref}
\\usepackage[french]{babel}
""",
    "documentTitle":  """
\\title{Traduction FFF numero @FFFnum ) }
\\author{ @FFFurl }
""",
    "documentBegin":  """
\\begin{document}
    \\maketitle
    \\tableofcontents
""",
    "documentEnd":    """
\\end{document}\n
""",
    "ul":             """
\\begin{itemize}\n 
    @generateLatexFromElement 
\\end{itemize}\n
""",
    "table":          """
\\begin{figure}[H]\n
    \\resizebox{\\textwidth}{!}{\n
    @tableFlagSet
    \\begin{ tabular }{ @tableSizeStr }\n 
        
        @generateLatexFromElement 
        
    \\end{tabular}}\n
    @tableFlagClear
\\end{figure}\n
""",
    "tbody":          """
@generateLatexFromChildren
""",
    "tr":             """
@generateTableCellLaTeX
""",
    "td":             """
@sanitizeText
@generateLatexFromChildren
""",
    "li":             """
\\item @sanitizeText \n
""",
    "p":              """
@playbackCheck
@generateLatexFromChildren
""",

    "h2":             """
\\section{ @sanitizeText }\n
""",
    "h3":             """
\\subsection{ @sanitizeText }\n
""",
    "video":          """
@generateLatexFromChildren
""",
    "source":         """
@addVideo
""",
    "img":            """
@addImage
"""
}
