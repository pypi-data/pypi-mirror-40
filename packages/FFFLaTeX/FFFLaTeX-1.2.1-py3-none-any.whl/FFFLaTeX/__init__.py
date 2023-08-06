#  -*- coding: utf-8 -*-

import os

import urllib3
from bs4 import BeautifulSoup, NavigableString


imgUrls = set()
imgSize = {}
imgNames = {}
imgExtension = {}


def sanitizeText(text: str):
    return text.replace(' ', ' ').replace("#", "\\#").replace("&",
                                                              "\\&").replace(
        "%", "\\%").replace("✕", "x")


def base10toN(val: int):
    """Change a  to a base-n number.
    Up to base-36 is supported without special notation."""
    num_rep = {
        0:  'a',
        1:  'b',
        2:  'c',
        3:  'd',
        4:  'e',
        5:  'f',
        6:  'g',
        7:  'h',
        8:  'i',
        9:  'j',
        10: 'k',
        11: 'l',
        12: 'm',
        13: 'n',
        14: 'o',
        15: 'p',
        16: 'q',
        17: 'r',
        18: 's',
        19: 't',
        20: 'u',
        21: 'v',
        22: 'w',
        23: 'x',
        24: 'y',
        25: 'z'
    }
    new_num_string = ''
    current = val
    if current == 0:
        return num_rep[0]
    while current != 0:
        remainder = current % 26
        remainder_string = num_rep[remainder]
        new_num_string = remainder_string + new_num_string
        current = current // 26
    return new_num_string


def generateName(index):
    return base10toN(index)


def discoverDimensions(tableelement):
    count_rows, count_cells = 0, 0
    for element in tableelement.descendants:
        if element.name in ["tr", "th"]:
            count_rows += 1
        if element.name in ["td"]:
            count_cells += 1
    return count_cells // count_rows


def generateLatexFromElement(element: NavigableString, size=0, inTable=False):
    if element in ['\n', '\t', "\r\n", '\r']:
        return
    if element.name == "ul":
        out.write("\\begin{itemize}\n")

        for c in element.children:
            generateLatexFromElement(c)

        out.write("\\end{itemize}\n")
    elif element.name == "table":
        size = discoverDimensions(element)
        sizeStr = (size - 1) * "c|" + "c"

        out.write("\\begin{figure}[H]\n\\resizebox{\\textwidth}{!}{\n\\begin{"
                  "tabular}{" + sizeStr + "}\n")

        generateLatexFromElement(element.tbody, size=size, inTable=True)

        out.write("\\end{tabular}}\n\\end{figure}\n")

    elif element.name == "tbody":
        for c in element.children:
            generateLatexFromElement(c, size=size, inTable=True)
    elif element.name == "tr":
        i = 0
        for c in element.children:
            if c.name == "td":
                generateLatexFromElement(c, inTable=True)
                i += 1
                if (i < size):
                    out.write('&')

        out.write("\\\\\\hline\n")
    elif element.name == "td":
        out.write(element.text.lstrip(

        ).rstrip())
        for c in element.children:
            generateLatexFromElement(c, inTable=True)

    elif element.name == "li":
        out.write(
            "\\item " + sanitizeText(element.text.lstrip().rstrip()) + "\n")
    elif element.name == "p":
        try:
            if (sanitizeText(element.text.lstrip().rstrip()) != "Webm/Mp4 "
                                                                "playback not supported on your device."):
                out.write("\\paragraph{}\n" + sanitizeText(
                    element.text.lstrip().rstrip()) + "\n")
        except Exception as e:
            print(e)
        for c in element.children:
            generateLatexFromElement(c)
    elif element.name == "h2":
        out.write(
            "\\section{" + sanitizeText(element.text.lstrip().rstrip()) + "}\n")
    elif element.name == "h3":
        out.write("\\subsection{" + sanitizeText(element.text.lstrip(

        ).rstrip()) + "}\n")
    elif element.name == "video":
        for c in element.children:
            generateLatexFromElement(c)
    elif element.name == "source":
        if (imgExtension[element.attrs["src"]] == ".webm"): return

        out.write("\\begin{figure}[H]\n\\centering\\includemedia["
                  "width=0.88\\linewidth,height=0.5\\linewidth, "
                  "attachfiles, \
                  transparent,"
                  "activate=pagevisible,"
                  "noplaybutton, \
                  passcontext,\
                  flashvars={\
                      source=" + imgNames[element.attrs["src"]] + imgExtension[
                      element.attrs[
                          "src"]] + "&autoPlay=true &loop=true &scaleMode=letterbox }, "
                                    "addresource=" + imgNames[
                      element.attrs["src"]] + imgExtension[element.attrs[
            "src"]] + "]{" + "\\color{gray}\\framebox[0.4\\linewidth][c]{"
                             "Loading Video}" + "}{VPlayer9.swf}\n\\end{"
                                                "figure}\n")

    elif element.name == "img":
        if not inTable:
            out.write("\\begin{figure}[H]\n\\centering")
        out.write("\\" + imgNames[element.attrs["src"]])
        if not inTable:
            out.write("\\end{figure}\n")


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    global out
    global imgUrls
    print("FFF Latex document generator\n")
    num = input("Enter the number of the current FFF: ")
    while True:
        try:
            num = int(num)
            break
        except Exception as e:
            num = input("Enter the number of the current FFF:")

    blog_url = "https://factorio.com/blog/post/fff-" + str(num)
    http = urllib3.PoolManager()
    response = http.request('GET', blog_url)

    soup = BeautifulSoup(response.data.decode('utf-8'), 'html5lib')

    for link in soup.find_all('img'):
        imgUrls.add(link.get('src'))
        width = link.get('width')
        if width is None:
            width = "0.8\\textwidth"
        imgSize[link.get('src')] = width

    for link in soup.find_all('source'):
        src = link.get('src')
        imgUrls.add(src)
        width = link.get('width')
        if width is None:
            width = "0.8\\textwidth"
        imgSize[link.get('src')] = width

    i = 0
    for imgUrl in imgUrls:
        name = "FFFparserNUM" + generateName(
            num).lower() + "IMG" + generateName(i).lower()
        for ext in [".png", ".jpg", ".gif", ".mp4", ".webm"]:
            if imgUrl.endswith(ext):
                imgExtension[imgUrl] = ext
                break

        print(imgUrl,"\t->\t",name, ", width=", imgSize[imgUrl])
        i += 1
        imgNames[imgUrl] = name

    imgUrls = filter(lambda url : not url.endswith(".webm"), imgUrls)


    doc_name = "FFF" + str(num)

    ensure_dir("./" + doc_name + "/")

    with open("./" + doc_name + "/" + doc_name + ".tex", "w") as out:
        header = """
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
    """

        out.write(header)

        # generate constants
        for imgUrl in imgUrls:
            args = []
            if imgSize[imgUrl] is not None:
                args.append("width=" + str(imgSize[imgUrl]))

            out.write("\\write18{wget -N " + imgUrl + " -P ../out/pics/ -O " +
                      imgNames[imgUrl] + imgExtension[
                          imgUrl] + " }\n" + "\\newcommand{\\" + imgNames[
                          imgUrl] + "}{\\includegraphics[" + ','.join(
                args) + "]{" + imgNames[imgUrl] + imgExtension[imgUrl] + "}}\n")

        out.write("""
    \\title{Traduction FFF numero """ + str(num) + """}
    \\author{""" + blog_url + """}
    \\begin{document}
    \\maketitle
    \\tableofcontents
    """)
        # generate content

        blog = soup.find("div", class_="blog-post")

        for element in blog.children:
            generateLatexFromElement(element)

        out.write("\\end{document}\n")


if __name__ == "__main__":
    main()
