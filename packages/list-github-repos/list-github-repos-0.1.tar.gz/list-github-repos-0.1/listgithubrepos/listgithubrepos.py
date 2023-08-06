#!/usr/bin/python

"""
list-github-repos is a utility that lists the repos from a GitHub profile
by scraping and parsing the public GitHub page.

Kailash Nadh, https://nadh.in

Licensed under the MIT License.
"""

import sys
import argparse
import urllib3
import json
import io
import csv
from bs4 import BeautifulSoup


TYPES = ["source", "fork", "archived"]
FIELDS = ["name", "url", "modified", "description", "types"]


def fetch_page(url):
    """Fetch a page over HTTP."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    c = urllib3.connection_from_url(url)
    r = c.urlopen("GET", url)
    c.close()

    if r.status != 200:
        raise Exception("User not found")

    return r.data.decode("utf-8")


def parse(html):
    """Parse the repo information out the GitHub profile HTML."""
    p = BeautifulSoup(html, features="lxml")
    div = p.body.find("div", attrs={"id": "user-repositories-list"})
    if not div:
        raise Exception("Looks like the GitHub layout has changed.")

    out = []
    for li in div.find_all("li"):
        # Name and URI.
        a = li.find("a")
        if not a:
            continue

        name = a.text.strip().encode("utf-8")
        uri = a["href"].strip()

        # Description.
        desc = li.find("p", attrs={"itemprop": "description"})
        if desc:
            desc = desc.text.strip().encode("utf-8")

        # Types from classes.
        types = []
        for c in li["class"]:
            c = c.strip()
            if c in TYPES:
                types.append(c.encode("utf-8"))

        # Date
        date = li.find("relative-time")["datetime"].strip().encode("utf-8")

        out.append({
            "name": name,
            "url": ("https://github.com" + uri).encode("utf-8"),
            "description": desc,
            "types": types,
            "modified": date
        })

    return out


def main():
    """Commandline entry point."""
    p = argparse.ArgumentParser(description="List GitHub repos of a profile")

    p.add_argument("-u", "--user", action="store", dest="user",
                   type=str, required=True, default="",
                   help="GitHub user ID")

    p.add_argument("-t", "--type", action="store", dest="type",
                   type=str, required=False, default="all",
                   choices=["all", "source", "fork", "archived"])

    p.add_argument("-f", "--format", action="store", dest="format",
                   type=str, required=False, default="view",
                   choices=["view", "csv", "json"])

    p.add_argument("-s", "--sort", action="store", dest="sort",
                   type=str, required=False, default="name",
                   choices=["name", "modified"])

    p.add_argument("-o", "--sort-order", action="store", dest="order",
                   type=str, required=False, default="asc",
                   choices=["asc", "desc"])

    args = p.parse_args()

    # Retrieve the GitHub page.
    try:
        html = fetch_page("https://github.com/%s?tab=repositories" % (args.user,))
    except Exception as e:
        print("error fetching GitHub page: %s" % (e,))
        sys.exit(1)

    if not html:
        print("GitHub returned a blank page")
        sys.exit(1)

    try:
        data = parse(html)
    except Exception as e:
        print("error parsing GitHub page: %s" % (e,))
        sys.exit(1)


    # Filter
    if args.type != "all":
        data = list(filter(lambda d: args.type in d["types"], data))

    # Sort.
    data = sorted(data, key=lambda k: k[args.sort].lower(),
                  reverse=True if args.order == "desc" else False)

    # Print the data.
    if args.format == "view":
        fmt = "{:<25} {:<20} {:s}"
        for d in data:
            print(fmt.format(d["modified"], ", ".join(d["types"]), d["url"]))
        return
    elif args.format == "json":
        print(json.dumps(data, indent=4))
        return
    elif args.format == "csv":
        out = io.BytesIO()
        w = csv.writer(out)

        w.writerow(FIELDS)
        for d in data:
            w.writerow(["|".join(d[f]) if isinstance(d[f], list) else d[f] for f in FIELDS])

        print(out.getvalue())


if __name__ == "__main__":
    main()
