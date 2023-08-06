#  -*- coding: utf-8 -*-

import os
import sys

import urllib3
from bs4 import BeautifulSoup


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


def generate_img_data(soup, img_urls, img_size):
    for link in soup.find_all('img'):
        img_urls.add(link.get('src'))
        width = link.get('width')
        if width is None:
            width = "0.8\\textwidth"
        img_size[link.get('src')] = width
    return (soup, img_urls, img_size)


def generate_mp4_data(soup, img_urls, img_size):
    for link in soup.find_all('source'):
        src = link.get('src')
        img_urls.add(src)
        width = link.get('width')
        if width is None:
            width = "0.8\\textwidth"
        img_size[link.get('src')] = width
    return (soup, img_urls, img_size)


def generate_media_names(img_urls, img_extension, img_size, img_names):
    from FFFLaTeX.parserutil import generate_name

    i = 0
    for img_url in img_urls:
        name = "FFFparserIMG" + generate_name(i).lower()
        for ext in [".png", ".jpg", ".gif", ".mp4", ".webm"]:
            if img_url.endswith(ext):
                img_extension[img_url] = ext
                break

        print(img_url, "\t->\t", name, ", width=", img_size[img_url])
        i += 1
        img_names[img_url] = name
    return (img_urls, img_extension, img_size, img_names)


def get_blog_number(url):
    num = ""
    for c in url[::-1]:
        if c.isnumeric():
            num = c + num
        else:
            return num


def filter_out_incompatible_medias(img_urls):
    return filter(lambda url: not url.endswith(".webm"), img_urls)


def main():
    from FFFLaTeX.parserutil import get_latex_for_element, \
        generate_latex_from_element, process_symbols
    img_urls = set()
    img_size = {}
    img_names = {}
    img_ext = {}
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    latest_version_data = get_latest_version_data()
    blog_url = get_blog_url(latest_version_data)
    num = get_blog_number(blog_url)
    soup = get_soup(blog_url)

    soup, img_urls, img_size = generate_img_data(soup, img_urls, img_size)
    soup, img_urls, img_size = generate_mp4_data(soup, img_urls, img_size)
    img_urls, img_ext, img_size, img_names = generate_media_names(img_urls,
                                                                  img_ext,
                                                                  img_size,
                                                                  img_names)

    img_urls = filter_out_incompatible_medias(img_urls)

    doc_name = "FFF" + str(num)

    ensure_dir("./" + doc_name + "/")

    with open("./" + doc_name + "/" + doc_name + ".tex", "w") as out:
        payload = {
            "TeX":   "",
            "__num": num,
            "__url": blog_url,
            "__img_urls": img_urls,
            "__img_ext": img_ext,
            "__img_names": img_names,
            "__img_size": img_size
        }

        out.write(process_symbols(None, payload, get_latex_for_element(
                                           "documentHeader")))

        # generate constants
        for img_url in img_urls:
            args = []
            if img_size[img_url] is not None:
                args.append("width=" + str(img_size[img_url]))

            out.write("\\write18{wget -N " + img_url + " -P ../out/pics/ -O " +
                      img_names[img_url] + img_ext[
                          img_url] + " }\n" + "\\newcommand{\\" + img_names[
                          img_url] + "}{\\includegraphics[" + ','.join(
                args) + "]{" + img_names[img_url] + img_ext[img_url] + "}}\n")

        out.write(process_symbols(None, payload, get_latex_for_element(
                                           "documentTitle")))

        out.write(process_symbols(None, payload, get_latex_for_element(
                                           "documentBegin")))

        # generate content

        blog = soup.find("div", class_="blog-post")

        for element in blog.children:
            out.write(generate_latex_from_element(element, payload))

        out.write(process_symbols(None, payload, get_latex_for_element(
                                           "documentEnd")))


if __name__ == "__main__":
    main()
