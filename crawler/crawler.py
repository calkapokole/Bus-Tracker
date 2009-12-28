#!/usr/bin/python
# -*- coding: utf8 -*-

from __future__ import print_function
from BeautifulSoup import BeautifulSoup
import re
import urllib2
import hashlib


class Crawler(object):
    def __init__(self, baseurl = 'http://ztm.kielce.pl/pl/rozklady/'):
        self._baseurl = baseurl

    def get_html(self, url):
        print(url)
        try:
            html = urllib2.urlopen(url).read()
        except urllib2.URLError, e:
            print('### Crawler Error: {0} ({1})'.format(e, url))

        hash = hashlib.sha1(html).hexdigest()
        print(hash)
        return html


class Parser(object):
    def __get_all_links(self, node, regexp):
        links = []
        for a in node.findAll('a', attrs = {'href':True}):
            a_href = a['href']
            a_name = a.renderContents().strip('<b></b>')
            match = re.match(regexp, a_href)
            if not match:
                print("### Skipping, pattern not matched for: {0}".format(a))
                continue
            groups = match.groupdict()
            a_id = groups.pop('a_id')
            attributes = tuple([a_name, a_href] + groups.values())
            links.append((a_id, attributes))
        return links

    def get_line(self, html):
        soup = BeautifulSoup(html)
        line = {}
        tables = soup.findAll('table')[2:]
        for i, table in enumerate(tables):
            result = table.find('font')
            if not result:
                continue
            direction = result.contents[2]

            # find all stop number / name pairs and save them in a dictionary
            stops = self.__get_all_links(table, r'\d+t(?P<a_id>[a-z0-9_]+)')
            #stops = sorted(stops, lambda a, b: cmp(a[0], b[0]))  # sort by key
            line[(i, direction)] = dict(stops)
        return line

    def get_lines(self, html):
        soup = BeautifulSoup(html)
        table = soup.findAll('table')[1]
        #b_timetable = table.find('b', text='ROZK')
        lines = self.__get_all_links(table, r'^(?P<a_id>[a-z0-9_]+)/w')
        return lines

    def get_stops(self, html):
        soup = BeautifulSoup(html)
        table = soup.findAll('table')[2]
        stops = self.__get_all_links(table, r'^p/p(?P<a_id>[a-z0-9_]+)')
        return stops

    def get_stop(self, html):
        soup = BeautifulSoup(html)
        table = soup.findAll('table')[1]
        stop = [self.__get_all_links(table, r'\.\./\d+/(?P<a_nr>[a-z0-9_]+)t(?P<a_id>[a-z0-9_]+)')]
        return stop

    def get_timetable(self, html):
        timetable = {}
        soup = BeautifulSoup(html)
        table = soup.findAll('table')[3]
        rows = table.findAll('tr')

        # parse header and footer
        timetable['header'] = [unicode(b.renderContents()).lower()
                               for b in rows[0].findAll('b')]
        timetable['footer'] = [s for s in rows[-1].findAll(text = True)]

        # parse the timetable
        current = ''
        rows = rows[1:-1]
        for row in rows:
            data = row.find(text = True)
            if re.match('^Dni robocze', data):
                current = 'weekdays'
                timetable[current] = {}
            elif re.match('^Soboty', data):
                current = 'saturdays'
                timetable[current] = {}
            elif re.match('^Niedziele', data):
                current = 'sundays'
                timetable[current] = {}
            elif re.match('^Godz', data):
                timetable[current]['hours'] = row.findAll('b', text = True)[1:]
            elif re.match('^Min', data):
                timetable[current]['minutes'] = [item.findAll(text = True)
                                                 for item in row.contents[1:]]


        days_list = [(k, v) for (k, v) in timetable.iteritems()
                     if not k in ['header', 'footer']]

        # Change separate hours and minutes into times with emblems
        for day, value in days_list:
            hours = value['hours']
            minutes = value['minutes']
            assert len(hours) == len(minutes)
            times = []
            for i, hour in enumerate(hours):
                for minute in minutes[i]:
                    match = re.match(r'^(?P<minute>\d{2})(?P<emblems>[a-zA-Z]+)?', minute)
                    if not match:
                        print('### Skipping minute: ' + minute)
                        continue
                    time = '{0}:{1}'.format(hour, match.group('minute'))
                    times.append((time, match.group('emblems')))
            timetable[day] = times
        return timetable


if __name__ == '__main__':
    baseurl = 'http://ztm.kielce.pl/pl/rozklady/'
    crawler = Crawler()
    parser = Parser()

    # All lines
    print("\n#### All Lines ####\n")
    url = baseurl + 'linie.htm'
    html = crawler.get_html(url)
    lines = parser.get_lines(html)
    for line in lines:
        print(line)

    # Single Line
    print("\n#### Single Line ####\n")
    url = baseurl + '0028/w.htm'
    html = crawler.get_html(url)
    line = parser.get_line(html)
    print("len: {0}".format(len(line)))
    for d in line:
        print('({0}, {1})'.format(d[0], d[1]))
        stops = sorted(line[d].items(), lambda a, b: cmp(a[0], b[0]))
        for s in stops:
            print('    {0} : {1}'.format(s[0], s[1]))

    # All Stops
    print("\n#### All Stops ####\n")
    url = baseurl + 'przystan.htm'
    html = crawler.get_html(url)
    stops = parser.get_stops(html)
    print("len: {0}".format(len(stops)))
    for stop in sorted(stops, lambda a, b: cmp(a[0], b[0])):
        print(stop)

    # Single stop
    print("\n#### Single Stop ####\n")
    url = baseurl + 'p/p0003.htm'
    html = crawler.get_html(url)
    stop = parser.get_stop(html)
    print(stop)

    # Timetable
    print("\n#### Timetable ####\n")
    url = baseurl + '0028/0028t006.htm'
    html = crawler.get_html(url)
    parser.get_timetable(html)

    print("\n#### Timetable ####\n")
    url = baseurl + '000c/000ct006.htm'
    html = crawler.get_html(url)
    timetable = parser.get_timetable(html)
    for key in ['header', 'weekdays', 'saturdays', 'sundays', 'footer']:
        try:
            print(key, timetable[key])
        except KeyError:
            print('### Skipping key: ' + key)
            continue

