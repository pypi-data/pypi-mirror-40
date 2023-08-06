#  -*- coding: utf-8 -*-

import os
import sys

import urllib3
from bs4 import BeautifulSoup

from parserutil import *


imgUrls = set()
imgSize = {}
imgNames = {}
imgExtension = {}


def print_help():
    print("USAGE : FFFLaTeX [<Number of FFF>|latest]")


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def latest_version():
    blog_list_url = "https://www.factorio.com/blog/"
    http = urllib3.PoolManager()
    response = http.request('GET', blog_list_url)

    soup = BeautifulSoup(response.data.decode('utf-8'), 'html5lib')
    last_blog_listing = soup.h2.find_next("ul").find_next("li")
    url = "https://factorio.com" + last_blog_listing.find_next("a").get("href")
    name = last_blog_listing.find_next("a").text.lstrip().rstrip()
    author = last_blog_listing.find_next("div").text.lstrip().rstrip()
    return (name, author, url)

def main(*args, **kwargs):
    global out
    global imgUrls
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print("FFF Latex document generator\n")

    print("Latest FFF:\t")
    latest_version_data = latest_version()
    print("\n".join(latest_version_data))

    blog_url = latest_version_data[2]
    if len(sys.argv) == 1:
        num = input("Enter the number of the current FFF: ")
        while True:
            try:
                num = int(num)
                break
            except Exception:
                num = input("Enter the number of the current FFF:")
    elif len(sys.argv) == 2:
        try:
            num = int(sys.argv[1])
            blog_url = "https://factorio.com/blog/post/fff-" + str(num)
        except Exception as e:
            if sys.argv[1] != "latest":
                print_help()
                return
    else:
        print_help()
        return

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
        name = "FFFparserNUM" + generate_name(
            num).lower() + "IMG" + generate_name(i).lower()
        for ext in [".png", ".jpg", ".gif", ".mp4", ".webm"]:
            if imgUrl.endswith(ext):
                imgExtension[imgUrl] = ext
                break

        print(imgUrl, "\t->\t", name, ", width=", imgSize[imgUrl])
        i += 1
        imgNames[imgUrl] = name

    imgUrls = filter(lambda url: not url.endswith(".webm"), imgUrls)

    doc_name = "FFF" + str(num)

    ensure_dir("./" + doc_name + "/")

    with open("./" + doc_name + "/" + doc_name + ".tex", "w") as out:
        payload = {
            "TeX":   "",
            "__num": num,
            "__url": blog_url
        }

        from configLaTeX import get_latex_for_element

        out.write(process_symbols(None, payload,
                                  get_latex_for_element("documentHeader")))

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

        out.write(process_symbols(None, payload,
                                  get_latex_for_element("documentTitle")))

        out.write(process_symbols(None, payload,
                                  get_latex_for_element("documentBegin")))

        # generate content

        blog = soup.find("div", class_="blog-post")

        for element in blog.children:
            from configSymbols import generateLatexFromElement
            out.write(generateLatexFromElement(element, payload))

        out.write(process_symbols(None, payload,
                                  get_latex_for_element("documentEnd")))


if __name__ == "__main__":
    main()
