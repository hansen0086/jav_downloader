import requests
import re
import os
from bs4 import BeautifulSoup

key_word = "深田" # the searching keyword
resolution = "480p"# can choose 480p or 720p
new_folder_name = key_word
os.mkdir(new_folder_name)



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

#print(row2)

video_counter =0

#for each video page in this search result page
for instance in row2.find_all('div',class_='col-sm-6 col-md-4 col-lg-4'):
    video_counter+=1
    href = instance.find('div',class_='well well-sm').a['href']#video name
    videopageurl = "http://avjoy.me"+href #the url of the video page

    #print(videopageurl)
    text = getHTMLText(videopageurl)
    soup = BeautifulSoup(text,'lxml')
    row2 = soup.find('div',id='wrapper').find('div',class_='container').find_all('div',class_='row')[1]
    mp4url= row2.find('div',class_='col-md-8').find('div').find('div',class_='video-container').find('video').find('source',label=resolution)['src']
    #print(mp4url)
    file_name = href.split('/')[3]
    print("Downloading:")
    print(file_name)
    r = requests.get(mp4url,timeout=1000)

    with open (new_folder_name+"/"+file_name,'wb') as fd:
        fd.write(r.content)

    #now use the mp4url to download the mp4 file





    

    
print("%d videos downloaded" %(video_counter))


 










