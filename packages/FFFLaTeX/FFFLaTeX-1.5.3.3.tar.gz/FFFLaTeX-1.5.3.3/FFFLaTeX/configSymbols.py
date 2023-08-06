#  -*- coding: utf-8 -*-
from bs4 import NavigableString

import FFFLaTeX.parserutil as util
from FFFLaTeX.configLaTeX import get_latex_for_element


def sanitize_string(text: str) -> str:
    cursed = {
        "#":    "\\#",
        "&":    "\\&",
        "%":    "\\%",
        "✕":    "x",
        "\xa0": " "
    }
    for c in cursed.keys():
        text = text.replace(c, cursed[c])
    return text.lstrip().rstrip()


def generate_latex_from_element(element: NavigableString, payload: dict):
    if element in ['\n', '\t', "\r\n", '\r']:
        return ""
    data = util.process_symbols(element, payload,
                                get_latex_for_element(element.name))
    return data


def generate_latex_from_children(element: NavigableString, payload: dict):
    for c in element.children:
        payload["TeX"] += generate_latex_from_element(c, payload)
    return payload


def discover_dimensions(element: NavigableString, payload=dict):
    count_rows, count_cells = 0, 0
    for c in element.descendants:
        if c.name in ["tr", "th"]:
            count_rows += 1
        if c.name in ["td"]:
            count_cells += 1
    payload["tableSize"] = count_cells // count_rows
    return payload


def table_size_str(element: NavigableString, payload: dict):
    payload = discover_dimensions(element, payload)
    payload["TeX"] = (payload["tableSize"] - 1) * "c|" + "c"
    return payload


def table_flag_set(element: NavigableString, payload: dict):
    payload["inTable"] = True
    return payload


def table_flag_clear(element: NavigableString, payload: dict):
    del payload["inTable"]
    return payload


def generate_table_cell_latex(element: NavigableString, payload: dict):
    i = 0
    for c in element.children:
        if c.name == "td":
            payload["TeX"] += generate_latex_from_element(c, payload)
            i += 1
            if (i < payload["tableSize"]):
                payload["TeX"] += '&'

    payload["TeX"] += "\\\\\\hline\n"
    return payload


def stripped_text(element: NavigableString, payload: dict):
    payload["TeX"] += element.text.lstrip().rstrip()
    for c in element.children:
        payload["TeX"] += generate_latex_from_element(c, payload)
    return payload


def sanitize_text(element: NavigableString, payload: dict):
    payload["TeX"] = sanitize_string(element.text)
    return payload


def playback_check(element: NavigableString, payload: dict):
    try:
        text = sanitize_text(element, payload)["TeX"]
        if (text.find("Webm/Mp4 playback not supported on your device.") != -1):
            payload["TeX"] = "\\paragraph{}\n" + text + "\n"
    except Exception as e:
        print(e)
    finally:
        return payload


def add_video(element: NavigableString, payload: dict):
    if (payload["__img_ext"][element.attrs["src"]] == ".webm"):
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

    payload["TeX"] += payload["__img_names"][element.attrs["src"]]
    payload["TeX"] += payload["__img_ext"][element.attrs["src"]]
    payload["TeX"] += """
            &autoPlay=true 
            &loop=true 
            &scaleMode=letterbox }, 
        addresource="""
    payload["TeX"] += payload["__img_names"][element.attrs["src"]]
    payload["TeX"] += payload["__img_ext"][element.attrs["src"]]
    payload["TeX"] += """]
    {{\\color{gray} Loading Video }}
    {VPlayer9.swf}\n
\\end{ figure }\n"""
    return payload


def add_image(element: NavigableString, payload: dict):
    figure = "inTable" not in payload.keys()
    if figure:
        payload["TeX"] += "\\begin{figure}[H]\n\\centering"
    payload["TeX"] += "\\" + payload["__img_names"][element.attrs["src"]]
    if figure:
        payload["TeX"] += "\\end{figure}\n"
    return payload


def add_link(element: NavigableString, payload: dict):
    payload["TeX"] += "\\href{" + element.attrs[
        "href"] + "}{" + sanitize_string(
        element.text) + "}"
    return payload


def fff_url(element: NavigableString, payload: dict):
    payload["TeX"] += payload["__url"]
    return payload


def fff_num(element: NavigableString, payload: dict):
    payload["TeX"] += str(payload["__num"])
    return payload


symbols = {

    "@table_size_str":               table_size_str,
    "@generate_latex_from_children": generate_latex_from_children,
    "@generate_table_cell_latex":    generate_table_cell_latex,
    "@table_flag_set":               table_flag_set,
    "@table_flag_clear":             table_flag_clear,
    "@stripped_text":                stripped_text,
    "@sanitize_text":                sanitize_text,
    "@playback_check":               playback_check,
    "@add_video":                    add_video,
    "@add_image":                    add_image,
    "@add_link":                     add_link,
    "@fff_url":                      fff_url,
    "@fff_num":                      fff_num

}