# Kinetix Solutions, Inc
# VIRTOUX Screen Scrapper request
# author: Kelvin Njeri
# kelvin@kinetixsolutions.com
# IDLE: PyCharm 3.0 (python 2.7.12)
# The purpose of this script is to extract data from a
# generated list of contact information in a web page

# necessary imports
import csv
import urllib2
from xlwt import *
import xlrd

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup



# storing information on a file of type xlxs
book = Workbook()

# storing 1000 USA zip codes
with open('codes.txt') as f:
    lines = f.readlines()

zips = []
for x in range(1000):
    zips.append(lines[x])

# extracting and storing data in a list of list
def extractData(line, contact):
    try:
        for row in line:
            list_of_cells = []
            for cell in row.find_all('td')[1:]:
                data = cell.text.replace(u'\xa0', '')
                data.replace(u'\xae', '')
                data.replace('\n', '')
                data.replace('\t', '')
                data.lstrip()
                data.rstrip()
                data.encode('utf-8')
                list_of_cells.append(data)
            contact.append(list_of_cells)#created lists of lists
            #print "number of contacts collected = %d" % len(contact)
    except Exception as p:
        print p
        pass


# loops through every zip code in the search option
for x in zips:
    contact = []  # stores primary contact information
    physician = []
    practice = []
    address = []
    sheet = book.add_sheet(x)
    z = int(x)
    print "Accessing information in zipcode = %s" % x
    link = 'http://cigna.benefitnation.net/cigna/SearchResult.aspx?txtAddress=&zip=%s&radius=150&searchType=phys&searchName=&city=&state=&ccn=Y&lang=&gender=&hplan=&hca=&hden=&hphm=&hvis=&productplan=OA&netid=&NPOid=&ResidentZipCode=&Pspec=&role=S&Sspec=PL' % z

    try:  # use of beautiful soup feature
        http = urllib2.urlopen(link)
        soup = BeautifulSoup(http, "html5lib")
    except urllib2.HTTPError:
        pass #clears out invalid URLs
    except Exception as he:
        print (he)
        exit()
    except AttributeError as se:
        print (se)
        exit()
    oddLine = soup.find_all('tr', {'class': 'resultslistitem'})
    evenLine = soup.find_all('tr', {'class': 'gridAlter'})
    extractData(oddLine, contact)
    extractData(evenLine, contact)

    for x in contact:
        p = x[0]
        j = x[3]
        a = x[4]
        print (p, j, a)

    for x in contact:
        physician.append(x[0])
        practice.append(x[3])
        address.append(x[4])

    for n in range(len(contact)):
        sheet.write(n, 0, physician[n])
        sheet.write(n, 1, practice[n])
        sheet.write(n, 2, address[n])

    book.save("cigna 1-1000.xlxs") #sample file name
