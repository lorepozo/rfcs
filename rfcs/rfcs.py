"""
rfcs
====

The complete command-line tool for searching and viewing RFCs
"""

import argparse
from bs4 import BeautifulSoup
import pydoc
import requests
import textwrap

__version__ = '1.0.0'

description = 'The complete command-line tool for searching and viewing RFCs'

IETF = 'https://datatracker.ietf.org'
SEARCH = IETF+'/doc/search/'
INFO = IETF+'/doc/rfc%d/'
TEXT = 'https://www.rfc-editor.org/rfc/rfc%d.txt'
HTML = 'https://tools.ietf.org/html/rfc%d'
PDF = 'https://www.rfc-editor.org/rfc/pdfrfc/rfc%d.txt.pdf'
BIBTEX = IETF+'/doc/rfc%d/bibtex/'


def clean(text):
    without_blank_lines = "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])
    return textwrap.indent(textwrap.dedent(without_blank_lines), '  ')


def info(rfc):
    r = requests.get(INFO % (rfc,))
    soup = BeautifulSoup(r.text, 'html.parser')
    tb = soup.find('tbody')
    return '%s\n%s\nType:\n%s\nLast updated:\n  %s\nStream:\n  %s' % \
           (soup.find('h1').contents[0],  # title
            soup.find('h1').small.text,  # subtitle
            clean(tb.tr.find_all('td')[1].text),  # type
            tb.find_all('tr')[1].find_all('td')[1].text.strip(),  # last updated
            tb.find_all('tr')[2].find_all('td')[1].text.strip(),  # stream
            )


def url(rfc, format):
    if format == 'html':
        return HTML % (rfc,)
    elif format == 'pdf':
        return PDF % (rfc,)
    elif format == 'bibtex':
        return BIBTEX % (rfc,)
    return TEXT % (rfc,)


def text(rfc):
    return requests.get(url(rfc, 'text')).text


def search(query, max_results):
    payload = {'name': query, 'rfcs': 'on'}
    r = requests.get(SEARCH, params=payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    tb = soup.find(id='search_form').find_next_sibling('table').find_all('tbody')[1]
    results = []
    for row in tb.find_all('tr'):
        if len(results) >= max_results:
            break
        tds = row.find_all('td')
        result = {'rfc': tds[1].a.text,
                  'url': tds[1].a['href'],
                  'title': tds[1].b.text,
                  'date': tds[2].span.text.strip(),
                  'size': tds[2].small.text
                  }
        results.append(result)
    return '\n'.join("%s: %s (%s, %s)" % (r['rfc'], r['title'],
                     r['date'], r['size']) for r in results)


def main():
    parser = argparse.ArgumentParser(prog='rfcs', description=description)
    parser.add_argument('--version', action='store_true')
    subparsers = parser.add_subparsers(title='subcommands', dest='command')
    parser_search = subparsers.add_parser('search', help='search for RFCs matching a query')
    parser_search.add_argument('query', type=str, help='search query')
    parser_search.add_argument('--maxresults', type=int, dest='N', metavar='N',
                               default=5, help='maximum number of displayed results')
    parser_info = subparsers.add_parser('info', help='get information on a particular RFC')
    parser_info.add_argument('rfc', type=int, help='number of RFC')
    parser_text = subparsers.add_parser('text', help='view the text of a particular RFC')
    parser_text.add_argument('rfc', type=int, help='number of RFC')
    parser_text.add_argument('--nopager', action='store_true',
                             help='write to stdout instead of opening pager')
    parser_url = subparsers.add_parser('url', help='get a URL to view a particular RFC')
    parser_url.add_argument('rfc', type=int, help='number of RFC')
    parser_url.add_argument('--format', choices=['text', 'html', 'pdf', 'bibtex'], default='text')
    args = parser.parse_args()
    if args.version:
        print(__version__)
    elif args.command == 'search':
        print(search(args.query, args.N))
    elif args.command == 'info':
        print(info(args.rfc))
    elif args.command == 'text':
        if args.nopager:
            print(text(args.rfc))
        else:
            pydoc.pager(text(args.rfc))
    elif args.command == 'url':
        print(url(args.rfc, args.format))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
