#  -*- coding: utf-8 -*-

import os
import sys

import urllib3
from bs4 import BeautifulSoup

import parserutil as util


def print_help():
    print("USAGE : FFFLaTeX [<Number of FFF>|latest]")


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_latest_version_data():
    blog_list_url = "https://www.factorio.com/blog/"
    soup = get_soup(blog_list_url)
    last_blog_listing = soup.h2.find_next("ul").find_next("li")
    url = "https://factorio.com" + last_blog_listing.find_next("a").get("href")
    name = last_blog_listing.find_next("a").text.lstrip().rstrip()
    author = last_blog_listing.find_next("div").text.lstrip().rstrip()
    return (name, author, url)


def print_latest_version(version_data: tuple):
    print("Latest FFF:\t" + "\n".join(version_data))


def get_blog_url(latest_version_data: tuple) -> str:
    blog_url = latest_version_data[2]
    if len(sys.argv) == 1:
        print_latest_version(latest_version_data)
        num = input("Enter the number of the current FFF: ")
        while True:
            try:
                num = int(num)
                break
            except Exception:
                num = input("Enter the number of the current FFF:")
        print("Generating FFF", num)
        return "https://factorio.com/blog/post/fff-" + str(num)
    elif len(sys.argv) == 2:
        try:
            num = int(sys.argv[1])
            print("Generating FFF", num)
            return "https://factorio.com/blog/post/fff-" + str(num)
        except Exception as e:
            if sys.argv[1] != "latest":
                print_help()
                exit(-1)
    else:
        print_help()
        exit(-1)
    print("Generating latest FFF")
    return blog_url


def get_soup(url: str):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return BeautifulSoup(response.data.decode('utf-8'), 'html5lib')


def generate_img_data(soup, imgUrls, imgSize):
    for link in soup.find_all('img'):
        imgUrls.add(link.get('src'))
        width = link.get('width')
        if width is None:
            width = "0.8\\textwidth"
        imgSize[link.get('src')] = width
    return (soup, imgUrls, imgSize)


def generate_mp4_data(soup, imgUrls, imgSize):
    for link in soup.find_all('source'):
        src = link.get('src')
        imgUrls.add(src)
        width = link.get('width')
        if width is None:
            width = "0.8\\textwidth"
        imgSize[link.get('src')] = width
    return (soup, imgUrls, imgSize)


def generate_media_names(imgUrls, imgExtension, imgSize, imgNames):
    i = 0
    for imgUrl in imgUrls:
        name = "FFFparserIMG" + util.generate_name(i).lower()
        for ext in [".png", ".jpg", ".gif", ".mp4", ".webm"]:
            if imgUrl.endswith(ext):
                imgExtension[imgUrl] = ext
                break

        print(imgUrl, "\t->\t", name, ", width=", imgSize[imgUrl])
        i += 1
        imgNames[imgUrl] = name
    return (imgUrls, imgExtension, imgSize, imgNames)


def get_blog_number(url):
    num = ""
    for c in url[::-1]:
        if c.isnumeric():
            num = c + num
        else:
            return num


def filter_out_incompatible_medias(imgUrls):
    return filter(lambda url: not url.endswith(".webm"), imgUrls)


def main():
    imgUrls = set()
    imgSize = {}
    imgNames = {}
    imgExt = {}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    latest_version_data = get_latest_version_data()
    blog_url = get_blog_url(latest_version_data)
    num = get_blog_number(blog_url)
    soup = get_soup(blog_url)

    soup, imgUrls, imgSize = generate_img_data(soup, imgUrls, imgSize)
    soup, imgUrls, imgSize = generate_mp4_data(soup, imgUrls, imgSize)
    imgUrls, imgExt, imgSize, imgNames = generate_media_names(imgUrls, imgExt,
                                                              imgSize, imgNames)

    imgUrls = filter_out_incompatible_medias(imgUrls)

    doc_name = "FFF" + str(num)

    ensure_dir("./" + doc_name + "/")

    with open("./" + doc_name + "/" + doc_name + ".tex", "w") as out:
        payload = {
            "TeX":   "",
            "__num": num,
            "__url": blog_url,
            "__imgUrls": imgUrls,
            "__imgExt": imgExt,
            "__imgNames": imgNames,
            "__imgSize": imgSize
        }

        from configLaTeX import get_latex_for_element

        out.write(util.process_symbols(None, payload,
                                       get_latex_for_element("documentHeader")))

        # generate constants
        for imgUrl in imgUrls:
            args = []
            if imgSize[imgUrl] is not None:
                args.append("width=" + str(imgSize[imgUrl]))

            out.write("\\write18{wget -N " + imgUrl + " -P ../out/pics/ -O " +
                      imgNames[imgUrl] + imgExt[
                          imgUrl] + " }\n" + "\\newcommand{\\" + imgNames[
                          imgUrl] + "}{\\includegraphics[" + ','.join(
                args) + "]{" + imgNames[imgUrl] + imgExt[imgUrl] + "}}\n")

        out.write(util.process_symbols(None, payload,
                                  get_latex_for_element("documentTitle")))

        out.write(util.process_symbols(None, payload,
                                       get_latex_for_element("documentBegin")))

        # generate content

        blog = soup.find("div", class_="blog-post")

        for element in blog.children:
            from configSymbols import generateLatexFromElement
            out.write(generateLatexFromElement(element, payload))

        out.write(util.process_symbols(None, payload,
                                       get_latex_for_element("documentEnd")))


if __name__ == "__main__":
    main()
