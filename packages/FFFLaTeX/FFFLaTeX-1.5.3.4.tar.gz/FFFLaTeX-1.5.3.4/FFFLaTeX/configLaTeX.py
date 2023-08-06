#  -*- coding: utf-8 -*-

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
\\title{Traduction FFF numero @fff_num ) }
\\author{ @fff_url }
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
    @generate_latex_from_children 
\\end{itemize}\n
""",
    "table":          """
\\begin{figure}[H]\n
    \\resizebox{\\textwidth}{!}{\n
    @table_flag_set
    \\begin{ tabular }{ @table_size_str }\n 
        
        @generate_latex_from_children 
        
    \\end{tabular}}\n
    @table_flag_clear
\\end{figure}\n
""",
    "tbody":          """
@generate_latex_from_children
""",
    "tr":             """
@generate_table_cell_latex
""",
    "td":             """
@sanitize_text
@generate_latex_from_children
""",
    "li":             """
\\item @sanitize_text \n
""",
    "p":              """
@playback_check
@generate_latex_from_children
""",

    "h2":             """
\\section{ @sanitize_text }\n
""",
    "h3":             """
\\subsection{ @sanitize_text }\n
""",
    "video":          """
@generate_latex_from_children
""",
    "source":         """
@add_video
""",
    "img":            """
@add_image
""",
    "a":              """
@add_link
"""
}
