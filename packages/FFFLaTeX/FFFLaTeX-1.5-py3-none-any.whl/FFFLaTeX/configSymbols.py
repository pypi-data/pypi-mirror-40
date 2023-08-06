from bs4 import NavigableString

from configLaTeX import get_latex_for_element


def generateLatexFromElement(element: NavigableString, payload: dict):
    if element in ['\n', '\t', "\r\n", '\r']:
        return ""
    from parserutil import process_symbols
    data = process_symbols(element, payload,
                           get_latex_for_element(element.name))
    return data


def generateLatexFromChildren(element: NavigableString, payload: dict):
    for c in element.children:
        payload["TeX"] += generateLatexFromElement(c, payload)
    return payload


def discoverDimensions(element: NavigableString, payload=dict):
    count_rows, count_cells = 0, 0
    for c in element.descendants:
        if c.name in ["tr", "th"]:
            count_rows += 1
        if c.name in ["td"]:
            count_cells += 1
    payload["tableSize"] = count_cells // count_rows
    return payload


def tableSizeStr(element: NavigableString, payload: dict):
    payload = discoverDimensions(element, payload)
    payload["TeX"] = (payload["tableSize"] - 1) * "c|" + "c"
    return payload


def tableFlagSet(element: NavigableString, payload: dict):
    payload["inTable"] = True
    return payload


def tableFlagClear(element: NavigableString, payload: dict):
    del payload["inTable"]
    return payload


def generateTableCellLaTeX(element: NavigableString, payload: dict):
    i = 0
    for c in element.children:
        if c.name == "td":
            payload["TeX"] += generateLatexFromElement(c, payload)
            i += 1
            if (i < payload["tableSize"]):
                payload["TeX"] += '&'

    payload["TeX"] += "\\\\\\hline\n"
    return payload


def strippedText(element: NavigableString, payload: dict):
    payload["TeX"] += element.text.lstrip().rstrip()
    for c in element.children:
        payload["TeX"] += generateLatexFromElement(c, payload)
    return payload


def sanitizeText(element: NavigableString, payload: dict):
    text = element.text
    cursed = {
        "#":    "\\#",
        "&":    "\\&",
        "%":    "\\%",
        "✕":    "x",
        "\xa0": " "
    }
    for c in cursed.keys():
        text = text.replace(c, cursed[c])
    payload["TeX"] = text.lstrip().rstrip()
    return payload


def playbackCheck(element: NavigableString, payload: dict):
    try:
        text = sanitizeText(element, payload)["TeX"]
        if (text.find("Webm/Mp4 playback not supported on your device.") != -1):
            payload["TeX"] = "\\paragraph{}\n" + text + "\n"
    except Exception as e:
        print(e)
    finally:
        return payload


def addVideo(element: NavigableString, payload: dict):
    from FFFparser import imgExtension
    if (imgExtension[element.attrs["src"]] == ".webm"):
        return payload

    payload["TeX"] += """
\\begin{figure}[H]\n
    \\centering
    \\includemedia[
        width=0.88\\linewidth,
        height=0.5\\linewidth, 
        attachfiles, 
        transparent,
        activate=pagevisible,
        noplaybutton, 
        passcontext,
        flashvars={
            source="""

    from FFFparser import imgNames
    payload["TeX"] += imgNames[element.attrs["src"]]
    payload["TeX"] += imgExtension[element.attrs["src"]]
    payload["TeX"] += """
            &autoPlay=true 
            &loop=true 
            &scaleMode=letterbox }, 
        addresource="""
    payload["TeX"] += imgNames[element.attrs["src"]]
    payload["TeX"] += imgExtension[element.attrs["src"]]
    payload["TeX"] += """]
    {{\\color{gray} Loading Video }}
    {VPlayer9.swf}\n
\\end{ figure }\n"""
    return payload


def addImage(element: NavigableString, payload: dict):
    figure = "inTable" not in payload.keys()
    if figure:
        payload["TeX"] += "\\begin{figure}[H]\n\\centering"
    from FFFparser import imgNames
    payload["TeX"] += "\\" + imgNames[element.attrs["src"]]
    if figure:
        payload["TeX"] += "\\end{figure}\n"
    return payload


def FFFurl(element: NavigableString, payload: dict):
    payload["TeX"] += payload["__url"]
    return payload


def FFFnum(element: NavigableString, payload: dict):
    payload["TeX"] += str(payload["__num"])
    return payload


symbols = {

    "@tableSizeStr":              tableSizeStr,
    "@generateLatexFromElement":  generateLatexFromChildren,
    "@generateLatexFromChildren": generateLatexFromChildren,
    "@generateTableCellLaTeX":    generateTableCellLaTeX,
    "@tableFlagSet":              tableFlagSet,
    "@tableFlagClear":            tableFlagClear,
    "@strippedText":              strippedText,
    "@sanitizeText":              sanitizeText,
    "@playbackCheck":             playbackCheck,
    "@addVideo":                  addVideo,
    "@addImage":                  addImage,
    "@FFFurl":                    FFFurl,
    "@FFFnum":                    FFFnum

}
