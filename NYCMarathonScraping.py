#This script let you download NYC marathon race results from nyrr.org
#
# Ivan Zalamea, 2014
#
# Line 16: Please enter the first year for which you want to retrieve
#          marathon data (anything from 1970 to 2011)
# Line 17: Enter last year for which you want to retrive marathon data
#          (anything from 1970 to 2011)
#
# Line 18: Enter the name of the directory where the marathon data will
#         be saved. Please create this directory before running the script

import requests
import re

FirstYear=1976
LastYear=1976
DirectoryToSaveMaratonData='NYCMarathonData/'

def StringBetweenBraces(string):
    SBB=''
    inside=True
    for i in string:
        if not inside and i!='<':
            SBB=SBB+i
        if i=='>':
            inside=False
        elif i=='<':
            inside=True
    return SBB

def writeData(fileW,html):
    string=''
    dataline=[]
    adding=False
    for i in range(0,len(html)):
        c=html[i]
        if c!='\n' and c!='\r':
            string =string+c
        else:
            if not adding:
                #print string
                searchObj = re.search( r'(.*)<tr class="text" bgcolor="#E0E0E0">(.*)', string)
                if searchObj:
                    adding=True
                else: pass
            else:
                if len(string)>0:
                    searchObj = re.search( r'(.*)</tr>(.*)', string)
                    if searchObj and len(dataline)>0:
                        datatoadd=''
                        for field in dataline:
                            datatoadd=datatoadd+str(field.encode('utf-8'))+str(' || ')    
                        #print datatoadd
                        fileW.write(datatoadd+"\n")
                        dataline=[]
                    else:
                        searchObj = re.search( r'(.*)<tr class="text" bgcolor="#FFFFFF">(.*)', string)
                        if searchObj:
                            pass
                        else:
                            searchObj = StringBetweenBraces(string)
                            dataline.append(searchObj)

            string = ''
    return

def writeHeaders(fileW,html):
    string=''
    headerFields=[]
    for i in range(0,len(html)):
        c=html[i]
        if c!='\n' and c!='\r':
            string =string+c
        else:
            if len(string)>0:
                searchObj = re.search( r'(.*)<TITLE>(.*)</TITLE>(.*)', string)
                if searchObj:
                    fileW.write(str(searchObj.group(2).encode('utf-8'))+"\n")
                    print 'Title: '+str(searchObj.group(2).encode('utf-8'))
                searchObj = re.search( r'(.*)<span class="bighead">(.*)</span><br>(.*)', string)
                if searchObj:
                    fileW.write(str(searchObj.group(2).encode('utf-8'))+"\n")
                    print 'Title2: '+str(searchObj.group(2).encode('utf-8'))
                searchObj = re.search( r'(.*)<b>Distance:&nbsp;&nbsp;</b>(.*)<br>(.*)', string)
                if searchObj:
                    fileW.write(str(searchObj.group(2).encode('utf-8'))+"\n")
                    print 'Distance: '+str(searchObj.group(2).encode('utf-8'))
                searchObj = re.search( r'(.*)<b>Date/Time:&nbsp;&nbsp;</b>(.*)<br>(.*)', string)
                if searchObj:
                    fileW.write(str(searchObj.group(2).encode('utf-8'))+"\n")
                    print 'Date/time: '+str(searchObj.group(2).encode('utf-8'))
                searchObj = re.search( r'(.*)<b>Location:&nbsp;&nbsp;</b>(.*)<br>(.*)', string)
                if searchObj:
                    fileW.write(str(searchObj.group(2).encode('utf-8'))+"\n")
                    print 'Location: '+str(searchObj.group(2).encode('utf-8'))
                searchObj = re.search( r'(.*)<b>Weather:&nbsp;&nbsp;</b>(.*)<br>(.*)', string)
                if searchObj:
                    fileW.write(str(searchObj.group(2).encode('utf-8'))+"\n")
                    print 'Weather: '+str(searchObj.group(2).encode('utf-8'))
                searchObj = re.search( r'(.*)<td class="heading">(.*)</td>(.*)', string)
                if searchObj:
                    print 'Field: '+str(searchObj.group(2).encode('utf-8'))
                    headerFields.append(searchObj.group(2))               
                searchObj = re.search( r'(.*)<td class="heading ctr">(.*)</td>', string)
                if searchObj:
                    print 'Field: '+str(searchObj.group(2).encode('utf-8'))
                    headerFields.append(searchObj.group(2))
            string = ''
    string = ''
    for field in headerFields:
        string=string+str(field.encode('utf-8'))+str(' || ')
    
    fileW.write(string+"\n")
    return

def getRaceResults(url_0,filePathName):
    s = requests.session()
    #url_0='http://web2.nyrrc.org/cgi-bin/start.cgi/aes-programs/results/startup.html?result.id=b30518&result.year=2013'
    r=s.get(url_0)

    print len(r.text)
    print r.url


    string=''
    goodlines=[]
    for i in range(0,len(r.text)):
        c=r.text[i]
        if c!='\n' and c!='\r':
            string =string+c
        else:
            if len(string)>0:
                searchObj = re.search( r'(.*)form method=post action=(.*?)>(.*)', string)
                if searchObj:
                    goodlines.append(searchObj.group(2))
            string = ''


    if len(goodlines)>0:
        url=goodlines[0]
    else:
        print 'No searchable results. Moving to next race...'
        return 

    print url


    payload = {
        "search.method": "search.overall",
        "input.lname" : "",
        "input.fname" : "",
        "input.bib" : "",    
        "overalltype": "All",
        "input.agegroup.m" : "0 to 11",
        "input.agegroup.f" : "0 to 11",
        "teamgender" : "",
        "team_code" : "0",    
        "items.display" : "7000000",
        "AESTIVACVNLIST" : "\"All\",\"0 to 11\",\"0 to 11\",\"\",\"0\"",
        }

    r = requests.post(url, payload)

    print r.status_code
    tries=0
    while r.url=="http://www.nyrr.org/" and tries<200:
        url=goodlines[0]
        print url
        r = requests.post(url, payload)
        print r.status_code
        print len(r.text)
        print r.url
        print tries
        tries=tries+1

    print len(r.text)
    print r.url
    
    
    fileW=open(filePathName,'w')
    #fileW=open('datos_BrooklynHalf_2013_.data','w')

    writeHeaders(fileW,r.text)
    writeData(fileW,r.text)

    fileW.close()

    return


def main():
    for year in range(FirstYear,LastYear+1):
        print 'Downloading NYC marathon results for '+str(year)
        s = requests.session()
        url_0='http://web2.nyrrc.org/cgi-bin/start.cgi/mar-programs/archive/archive_search.html'
        r=s.get(url_0)
        
        print len(r.text)
        print r.url
        
        
        string=''
        goodlines=[]
        for i in range(0,len(r.text)):
            c=r.text[i]
            if c!='\n' and c!='\r':
                string =string+c
            else:
                if len(string)>0:
                    searchObj = re.search( r'(.*)form method=post action=(.*?)>(.*)', string)
                    if searchObj:
                        print
                        goodlines.append(searchObj.group(2))
                string = ''


        if len(goodlines)>0:
            url=goodlines[0]
        else:
            print 'No searchable results. Moving to next race...'
            return 

        print url



        payload = {
            "input.hist.fname": "",
            "input.hist.lname": "",
            "search.method": "search.top",
            "input.top": "100000",
            "top.type": "B",
            "input.agegroup": "",
            "input.f.age": "",
            "input.t.age": "",
            "input.f.hh": "",
            "input.f.mm": "",
            "input.t.hh": "",
            "input.t.mm": "",
            "team_code": "",
            "input.state": "",
            "input.country": "",
            "input.lname": "",
            "input.bib": "",
            "input.top.wc": "10",
            "top.wc.type": "P",
            "top.wc.gender": "M",
            "AESTIVACVNLIST": "input.searchyear,input.top,input.agegroup,input.f.hh,input.f.mm,input.t.hh,input.t.mm,team_code,input.state,input.country,input.top.wc"
            }

        payload["input.searchyear"]=str(year)

        r = requests.post(url, payload)

        print r.status_code
        tries=0
        while r.url=="http://www.nyrr.org/" and tries<200:
            # the post request is not always successful
            # we try to get the data for up to 200 times
            url=goodlines[0]
            print url
            r = requests.post(url, payload)
            print r.status_code
            print len(r.text)
            print r.url
            print tries
            tries=tries+1

        print len(r.text)
        print r.url
    
    
        fileW=open(DirectoryToSaveMaratonData+'M'+str(year)+'.data','w')
        writeData(fileW,r.text)

        fileW.close()

    return

if __name__ == '__main__':
    main()
