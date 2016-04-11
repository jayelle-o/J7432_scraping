import csv, mechanize, urllib2
from bs4 import BeautifulSoup

output = open('output.csv', 'w')
writer = csv.writer(output)
writer.writerow(['county', 'clinton_pct', 'sanders_pct', 'cruz_pct', 'kasich_pct', 'trump_pct'])

br = mechanize.Browser()
br.open('http://enr.sos.mo.gov/EnrNet/CountyResults.aspx')
#print br.response().read()

#get HTML so I can target the countyForm via its HTML tags
html = br.response().read()
#transform HTML into a BeautifulSoup object so I can use soup.find on the countyForm
soup = BeautifulSoup(html, "html.parser")
#print soup

br.select_form(nr=0) #nr=0 to get the first (only) form on the page

#first dropdown menu:
br.form['ctl00$MainContent$cboElectionNames'] = ['750003566']
#br.submit('ctl00$MainContent$btnElectionType')
#why does the code break when I have two br.submits?

#second dropdown menu:
county = soup.find('select',
    {'name': 'ctl00$MainContent$cboCounty',
    'id': 'cboCounty'
})

for row in county.find_all('option'):
    countyValue = row['value']
    countyName = row.text.encode('utf-8')

    br.select_form(nr=0)
    br.form['ctl00$MainContent$cboCounty'] = [countyValue] 
    #why don't I need to do this: ['countyValue']
    br.submit('ctl00$MainContent$btnCountyChange')

    # use mechanize to read electtable as HTML
    html = br.response().read()

    # print html

    #use beautifulSoup to parse the HTML
    soup = BeautifulSoup(html, "html.parser")

    #select the table
    main_table = soup.find('table',
        {'class': 'electtable'} 
    )

    output=[]
    output.append(countyName)


    #extract info from table cells
    for row in main_table.find_all('tr'):
        data = [cell.text.encode('utf-8') for cell in row.find_all('td')]

        # select candidates of interest:
        if data:
            if data[0] in ['Hillary Clinton', 'Bernie Sanders', 'Ted Cruz', 'John R. Kasich','Donald J. Trump']:            
                output.append(data[3])
    #print output

    writer.writerow(output)
    
   

