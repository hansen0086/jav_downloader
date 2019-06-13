import requests
import re
import os
import sys
from bs4 import BeautifulSoup

try:
    key_word = sys.argv[1]
except:
    key_word = "桃谷" # the searching keyword
resolution = "480p"# can choose 480p or 720p
if (len(sys.argv)>=3):
    if (sys.argv[2]=="480" or sys.argv[2]=="480p"):
        resolution="480p"
    elif (sys.argv[2]=="720" or sys.argv[2]=="720p"):
        resolution="720p"

new_folder_name = key_word

try:
    os.mkdir(new_folder_name)
except:
    print("folder already exists")



def getHTMLText(url):
    try:
        r = requests.get(url,timeout=1000)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error in status"


base_url = "http://avjoy.me/search/videos?search_query="+key_word

#mp4_url = "http://avjoy.me:2087/video/Js29eUN1b2yt3YwGrrHxQw/1560169188/1871_480p.mp4"


text = getHTMLText(base_url)
soup = BeautifulSoup(text,'lxml')

wrapper = soup.find('div',id = 'wrapper')
container = wrapper.find('div',class_='container')
row = container.find('div',class_='row')
sm8= row.find('div',class_='col-md-9 col-sm-8')
row2 = sm8.find('div',class_='row')
row3 = row2
#print(row2)

video_counter =0

#print all the urls
for instance in row2.find_all('div',class_='col-sm-6 col-md-4 col-lg-4'):
    video_counter+=1
    href = instance.find('div',class_='well well-sm').a['href']#video name
    videopageurl = "http://avjoy.me"+href #the url of the video page

    text = getHTMLText(videopageurl)
    soup = BeautifulSoup(text,'lxml')
    row2 = soup.find('div',id='wrapper').find('div',class_='container').find_all('div',class_='row')[1]
    #print(row2.find('div',class_='col-md-8').find('div').find('div',class_='video-container'))
    try:
        #new version has property where label="480p" and type="video/mp4"
        mp4url= row2.find('div',class_='col-md-8').find('div').find('div',class_='video-container').find('video').find('source',label=resolution)['src']
    except:
        mp4url= row2.find('source')['src']
    #print(mp4url)
    file_name = href.split('/')[3]+".mp4"

    print("got %s from %s"% (file_name,mp4url))

print("%d videos in total"%(video_counter))

total = video_counter
video_counter =0
#for each video page in this search result page
for instance in row3.find_all('div',class_='col-sm-6 col-md-4 col-lg-4'):
    #print("in for loop")

    video_counter+=1
    href = instance.find('div',class_='well well-sm').a['href']#video name
    videopageurl = "http://avjoy.me"+href #the url of the video page

    #print(videopageurl)
    text = getHTMLText(videopageurl)
    soup = BeautifulSoup(text,'lxml')
    row3 = soup.find('div',id='wrapper').find('div',class_='container').find_all('div',class_='row')[1]
    #print(row3.find('div',class_='col-md-8').find('div').find('div',class_='video-container'))
    try:
        #new version has property where label="480p" and type="video/mp4"
        mp4url= row3.find('div',class_='col-md-8').find('div').find('div',class_='video-container').find('video').find('source',label=resolution)['src']
    except:
        mp4url= row3.find('source')['src']
    #print(mp4url)
    file_name = href.split('/')[3]+".mp4"

    if(os.path.exists(new_folder_name+"/"+file_name)):
        print("%s already exists, skipped"%(file_name))
        continue

    print("Downloading(%d/%d):"%(video_counter, total))
    print("%s from %s"% (file_name,mp4url))
    
    r = requests.get(mp4url,stream = True)
    with open (new_folder_name+"/"+file_name,'wb') as fd:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                fd.write(chunk)


    

print("%d videos downloaded" %(video_counter))

