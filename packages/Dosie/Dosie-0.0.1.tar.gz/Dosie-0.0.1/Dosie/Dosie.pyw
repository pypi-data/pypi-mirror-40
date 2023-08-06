import tkinter as tk
from tkinter import END
from tkinter import INSERT
from tkinter import messagebox
import random
from random import randint
from PIL import ImageTk
from PIL import Image
import urllib.parse
import urllib.request
from urllib.request import Request, urlopen
import threading
from threading import Thread
from Synx.Synx import Synx
from Synx.Synx import shareWithSynx
from style.style import style
import webbrowser as useWebBrowser
import string
import base64
import os
import re
import algo
import time
import sys
import math


PhotoImage = tk.PhotoImage
configPath = os.path.dirname(__file__)

communicateSIGNAL = False

class crawler():
    tabVacancy = 0
    tabCharLen = 1200
    curCharLen = 0
    whatIgot = []
    childVarC = 0
    MinimumRelScore = 0
    SS_CL_Relevance = 0
    SS_CL_DomainLim = 0
    SS_DL_Relevance = 0
    SS_DL_DomainLim = 0
    allGroupRelevance = 0
    allGroupRelevanceINDX = 0
    lastLastNow = ''
    lastLastNowUpper = 0
    relevanceLevel = []
    probeStop = False
    CompletionMessage = None
    probeTimeS = 0
    probeTimeM = 0
    relevanceIndexList = []
    tabsfromsetting = 0
    tabsfromsetting2 = False
    DownloaDableFiles = 0
    SearchTYpe = 'STATIC'

    pastHistory = []
    NewlyFoundDomains = []
    whereToGoAccessed = 0
    probeNewFoundStack = []
    alreadySeenLinks = []

    XML = []
    XMLurl = []
    
    whereToGo = [] 
    currentCrawlD = []
    domain4D = ['path='+configPath+'/img/domainICO/Icon.png;circular=True;','path='+configPath+'/img/domainICO/Icon.png;circular=True;','path='+configPath+'/img/domainICO/Icon.png;circular=True;','path='+configPath+'/img/domainICO/Icon.png;circular=True;']
    domainNow = [None,None]
    domainROOT = ''
    domainHere = ''
    LinkeDhere = ''
    wordekOn = 0
    def __init__(self,a,b,c,d,e,f):
        self.Synx = f
        self.TXchild = a
        self.TrackPos = b
        self.RelevanceSP = c
        self.RelevanceSPC = d
        self.probeTimer = e
        relPs = self.Synx.child_dimensions(self.RelevanceSP,'w',100)
        self.Section = algo.elementBody('default')
        self.T0Perspective = algo.Into_Perspective()
        self.reviseDomains()
        homeDir = os.path.expanduser("~")
        dirrX = [homeDir+'\\Pictures\\DosieSaved',homeDir+'\\Documents\\DosieDownloaded']
        #_____
        for dirrXX in dirrX:
            directory = dirrXX
            if not os.path.exists(directory):
                os.makedirs(directory)
        #_____^

        #_____
        with open(configPath+'/access/history.txt','r') as history:
            history = history.read()
            if len(history) > 0:
                history = history.split('\n\n<--DOSIE_NEXT-->\n\n')[0:-1]
                for i in range(len(history)):
                    divs = history[i].split('<--DOSIIx-->')
                    self.pastHistory.append([divs[0],divs[1],divs[2].split('<--DOSIIy-->'),divs[3].split('<--DOSIIy-->')])
        #_____^

        #_____
        try:
            with open(configPath+'/AppInit.txt','r') as AppInit:
                AppInitT = AppInit.read()
            for i in range(361):
                self.relevanceLevel.append('')
                fitted = configPath+'/img/rel/'+str(i)+'.png'
                self.relevanceLevel[i] = PhotoImage(file=fitted)
        except:
            with open(configPath+'/AppInit.txt','w+') as AppInit:
                AppInit.write('initialized')
            for i in range(361):
                self.relevanceLevel.append('')
                fitted = self.Synx.fitImage(relPs,configPath+'/img/rel/'+str(i)+'.png',100)
                fitted = configPath+'/img/rel/'+str(i)+'.png'
                self.relevanceLevel[i] = PhotoImage(file=fitted)
        #_____^
        self.closeObjectOption('welcomePage0')
        self.mbOcupy()

    def closeObjectOption(self,target):
        try:
            mom = self.Synx.getChild(target)
            for widget in mom.winfo_children():
                widget.destroy()
            mom.destroy()
            self.Synx.delFromSynx(target)
        except:
            pass

    def convert_size(self,size_bytes):
        if size_bytes == 0:
           return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def mbOcupy(self):
        files = [configPath+'/img/discovered/',configPath+'/img/domainICO/',configPath+'/folders/',configPath+'/access/',self.Synx.mediaPath+'\\',configPath+'/folders/folderImages/',os.path.expanduser("~")+'\\Pictures\\DosieSaved',os.path.expanduser("~")+'\\Documents\\DosieDownloaded']
        mb = 0
        for i in files:
            folder = i
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        mb += os.path.getsize(file_path)
                except Exception as e:
                    pass
                    #print(e)
        mb = self.convert_size(mb)
        self.Synx.getChild('navBottomTxt0').configure(text=str(mb))

    def query(self,say='',WtG=[]):
        global communicateSIGNAL
        global communicateCANCELLATION
        global SEARCH_TYPE
        communicateSIGNAL = False
        if len(say.replace(' ','')) > 0:
            #--
            global BRIDGE_Info_Arr
            communicateCANCELLATION = False
            BRIDGE_Info_Arr = []
            self.curCharLen = 0
            self.whereToGoAccessed = 0
            self.relevanceLevelCount = 0
            self.whatIgot = []
            self.relevanceIndexList = []
            self.relevanceWhoMatter = 0
            #--

            #___
            with open(configPath+'/access/newDomains.txt','w+') as domains:
                domains.write('')
            with open(configPath+'/access/downloadableFiles.txt','w') as downloadableFiles:
                downloadableFiles.write('')
            with open(configPath+'/config/SS_Relevance.txt','r') as SS_Relevance:
                self.MinimumRelScore = int(SS_Relevance.read())
            with open(configPath+'/config/SS_CL_Relevance.txt','r') as SS_Relevance:
                self.SS_CL_Relevance = int(SS_Relevance.read())
            with open(configPath+'/config/SS_CL_DomainLim.txt','r') as SS_Relevance:
                self.SS_CL_DomainLim = int(SS_Relevance.read())
            with open(configPath+'/config/SS_DL_Relevance.txt','r') as SS_Relevance:
                self.SS_DL_Relevance = int(SS_Relevance.read())
            with open(configPath+'/config/SS_DL_DomainLim.txt','r') as SS_Relevance:
                self.SS_DL_DomainLim = int(SS_Relevance.read())
            with open(configPath+'/config/SS_DL_ITL.txt','r') as SS_Relevance:
                self.SS_DL_ITL = int(SS_Relevance.read())
            #___
            self.probeStop = True
            self.relevanceLevelCount = 0
            self.allGroupRelevanceINDX = 0
            self.allGroupRelevance = 0#XXXXX
            #self.relevanceLevel = []#XXXXXXX
            self.TrelMaster = 0
            self.probeTimeM = 0
            self.probeTimeS = 0
            self.alreadySeenLinks = []
            self.DownloaDableFiles = 0
            self.SearchTYpe = SEARCH_TYPE
            self.thatsWhatYouSaid = say
            self.XML = []
            self.XMLurl = []
            self.whereToGo = WtG #['http://academicguides.waldenu.edu/writingcenter/grammar/sentencestructure','http://academicguides.waldenu.edu/writingcenter/grammar/sentencestructure','http://academicguides.waldenu.edu/writingcenter/grammar/sentencestructure','https://www.englishclub.com/grammar/sentence/type.htm','https://essaypro.com/blog/types-of-sentences/','http://grammar.yourdictionary.com/grammar/sentences/types-of-sentences.html','https://www.grammar-monster.com/glossary/sentences.htm']

            if self.CancelSearch():
                return
            
            self.Section.initQuery(say)
            
            self.timer()
            self.TXchild.configure(text='Initializing...')
            self.TXchild.update()
            self.crawl_init()

    def CancelSearch(self,Cn=False):
        global communicateCANCELLATION
        if Cn:
            communicateCANCELLATION = True
        if communicateCANCELLATION:
            self.Synx.getChild('StateInfo0').configure(text='Search Canceled')
            return True
        else:
            return False

    def remove_transparency(self,im, bg_colour=(255, 255, 255)):
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            alpha = im.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", im.size, bg_colour + (255,))
            bg.paste(im, mask=alpha)
            return bg
        else:
            return im

    def download_file(self,url,name,domainICO):
        local_filename = domainICO + url.split('/')[-1]
        if 'domainICO' in domainICO and 'icon.png' in local_filename.lower():
            local_filename = '/'.join(local_filename.split('/')[0:-1]) + '/IIcon.png'
        if '?' in local_filename:
            local_filename = local_filename[0:local_filename.find('?')]
        try:
            Greq = Request(url, headers={'User-Agent': 'Mozilla/'+str(randint(0,5))+'.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'})
            response = urlopen(Greq)
            CHUNK = 2 * 1024
            with open(local_filename, 'wb') as f:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)
            img = Image.open(local_filename)
            img = self.remove_transparency(img)
            img.save(domainICO+name+'.png')
            os.unlink(local_filename)
            return domainICO+name+'.png'
        except:
            return configPath+'/img/domainICO/Icon.png'

    def linkAccess(self,url):
        Greq = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:62.0) Gecko/20100101 Firefox/6'+str(randint(0,5))+'.0 '})
        try:
            with urlopen(Greq) as response:
                content = str(response.read())
        except:
            self.TXchild.configure(text='Link Access Failed X')
            self.TXchild.update()
            content = ''
        return content

    def linkCheck(self):
        traverseLim = 0
        for link in self.XML:
            content = self.linkAccess(link)
            links = list(set(re.findall(r"https?://[\w\-.~/?:#\[\]@!$&'()*+,;=]+", content)))
            matchingXML = [s for s in links if ".xml" in s]
            matchingURL = [s for s in links if ".xml" not in s]
            if traverseLim <= 5:
                self.XML = self.XML + matchingXML
            self.XMLurl = self.XMLurl + matchingURL
            self.XML = self.XML[1:]
            traverseLim += 1

    def crawl_init(self):
        whatIknow = ''
        sectionsCount = 0
        self.pastHistory.append([self.thatsWhatYouSaid,self.SearchTYpe,[],[]])
        while len(self.whereToGo) > 0:
            if self.CancelSearch():
                return
            self.Section.reset()
            self.T0Perspective.reset()
            self.TrackPos.reset()
            url = self.whereToGo[0]
            self.tabsfromsetting2 = False
            
            #___RESOLVE URL____________
            if 'https://' not in url and 'http://' not in url:
                url = 'http://'+url
            #___RESOLVE URL____________
            self.whereToGoAccessed += 1
            self.Synx.getChild('statusPlc1').configure(text=str(len(self.whereToGo) - 1))
            self.Synx.getChild('statusPlc3').configure(text=str(self.whereToGoAccessed))
            self.Synx.getChild('StateInfo0').configure(text='Accessing link...')
            self.Synx.getChild('StateInfo0').update()
            
            domainName = url[url.find('//') + 2:].replace('www.','')
            if domainName.find('/') > -1:
                domainName = domainName[0:domainName.find('/')]
            self.alreadySeenLinks.append(url)
            if '.xml' in url:
                self.XML = [url]
                self.linkCheck()
                self.linkCheck()
                self.linkCheck()
                self.linkCheck()
                clout = []
                cloutX = []
                for URL in self.XMLurl:
                    relV = self.relevanceScore(['a',URL])
                    if relV > 5:
                        clout.append(relV)
                        cloutX.append(str(relV)+'<--|| '+URL)
                clout.sort(key=int, reverse=True)
                finaly = []
                for ink in clout:
                    finaly = finaly + [s for s in cloutX if str(ink)+'<--||' in s]
                    if len(finaly) > 10:
                        break
                finaly = [i.split('<--|| ', 1)[1] for i in finaly]
                self.whereToGo = self.whereToGo[0:1] + finaly[1:] + self.whereToGo[1:]
                if len(finaly) > 0:
                    url = finaly[0]
                else:
                    url = 'https://dosieFail--.com'
            Greq = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:62.0) Gecko/20100101 Firefox/6'+str(randint(0,5))+'.0 '})
            self.domainROOT = url[0:url.find(domainName) + len(domainName)]
            self.domainHere = '/'.join(url.split('/')[0:-1])
            self.LinkeDhere = url
            if self.CancelSearch():
                return
            try:
                with urlopen(Greq) as response:
                    content = str(response.read())
            except:
                self.whereToGo = self.whereToGo[1:]
                self.TXchild.configure(text='Link Access Failed')
                self.TXchild.update()
                continue
            StripJS = re.subn(r'<(script).*?</\1>(?s)', '', content)[0]
            StripCSS = re.subn(r'<(style).*?</\1>(?s)', '', StripJS)[0]
            content = StripCSS
            jorafild = False
            for i in range(len(self.currentCrawlD)):
                if self.currentCrawlD[i][0] == domainName:
                    jora = self.currentCrawlD[i][1]
                    jorafild = True
                    break
            if not jorafild:
                if self.CancelSearch():
                    return
                self.Synx.getChild('StateInfo0').configure(text='Fetching Favicon...')
                self.Synx.getChild('StateInfo0').update()
                jora = self.download_file('http://'+domainName+'/favicon.ico',domainName,configPath+'/img/domainICO/')
                if jora == configPath+'/img/domainICO/Icon.png':
                    CTfind1 = content.find('<link rel="icon"')
                    CTfind2 = content.find('<link rel="shortcut icon"')
                    if CTfind1 > -1:
                        pointTo = CTfind1
                    else:
                        pointTo = CTfind2
                    nowhave = content[pointTo:pointTo + 300]
                    nowhave = nowhave[nowhave.find(' href="') + len(' href="'):]
                    nowhave = nowhave[0:nowhave.find('"')]
                    nowhave = self.completeURL(nowhave)
                    if 'http://' in nowhave or 'https://' in nowhave:
                        jora = self.download_file(nowhave,domainName,configPath+'/img/domainICO/')
                    else:
                        jora = self.download_file('http://'+nowhave,domainName,configPath+'/img/domainICO/')
                    if jora == configPath+'/img/domainICO/Icon.png':
                        jora = 'path='+configPath+'/img/domainICO/Icon.png;circular=True;'
                        self.Synx.getChild('StateInfo0').configure(text='Favicon not found')
                        self.Synx.getChild('StateInfo0').update()
                    else:
                        jora = 'path='+jora+';circular=True;'
                else:
                    jora = 'path='+jora+';circular=True;'
                self.currentCrawlD.append([domainName,jora])
                self.NewlyFoundDomains.append([domainName,'path='+jora.replace('path=','').replace(';circular=True;','')+';circular=True;'])
                self.updateStatusNewDomains()
                self.addAllDomains(['None',domainName+'<--DOSIEx-->path='+jora.replace('path=','').replace(';circular=True;','')+';circular=True;<--DOSIEx-->'+('/'.join(url.split('/')[0:-1]))])
            if self.CancelSearch():
                return
            self.domainNow[0] = domainName
            self.domainNow[1] = jora
            self.pastHistory[len(self.pastHistory) - 1][3].append(url)
            self.workingDomainLink(domainName,url)
            content = content[content.find('<body>') + len('<body>'):]
            self.TXchild.configure(text='Identifying Sections...')
            self.TXchild.update()
            for i in range(len(content)):
                if self.CancelSearch():
                    return
                self.Section.setEopen(content[i])
                self.Section.setEclose(content[i])
                if whatIknow != self.Section.parentName:
                    self.TXchild.configure(text='Section Name --> '+self.Section.parentName)
                    self.TXchild.update()
                    sectionsCount += 1
                    whatIknow = self.Section.parentName
            if self.CancelSearch():
                return
            self.TXchild.configure(text='Number Of Sections Identified : '+str(sectionsCount))
            self.TXchild.update()
            self.TXchild.configure(text='Initializing Section plaques...')
            self.TXchild.update()
            self.whereToGo = self.whereToGo[1:]
            self.results()
            if self.SearchTYpe == 'DYNAMIC':
                nullL = []
                for bc in self.probeNewFoundStack:
                    if bc not in self.alreadySeenLinks:
                        nullL.append(bc)
                self.whereToGo = nullL + self.whereToGo
            self.probeNewFoundStack = []
        self.probeStop = False

    def updateStatusNewDomains(self):
        lenn = len(self.NewlyFoundDomains)
        div = lenn / 5
        point = str(div).split('.')
        if len(point) == 2:
            index = int(point[1])
        else:
            index = 8
        if index == 0:
            index = 2
        self.Synx.affect(child='newDomainsFound',point=[index - 2],pointSet=[{'rounded':self.NewlyFoundDomains[lenn - 1][1]}])
        self.Synx.affect(child='newDomainsFound',point=[index - 1],pointSet=[{'style':'text='+self.NewlyFoundDomains[lenn - 1][0]+';'}])
        self.Synx.getChild('statusPlc7').configure(text=str(lenn))

    def reviseDomains(self):
        ccD = []
        self.currentCrawlD = []
        with open(configPath+'/access/domains.txt','r') as domains:
            domains = domains.read().split('<--DOSIEcatEnd-->\n\n')[0:-1]
            for i in range(len(domains)):
                diff = domains[i].split('<--DOSIEcat-->\n')
                dm = diff[1].split('\n\n<--DOSIEy-->\n\n')[0:-1]
                for j in range(len(dm)):
                    dmx = dm[j].split('<--DOSIEx-->')
                    if dmx[0] not in ccD:
                        self.currentCrawlD.append([dmx[0],dmx[1]])
                        ccD.append(dmx[0])

    def addAllDomains(self,new):
        with open(configPath+'/access/newDomains.txt','a+') as domains:
            domains.write(new[0]+'<--DOSIExM-->'+new[1]+'<--DOSIExN-->\n\n')

    def rewriteHistory(self):
        txt = ''
        if len(self.pastHistory) > 48:
            self.pastHistory.pop(0)
        else:
            pass
        i = len(self.pastHistory) - 1
        lim = 1
        while i >= 0 and lim != 51:
            interM = ''
            for j in range(len(self.pastHistory[i])):
                if j == 0 or j == 1:
                    interM += self.pastHistory[i][j]+'<--DOSIIx-->'
                elif j == 2:
                    interM += '<--DOSIIy-->'.join(self.pastHistory[i][j])+'<--DOSIIx-->'
                elif j == 3:
                    interM += '<--DOSIIy-->'.join(self.pastHistory[i][j])
            txt += interM+'\n\n<--DOSIE_NEXT-->\n\n'
            i -= 1
            lim += 1
        with open(configPath+'/access/history.txt','w+') as history:
            history.write(txt)

    def timer(self):
        if self.probeStop:
            self.probeTimeS += 1
            if self.probeTimeS == 60:
                self.probeTimeM += 1
                self.probeTimeS = 0
            self.probeTimer.configure(text=str(self.probeTimeM)+'m '+str(self.probeTimeS)+'s')
            self.probeTimer.update()
            self.PSTtime = self.probeTimer.after(1000,self.timer)
            if self.CancelSearch():
                self.Synx.getChild('StateInfo0').configure(text='Search Canceled')
                self.probeStop = False
        else:
            if self.CancelSearch():
                self.Synx.getChild('StateInfo0').configure(text='Search Canceled')
            else:
                self.Synx.getChild('StateInfo0').configure(text='Search Complete')
            if self.CompletionMessage:
                self.Synx.getChild('StateInfo0').configure(text=self.CompletionMessage)
            self.mbOcupy()
            self.rewriteHistory()
            self.Synx.getChild('StateInfo0').update()
            self.probeTimer.after_cancel(self.PSTtime)

    def identifyTag(self,txt):
        return txt[1:txt.find('>')]

    def stripTag(self,tag,txt):
        return txt.replace('</'+tag+'>','').replace('<'+tag+'>','')

    def sortForTab(self,plaque):
        div = plaque.split('<-||DOSIE||->\n')
        for i in range(len(div) - 1):
            if self.curCharLen < self.tabCharLen:
                fLen = len(div[i])
                minFlen = fLen - self.tabCharLen
                if minFlen < 0:
                    tag = self.identifyTag(div[i][0:10])
                    if tag == 'img' or tag == 'a':
                        content = self.stripTag(tag,div[i])
                        self.whatIgot.append([tag,content])
                        if tag == 'a':
                            try:
                                self.curCharLen += len(content.split(' ~||~ ')[1])
                            except:
                                self.curCharLen += 3
                        else:
                            self.curCharLen += 1
                    else:
                        content = self.stripTag(tag,div[i])
                        self.whatIgot.append([tag,content])
                        self.curCharLen += len(content)
                else:
                    tag = self.identifyTag(div[i][0:minFlen][0:10])
                    if tag == 'img' or tag == 'a':
                        content = self.stripTag(tag,div[i])
                        self.whatIgot.append([tag,content])
                        if tag == 'a':
                            try:
                                self.curCharLen += len(content.split(' ~||~ ')[1])
                            except:
                                self.curCharLen += 3
                        else:
                            self.curCharLen += 1
                    else:
                        content = self.stripTag(tag,div[i][0:minFlen])
                        self.whatIgot.append([tag,content])
                        self.curCharLen += len(content)
            else:
                return self.whatIgot
        return self.whatIgot

    def imageInList(self,List):
        im = 0
        for i in range(len(List)):
            if List[i][0] == 'img':
                im += 1
        return im

    def findVacancy(self):
        if self.tabVacancy == 0:
            return 'Mresults10'
        elif self.tabVacancy == 1:
            return 'Mresults11'
        elif self.tabVacancy == 2:
            return 'Mresults20'
        elif self.tabVacancy == 3:
            return 'Mresults21'

    def completeURL(self,url):
        url = url.replace(' ','')
        if url[0:1] == '/':
            if url[0:2] == '//':
                url = url.replace('//','http://')
            else:
                url = self.domainROOT + url
        elif url[0:1] == '.':
            url = self.domainHere +'/'+ url[1:]
        else:
            pass
        return url

    def imageIncluded(self,imn,List):
        vacancy = self.findVacancy()
        self.Synx.getChild(vacancy).configure(bg='#ffffff')
        if vacancy[-2:] == '10' or vacancy[-2:] == '20' or vacancy[-2:] == '21':
            for widget in self.Synx.getChild(vacancy).winfo_children():
                widget.destroy()
            self.Synx.getChild(child=vacancy).update()
            if imn == 1:
                self.Synx.layout(parent=vacancy,child='I'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=style('default5'),sectionN=2,rowN=2,heightR='98:98',widthR='47:47')
                self.Synx.getChild(child=vacancy).update()
                if len(List) - 1 > 0:
                    length = 1
                else:
                    length = len(List)
            elif imn == 2:
                self.Synx.layout(parent=vacancy,child='I'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=style('default5'),sectionN=3,rowN=2,heightR='45:45:45',widthR='47:47')
                self.Synx.affect(child='I'+str(self.childVarC)+'frame',point=[2],pointSet=[{'style':'width=70;'}])
                self.Synx.getChild(child=vacancy).update()
                if len(List) - 2 > 0:
                    length = 2
                else:
                    length = len(List)
            else:
                self.Synx.layout(parent=vacancy,child='I'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=style('default5'),sectionN=4,rowN=2,heightR='45:45:45:45',marginYR='0:0:5:5')
                self.Synx.getChild(child=vacancy).update()
                if len(List) - 4 > 0:
                    length = 4
                else:
                    length = len(List)
            for i in range(length):
                if List[i][0] == 'img':
                    if self.domainNow[0] == 'google.com' and 'data:image/' in List[i][1]:
                        try:
                            vv = List[i][1]
                            Fformat = vv[vv.find('/')+1:vv.find(';')]
                            B64 = vv[vv.find(',')+1:].replace(' ','')
                            i64name = configPath+'/img/discovered/googleFF.'+Fformat
                            with open(i64name,'wb') as im:
                                im.write(base64.b64decode(B64))
                            i64image = Image.open(i64name)
                            randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                            i64image2 = configPath+'/img/discovered/'+randP+'.png'
                            i64image.save(i64image2)
                            i64image.close()
                            os.unlink(i64name)
                            List[i][1] = i64image2
                        except:
                            List[i][1] = configPath+'/img/domainICO/Icon.png'
                    else:
                        List[i][1] = List[i][1].replace(' ','')
                        if List[i][1][0:1] == '/':
                            if List[i][1][0:2] == '//':
                                List[i][1] = List[i][1].replace('//','http://')
                                List[i][1] = self.download_file(List[i][1],str(randint(0,100)),configPath+'/img/discovered/')
                            else:
                                List[i][1] = self.download_file(self.domainROOT + List[i][1],str(randint(0,100)),configPath+'/img/discovered/')
                        elif List[i][1][0:1] == '.':
                            List[i][1] = self.download_file(self.domainHere +'/'+ List[i][1][1:],str(randint(0,100)),configPath+'/img/discovered/')
                        else:
                            List[i][1] = self.download_file(List[i][1],str(randint(0,100)),configPath+'/img/discovered/')
                    self.Synx.affect(child='I'+str(self.childVarC)+'frame',point=[i],pointSet=[{'rounded':'path='+List[i][1]+';'}])
                    self.Synx.getChild(child=vacancy).update()
                else:
                    self.Synx.affect(child='I'+str(self.childVarC)+'frame',point=[i],pointSet=({'style':'image=;width=60;height=60;text='+List[i][1]+';'}))
                    self.Synx.getChild(child=vacancy).update()
            if self.childVarC < 3:
                self.childVarC += 1
            else:
                self.childVarC = 0
        else:
            if self.domainNow[0] == 'google.com' and 'data:image/' in List[0][1]:
                try:
                    vv = List[0][1]
                    Fformat = vv[vv.find('/')+1:vv.find(';')]
                    B64 = vv[vv.find(',')+1:].replace(' ','')
                    i64name = configPath+'/img/discovered/googleFF.'+Fformat
                    with open(i64name,'wb') as im:
                        im.write(base64.b64decode(B64))
                    i64image = Image.open(i64name)
                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                    i64image2 = configPath+'/img/discovered/'+randP+'.png'
                    i64image.save(i64image2)
                    i64image.close()
                    os.unlink(i64name)
                    List[i][1] = i64image2
                except:
                    List[0][1] = configPath+'/img/domainICO/Icon.png'
            else:
                List[0][1] = List[0][1].replace(' ','')
                if List[0][1][0:1] == '/':
                    if List[0][1][0:2] == '//':
                        List[0][1] = List[0][1].replace('//','http://')
                        List[0][1] = self.download_file(List[0][1],str(randint(0,100)),configPath+'/img/discovered/')
                    else:
                        List[0][1] = self.download_file(self.domainROOT + List[0][1],str(randint(0,100)),configPath+'/img/discovered/')
                elif List[0][1][0:1] == '.':
                    List[0][1] = self.download_file(self.domainHere +'/'+ List[0][1][1:],str(randint(0,100)),configPath+'/img/discovered/')
                else:
                    List[0][1] = self.download_file(List[0][1],str(randint(0,100)),configPath+'/img/discovered/')
            self.Synx.layout(parent=vacancy,child='I'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded='path='+List[0][1]+';',sectionN=1,rowN=1,widthR='100',heightR='99')
            self.Synx.getChild(child=vacancy).update()
            if self.childVarC < 3:
                self.childVarC += 1
            else:
                self.childVarC == 0

    def textOnly(self,List):
        vacancy = self.findVacancy()
        self.Synx.getChild(vacancy).configure(bg='#ffffff')
        for widget in self.Synx.getChild(vacancy).winfo_children():
            widget.destroy()
        self.Synx.getChild(vacancy).update()
        if vacancy[-2:] == '10' or vacancy[-2:] == '21':
            strlen = 1200
            widthTK = 60
            wtcons = 50
        else:
            strlen = 800
            widthTK = 35
            wtcons = 20
        acceptArr = []
        mgYR = ''
        hgYR = ''
        for i in range(len(List)):
            if List[i][0] == 'a':
                if ' ~||~ ' not in List[i][1]:
                    List[i][1] = List[i][1] + ' ~||~ link_fail'
                leng = len(List[i][1].split(' ~||~ ')[1])
                fixedLink = self.completeURL(List[i][1].split(' ~||~ ')[0])
                if self.SearchTYpe == 'DYNAMIC':
                    self.probeNewFoundStack.append(fixedLink)
                List[i][1] = fixedLink + ' ~||~ ' + List[i][1].split(' ~||~ ')[1]
                fileExtensions = ['.mp4','.jpg','.png','.mp3','.wav','.pdf','.txt']
                if fixedLink[-4:] in fileExtensions:
                    with open(configPath+'/access/downloadableFiles.txt','a+') as downloadableFiles:
                        downloadableFiles.write('<--DOSIEx-->'.join([List[i][1].split(' ~||~ ')[1].strip(),fixedLink[-4:],fixedLink]) + '\n<--DOSIEy-->\n')
                        self.DownloaDableFiles += 1
                    self.Synx.getChild('StatusButtons'+str(1)).configure(text='Found Files ('+str(self.DownloaDableFiles)+')')
            else:
                leng = len(List[i][1])
            if i == len(List) - 1:
                strlen = -1
            if strlen - leng > 0:
                acceptArr.append([List[i][0],List[i][1]])
                mgYR += '10:'
                hgYR += '1:'
                strlen -= leng
            else:
                acceptArr.append([List[i][0],List[i][1][0:strlen]+'...'])
                mgYR += '10:'
                hgYR += '1:'
                strlen = 0
                self.Synx.layout(parent=vacancy,child='I'+str(self.childVarC)+'frame',widget=tk.Label,style=style()+'anchor=w;',resolveWH=True,rounded=style('default5'),sectionN=len(acceptArr),rowN=1,widthR='180',heightR=hgYR,marginYR='0'+mgYR[1:-1])
                self.Synx.getChild(vacancy).update()
                for j in range(len(acceptArr)):
                    if acceptArr[j][1].find(' ~||~ ') > 0:
                        dispTxt = acceptArr[j][1].split(' ~||~ ')[1].replace('\n','')
                        textFont = 'fg=#0000cd;'
                    else:
                        if acceptArr[j][0] == 'plane':
                            dispTxt = acceptArr[j][1].replace('\n','')
                            textFont = 'fg=#6e6e6e;'
                        else:
                            dispTxt = acceptArr[j][1].replace('\n','').upper()
                            textFont = 'fg=#000000;'
                    self.Synx.affect(child='I'+str(self.childVarC)+'frame',point=[j],pointSet=[{'style':'image=;wraplength='+str(widthTK * 7)+';anchor=w;'+textFont+'height='+str(round(len(dispTxt) / wtcons))+';text='+dispTxt.replace('=','').replace(';','')+';'}])
                    self.Synx.getChild(vacancy).update()
                if self.childVarC < 3:
                    self.childVarC += 1
                else:
                    self.childVarC = 0
                return

    def workingLink(self,x1,x2):
        if len(x1) > 35:
            x1 = x1[0:35]+'...'
        self.Synx.getChild('doneDm'+str(self.wordekOn)).configure(text=x1)
        self.Synx.getChild('doneDm'+str(self.wordekOn + 1)).configure(text=x2)
        self.Synx.getChild('doneDm'+str(self.wordekOn)).update()
        self.Synx.getChild('doneDm'+str(self.wordekOn + 1)).update()
        self.wordekOn += 2
        if self.wordekOn >= 9:
            self.wordekOn = 0

    def workingDomainLink(self,x1,x2):
        if len(x2) > 50:
            x2 = x2[0:50]+'...'
        self.Synx.getChild('DomainP0').configure(text=x1)
        self.Synx.getChild('DomainP1').configure(text=x2)
        self.Synx.getChild('DomainP0').update()
        self.Synx.getChild('DomainP1').update()

    def topDomains(self):
        i = 4
        j = 3
        while i > 0:
            self.Synx.affect(child='process',point=[i],pointSet=[{'rounded':self.domain4D[j]}])
            self.Synx.getChild('process'+str(i)).update()
            i -= 1
            j -= 1

    def chunkIt(self,seq,num):
        if num < 1:
            num = 1
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    def magnitude(self,ar,indx,order=True):
        ls = []
        for i in range(len(ar)):
            ls.append(int(ar[i][indx][0:-1]))
        ls = sorted(ls,key=int,reverse=order)
        ret = []
        self.pastHistory[len(self.pastHistory) - 1][2] = []
        knownindex = []
        for i in range(len(ls)):
            for j in range(len(ar)):
                if int(ar[j][indx][0:-1]) == ls[i] and j not in knownindex:
                    ret.append(ar[j])
                    self.pastHistory[len(self.pastHistory) - 1][2].append(ar[j][1])
                    knownindex.append(j)
        return ret

    def relevanceScore(self,talkingX):
        talking = talkingX[1]
        keyw=self.thatsWhatYouSaid
        talkLength = len(talking)
        keyw = keyw.split(' ')
        
        total_match = 0
        total_misMatch = 0
        total_seen = 0
        kwDist = 0
        kwDistArr = []
        prevIndx = 0

        if talkingX[0] == 'a' and 'google.' in talking:
            return 0
        for i in range(len(keyw)):
            if keyw[i] != '':
                if talkingX[0] == 'a':
                    find = re.findall((keyw[i]).lower(),talking.lower())
                else:
                    find = re.findall((' '+keyw[i]+' ').lower(),talking.lower())
                seen = len(find)
                total_match += seen
                if seen == 0:
                    total_misMatch += 1
                else:
                    if talkingX[0] == 'a':
                        smIndex = talking.lower().find((keyw[i]).lower())
                    else:
                        smIndex = talking.lower().find((' '+keyw[i]+' ').lower())
                    if i > 0:
                        total_seen += 1
                        currIndx = smIndex
                        lendif = currIndx - prevIndx
                        kwDistArr.append(lendif)
                        kwDist += round(((talkLength - lendif) / talkLength) * 100)
                    prevIndx = smIndex + len(keyw[i]+' ')
        if total_seen == 0:
            total_seen = 1
        howManyShowed = round(((len(keyw) - total_misMatch) / len(keyw)) * 100)
        distHealth = round((kwDist / (total_seen * 100)) * 100)
        aboundance = round((total_match / len(talking.split(' '))) * 100)
        totalRelevance = round(((howManyShowed + distHealth + aboundance) / 300) * 100)
        return totalRelevance

    def endOfTheLine(self,compileTO,BRIDGE_Info_ArrPOINT,sectionTotal,domainTotal):
        global BRIDGE_Info_Arr
        if sectionTotal == 0:
            self.relevanceLevelCount = 1
        else:
            self.relevanceLevelCount = round((domainTotal / (sectionTotal)) * 100)
        self.allGroupRelevanceINDX += 1
        self.allGroupRelevance += self.relevanceLevelCount
        allGroupRelevanceNOW = round((self.allGroupRelevance / (100 * self.allGroupRelevanceINDX)) * 100)
        perDegSCore = round((allGroupRelevanceNOW / 100) * 360)
        #print deg
        self.RelevanceSP.configure(image=self.relevanceLevel[perDegSCore])
        self.RelevanceSP.update()
        self.RelevanceSPC.configure(text=str(allGroupRelevanceNOW)+'%')
        self.RelevanceSPC.update()
        self.Synx.getChild('StateInfo0').configure(text='Domain relevance ('+str(self.relevanceLevelCount)+'%)')
        self.Synx.getChild('StateInfo0').update()
        #print deg
        setasREL = str(int(compileTO[2][0:-1]) + self.relevanceLevelCount)
        self.workingLink(self.LinkeDhere,'REL: '+ str(setasREL) + '%')
        compileTO[2] = setasREL+'%'
        BRIDGE_Info_Arr[BRIDGE_Info_ArrPOINT] = compileTO
        BRIDGE_Info_Arr = self.magnitude(BRIDGE_Info_Arr,2,True)
        for i in range(4):
            if i < len(BRIDGE_Info_Arr):
                self.domain4D[i] = BRIDGE_Info_Arr[i][1]
        self.topDomains()
        #CHECK_: Relevance Limit Reached___________
        if allGroupRelevanceNOW >= self.SS_CL_Relevance:
            self.CancelSearch(Cn=True)
            self.CompletionMessage = 'Search Ended: Relevance Limit Reached'
            return
        #CHECK_: Relevance Limit Reached___________

        #CHECK_: ____________________
        if self.relevanceLevelCount >= self.SS_DL_Relevance:
            excess = 0
            for Jv in range(len(self.whereToGo)):
                if self.domainNow[0] in self.whereToGo[Jv]:
                    excess += 1
                    self.whereToGo[Jv] = None
            if excess > 0:
                self.Synx.getChild('StateInfo0').configure(text='Domain Minimum Relevance Limit reached ('+str(excess)+' removed)')
                self.Synx.getChild('StateInfo0').update()
            self.whereToGo = list(filter(None, self.whereToGo))
        #CHECK_: ____________________

        #CHECK lastLastNow______________________
        if self.lastLastNow == self.domainNow[0]:
            self.lastLastNowUpper += 1
        else:
            self.lastLastNow = self.domainNow[0]
            self.lastLastNowUpper = 0
        if self.lastLastNowUpper >= self.SS_DL_DomainLim:
            excess = 0
            for Jv in range(len(self.whereToGo)):
                if self.domainNow[0] in self.whereToGo[Jv]:
                    excess += 1
                    self.whereToGo[Jv] = None
            if excess > 0:
                self.Synx.getChild('StateInfo0').configure(text='Domain Minimum Link Limit reached ('+str(excess)+' removed)')
                self.Synx.getChild('StateInfo0').update()
            self.whereToGo = list(filter(None, self.whereToGo))
        #CHECK lastLastNow______________________

    def results(self):
        if self.CancelSearch():
            return
        global BRIDGE_Info_Arr
        #['Tesla','m3','98%','04',['plaq1','plaq2','plaq3']]
        BRIDGE_Info_ArrPOINT = None
        foundIN = False
        for i in range(len(BRIDGE_Info_Arr)):
            if BRIDGE_Info_Arr[i][0] == self.domainNow[0]:
                foundIN = True
                compileTO = BRIDGE_Info_Arr[i]
                BRIDGE_Info_ArrPOINT = i
                break
        if not foundIN:
            BRIDGE_Info_Arr.append([self.domainNow[0],self.domainNow[1],'00',00,[]])
            BRIDGE_Info_ArrPOINT = len(BRIDGE_Info_Arr) - 1
            compileTO = BRIDGE_Info_Arr[BRIDGE_Info_ArrPOINT]

        #CHECK_: Domain Limit Reached______________
        if len(BRIDGE_Info_Arr) > self.SS_CL_DomainLim:
            BRIDGE_Info_Arr = BRIDGE_Info_Arr[:-1]
            self.CancelSearch(Cn=True)
            self.CompletionMessage = 'Search Ended: Domain Limit Reached'
            return
        #CHECK_: Domain Limit Reached______________
        domainTotal = 0
        sectionTotal = 0
        kk = 0
        varr = self.Section.full_find
        #print(self.Section.full_find)
        sNN = self.Section.sectionNameing
        self.Synx.getChild('StateInfo0').configure(text=str(len(sNN))+' section(s) found...')
        self.Synx.getChild('StateInfo0').update()
        for i in range(len(sNN)):
            if self.CancelSearch():
                return
            if self.tabsfromsetting2:
                self.endOfTheLine(compileTO,BRIDGE_Info_ArrPOINT,sectionTotal,domainTotal)
                return
            if sNN[i][0] == True:
                relevanceWhoMatter = len(sNN[i])
                #___BR
                compileTO[3] = int(compileTO[3])
                compileTO[3] += 1
                #___BR
                self.TXchild.configure(text='SECTION ('+sNN[i][1]+'):')
                self.TXchild.update()
                varPlaques = self.T0Perspective.Tabs(varr[sNN[i][2]])
                for j in range(len(varPlaques)):
                    if self.CancelSearch():
                        return
                    if self.tabsfromsetting2:
                        self.endOfTheLine(compileTO,BRIDGE_Info_ArrPOINT,sectionTotal,domainTotal)
                        return
                    Srt = self.sortForTab(varPlaques[j])
                    if isinstance(Srt,list):
                        self.TXchild.configure(text='SECTION ('+sNN[i][1]+') --> COMPLETE')
                        self.TXchild.update()
                        sendTroops = []
                        TrelMaster = len(self.whatIgot)
                        for l in range(len(self.whatIgot)):
                            if self.CancelSearch():
                                return
                            if self.whatIgot[l][0] == 'img':
                                embeed = randint(self.MinimumRelScore,99)
                            else:
                                embeed = self.relevanceScore(self.whatIgot[l])
                            if embeed >= self.MinimumRelScore:
                                self.relevanceLevelCount += round((embeed / 100) * (100 / TrelMaster))
                                self.relevanceIndexList.append(embeed)
                                sendTroops.append(self.whatIgot[l])
                        self.relevanceLevelCount = round((self.relevanceLevelCount / 100) * (100 / relevanceWhoMatter))
                        perDegSCore = round((self.relevanceLevelCount / 100) * 360)
                        #print deg
                        self.RelevanceSP.configure(image=self.relevanceLevel[perDegSCore])
                        self.RelevanceSP.update()
                        self.RelevanceSPC.configure(text=str(self.relevanceLevelCount)+'%')
                        self.RelevanceSPC.update()
                        #print deg
                        domainTotal += self.relevanceLevelCount
                        sectionTotal += 100 / relevanceWhoMatter
                        self.relevanceLevelCount = 0
                        self.whatIgot = sendTroops
                        sortedRelI = sorted(self.relevanceIndexList,key=int,reverse=True)
                        if len(self.whatIgot) > 0:
                            #___BR
                            compileTO[3] = str(compileTO[3])
                            for M in range(len(sortedRelI)):
                                for N in range(len(self.relevanceIndexList)):
                                    # """ and len(compileTO[4]) <= self.SS_DL_ITL <__DOSIE__> limit tabs from setting """
                                    if sortedRelI[M] == self.relevanceIndexList[N] and len(compileTO[4]) <= self.SS_DL_ITL:
                                        compileTO[4].append(self.whatIgot[N])
                            #___BR
                        self.relevanceIndexList = []
                        resChunk = self.chunkIt(self.whatIgot,round(len(self.whatIgot) / 4))
                        for k in range(len(resChunk)):
                            if self.CancelSearch():
                                return
                            if self.tabsfromsetting >= self.SS_DL_ITL:
                                self.tabsfromsetting2 = True
                                if self.tabsfromsetting2:
                                    self.endOfTheLine(compileTO,BRIDGE_Info_ArrPOINT,sectionTotal,domainTotal)
                                    return
                                break
                            self.tabsfromsetting += len(resChunk[k])
                            imageCK = self.imageInList(resChunk[k])
                            if imageCK > 0:
                                self.imageIncluded(imageCK,resChunk[k])
                            else:
                                self.textOnly(resChunk[k])
                            if self.tabVacancy >= 3:
                                self.tabVacancy = 0
                            else:
                                self.tabVacancy += 1
                        self.whatIgot = []
                        self.curCharLen = 0
            else:
                self.TXchild.configure(text='SECTION ('+sNN[i][1]+') --> EMPTY')
                self.TXchild.update()
        self.endOfTheLine(compileTO,BRIDGE_Info_ArrPOINT,sectionTotal,domainTotal)
        if self.CancelSearch():
            return



#__BRIDGE_____________________________________
communicateCANCELLATION = False
communicateSIGNAL = False
COMMUNICATE_WITH = None
THREADSIGNAL = False
SEARCH_TYPE = 'STATIC'
def quitDosieX():
    TKclown.deiconify()
    TKclown.destroy()
    sys.exit()

def communicationThread():
    pass

BRIDGE_Info_Arr = []
#__BRIDGE_____________________________________



class DosieGUI(threading.Thread):
    thatsWhatTheySaid = ''
    CSearchinfoArr = []
    FlipThroughSI = []
    tabVacancy = 0
    childVarC = 0
    checkLastTab = 0
    checkTabsPointing = 0
    homeLinkInpArr = []
    pastHistory = []
    domainAllList = {}
    ViewMediaList = []
    AllSearchKeywords = []
    MediaAndFolders = []

    SearchLinkName = []
    SearchLinkLink = []
    MarkCategory = []
    selectedFilesFound = []
    KeywordsAuto = []
    KeywordsAutoIndex = []
    ViewMediaListAuto = []

    selectedDomainsAdding = []
    DomainListedCategories = []
    downloadsAvail = ['default5','','NONE','NONE','NONE',0,'NONE']

    #__FB_NAV________
    frontBackRge = []
    frontBackPoint = 0
    fronBackBegin = True
    #__FB_NAV________
    SavedFoldersList = []
    SavedFoldersListName = []

    def __init__(self):
        global Synx
        self.Synx = Synx
        self.reviseDomains()
        self.reviseKeywords()
        #__CONFIG_FILES_________________
        if not os.path.isfile(configPath+'/config/SS_Relevance.txt'):
            with open(configPath+'/config/SS_Relevance.txt','w+') as SS_Relevance:
                SS_Relevance.write('0')
        if not os.path.isfile(configPath+'/config/SS_CL_Relevance.txt'):
            with open(configPath+'/config/SS_CL_Relevance.txt','w+') as SS_Relevance:
                SS_Relevance.write('0')
        if not os.path.isfile(configPath+'/config/SS_CL_DomainLim.txt'):
            with open(configPath+'/config/SS_CL_DomainLim.txt','w+') as SS_Relevance:
                SS_Relevance.write('0')
        if not os.path.isfile(configPath+'/config/SS_DL_Relevance.txt'):
            with open(configPath+'/config/SS_DL_Relevance.txt','w+') as SS_Relevance:
                SS_Relevance.write('0')
        if not os.path.isfile(configPath+'/config/SS_DL_DomainLim.txt'):
            with open(configPath+'/config/SS_DL_DomainLim.txt','w+') as SS_Relevance:
                SS_Relevance.write('0')
        if not os.path.isfile(configPath+'/config/SS_DL_ITL.txt'):
            with open(configPath+'/config/SS_DL_ITL.txt','w+') as SS_Relevance:
                SS_Relevance.write('0')
        if not os.path.isfile(configPath+'/access/keywords.txt'):
            with open(configPath+'/access/keywords.txt','a+') as keywords:
                keywords.write('')
        self.updateFoldersListing()
        #__CONFIG_FILES_________________
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def callback(self):
        self.root.quit()

    def dosome(self):
        return [self.TXchild,self.TrackPos,self.RelevanceSP,self.RelevanceSPC,self.probeTimer,self.Synx]

    def connectOUT(self,say,WtG):
        global communicateSIGNAL
        global COMMUNICATE_WITH
        global THREADSIGNAL
        global communicationThread
        if say == 'FOCUS__':
            communicationThread()
        elif say == 'FOCUS_OUT__':
            self.root.focus()
            THREADSIGNAL = 'COMMUNICATION_CANCEL__'
        elif say[:-2] != '__':
            self.root.focus()
            communicateSIGNAL = say
            COMMUNICATE_WITH = WtG
            self.thatsWhatTheySaid = say

    def CancelSearch(self):
        global communicateCANCELLATION
        communicateCANCELLATION = True

    def cleanUp(self,domain=False,cache=False):
        Dvalid = ['Icon']
        if domain:
            folder = configPath+'/img/domainICO/'
            for key in self.domainAllList:
                for key2 in self.domainAllList[key]:
                    Dvalid.append(key2[0])
        elif cache:
            folder = configPath+'/__pycache__/'
        else:
            folder = configPath+'/img/discovered/'
        try:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path) and file_path.split('/')[-1].replace('.png','') not in Dvalid:
                        os.unlink(file_path)
                except Exception as e:
                    pass
        except Exception as e:
            pass

    def quitDosie(self):
        global quitDosieX
        with open(configPath+'/access/newDomains.txt','w+') as domains:
            domains.write('')
        with open(configPath+'/access/downloadableFiles.txt','w') as downloadableFiles:
            downloadableFiles.write('')
        self.Synx.cleanUp()
        self.cleanUp()
        quitDosieX()
        sys.exit()

    def backHold(self):
        pass

    def chunkIt(self,seq,num):
        if num < 1:
            num = 1
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    def imageInList(self,List):
        im = 0
        for i in range(len(List)):
            if List[i][0] == 'img':
                im += 1
        return im

    def findVacancy(self):
        if self.tabVacancy == 0:
            return 'CHplaneDV0'
        elif self.tabVacancy == 1:
            return 'CHplaneDV1'
        elif self.tabVacancy == 2:
            return 'CHplane2DV0'
        elif self.tabVacancy == 3:
            return 'CHplane2DV1'

    def download_file(self,url,name,domainICO):
        local_filename = domainICO + url.split('/')[-1]
        try:
            response = urlopen(url)
            CHUNK = 2 * 1024
            with open(local_filename, 'wb') as f:
                while True:
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)
            img = Image.open(local_filename)
            img = self.remove_transparency(img)
            img.save(domainICO+name+'.png')
            os.unlink(local_filename)
            return domainICO+name+'.png'
        except:
            return None

    def imageIncluded(self,imn,List):
        vacancy = self.findVacancy()
        self.Synx.getChild(vacancy).configure(bg='#ffffff')
        if vacancy[-4:] == 'eDV0' or vacancy[-4:] == '2DV1' or vacancy[-4:] == '2DV0':
            for widget in self.Synx.getChild(vacancy).winfo_children():
                widget.destroy()
            self.Synx.getChild(child=vacancy).update()
            if imn == 1:
                self.Synx.layout(parent=vacancy,child='IX'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=style('default5'),sectionN=2,rowN=2,heightR='98:98',widthR='47:47')
                self.Synx.getChild(child=vacancy).update()
                if len(List) - 1 > 0:
                    length = 1
                else:
                    length = len(List)
            elif imn == 2:
                self.Synx.layout(parent=vacancy,child='IX'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=style('default5'),sectionN=3,rowN=2,heightR='45:45:45',widthR='47:47')
                self.Synx.affect(child='IX'+str(self.childVarC)+'frame',point=[2],pointSet=[{'style':'width=70;'}])
                self.Synx.getChild(child=vacancy).update()
                if len(List) - 2 > 0:
                    length = 2
                else:
                    length = len(List)
            else:
                self.Synx.layout(parent=vacancy,child='IX'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=style('default5'),sectionN=4,rowN=2,heightR='45:45:45:45',marginYR='0:0:5:5')
                self.Synx.getChild(child=vacancy).update()
                if len(List) - 4 > 0:
                    length = 4
                else:
                    length = len(List)
            for i in range(length):
                if List[i][0] == 'img':
                    if ' ' in List[i][1]:
                        List[i][1] = configPath+'/img/domainICO/Icon.png'
                    if '/img/' not in List[i][1] and '/folderImages/' not in List[i][1]:
                        List[i][1] = configPath+'/img/domainICO/Icon.png'
                    accessPath = 'path='+List[i][1]+';'
                    self.Synx.affect(child='IX'+str(self.childVarC)+'frame',point=[i],pointSet=[{'rounded':accessPath}])
                    self.Synx.getChild('IX'+str(self.childVarC)+'frame'+str(i)).bind('<Button- 1>',lambda event, XXc = accessPath:self.objectOption(XXc))
                    self.Synx.getChild(child=vacancy).update()
                else:
                    self.Synx.affect(child='IX'+str(self.childVarC)+'frame',point=[i],pointSet=({'style':'image=;width=60;height=60;text='+List[i][1]+';'}))
                    self.Synx.getChild(child=vacancy).update()
            if self.childVarC < 3:
                self.childVarC += 1
            else:
                self.childVarC = 0
        else:
            if ' ' in List[0][1]:
                List[0][1] = configPath+'/img/domainICO/Icon.png'
            if '/img/' not in List[0][1] and '/folderImages/' not in List[0][1]:
                List[0][1] = configPath+'/img/domainICO/Icon.png'
            accessPath = 'path='+List[0][1]+';'
            self.Synx.layout(parent=vacancy,child='IX'+str(self.childVarC)+'frame',widget=tk.Label,style=style(),rounded=accessPath,sectionN=1,rowN=1,widthR='100',heightR='99')
            self.Synx.getChild('IX'+str(self.childVarC)+'frame0').bind('<Button- 1>',lambda event, XXc = accessPath:self.objectOption(XXc))
            self.Synx.getChild(child=vacancy).update()
            if self.childVarC < 3:
                self.childVarC += 1
            else:
                self.childVarC == 0

    def textOnly(self,List):
        vacancy = self.findVacancy()
        self.Synx.getChild(vacancy).configure(bg='#ffffff')
        for widget in self.Synx.getChild(vacancy).winfo_children():
            widget.destroy()
        self.Synx.getChild(vacancy).update()
        if vacancy[-4:] == 'eDV0' or vacancy[-4:] == '2DV1':
            strlen = 1000
            widthTK = 60
            wtcons = 50
        else:
            strlen = 600
            widthTK = 35
            wtcons = 20
        acceptArr = []
        mgYR = ''
        hgYR = ''
        for i in range(len(List)):
            if List[i][0] == 'a':
                if ' ~||~ ' in List[i][1]:
                    leng = len(List[i][1].split(' ~||~ ')[1])
                else:
                    List[i][1] = List[i][1]+ ' ~||~ https://error.error'
                    leng = len(List[i][1].split(' ~||~ ')[1])
            else:
                leng = len(List[i][1])
            if i == len(List) - 1:
                strlen = -1
            if strlen - leng > 0:
                acceptArr.append([List[i][0],List[i][1]])
                mgYR += '10:'
                hgYR += '1:'
                strlen -= leng
            else:
                acceptArr.append([List[i][0],List[i][1][0:strlen]+'...'])
                mgYR += '10:'
                hgYR += '1:'
                strlen = 0
                self.Synx.layout(parent=vacancy,child='IX'+str(self.childVarC)+'frame',widget=tk.Label,style=style()+'anchor=w;',resolveWH=True,rounded=style('default5'),sectionN=len(acceptArr),rowN=1,widthR='180',heightR=hgYR,marginYR='0'+mgYR[1:-1])
                self.Synx.getChild(vacancy).update()
                for j in range(len(acceptArr)):
                    linkCommand = False
                    if acceptArr[j][1].find(' ~||~ ') > 0:
                        dividePlus = acceptArr[j][1].split(' ~||~ ')
                        dispTxt = dividePlus[1].replace('\n','')
                        urlLink = dividePlus[0]
                        textFont = 'fg=#0000cd;'
                        linkCommand = True
                    else:
                        if acceptArr[j][0] == 'plane':
                            dispTxt = acceptArr[j][1].replace('\n','')
                            textFont = 'fg=#6e6e6e;'
                        else:
                            dispTxt = acceptArr[j][1].replace('\n','').upper()
                            textFont = 'fg=#000000;'
                    self.Synx.affect(child='IX'+str(self.childVarC)+'frame',point=[j],pointSet=[{'style':'image=;wraplength='+str(widthTK * 7)+';anchor=w;'+textFont+'height='+str(round(len(dispTxt) / wtcons))+';text='+dispTxt.replace('=','').replace(';','')+';'}])
                    if linkCommand:
                        self.Synx.getChild('IX'+str(self.childVarC)+'frame'+str(j)).bind('<Button- 1>',lambda event,XXc = urlLink:self.viewInBrowser(XXc))
                    self.Synx.getChild(vacancy).update()
                if self.childVarC < 3:
                    self.childVarC += 1
                else:
                    self.childVarC = 0
                return

    def viewInBrowser(self,url):
        useWebBrowser.open_new_tab(url)

    def objectOption(self,imp,delf=False,dell=False,Kwo=False,DDl=False,point=[]):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.closeObjectOption('objectOption0')
        self.closeObjectOption('fileSaveDialogue0')
        self.Synx.layout(parent='win',child='objectOption',widget=tk.Label,sectionN=1,rowN=1,style='bd=0;bg=#ffffff;',rounded=style('Xbg'),widthR='20',heightR='20')
        self.Synx.getChild('objectOption0').grid(padx=(x,0),pady=(y,0))
        self.Synx.layout(parent='objectOption0',child='objectOptionList',widget=tk.LabelFrame,sectionN=4,rowN=1,style='bd=0;bg=#f7f7f7;padx=1;pady=5;fg=#0000cd;',widthR='100',heightR='10:10:10:10',marginYR='5:8:5:5')
        if dell:
            self.Synx.affect(child='objectOptionList',point=[0,1,2],pointSet=[{'style':'text=X  ;labelanchor=e;fg=#ff0000;'},{'style':'text=  View Full;'},{'style':'text=  Delete Media;'}])
            self.Synx.getChild('objectOptionList1').bind('<Button- 1>',lambda event:self.viewFullIMG(imp))
            self.Synx.getChild('objectOptionList2').bind('<Button- 1>',lambda event:self.deleteDialouge(imp,point))
        elif delf:
            self.Synx.affect(child='objectOptionList',point=[0,1,2],pointSet=[{'style':'text=X  ;labelanchor=e;fg=#ff0000;'},{'style':'text=  Delete folder;'},{'style':'text=  ;'}])
            self.Synx.getChild('objectOptionList1').bind('<Button- 1>',lambda event:self.deleteTfFolder(imp,point))
            self.Synx.getChild('objectOptionList2').bind('<Button- 1>',lambda event, X='':self.backHold())
        elif Kwo:
            self.Synx.affect(child='objectOptionList',point=[0,1,2],pointSet=[{'style':'text=X  ;labelanchor=e;fg=#ff0000;'},{'style':'text=  View Details;'},{'style':'text=  Delete;'}])
            self.Synx.getChild('objectOptionList1').bind('<Button- 1>',lambda event:self.ThisKeywordDetails(imp,point))
            self.Synx.getChild('objectOptionList2').bind('<Button- 1>',lambda event:self.ThisKeywordDelete(imp,point[2]))
        elif DDl:
            self.Synx.affect(child='objectOptionList',point=[0,1,2,3],pointSet=[{'style':'text=X  ;labelanchor=e;fg=#ff0000;'},{'style':'text=  View Details;'},{'style':'text=  Edit;'},{'style':'text=  Delete;'}])
            self.Synx.getChild('objectOptionList1').bind('<Button- 1>',lambda event:self.ThisDomainDetails([x,y],imp,point))
            self.Synx.getChild('objectOptionList2').bind('<Button- 1>',lambda event:self.ThisDomainEdit([x,y],imp,point))
            self.Synx.getChild('objectOptionList3').bind('<Button- 1>',lambda event:self.ThisDomainDelete([x,y],imp,point))
        else:
            self.Synx.affect(child='objectOptionList',point=[0,1,2],pointSet=[{'style':'text=X  ;labelanchor=e;fg=#ff0000;'},{'style':'text=  View Full;'},{'style':'text=  Save Image;'}])
            self.Synx.getChild('objectOptionList1').bind('<Button- 1>',lambda event:self.viewFullIMG(imp))
            self.Synx.getChild('objectOptionList2').bind('<Button- 1>',lambda event:self.saveDialouge(imp))
        self.Synx.getChild('objectOptionList0').bind('<Button- 1>',lambda event:self.closeObjectOption('objectOption0'))

    def closeObjectOption(self,target):
        try:
            mom = self.Synx.getChild(target)
            for widget in mom.winfo_children():
                widget.destroy()
            mom.destroy()
            self.Synx.delFromSynx(target)
        except:
            pass

    def viewFullIMG(self,imp):
        self.closeObjectOption('objectOption0')
        self.closeObjectOption('seeingIMGfull0')
        self.Synx.layout(parent='activity2',child='seeingIMGfull',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='100')
        self.Synx.layout(parent='seeingIMGfull0',child='IMGfullFrame',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style('Wbg'),widthR='100',heightR='3:95',marginYR='0:2')
        self.Synx.affect(child='IMGfullFrame',point=[0],pointSet=[{'style':'text=X;font=Helvetica 11 bold;labelanchor=e;fg=#ff0000;'}])
        self.Synx.getChild('IMGfullFrame0').bind('<Button- 1>',lambda event:self.closeObjectOption('seeingIMGfull0'))
        self.Synx.layout(parent='IMGfullFrame1',child='IMGfullSeeFull',widget=tk.Label,sectionN=1,rowN=1,style=style('Wbg'),rounded=imp,widthR='100',heightR='100')

    def saveDialouge(self,imp):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.closeObjectOption('objectOption0')
        self.closeObjectOption('fileSaveDialogue0')
        self.Synx.layout(parent='win',child='fileSaveDialogue',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Bfc')+'text=  Name The File;fg=#0000cd;padx=15;',widthR='20',heightR='20')
        self.Synx.getChild('fileSaveDialogue0').grid(padx=(x - 10,0),pady=(y - 10,0))
        self.Synx.layout(parent='fileSaveDialogue0',child='fileSaveDialogueX',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Bfc'),widthR='2:50',heightR='30:30')
        self.Synx.affect(child='fileSaveDialogueX',point=[1],pointSet=[{'style':'text=X;font=Helvetica 11 bold;labelanchor=ne;fg=#ff0000;'}])
        self.Synx.layout(parent='fileSaveDialogue0',child='fileSaveDialogueName',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='30',marginYR='30')
        self.Synx.layout(parent='fileSaveDialogue0',child='fileSaveDialogueSave',widget=tk.Button,resolveWH=True,sectionN=1,rowN=1,style=style('Bbg')+'text=SAVE;fg=#ffffff;',widthR='30',heightR='30',marginYR='60')
        self.Synx.getChild('fileSaveDialogueSave0').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('fileSaveDialogue0'),'w',35),0))
        self.Synx.getChild('fileSaveDialogueName0').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('fileSaveDialogue0'),'w',12),0))
        self.Synx.getChild('fileSaveDialogueX1').bind('<Button- 1>',lambda event:self.closeObjectOption('fileSaveDialogue0'))
        self.Synx.getChild('fileSaveDialogueSave0').bind('<Button- 1>',lambda event:self.saveMediaFile(imp))

    def saveMediaFile(self,imp):
        name = self.Synx.getChild('fileSaveDialogueName0').get('1.0',END).replace('\n','').replace(' ','').replace('\\','').replace('/','')
        if len(name) < 1:
            messagebox.showerror("File Save", "You forgot to name the file")
            return
        self.closeObjectOption('fileSaveDialogue0')
        homeDir = os.path.expanduser("~")
        directory = homeDir+'\\Pictures\\DosieSaved'
        if not os.path.exists(directory):
            os.makedirs(directory)
        if os.path.isfile(directory+'\\'+name+'.png'):
            messagebox.showerror("File Save", "file already exists")
            return
        img = Image.open(imp.replace('path=','').replace(';',''))
        img.save(directory+'\\'+name+'.png')
        img.close()
        self.mbOcupy()

    def deleteDialouge(self,imp,point):
        self.closeObjectOption('objectOption0')
        var = tk.messagebox.askyesnocancel ('Delete file','Are you sure?')
        if var:
            os.unlink(imp.replace('path=','').replace(';',''))
            self.Synx.getChild(point[0]).bind('<Button- 1>',lambda event, X='':self.backHold())
            self.Synx.affect(child=point[0][0:-1],point=[int(point[0][-1:])],pointSet=[{'rounded':style('default5')}])
            self.ViewMediaList[point[1]] = style('default5').replace('path=','').replace(';','')

    def deleteTfFolder(self,imp,point):
        self.closeObjectOption('objectOption0')
        var = tk.messagebox.askyesnocancel ('Delete folder','Are you sure?')
        if var:
            with open(imp,'r') as fd:
                fd = fd.read()
                fd = fd.split('<--DOSIEy-->')[:-1]
                for i in range(len(fd)):
                    pfr = fd[i].split('<--DOSIEx-->')
                    if pfr[0] == 'img':
                        os.unlink(pfr[1])
            os.unlink(imp)
            self.Synx.getChild(point[0]).bind('<Button- 1>',lambda event, X='':self.backHold())
            self.Synx.getChild(point[0]).bind('<Button- 3>',lambda event, X='':self.backHold())
            self.Synx.affect(child=point[0][0:-1],point=[int(point[0][-1:])],pointSet=[{'rounded':style('default5')}])
            self.Synx.getChild(point[1]).configure(text='')
            self.SavedFoldersListName[point[2]] = ''
            self.SavedFoldersList[point[2]] = ''

    def autoComplete(self,widget,enter,mapp):
        arr = []
        if mapp == 'folders':
            arr = self.SavedFoldersListName
            arrenter = self.SavedFoldersListName
        elif mapp == 'searchLinks':
            arr = self.SearchLinkName
            arrenter = self.SearchLinkLink
        elif mapp == 'addDomain':
            arr = self.DomainListedCategories
            arrenter = self.DomainListedCategories
        write = self.Synx.getChild(widget).get('1.0',END)
        for i in range(len(arr)):
            if (write[0:-1] + arr[i][len(write[0:-1]):]).lower() == arr[i].lower():
                self.Synx.getChild(enter).configure(text = write[0:-1] + arr[i][len(write[0:-1]):])
                self.Synx.getChild(enter).bind('<Button- 1>',lambda event, widget = widget, enter = enter, text = arrenter[arr.index(write[0:-1] + arr[i][len(write[0:-1]):])]:self.acceptAutoComplete(widget,enter,text))
                self.Synx.getChild(enter).update()
                return
        self.Synx.getChild(enter).configure(text = '')
        self.Synx.getChild(enter).bind('<Button- 1>',lambda event, X='':self.backHold())

    def acceptAutoComplete(self,widget,enter,text):
        self.Synx.getChild(widget).delete('1.0', END)
        self.Synx.getChild(widget).insert(INSERT, text)
        self.Synx.getChild(enter).configure(text = '')
        

    def saveToFolderFile(self,ccj):
        name = self.Synx.getChild('folderSaveDialogueName0').get('1.0',END)
        name = name.replace(' ','_').replace('\n','').strip()
        if len(name) < 1:
            messagebox.showerror("Save To Folder", "You forgot to name the folder")
            return
        for i in self.MediaAndFolders:
            img = Image.open(i[0])
            img.save(i[1])
            img.close()
        with open(configPath+'/folders/'+name+'.txt','a+') as folder:
            folder.write(ccj)
        self.closeObjectOption('folderSaveDialogue0')
        self.MediaAndFolders = []
        self.mbOcupy()

    def updateFoldersListing(self):
        self.SavedFoldersList = []
        self.SavedFoldersListName = []
        directory = configPath+'/folders/'
        for the_file in os.listdir(directory):
            if the_file != 'folderImages':
                self.SavedFoldersList.append(os.path.join(directory, the_file))
                self.SavedFoldersListName.append('.'.join(the_file.split('.')[:-1]).replace('_',' '))

    def saveToFolderDialouge(self,ccj):
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        self.closeObjectOption('objectOption0')
        self.closeObjectOption('folderSaveDialogue0')
        self.Synx.layout(parent='win',child='folderSaveDialogue',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Bfc')+'text=  Choose a folder;fg=#0000cd;padx=15;',widthR='20',heightR='30')
        self.Synx.getChild('folderSaveDialogue0').grid(padx=(x + 150,0),pady=(y - 600,0))
        self.Synx.layout(parent='folderSaveDialogue0',child='folderSaveDialogueX',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Bfc'),widthR='2:50',heightR='30:30')
        self.Synx.affect(child='folderSaveDialogueX',point=[1],pointSet=[{'style':'text=X;font=Helvetica 11 bold;labelanchor=ne;fg=#ff0000;'}])
        self.Synx.layout(parent='folderSaveDialogue0',child='folderSaveDialogueName',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='20',marginYR='20')
        self.Synx.layout(parent='folderSaveDialogue0',child='folderAutoComplete',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Bfc')+'fg=#0000cd;',widthR='120',heightR='20',marginYR='40')
        self.Synx.layout(parent='folderSaveDialogue0',child='folderSaveDialogueSave',widget=tk.Button,resolveWH=True,sectionN=1,rowN=1,style=style('Bbg')+'text=SAVE;fg=#ffffff;',widthR='30',heightR='20',marginYR='60')
        self.Synx.getChild('folderSaveDialogueSave0').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('folderSaveDialogue0'),'w',35),0))
        padx = self.Synx.child_dimensions(self.Synx.getChild('folderSaveDialogue0'),'w',12)
        self.Synx.getChild('folderSaveDialogueName0').grid(padx=(padx,0))
        self.Synx.getChild('folderAutoComplete0').grid(padx=(padx,0))
        self.Synx.getChild('folderAutoComplete0').bind("<Enter>", lambda e: e.widget.config(fg='#548b54'))
        self.Synx.getChild('folderAutoComplete0').bind("<Leave>", lambda e: e.widget.config(fg='#0000cd'))
        self.Synx.getChild('folderSaveDialogueName0').bind('<Key>',lambda event, widget = 'folderSaveDialogueName0', enter = 'folderAutoComplete0', mapp = 'folders':self.autoComplete(widget,enter,mapp))
        self.Synx.getChild('folderSaveDialogueX1').bind('<Button- 1>',lambda event:self.closeObjectOption('folderSaveDialogue0'))
        self.Synx.getChild('folderSaveDialogueSave0').bind('<Button- 1>',lambda event:self.saveToFolderFile(ccj))
        self.updateFoldersListing()

    def saveToFolder(self,index):
        self.MediaAndFolders = []
        gathering = []
        congrigation = ''
        for i in range(len(index)):
            if index[i] > len(self.FlipThroughSI) - 1:
                break
            for j in range(len(self.FlipThroughSI[index[i]])):
                gathering.append(self.FlipThroughSI[index[i]][j])
        for i in range(len(gathering)):
            if gathering[i][0] == 'img':
                LinkIHave = gathering[i][1]
                randPP = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + '@#$%^)!_-~') for _ in range(70))
                LinkIWant = configPath+'/folders/folderImages/'+randPP+'.png'
                self.MediaAndFolders.append([LinkIHave,LinkIWant])
                congrigation += gathering[i][0]+'<--DOSIEx-->'+LinkIWant+'<--DOSIEy-->'
            else:
                congrigation += gathering[i][0]+'<--DOSIEx-->'+gathering[i][1]+'<--DOSIEy-->'
        self.saveToFolderDialouge(congrigation)
    
    def setIntoVacant(self,index,PRV=None):
        checkLastTabBefore = self.checkLastTab
        for i in range(len(index)):
            if index[i] > len(self.FlipThroughSI) - 1:
                self.Synx.getChild('Ctrlbutt3').configure(text='Done')
                self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild('CHplaneD5').configure(text=str(self.checkTabsPointing)+'/'+str(self.checkTabsPointing))
                self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
                self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event,PRvV=checkLastTabBefore:self.setIntoVacant([index[0] - 4,index[1] - 4,index[2] - 4,index[3] - 4],PRV=PRvV))
                return
            imageCK = self.imageInList(self.FlipThroughSI[index[i]])
            if imageCK > 0:
                self.imageIncluded(imageCK,self.FlipThroughSI[index[i]])
            else:
                self.textOnly(self.FlipThroughSI[index[i]])
            self.checkLastTab += len(self.FlipThroughSI[index[i]])
            if self.tabVacancy >= 3:
                self.tabVacancy = 0
            else:
                self.tabVacancy += 1
        nextIndex = []
        for i in range(4):
            nextIndex.append((i + 1)+index[len(index) - 1])
        if index[0] > 3:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event,PRvV=checkLastTabBefore:self.setIntoVacant([index[0] - 4,index[1] - 4,index[2] - 4,index[3] - 4],PRV=PRvV))
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        if isinstance(PRV,int):
            self.checkLastTab = PRV
        self.Synx.getChild('Ctrlbutt1').configure(text='Save')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.saveToFolder(index))
        self.Synx.getChild('Ctrlbutt3').configure(text='Next')
        self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event, indx=nextIndex:self.setIntoVacant(indx))
        self.Synx.getChild('CHplaneD5').configure(text=str(self.checkLastTab)+'/'+str(self.checkTabsPointing))

    def renameTopLab(self,word,qte=False):
        if qte == True:
            if len(word) > 34:
                self.Synx.getChild('processName0').configure(text='"'+word[0:34]+'..."')
            else:
                self.Synx.getChild('processName0').configure(text='"'+word+'"')
        else:
            if len(word) > 34:
                self.Synx.getChild('processName0').configure(text=word[0:34]+'...')
            else:
                self.Synx.getChild('processName0').configure(text=word)

    def frontAndBack(self,index):
        if index == '0 - 1':
            self.CurrentSearchResults(self.frontBackRge)
            self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 0'))
            self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 2'))
        elif index == '1 - 2':
            self.ShowDomainResultFull(self.frontBackPoint)
            self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('2 - 1'))
            self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack(0))
        elif index == '2 - 1':
            if len(self.CSearchinfoArr) > 0:
                self.Synx.getChild('CurrentSearchResFull0').destroy()
            self.Synx.getChild('Ctrlbutt3').configure(text='')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('Ctrlbutt1').configure(text='')
            self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('Ctrlbutt0').configure(text='')
            self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.backHold())
            self.CurrentSearchResults(self.frontBackRge)
            self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 0'))
            self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 2'))
        elif index == '1 - 0':
            self.Synx.getChild('CurrentSearchRes0').destroy()
            self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack(0))
            self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack('0 - 1'))
            self.Synx.getChild('Ctrlbutt3').configure(text='')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('Ctrlbutt1').configure(text='')
            self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('Ctrlbutt0').configure(text='')
            self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.backHold())
        elif index == 'X':
            self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 0'))
            self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event, X='':self.backHold())

    def ShowDomainResultFull(self,point):
        if len(self.CSearchinfoArr) < 1:
            self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('2 - 1'))
            self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack(0))
            return
        self.fronBackBegin = False
        self.frontBackPoint = point
        self.Synx.layout(parent='activity2',child='CurrentSearchResFull',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='100')
        self.Synx.layout(parent='CurrentSearchResFull0',child='CHplane',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style('Wbg'),widthR='100',heightR='10:87')
        self.Synx.layout(parent='CHplane0',child='CHplaneD',widget=tk.Label,style=style('Wbg'),sectionN=6,rowN=6,rounded=style('default5'),widthR='7:30:10:10:10:10',marginXR='2:10:2:6:2')
        self.Synx.affect(child='CHplaneD',point=[0,1,2,3,4,5],pointSet=[{'rounded':self.CSearchinfoArr[point][1]},{'style':'image=;text='+self.CSearchinfoArr[point][0]+';width=27;height=4;font=Helvetica 8 bold;anchor=w;fg=#000000;'},{'style':'image=;text=Relevance;width=10;height=3;anchor=w;fg=#7d7d7d;'},{'style':'image=;text='+self.CSearchinfoArr[point][2]+';width=10;height=3;anchor=w;fg=#0000cd;'},{'style':'image=;text=Info tabs;width=10;height=3;anchor=w;fg=#7d7d7d;'},{'style':'image=;text=2/'+str(len(self.CSearchinfoArr[point][4]))+';width=10;height=3;anchor=w;fg=#0000cd;'}])
        self.Synx.layout(parent='CHplane1',child='CHplaneI',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style('Wbg'),widthR='100',heightR='47:47')
        self.Synx.layout(parent='CHplaneI0',child='CHplaneDV',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='63:35',heightR='100:100')
        self.Synx.layout(parent='CHplaneI1',child='CHplane2DV',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='35:63',heightR='100:100')
        self.Synx.getChild('CurrentSearchResFull0').update()
        self.checkTabsPointing = len(self.CSearchinfoArr[point][4])
        #__BR
        self.FlipThroughSI = self.chunkIt(self.CSearchinfoArr[point][4],round(len(self.CSearchinfoArr[point][4]) / 4))
        #__BR
        self.checkLastTab = 0
        self.setIntoVacant([0,1,2,3])
        self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('2 - 1'))
        self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack(0))

    def CurrentResList(self,rge):
        self.frontBackRge = rge
        done = False
        isat = 0
        frameindx = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i + 1
                self.Synx.affect(child=str(frameindx)+'firstLine',point=[0,1],pointSet=[{'rounded':self.CSearchinfoArr[i][1]},{'style':'text='+self.CSearchinfoArr[i][0]+';'}])
                self.Synx.getChild(str(frameindx)+'firstLine0').bind('<Button- 1>',lambda event, point=i:self.ShowDomainResultFull(point))
                self.Synx.affect(child=str(frameindx)+'secondLine',point=[1,2,3,4,5,6],pointSet=[{'style':'text=Relevance;'},{'style':'text='+self.CSearchinfoArr[i][2]+';'},{'style':'text=Sections;'},{'style':'text='+str(self.CSearchinfoArr[i][3])+';'},{'style':'text=Info Tabs;'},{'style':'text='+str(len(self.CSearchinfoArr[i][4]))+';'}])
                self.Synx.getChild('CSinfoLine'+str(frameindx)).update()
                self.Synx.getChild('CurrentSearchRes0').update()
                if frameindx == 3:
                    break
                if i >= len(self.CSearchinfoArr) - 1:
                    done = True
            else:
                self.Synx.affect(child=str(frameindx)+'firstLine',point=[0,1],pointSet=[{'rounded':style('default5')},{'style':'text=;'}])
                self.Synx.getChild(str(frameindx)+'firstLine0').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.affect(child=str(frameindx)+'secondLine',point=[1,2,3,4,5,6],pointSet=[{'style':'text=;'},{'style':'text=;'},{'style':'text=;'},{'style':'text=;'},{'style':'text=;'},{'style':'text=;'}])
            frameindx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next ('+str(len(self.CSearchinfoArr) - isat)+')')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.CurrentResList([i + 1,i + 5]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 1:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous ('+str(isat - 1)+')')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.CurrentResList([rge[0] - 4,rge[1] - 4]))
        self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 0'))
        self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack('1 - 2'))

    def CurrentSearchResults(self,ptArr=False):
        global BRIDGE_Info_Arr
        self.renameTopLab(self.thatsWhatTheySaid,True)
        self.CSearchinfoArr = BRIDGE_Info_Arr
        try:
            self.Synx.getChild('CurrentSearchRes0').destroy()
        except:
            pass
        self.Synx.layout(parent='activity2',child='CurrentSearchRes',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='100')
        self.Synx.layout(parent='CurrentSearchRes0',child='CSinfoLine',widget=tk.LabelFrame,sectionN=4,rowN=1,style=style('Wbg'),widthR='100',heightR='21:21:21:21:21',marginYR='0:5:5:5:4')
        if len(self.CSearchinfoArr) < 1:
            self.frontAndBack('X')
            return
        for i in range(4):
            self.Synx.layout(parent='CSinfoLine'+str(i),child=str(i)+'childLine',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style('Wbg'),widthR='100',heightR='47:47',marginYR='0:6')
            self.Synx.layout(parent=str(i)+'childLine0',child=str(i)+'firstLine',widget=tk.Button,sectionN=2,rowN=2,style=style('Wbg'),rounded=style('default5'),widthR='7:80',heightR='94:90',marginXR='5')
            self.Synx.affect(child=str(i)+'firstLine',point=[0,1],pointSet=[{'rounded':style('default5')},{'style':'image=;text=;width=35;height=2;font=Helvetica 8 bold;anchor=w;'}])
            self.Synx.layout(parent=str(i)+'childLine1',child=str(i)+'secondLine',widget=tk.LabelFrame,sectionN=7,rowN=7,style=style(),widthR='7:12:12:12:12:12:12',marginXR='5:2:5:2:5:2:5')
            self.Synx.affect(child=str(i)+'secondLine',point=[1,2,3,4,5,6],pointSet=[{'style':'text=;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'},{'style':'text=;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'},{'style':'text=;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'}])
        if ptArr:
            self.CurrentResList(ptArr)
        else:
            self.CurrentResList([0,4])
        if self.fronBackBegin:
            self.frontAndBack('X')

    def closeFolderExplore(self):
        self.closeObjectOption('CurrentSearchResFull0')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())

    def exploreFolder(self,folder,name):
        self.renameTopLab('Folder "'+name+'"')
        with open(folder,'r') as fd:
            fd = fd.read()
            fd = fd.split('<--DOSIEy-->')[:-1]
            xxAr = []
            for i in range(len(fd)):
                xxAr.append(fd[i].split('<--DOSIEx-->'))
        self.CSearchinfoArr = [[name,style('folder'),'NONE',str(i),xxAr]]
        self.ShowDomainResultFull(0)
        self.Synx.getChild('Ctrlbutt2R2').bind('<Button- 1>',lambda event:self.frontAndBack(0))
        self.Synx.getChild('Ctrlbutt2R3').bind('<Button- 1>',lambda event:self.frontAndBack(0))
        self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeFolderExplore())

    def FlipThrougnFolderList(self,rge):
        done = False
        isat = 0
        frameindx = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i + 1
                if len(self.SavedFoldersListName[i]) > 11:
                    textXx = self.SavedFoldersListName[i][0:9]+'...'
                else:
                    textXx = self.SavedFoldersListName[i]
                self.Synx.affect(child='MenuFolderLabels',point=[frameindx],pointSet=[{'style':'text='+textXx+';'}])
                self.Synx.affect(child='MenuFolderFrames',point=[frameindx],pointSet=[{'rounded':style('folder')}])
                self.Synx.getChild('MenuFolderFrames'+str(frameindx)).bind('<Button- 1>',lambda event,folder = self.SavedFoldersList[i],name = textXx:self.exploreFolder(folder,name))
                self.Synx.getChild('MenuFolderFrames'+str(frameindx)).bind('<Button- 3>',lambda event,folder = self.SavedFoldersList[i],delff = True,pointt = ['MenuFolderFrames'+str(frameindx),'MenuFolderLabels'+str(frameindx),i]:self.objectOption(imp=folder,delf=delff,point=pointt))
                self.Synx.getChild('MenuFolderLabels'+str(frameindx)).update()
                self.Synx.getChild('MenuFolderFrames'+str(frameindx)).update()
                if frameindx == 35:
                    break
                if i >= len(self.SavedFoldersListName) - 1:
                    done = True
            else:
                self.Synx.affect(child='MenuFolderLabels',point=[frameindx],pointSet=[{'style':'text=;'}])
                self.Synx.affect(child='MenuFolderFrames',point=[frameindx],pointSet=[{'rounded':style('default5')}])
                self.Synx.getChild('MenuFolderFrames'+str(frameindx)).bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild('MenuFolderFrames'+str(frameindx)).bind('<Button- 1>',lambda event:self.backHold())
            frameindx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.FlipThrougnFolderList([i + 1,i + 37]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 1:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.FlipThrougnFolderList([rge[0] - 36,rge[1] - 36]))
        self.Synx.getChild('dFTagsFolder2').configure(text=str(isat)+'/'+str(len(self.SavedFoldersListName)))

    def menuFolders(self):
        self.Synx.layout(parent='menuFrames0',child='FolderFrames',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style('Wbg'),widthR='100',heightR='5:90')
        self.Synx.layout(parent='FolderFrames0',child='dFTagsFolder',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'anchor=w;',marginXR='50:1')
        self.Synx.affect(child='dFTagsFolder',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.renameTopLab('Folders')
        self.Synx.layout(parent='FolderFrames1',child='MenuFolderFrames',widget=tk.Button,sectionN=36,rowN=6,style=style('Wbg'),rounded=style('default5'),widthR='7:7:7:7:7:7',marginXR='10:10:12:12:12',heightR='10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10:10',marginYR='0:0:0:0:0:0:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7:7')
        self.Synx.layout(parent='FolderFrames1',child='MenuFolderLabels',widget=tk.Label,sectionN=36,rowN=6,style=style('Wbg'),rounded=style('default5'),widthR='12:12:12:12:12:12',marginXR='4:6:7:6:5',heightR='1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1:1',marginYR='10:10:10:10:10:10:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16:16')
        self.updateFoldersListing()
        for i in range(36):
            self.Synx.affect(child='MenuFolderLabels',point=[i],pointSet=[{'style':'image=;text=;width=12;height=1;anchor=s;'}])
            self.Synx.affect(child='MenuFolderFrames',point=[i],pointSet=[{'rounded':style('default5')}])
        self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())
        self.Synx.getChild('searchE0').bind('<Key>',lambda event:self.searchSomething('SearchFolders'))
        if len(self.SavedFoldersListName) < 1:
            return
        self.FlipThrougnFolderList([0,36])

    def listMenuMedia(self,rge):
        done = False
        isat = 0
        frameindx = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i + 1
                accessPath = 'path='+self.ViewMediaList[i]+';'
                self.Synx.affect(child='MMediaImageFrames',point=[frameindx],pointSet=[{'rounded':accessPath}])
                self.Synx.getChild('MMediaImageFrames'+str(frameindx)).bind('<Button- 1>',lambda event, XXc = accessPath,dell = True,points=['MMediaImageFrames'+str(frameindx),i]:self.objectOption(imp=XXc,dell=dell,point=points))
                if frameindx == 8:
                    break
                if i >= len(self.ViewMediaList) - 1:
                    done = True
            else:
                self.Synx.affect(child='MMediaImageFrames',point=[frameindx],pointSet=[{'rounded':style('default5')}])
            frameindx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.listMenuMedia([i + 1,i + 10]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 1:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.listMenuMedia([rge[0] - 9,rge[1] - 9]))
        self.Synx.getChild('dFTagsMedia2').configure(text=str(isat)+'/'+str(len(self.ViewMediaList)))

    def menuMedia(self):
        self.Synx.layout(parent='menuFrames0',child='MMediaFrames',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style('Wbg'),widthR='100',heightR='5:90')
        self.Synx.layout(parent='MMediaFrames0',child='dFTagsMedia',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'anchor=w;',marginXR='50:1')
        self.Synx.affect(child='dFTagsMedia',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.renameTopLab('Media')
        self.Synx.layout(parent='MMediaFrames1',child='MMediaImageFrames',widget=tk.Label,sectionN=9,rowN=3,style=style('Wbg'),rounded=style('default5'),widthR='30:30:30')
        self.ViewMediaList = []
        self.ViewMediaListAuto = []
        homeDir = os.path.expanduser("~")
        directory = homeDir+'\\Pictures\\DosieSaved\\'
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            self.ViewMediaList.append(file_path)
            self.ViewMediaListAuto.append(the_file)
        self.Synx.getChild('searchE0').bind('<Key>',lambda event:self.searchSomething('SearchMedia'))
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        if len(self.ViewMediaList) < 1:
            return
        self.listMenuMedia([0,9])

    def historyNav(self,rge):
        frameIndx = 1
        done = False
        isat = 0
        for i in range(rge[0],rge[1]):
            for widget in self.Synx.getChild('keywordFrames'+str(frameIndx)).winfo_children():
                    widget.destroy()
            if not done:
                isat = i
                self.Synx.layout(parent='keywordFrames'+str(frameIndx),child=str(frameIndx)+'KWMlist',widget=tk.Label,resolveWH=True,sectionN=2,rowN=2,style=style('Bfc')+'anchor=w;fg=#7d7d7d;',widthR='120:30',heightR='35:35',marginYR='30:30')
                self.Synx.affect(child=str(frameIndx)+'KWMlist',point=[0,1],pointSet=[{'style':'text='+self.pastHistory[i - 1][0]+';'},{'style':'text='+self.pastHistory[i - 1][1]+';anchor=s;'}])
                self.Synx.layout(parent='keywordFrames'+str(frameIndx),child=str(frameIndx)+'KWZlist',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='87:10',heightR='33:20',marginYR='73:55')
                self.Synx.affect(child=str(frameIndx)+'KWZlist',point=[1],pointSet=[{'style':'text=Search;labelanchor=s;pady=4;bg=#0000cd;fg=#ffffff;'}])
                self.Synx.layout(parent=str(frameIndx)+'KWZlist0',child=str(frameIndx)+'KWZlistIMG',widget=tk.Label,sectionN=10,rowN=10,style=style('Wbg'),rounded=style('default5'),widthR='3:3:3:3:3:3:3:3:3:3:3',marginXR='4:4:4:4:4:4:4:4:4:4:4',heightR='100:100:100:100:100:100:100:100:100:100:100')
                self.Synx.getChild(str(frameIndx)+'KWZlist1').bind('<Button- 1>',lambda event,text=self.pastHistory[i - 1][0],source=self.pastHistory[i - 1][3],wtg=self.pastHistory[i - 1][1]:self.initializeNewSearch(text=text,source=source,kwkw=True,wtg=wtg))
                for k in range(len(self.pastHistory[i - 1][2])):
                    if not self.pastHistory[i - 1][2][k]:
                        self.Synx.affect(child=str(frameIndx)+'KWZlistIMG',point=[k],pointSet=[{'rounded':style('fim')}])
                    else:
                        self.Synx.affect(child=str(frameIndx)+'KWZlistIMG',point=[k],pointSet=[{'rounded':self.pastHistory[i - 1][2][k]}])
                    if k == 8:
                        break
                if i >= len(self.pastHistory):
                    done = True
            frameIndx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.historyNav([i + 1,i + 6]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 2:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.historyNav([rge[0] - 5,rge[1] - 5]))
        self.Synx.getChild('dFTagsKeyword2').configure(text=str(isat)+'/'+str(len(self.pastHistory)))

    def clearHistory(self):
        var = tk.messagebox.askyesnocancel ('Clear History','Are you sure?')
        if var:
            self.cleanUp(domain=True)
            with open(configPath+'/access/history.txt','w+') as history:
                history.write('')
            self.closeMenuFrames()

    def menuHistory(self):
        self.Synx.layout(parent='menuFrames0',child='keywordFrames',widget=tk.LabelFrame,sectionN=6,rowN=1,style=style('Wbg'),widthR='100',heightR='5:14:14:14:14:14',marginYR='0:5:5:5:5:5')
        self.Synx.layout(parent='keywordFrames0',child='dFTagsKeyword',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'anchor=w;',marginXR='50:1')
        self.Synx.affect(child='dFTagsKeyword',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.renameTopLab('History')
        self.pastHistory = []
        with open(configPath+'/access/history.txt','r') as history:
            history = history.read()
            if len(history) > 0:
                history = history.split('\n\n<--DOSIE_NEXT-->\n\n')[0:-1]
                for i in range(len(history)):
                    divs = history[i].split('<--DOSIIx-->')
                    self.pastHistory.append([divs[0],divs[1],divs[2].split('<--DOSIIy-->'),divs[3].split('<--DOSIIy-->')])
        self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())
        self.Synx.getChild('Ctrlbutt1').configure(text='Clear Records')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.clearHistory())
        if len(self.pastHistory) < 1:
            return
        self.historyNav([1,6])

    def reviseKeywords(self):
        self.AllSearchKeywords = []
        self.KeywordsAuto = []
        self.KeywordsAutoIndex = []
        have = []
        idx = 0
        with open(configPath+'/access/keywords.txt','r') as keywords:
            keywords = keywords.read().split('\n<--DOSIEend-->\n')[0:-1]
            for i in keywords:
                ys = i.split('<--DOSIEy-->')
                Dsr = list(filter(None, ys[0].split('<--DOSIEx-->')))
                self.KeywordsAuto += Dsr
                for l in Dsr:
                    self.KeywordsAutoIndex.append(idx)
                for j in ys:
                    XXc = j.split('<--DOSIEx-->')
                    have.append(XXc)
                self.AllSearchKeywords.append(have)
                have = []
                idx += 1

    def keywordUpdateFromApp(self):
        present = ''
        for i in self.AllSearchKeywords:
            final = i
            present += '<--DOSIEx-->'.join(final[0])+'<--DOSIEy-->'+'<--DOSIEx-->'.join(final[1])+'<--DOSIEy-->'+'<--DOSIEx-->'.join(final[2])+'\n<--DOSIEend-->\n'
        with open(configPath+'/access/keywords.txt','w+') as keywords:
            keywords.write(present)

    def ThisKeywordDetails(self,imp,point):
        self.closeObjectOption('objectOption0')
        self.KeyworDSettings(imp,point)

    def ThisKeywordDelete(self,imp,frameIndx):
        var = tk.messagebox.askyesnocancel ('Delete Keywords','Are you sure?')
        self.closeObjectOption('objectOption0')
        if var:
            self.AllSearchKeywords.pop(imp)
            self.keywordUpdateFromApp()
            self.reviseKeywords()
            self.Synx.affect(child=str(frameIndx)+'keywordItem',point=[0,1,2,3],pointSet=[{'style':'text=;'},{'style':'text=;'},{'style':'text=;'},{'style':'text=;'}])
            self.Synx.affect(child=str(frameIndx)+'KWZlistIMG',point=[0,1,2,3,4,5,6,7,8],pointSet=[{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')}])
            self.Synx.affect(child=str(frameIndx)+'KWZlist',point=[1],pointSet=[{'style':'text=;bg=#ffffff;fg=#ffffff;'}])
            self.Synx.affect(child=str(frameIndx)+'KWMlist',point=[1],pointSet=[{'style':'text=;bg=#ffffff;fg=#ffffff;'}])
            self.Synx.getChild(str(frameIndx)+'KWMlist1').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild(str(frameIndx)+'keywordItem0').bind('<Button- 1>',lambda event:self.backHold())

    def restoreFlipThrougnmenuKeywords(self,point):
        self.closeMenuFrames()
        self.menuFrames('re')
        self.menuKeywords(True)
        self.flipThrougnmenuKeywords(point)


    def pointToKeyword(self,frameIndx,imp,indx):
        if self.AllSearchKeywords[imp][0][indx]:
            for i in range(4):
                if i == indx:
                    self.Synx.getChild(str(frameIndx)+'keywordItem'+str(i)).configure(fg='#0000cd;')
                    self.Synx.getChild(str(frameIndx)+'keywordItem'+str(i)).update()
                else:
                    self.Synx.getChild(str(frameIndx)+'keywordItem'+str(i)).configure(fg='#7d7d7d;')
                    self.Synx.getChild(str(frameIndx)+'keywordItem'+str(i)).update()
            self.Synx.getChild(str(frameIndx)+'KWZlist1').bind('<Button- 1>',lambda event,text=self.AllSearchKeywords[imp][0][indx],source=self.AllSearchKeywords[imp][2]:self.initializeNewSearch(text=text,source=source,kwkw=True,wtg='STATIC'))
        

    def flipThrougnmenuKeywords(self,rge):
        frameIndx = 1
        done = False
        isat = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i
                self.Synx.affect(child=str(frameIndx)+'keywordItem',point=[0,1,2,3],pointSet=[{'style':'text='+self.AllSearchKeywords[i - 1][0][0]+';'},{'style':'text='+self.AllSearchKeywords[i - 1][0][1]+';'},{'style':'text='+self.AllSearchKeywords[i - 1][0][2]+';'},{'style':'text='+self.AllSearchKeywords[i - 1][0][3]+';'}])
                self.Synx.affect(child=str(frameIndx)+'KWZlistIMG',point=[0,1,2,3,4,5,6,7,8],pointSet=[{'rounded':self.AllSearchKeywords[i - 1][1][0]},{'rounded':self.AllSearchKeywords[i - 1][1][1]},{'rounded':self.AllSearchKeywords[i - 1][1][2]},{'rounded':self.AllSearchKeywords[i - 1][1][3]},{'rounded':self.AllSearchKeywords[i - 1][1][4]},{'rounded':self.AllSearchKeywords[i - 1][1][5]},{'rounded':self.AllSearchKeywords[i - 1][1][6]},{'rounded':self.AllSearchKeywords[i - 1][1][7]},{'rounded':style('default5')}])
                self.Synx.affect(child=str(frameIndx)+'KWZlist',point=[1],pointSet=[{'style':'text=Search;bg=#0000cd;fg=#ffffff;'}])
                self.Synx.affect(child=str(frameIndx)+'KWMlist',point=[1],pointSet=[{'style':'text=Edit;bg=#0000cd;fg=#ffffff;'}])
                self.Synx.getChild(str(frameIndx)+'keywordItem0').bind('<Button- 3>',lambda event,imp=(i - 1),Kwo=True,point=['view',rge,frameIndx]:self.objectOption(imp=imp,Kwo=Kwo,point=point))
                self.Synx.getChild(str(frameIndx)+'KWMlist1').bind('<Button- 1>',lambda event,imp=(i - 1),point=['edit',rge]:self.KeyworDSettings(imp=imp,point=point))
                self.Synx.getChild(str(frameIndx)+'keywordItem0').bind('<Button- 1>',lambda event,frameIndx=frameIndx,imp=(i - 1),indx=0:self.pointToKeyword(frameIndx=frameIndx,imp=imp,indx=indx))
                self.Synx.getChild(str(frameIndx)+'keywordItem1').bind('<Button- 1>',lambda event,frameIndx=frameIndx,imp=(i - 1),indx=1:self.pointToKeyword(frameIndx=frameIndx,imp=imp,indx=indx))
                self.Synx.getChild(str(frameIndx)+'keywordItem2').bind('<Button- 1>',lambda event,frameIndx=frameIndx,imp=(i - 1),indx=2:self.pointToKeyword(frameIndx=frameIndx,imp=imp,indx=indx))
                self.Synx.getChild(str(frameIndx)+'keywordItem3').bind('<Button- 1>',lambda event,frameIndx=frameIndx,imp=(i - 1),indx=3:self.pointToKeyword(frameIndx=frameIndx,imp=imp,indx=indx))
                if i >= len(self.AllSearchKeywords):
                    done = True
            else:
                self.Synx.affect(child=str(frameIndx)+'keywordItem',point=[0,1,2,3],pointSet=[{'style':'text=;'},{'style':'text=;'},{'style':'text=;'},{'style':'text=;'}])
                self.Synx.affect(child=str(frameIndx)+'KWZlistIMG',point=[0,1,2,3,4,5,6,7,8],pointSet=[{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')},{'rounded':style('default5')}])
                self.Synx.affect(child=str(frameIndx)+'KWZlist',point=[1],pointSet=[{'style':'text=;bg=#ffffff;fg=#ffffff;'}])
                self.Synx.affect(child=str(frameIndx)+'KWMlist',point=[1],pointSet=[{'style':'text=;bg=#ffffff;fg=#ffffff;'}])
                self.Synx.getChild(str(frameIndx)+'KWMlist1').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild(str(frameIndx)+'keywordItem0').bind('<Button- 3>',lambda event:self.backHold())
                self.Synx.getChild(str(frameIndx)+'keywordItem0').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild(str(frameIndx)+'keywordItem1').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild(str(frameIndx)+'keywordItem2').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild(str(frameIndx)+'keywordItem3').bind('<Button- 1>',lambda event:self.backHold())
            frameIndx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.flipThrougnmenuKeywords(category,[i + 1,i + 6]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] <= 2:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.flipThrougnmenuKeywords([rge[0] - 5,rge[1] - 5]))
        self.Synx.getChild('dFTagsKeyword2').configure(text=str(isat)+'/'+str(len(self.AllSearchKeywords)))

    def menuKeywords(self,ResTr=False):
        self.Synx.layout(parent='menuFrames0',child='keywordFrames',widget=tk.LabelFrame,sectionN=6,rowN=1,style=style('Wbg'),widthR='100',heightR='5:14:14:14:14:14',marginYR='0:5:5:5:5:5')
        self.Synx.layout(parent='keywordFrames0',child='dFTagsKeyword',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'anchor=w;',marginXR='50:1')
        self.Synx.affect(child='dFTagsKeyword',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.renameTopLab('Keywords')
        for i in range(1,6):
            self.Synx.layout(parent='keywordFrames'+str(i),child=str(i)+'KWMlist',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='87:10',heightR='65:20',marginYR='0:30')
            self.Synx.layout(parent=str(i)+'KWMlist0',child=str(i)+'keywordItem',widget=tk.LabelFrame,sectionN=4,rowN=2,style=style('Wbg')+'fg=#7d7d7d;',widthR='48:48')
            self.Synx.affect(child=str(i)+'KWMlist',point=[1],pointSet=[{'style':'text=;labelanchor=s;pady=4;bg=#ffffff;fg=#ffffff;'}])
            self.Synx.layout(parent='keywordFrames'+str(i),child=str(i)+'KWZlist',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='87:10',heightR='33:20',marginYR='73:55')
            self.Synx.affect(child=str(i)+'KWZlist',point=[1],pointSet=[{'style':'text=;labelanchor=s;pady=4;bg=#ffffff;fg=#ffffff;'}])
            self.Synx.layout(parent=str(i)+'KWZlist0',child=str(i)+'KWZlistIMG',widget=tk.Label,sectionN=10,rowN=10,style=style('Wbg'),rounded=style('default5'),widthR='3:3:3:3:3:3:3:3:3:3:3',marginXR='4:4:4:4:4:4:4:4:4:4:4',heightR='100:100:100:100:100:100:100:100:100:100:100')
        self.Synx.getChild('searchE0').bind('<Key>',lambda event:self.searchSomething('SearchKeywords'))
        if len(self.AllSearchKeywords) < 1:
            return
        if not ResTr:
            self.flipThrougnmenuKeywords([1,6])

    def reURLdomain(self,imp,point):
        text = self.Synx.getChild('domainListInfoLineText0').get('1.0',END).replace('\n','').strip()
        if len(text) < 1:
            messagebox.showerror("Edit Domain URL", "Please enter a valit URL")
            return
        newURL = text
        if 'https://' not in newURL and 'http://' not in newURL:
            newURL = 'http://'+newURL
        domainName = newURL[newURL.find('//') + 2:].replace('www.','')
        if domainName.find('/') > -1:
            domainName = domainName[0:domainName.find('/')]
        self.domainAllList[point[0]][imp][0] = domainName
        self.domainAllList[point[0]][imp][2] = newURL
        self.updateFromAppToDomainFile()
        self.reviseDomains()
        self.Synx.affect(child=str(point[1])+'dFlistT',point=[1],pointSet=[{'style':'text='+domainName+';'}])
        self.closeObjectOption('objectOption0')
        self.closeObjectOption('domainListInfo0')

    def ThisDomainDetails(self,ev,imp,point,edit=False):
        self.closeObjectOption('objectOption0')
        self.closeObjectOption('domainListInfo0')
        self.Synx.layout(parent='menuFrames0',child='domainListInfo',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='80',heightR='20',marginYR='30')
        self.Synx.getChild('domainListInfo0').grid(padx=(ev[0]-160,0),pady=((ev[1] - 140),0))
        self.Synx.layout(parent='domainListInfo0',child='domainListInfoLine',widget=tk.LabelFrame,sectionN=4,rowN=1,style=style('Wbg'),widthR='100',heightR='15:20:20:20')
        self.Synx.affect(child='domainListInfoLine',point=[0,1],pointSet=[{'style':'text=X  ;fg=#ff0000;font=Helvetica 11 bold;labelanchor=e;'},{'style':'text=  '+self.domainAllList[point[0]][imp][0]+';fg=#0000cd;'}])
        self.Synx.getChild('domainListInfoLine0').bind('<Button- 1>',lambda event:self.closeObjectOption('domainListInfo0'))
        self.Synx.layout(parent='domainListInfoLine2',child='domainListInfoLineText',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg'),widthR='140',heightR='100')
        self.Synx.getChild('domainListInfoLineText0').insert(INSERT,self.domainAllList[point[0]][imp][2])
        if edit:
            self.Synx.layout(parent='domainListInfoLine3',child='domainListInfoLineTextBt',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Bbg')+'text=SAVE;fg=#ffffff;labelanchor=s;',widthR='14',heightR='100')
            self.Synx.getChild('domainListInfoLineTextBt0').bind('<Button- 1>',lambda event:self.reURLdomain(imp,point))
            self.Synx.getChild('domainListInfoLineTextBt0').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('domainListInfoLine3'),'w',85),0))
        else:
            self.Synx.getChild('domainListInfoLineText0').configure(state='disabled')

    def ThisDomainEdit(self,ev,imp,point):
        self.ThisDomainDetails(ev,imp,point,edit=True)
    
    def ThisDomainDelete(self,ev,imp,point):
        var = tk.messagebox.askyesnocancel ('Delete Domain','Delete domain from this category?')
        if var:
            self.domainAllList[point[0]].pop(imp)
            self.updateFromAppToDomainFile()
            self.reviseDomains()
            self.Synx.affect(child=str(point[1])+'dFlistT',point=[0,1,3],pointSet=[{'rounded':style('default5')},{'style':'text=;'},{'style':'text=;fg=#ffffff;'}])
            self.Synx.getChild(str(point[1])+'dFlistT0').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild(str(point[1])+'dFlistTenter0').delete('1.0',END)
            self.Synx.getChild(str(point[1])+'dFlistTenter0').configure(state='disabled')
            self.Synx.getChild(str(point[1])+'dFlistT3').bind('<Button- 1>',lambda event:self.backHold())
            self.closeObjectOption('objectOption0')
            self.closeObjectOption('domainListInfo0')

    def domainNav(self,category,rge):
        frameIndx = 1
        done = False
        isat = 0
        for i in range(rge[0],rge[1]):
            for widget in self.Synx.getChild('domainFrames'+str(frameIndx)).winfo_children():
                    widget.destroy()
            if not done:
                isat = i
                self.Synx.layout(parent='domainFrames'+str(frameIndx),child=str(frameIndx)+'dFlistT',widget=tk.Label,sectionN=4,rowN=4,style=style('Wbg'),rounded=style('default5'),widthR='10:40:30:10',heightR='80:20:20:20',marginYR='10:35:35:35')
                self.Synx.layout(parent=str(frameIndx)+'dFlistT2',child=str(frameIndx)+'dFlistTenter',widget=tk.Text,sectionN=1,rowN=1,style='width=25;height=1;bd=0;fg=#7d7d7d;',widthR='1',heightR='1')
                self.Synx.getChild(str(frameIndx)+'dFlistTenter0').insert(END,'Search...')
                self.Synx.affect(child=str(frameIndx)+'dFlistT',point=[0,1,3],pointSet=[{'rounded':self.domainAllList[category][i - 1][1]},{'style':'image=;width=40;height=1;text='+self.domainAllList[category][i - 1][0]+';anchor=w;fg=#7d7d7d;'},{'style':'image=;width=8;height=1;text=Search;anchor=w;fg=#0000cd;'}])
                self.Synx.getChild(str(frameIndx)+'dFlistT0').bind('<Button- 1>',lambda event,imp=(i - 1),DDl=True,point=[category,frameIndx]:self.objectOption(imp=imp,DDl=DDl,point=point))
                gagani = self.domainAllList[category][i - 1][2]
                if gagani[-1:] == '/':
                    SMxml = gagani+'sitemap.xml'
                else:
                    SMxml = gagani+'/sitemap.xml'
                self.Synx.getChild(str(frameIndx)+'dFlistT3').bind('<Button- 1>',lambda event,text=str(frameIndx)+'dFlistTenter0',source=[gagani,SMxml]:self.initializeNewSearch(text=text,source=source,wtg='STATIC'))
                if i >= len(self.domainAllList[category]):
                    done = True
            frameIndx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.domainNav(category,[i + 1,i + 6]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 2:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.domainNav(category,[rge[0] - 5,rge[1] - 5]))
        self.Synx.getChild('dFTags2').configure(text=str(isat)+'/'+str(len(self.domainAllList[category])))

    def reviseDomains(self):
        with open(configPath+'/access/domains.txt','r') as domains:
            self.domainAllList = {}
            self.MarkCategory = []
            domains = domains.read().split('<--DOSIEcatEnd-->\n\n')[0:-1]
            for i in range(len(domains)):
                diff = domains[i].split('<--DOSIEcat-->\n')
                category = diff[0]
                self.DomainListedCategories.append(category.replace('_',' '))
                dm = diff[1].split('\n\n<--DOSIEy-->\n\n')[0:-1]
                self.domainAllList[category] = []
                self.MarkCategory.append(category)
                for j in range(len(dm)):
                    dmx = dm[j].split('<--DOSIEx-->')
                    self.domainAllList[category].append(dmx)
                    self.SearchLinkName.append(dmx[0])
                    self.SearchLinkLink.append(dmx[2])

    def convert_size(self,size_bytes):
        if size_bytes == 0:
           return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def mbOcupy(self):
        files = [configPath+'/img/discovered/',configPath+'/img/domainICO/',configPath+'/folders/',configPath+'/access/',self.Synx.mediaPath+'\\',configPath+'/folders/folderImages/',os.path.expanduser("~")+'\\Pictures\\DosieSaved']
        mb = 0
        for i in files:
            folder = i
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        mb += os.path.getsize(file_path)
                except Exception as e:
                    pass
                    #print(e)
        mb = self.convert_size(mb)
        self.Synx.getChild('navBottomTxt0').configure(text=str(mb))

    def menuDomains(self):
        self.reviseDomains()
        self.Synx.layout(parent='menuFrames0',child='domainFrames',widget=tk.LabelFrame,sectionN=6,rowN=1,style=style('Wbg'),widthR='100',heightR='5:17:17:17:17:17',marginYR='0:2:2:2:2:2')
        categoryName = ''
        for key in self.domainAllList:
            categoryName = key
            break
        self.renameTopLab('Category: '+categoryName+'')
        self.Synx.layout(parent='domainFrames0',child='dFTags',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'text=play;anchor=w;',marginXR='50:1')
        self.Synx.affect(child='dFTags',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text='+categoryName+';fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('searchE0').bind('<Key>',lambda event:self.searchSomething('SearchDomainCategory'))
        if len(self.domainAllList) < 1:
            return
        self.domainNav(categoryName,[1,6])

    def applyLinkEdit(self,index):
        txx = self.Synx.getChild('linkTextenter0').get('1.0',END).replace('\n','')
        self.Synx.getChild('linkTextenter0').delete('1.0',END)
        self.Synx.getChild('saidLink'+str(index + 1)+'0').configure(text=txx,fg='#0000cd')
        self.homeLinkInpArr[index] = txx
        self.Synx.getChild('linkTextenter0').bind('<Return>',lambda event:self.nextLink())


    def deleteLink(self,index):
        self.Synx.getChild('saidLink'+str(index + 1)+'0').configure(text='')
        self.Synx.getChild('saidLink'+str(index + 1)+'0').update()
        self.Synx.getChild('saidLink'+str(index + 1)+'1').configure(image='')
        self.Synx.getChild('saidLink'+str(index + 1)+'2').configure(image='')
        self.Synx.getChild('saidLink'+str(index + 1)+'1').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('saidLink'+str(index + 1)+'2').bind('<Button- 1>',lambda event:self.backHold())
        self.homeLinkInpArr[index] = None

    def editLink(self,index):
        txt = self.homeLinkInpArr[index]
        self.Synx.getChild('linkTextenter0').delete('1.0',END)
        self.Synx.getChild('linkTextenter0').insert(INSERT,txt)
        self.Synx.getChild('saidLink'+str(index + 1)+'0').configure(fg='#548b54')
        self.Synx.getChild('linkTextenter0').bind('<Return>',lambda event:self.applyLinkEdit(index))

    def nextLink(self):
        wtd = self.Synx.getChild('linkTextenter0').get('1.0',END).replace('\n','').strip()
        self.Synx.getChild('linkTextenter0').delete('1.0',END)
        if isinstance(wtd,str):
            if len(wtd.replace(' ','')) > 0:
                if len(self.homeLinkInpArr) <= 7:
                    self.homeLinkInpArr.append(wtd)
                    newIndex = len(self.homeLinkInpArr)
                    parent = self.Synx.getChild('initiateSearch'+str(newIndex))
                    for widget in parent.winfo_children():
                        widget.destroy()
                    self.Synx.layout(parent='initiateSearch'+str(newIndex),child='saidLink'+str(newIndex),widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg'),rounded=style('default5'),widthR='86:3:3',heightR='100:50:50',marginYR='0:20:20',marginXR='4:4')
                    self.Synx.affect(child='saidLink'+str(newIndex),point=[0,1,2],pointSet=[{'style':'image=;width=77;height=2;text='+wtd+';anchor=w;fg=#0000cd;'},{'rounded':style('lked')},{'rounded':style('lkdl')}])
                    self.Synx.getChild('saidLink'+str(newIndex)+'1').bind('<Button- 1>',lambda event,inx=newIndex - 1:self.editLink(inx))
                    self.Synx.getChild('saidLink'+str(newIndex)+'2').bind('<Button- 1>',lambda event,inx=newIndex - 1:self.deleteLink(inx))
                    newIndex += 1
                    self.Synx.layout(parent='initiateSearch'+str(newIndex),child='domainwordentry',widget=tk.Label,sectionN=4,rowN=4,style=style('Wbg'),rounded=style('default5'),widthR='77:3:3:3',heightR='80:50:50:50',marginYR='0:38:38:38',marginXR='5:5:4')
                    self.Synx.layout(parent='domainwordentry0',child='linkTextenter',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Tbd'),widthR='160',heightR='100')
                    self.Synx.affect(child='domainwordentry',point=[1,2,3],pointSet=[{'rounded':style('lkst')},{'rounded':style('lksv')},{'rounded':style('lksh')}])
                    self.Synx.getChild('linkTextenter0').bind('<Return>',lambda event:self.nextLink())
                    self.Synx.layout(parent='initiateSearch'+str(newIndex),child='domainwordentryAutoComplete',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'fg=#551a8b;anchor=nw;',widthR='130',heightR='100',marginYR='80')
                    self.Synx.getChild('linkTextenter0').bind('<Key>',lambda event:self.autoComplete('linkTextenter0','domainwordentryAutoComplete0','searchLinks'))
                    self.Synx.getChild('domainwordentry3').bind('<Button- 1>',lambda event:self.initializeNewSearch('keywordentryText0',self.homeLinkInpArr))
                    self.Synx.getChild('domainwordentry1').bind('<Button- 1>',lambda event:self.switchSearchType())
                    self.Synx.getChild('domainwordentry2').bind('<Button- 1>',lambda event:self.saveSearchAsKW())
        else:
            pass

    def switchSearchType(self):
        global SEARCH_TYPE
        if SEARCH_TYPE == 'STATIC':
            SEARCH_TYPE = 'DYNAMIC'
            self.Synx.affect(child='domainwordentry',point=[1],pointSet=[{'rounded':style('lkedyn')}])
        else:
            SEARCH_TYPE = 'STATIC'
            self.Synx.affect(child='domainwordentry',point=[1],pointSet=[{'rounded':style('lkst')}])

    def saveSearchAsKW(self):
        LkResult = list(filter(None, self.homeLinkInpArr))
        KWResult = [self.Synx.getChild('keywordentryText0').get('1.0',END).replace('\n','').strip()]
        KWResult = list(filter(None, KWResult))
        if len(LkResult) < 1:
            messagebox.showerror("Save as keyword", "Please make sure you type in a valid URL")
            return
        if len(KWResult) < 1:
            messagebox.showerror("Save as keyword", "Please make sure you type in a search term")
            return

        fullListL = []
        fullListIC = []
        for i in LkResult:
            newURL = i
            if 'https://' not in newURL and 'http://' not in newURL:
                newURL = 'http://'+newURL
            domainName = newURL[newURL.find('//') + 2:].replace('www.','')
            if domainName.find('/') > -1:
                domainName = domainName[0:domainName.find('/')]
            DNfound = False
            IMpath = 'path='+configPath+'/img/domainICO/Icon.png;circular=True;'
            for keyy in self.domainAllList:
                for i in self.domainAllList[keyy]:
                    if i[0] == domainName:
                        IMpath = i[1]
                        DNfound = True
                        break
                if DNfound:
                    break
            fullListL.append(newURL)
            fullListIC.append(IMpath)
        for i in range(len(fullListIC),8):
            fullListIC.append(style('default5')+'circular=True;')
        for i in range(len(KWResult),4):
            KWResult.append('')

        final = [KWResult,fullListIC,fullListL]
        with open(configPath+'/access/keywords.txt','a+') as keywords:
            keywords.write('<--DOSIEx-->'.join(final[0])+'<--DOSIEy-->'+'<--DOSIEx-->'.join(final[1])+'<--DOSIEy-->'+'<--DOSIEx-->'.join(final[2])+'\n<--DOSIEend-->\n')
        self.reviseKeywords()
        self.Synx.affect(child='domainwordentry',point=[2],pointSet=[{'rounded':style('kwsv')}])

    def doGoogleSearch(self):
        text = self.Synx.getChild('keywordentryText0').get('1.0',END).replace('\n','').strip()
        source = ['https://www.google.com/search?q='+text.replace(' ','+')+'&ie=utf-8&oe=utf-8&client=firefox-b-ab']
        self.initializeNewSearch(text=text,source=source,kwkw=True,wtg='DYNAMIC')

    def homeSpace(self):
        self.Synx.layout(parent='menuFrames0',child='HomeSpace',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='100')
        self.renameTopLab('Home')
        self.Synx.layout(parent='HomeSpace0',child='initiateSearch',widget=tk.LabelFrame,sectionN=10,rowN=1,style=style('Wbg'),widthR='100',heightR='8:8:8:8:8:8:8:8:8:8',marginYR='5:1:1:1:1:1:1:1:1:1')
        self.Synx.layout(parent='initiateSearch0',child='keywordentry',widget=tk.Label,sectionN=2,rowN=2,style=style('Wbg'),rounded=style('default5'),widthR='92:4',heightR='100:83')
        self.Synx.layout(parent='keywordentry0',child='keywordentryText',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Tbd'),widthR='160',heightR='100')
        self.Synx.affect(child='keywordentry',point=[1],pointSet=[{'rounded':style('google')}])
        self.Synx.layout(parent='initiateSearch1',child='domainwordentry',widget=tk.Label,sectionN=4,rowN=4,style=style('Wbg'),rounded=style('default5'),widthR='77:3:3:3',heightR='80:50:50:50',marginYR='0:38:38:38',marginXR='5:5:4')
        self.Synx.layout(parent='domainwordentry0',child='linkTextenter',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Tbd'),widthR='160',heightR='100')
        self.Synx.affect(child='domainwordentry',point=[1,2,3],pointSet=[{'rounded':style('lkst')},{'rounded':style('lksv')},{'rounded':style('lksh')}])
        self.Synx.getChild('linkTextenter0').bind('<Return>',lambda event:self.nextLink())
        self.Synx.layout(parent='initiateSearch1',child='domainwordentryAutoComplete',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'fg=#551a8b;anchor=nw;',widthR='130',heightR='100',marginYR='80')
        self.Synx.getChild('linkTextenter0').bind('<Key>',lambda event:self.autoComplete('linkTextenter0','domainwordentryAutoComplete0','searchLinks'))
        self.Synx.getChild('domainwordentry3').bind('<Button- 1>',lambda event:self.initializeNewSearch('keywordentryText0',self.homeLinkInpArr))
        self.Synx.getChild('domainwordentry1').bind('<Button- 1>',lambda event:self.switchSearchType())
        self.Synx.getChild('keywordentry1').bind('<Button- 1>',lambda event:self.doGoogleSearch())

    def addAllDomains(self,new):
        domainAllList = {}
        weedOut = []
        with open(configPath+'/access/domains.txt','r') as domains:
            domainAllList = {}
            domains = domains.read().split('<--DOSIEcatEnd-->\n\n')[0:-1]
            for i in range(len(domains)):
                diff = domains[i].split('<--DOSIEcat-->\n')
                category = diff[0]
                dm = diff[1].split('\n\n<--DOSIEy-->\n\n')[0:-1]
                domainAllList[category] = []
                for j in range(len(dm)):
                    domainAllList[category].append(dm[j].split('<--DOSIEx-->'))
        for i in range(len(new)):
            if new[i][0]:
                new[i][0] = new[i][0].replace(' ','_')
                try:
                    domainAllList[new[i][0]]
                except:
                    domainAllList[new[i][0]] = []
                domainAllList[new[i][0]].append(new[i][1].split('<--DOSIEx-->'))
            else:
                weedOut.append(new[i])
        with open(configPath+'/access/domains.txt','w+') as domains:
            domain = domainAllList
            txt = ''
            for key in domain:
                dm = domain[key]
                txt += key +'<--DOSIEcat-->\n'
                for i in range(len(dm)):
                    txt += dm[i][0] + '<--DOSIEx-->' + dm[i][1] + '<--DOSIEx-->' + dm[i][2] + '\n\n<--DOSIEy-->\n\n'
                txt += '<--DOSIEcatEnd-->\n\n'
            domains.write(txt)
        self.selectedDomainsAdding = weedOut
        self.reviseDomains()
        self.closeMenuFrames()

    def updateFromAppToDomainFile(self):
        with open(configPath+'/access/domains.txt','w+') as domains:
            domain = self.domainAllList
            txt = ''
            for key in domain:
                dm = domain[key]
                txt += key +'<--DOSIEcat-->\n'
                for i in range(len(dm)):
                    txt += dm[i][0] + '<--DOSIEx-->' + dm[i][1] + '<--DOSIEx-->' + dm[i][2] + '\n\n<--DOSIEy-->\n\n'
                txt += '<--DOSIEcatEnd-->\n\n'
            domains.write(txt)

    def addSelectedDomain(self,comand,idx,index):
        if comand == 'add':
            text = self.Synx.getChild('chooseDomainToAddText'+str(idx)+'0').get('1.0',END).replace('\n','')
            self.selectedDomainsAdding[index][0] = text
            self.Synx.getChild('chooseDomainToAddLab'+str(idx)+'3').configure(text='Remove',fg='#00ffff')
            self.Synx.getChild('chooseDomainToAddLab'+str(idx)+'3').bind('<Button- 1>',lambda event:self.addSelectedDomain('remove',idx,index))
        else:
            self.selectedDomainsAdding[index][0] = None
            self.Synx.getChild('chooseDomainToAddLab'+str(idx)+'3').configure(text='Add',fg='#ffffff')
            self.Synx.getChild('chooseDomainToAddLab'+str(idx)+'3').bind('<Button- 1>',lambda event:self.addSelectedDomain('add',idx,index))

    def chooseDomainToAddLIST(self,rge):
        frameIndx = 1
        done = False
        isat = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i
                if self.selectedDomainsAdding[i - 1][0]:
                    self.Synx.affect(child='chooseDomainToAddLab'+str(frameIndx),point=[0,1,3],pointSet=[{'rounded':self.selectedDomainsAdding[i - 1][1].split('<--DOSIEx-->')[1]},{'style':'text='+self.selectedDomainsAdding[i - 1][1].split('<--DOSIEx-->')[0]+';'},{'style':'text=Remove;fg=#00ffff;bg=#0000cd;'}])
                    self.Synx.getChild('chooseDomainToAddLab'+str(frameIndx)+'3').bind('<Button- 1>',lambda event,comand='remove',idx=frameIndx,index=i - 1:self.addSelectedDomain(comand,idx,index))
                    self.Synx.getChild('chooseDomainToAddText'+str(frameIndx)+'0').delete('1.0',END)
                    self.Synx.getChild('chooseDomainToAddText'+str(frameIndx)+'0').insert('1.0',self.selectedDomainsAdding[i - 1][0])
                else:
                    self.Synx.affect(child='chooseDomainToAddLab'+str(frameIndx),point=[0,1,3],pointSet=[{'rounded':self.selectedDomainsAdding[i - 1][1].split('<--DOSIEx-->')[1]},{'style':'text='+self.selectedDomainsAdding[i - 1][1].split('<--DOSIEx-->')[0]+';'},{'style':'text=Add;fg=#ffffff;bg=#0000cd;'}])
                    self.Synx.getChild('chooseDomainToAddLab'+str(frameIndx)+'3').bind('<Button- 1>',lambda event,comand='add',idx=frameIndx,index=i - 1:self.addSelectedDomain(comand,idx,index))
                    self.Synx.getChild('chooseDomainToAddText'+str(frameIndx)+'0').delete('1.0',END)
                    self.Synx.getChild('chooseDomainToAddText'+str(frameIndx)+'0').insert('1.0','Category...')
                self.Synx.affect(child='chooseDomainToAddText'+str(frameIndx),point=[0],pointSet=[{'style':'state=normal;'}])
                self.Synx.getChild('chooseDomainToAddText'+str(frameIndx)+'0').bind('<Key>',lambda event,widget='chooseDomainToAddText'+str(frameIndx)+'0',enter='chooseDomainToAddTextAuto'+str(frameIndx)+'0',mapp='addDomain':self.autoComplete(widget,enter,mapp))
                if i >= len(self.selectedDomainsAdding):
                    done = True
            else:
                self.Synx.affect(child='chooseDomainToAddLab'+str(frameIndx),point=[0,1,3],pointSet=[{'rounded':style('default5')},{'style':'text=;'},{'style':'text=;fg=#ffffff;bg=#ffffff;'}])
                self.Synx.affect(child='chooseDomainToAddText'+str(frameIndx),point=[0],pointSet=[{'style':'state=disabled;'}])
                self.Synx.getChild('chooseDomainToAddText'+str(frameIndx)+'0').delete('1.0',END)
                self.Synx.getChild('chooseDomainToAddLab'+str(frameIndx)+'3').bind('<Button- 1>',lambda event:self.backHold())
            frameIndx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.chooseDomainToAddLIST([i + 1,i + 10]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 2:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.self.chooseDomainToAddLIST([rge[0] - 9,rge[1] - 9]))
        self.Synx.getChild('addDTags2').configure(text=str(isat)+'/'+str(len(self.selectedDomainsAdding)))

    def chooseDomainToAdd(self):
        self.Synx.layout(parent='menuFrames0',child='chooseDomainToAdd',widget=tk.LabelFrame,sectionN=10,rowN=1,style=style('Wbg'),widthR='100',heightR='5:8:8:8:8:8:8:8:8:8',marginYR='0:8:2:2:2:2:2:2:2:2')
        self.renameTopLab('Add Domain')
        self.Synx.layout(parent='chooseDomainToAdd0',child='addDTags',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'text=play;anchor=w;',marginXR='50:1')
        self.Synx.affect(child='addDTags',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())
        self.Synx.getChild('Ctrlbutt1').configure(text='Save')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.addAllDomains(self.selectedDomainsAdding))
        self.selectedDomainsAdding = []
        with open(configPath+'/access/newDomains.txt','r') as domains:
            found = domains.read()
            found = found.split('<--DOSIExN-->\n\n')[0:-1]
            for i in range(len(found)):
                foundD = found[i].split('<--DOSIExM-->')
                if foundD[0] == 'None':
                    self.selectedDomainsAdding.append([None,foundD[1]])
                else:
                    self.selectedDomainsAdding.append([foundD[0],foundD[1]])
        for i in range(1,10):
            self.Synx.layout(parent='chooseDomainToAdd'+str(i),child='chooseDomainToAddLab'+str(i),widget=tk.Label,sectionN=4,rowN=4,style=style('Wbg'),rounded=style('default5'),widthR='5:50:30:10',heightR='100:100:100:50',marginYR='0:0:0:30')
            self.Synx.affect(child='chooseDomainToAddLab'+str(i),point=[1,2,3],pointSet=[{'style':'image=;text=;width=70;height=2;anchor=w;fg=#0000cd;'},{'rounded':style('default5')},{'style':'image=;text=;width=10;height=1;fg=#ffffff;bg=#ffffff;'}])
            self.Synx.layout(parent='chooseDomainToAddLab'+str(i)+'2',child='chooseDomainToAddText'+str(i),widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style()+'fg=#0000cd;',widthR='100',heightR='70')
            self.Synx.layout(parent='chooseDomainToAddLab'+str(i)+'2',child='chooseDomainToAddTextAuto'+str(i),widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style()+'fg=#8b6969;anchor=w;',widthR='180',heightR='5',marginYR='70')
        if len(self.selectedDomainsAdding) > 0:
            self.chooseDomainToAddLIST([1,10])

    def downloadFoundFile(self,name,ext,URL):
        self.menuFrames(19)
        homeDir = os.path.expanduser("~")
        directory = homeDir+'\\Documents\\DosieDownloaded\\'
        local_filename = directory + name.strip().replace(' ','_') + ext
        size = 0
        REcall = False
        try:
            response = urlopen(URL)
            CHUNK = 2 * 1024
            with open(local_filename, 'wb') as f:
                while True:
                    size += CHUNK
                    progR = round((size / 109489) * 100)
                    if progR > 100:
                        progR = 100
                    self.downloadsAvail = [ext[1:],'',name,str(progR)+'%','106 KB',progR,ext.upper()]
                    self.Synx.getChild('downloadSpaceInfoListBar0').configure(width=self.Synx.child_dimensions(self.Synx.getChild('downloadSpaceInfo0'),'w',self.downloadsAvail[5]))
                    self.Synx.getChild('downloadSpaceInfoListBar0').update()
                    self.Synx.getChild('downloadSpaceInfoList1').configure(text=self.downloadsAvail[3])
                    self.Synx.getChild('downloadSpaceInfoList1').update()
                    if not REcall:
                        self.menuFrames(19)
                        REcall = True
                    chunk = response.read(CHUNK)
                    if not chunk:
                        break
                    f.write(chunk)
            self.downloadsAvail[3] = 'COMPLETE'
            self.menuFrames(19)
            return local_filename
        except:
            self.downloadsAvail[3] = 'FAILED'
            self.menuFrames(19)
            return None

    def discoveredMediaFilesLIST(self,rge):
        frameIndx = 1
        done = False
        isat = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i
                self.Synx.affect(child='discoveredMediaFilesLab'+str(frameIndx),point=[0,1,2,3,4],pointSet=[{'style':'text='+self.selectedFilesFound[i - 1][0]+';'},{'style':'text='+self.selectedFilesFound[i - 1][1]+';'},{'style':'text='+self.selectedFilesFound[i - 1][2][0:45]+'...;'},{'style':'text=Visit;fg=#ffffff;bg=#0000cd;'},{'style':'text=Download;fg=#ffffff;bg=#0000cd;'}])
                self.Synx.getChild('discoveredMediaFilesLab'+str(frameIndx)+'3').bind('<Button- 1>',lambda event,URL=self.selectedFilesFound[i - 1][2]:self.viewInBrowser(URL))
                self.Synx.getChild('discoveredMediaFilesLab'+str(frameIndx)+'4').bind('<Button- 1>',lambda event,name=self.selectedFilesFound[i - 1][0],ext=self.selectedFilesFound[i - 1][1],URL=self.selectedFilesFound[i - 1][2]:self.downloadFoundFile(name,ext,URL))
                if i >= len(self.selectedFilesFound):
                    done = True
            else:
                self.Synx.affect(child='discoveredMediaFilesLab'+str(frameIndx),point=[0,1,2,3,4],pointSet=[{'style':'text=;'},{'style':'text=;'},{'style':'text=;'},{'style':'text=;fg=#ffffff;bg=#ffffff;'},{'style':'text=;fg=#ffffff;bg=#ffffff;'}])
                self.Synx.getChild('discoveredMediaFilesLab'+str(frameIndx)+'3').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild('discoveredMediaFilesLab'+str(frameIndx)+'4').bind('<Button- 1>',lambda event:self.backHold())
            frameIndx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.discoveredMediaFilesLIST([i + 1,i + 10]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 2:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.discoveredMediaFilesLIST([rge[0] - 9,rge[1] - 9]))
        self.Synx.getChild('discoFTags2').configure(text=str(isat)+'/'+str(len(self.selectedFilesFound)))

    def discoveredMediaFiles(self):
        self.Synx.layout(parent='menuFrames0',child='discoveredMediaFiles',widget=tk.LabelFrame,sectionN=10,rowN=1,style=style('Wbg'),widthR='100',heightR='5:8:8:8:8:8:8:8:8:8',marginYR='0:8:2:2:2:2:2:2:2:2')
        self.renameTopLab('Found Files')
        self.Synx.layout(parent='discoveredMediaFiles0',child='discoFTags',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'text=play;anchor=w;',marginXR='50:1')
        self.Synx.affect(child='discoFTags',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        for i in range(1,10):
            self.Synx.layout(parent='discoveredMediaFiles'+str(i),child='discoveredMediaFilesLab'+str(i),widget=tk.Label,sectionN=5,rowN=5,style=style('Wbg'),rounded=style('default5'),widthR='25:10:35:10:10',marginXR='1:4:6:1')
            self.Synx.affect(child='discoveredMediaFilesLab'+str(i),point=[0,1,2,3,4],pointSet=[{'style':'image=;text=;fg=#551a8b;anchor=w;width=25;height=2;'},{'style':'image=;text=;fg=#0000cd;width=13;height=2;'},{'style':'image=;text=;fg=#551a8b;anchor=w;width=40;height=2;'},{'style':'image=;text=;fg=#ffffff;bg=#ffffff;width=8;height=2;'},{'style':'image=;text=;fg=#ffffff;bg=#ffffff;width=8;height=2;'}])
        if len(self.selectedFilesFound) < 1:
            return
        self.discoveredMediaFilesLIST([1,10])

    def shiftPin(self,event,parent,point,config):
        x = event.x
        y = event.y
        per = round((x / self.Synx.child_dimensions(self.Synx.getChild(parent),'w',100)) * 100)
        self.Synx.getChild(point).grid(padx=(x,0))
        self.Synx.getChild(config).configure(text=str(per)+'%')
        if parent == 'relevanceFullBar0':
            with open(configPath+'/config/SS_Relevance.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(per))
        elif parent == 'SearchCompleteLimsRelBarR0':
            with open(configPath+'/config/SS_CL_Relevance.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(per))
        elif parent == 'IndivDomainLimsRelBarR0':
            with open(configPath+'/config/SS_DL_Relevance.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(per))

    def checkForBlue(self,text,parent,config):
        try:
            text = int(text[:-1])
        except:
            self.Synx.getChild(parent).configure(fg='#ff0000')
            return
        if text > 100 or text < 1:
            self.Synx.getChild(parent).configure(fg='#ff0000')
            return
        self.Synx.getChild(parent).configure(fg='#0000cd')
        self.Synx.getChild(config).configure(text=str(text))
        if parent == 'SearchCompleteLimsDomBarR0':
            with open(configPath+'/config/SS_CL_DomainLim.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(text))
        if parent == 'IndivDomainLimsLimsDomBarR0':
            with open(configPath+'/config/SS_DL_DomainLim.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(text))
        if parent == 'IndivDomainLimsLimsinfoTDomBarR0':
            with open(configPath+'/config/SS_DL_ITL.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(text))

    def setConfigTxT(self,event,parent,config):
        text = self.Synx.getChild(parent).get('1.0',END).replace('\n','')
        if event.char.isprintable() == False:
            self.checkForBlue(text,parent,config)
            return
        else:
            try:
                text = int(text+event.char)
            except:
                messagebox.showerror("Set Limit", "Please make sure you type in a number")
                self.Synx.getChild(parent).configure(fg='#ff0000')
                return
            if text > 100 or text < 1:
                messagebox.showerror("Set Limit", "Please make sure your number is from 1 - 100")
                self.Synx.getChild(parent).configure(fg='#ff0000')
                return
        self.Synx.getChild(parent).configure(fg='#0000cd')
        self.Synx.getChild(config).configure(text=str(text))
        if parent == 'SearchCompleteLimsDomBarR0':
            with open(configPath+'/config/SS_CL_DomainLim.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(text))
        if parent == 'IndivDomainLimsLimsDomBarR0':
            with open(configPath+'/config/SS_DL_DomainLim.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(text))
        if parent == 'IndivDomainLimsLimsinfoTDomBarR0':
            with open(configPath+'/config/SS_DL_ITL.txt','w+') as SS_Relevance:
                SS_Relevance.write(str(text))

    def saveNewKeywords(self,imp=None,pointT=None):
        Kws = ['KwywordListText0','KwywordListText1','KwywordListTextB0','KwywordListTextB1']
        Lks = []

        LkResult = []
        KWResult = []

        verifyK = False
        verifyL = False
        for i in range(5,13):
            tag = 'LinkListTextB'+str(i)+'0'
            Lks.append(tag)
            Lnn = self.Synx.getChild(tag).get('1.0',END).replace('\n','').strip()
            if not verifyL:
                if len(Lnn) > 0 and Lnn[0:-4] != 'URL ':
                    verifyL = True
            if Lnn[0:-4] != 'URL ':
                LkResult.append(Lnn)
            if i < 9:
                kww = self.Synx.getChild(Kws[i - 5]).get('1.0',END).replace('\n','').strip()
                if not verifyK:
                    if len(kww) > 0 and kww[0:-4] != 'Keyword ':
                        verifyK = True
                if kww[0:-4] != 'Keyword ':
                    KWResult.append(kww)
        if not verifyK:
            messagebox.showerror("Keywords", "Please make sure you add at least one keyword")
            return
        if not verifyL:
            messagebox.showerror("Keywords", "Please make sure you add at least one URL")
            return
        LkResult = list(filter(None, LkResult))
        KWResult = list(filter(None, KWResult))

        fullListL = []
        fullListIC = []
        for i in LkResult:
            newURL = i
            if 'https://' not in newURL and 'http://' not in newURL:
                newURL = 'http://'+newURL
            domainName = newURL[newURL.find('//') + 2:].replace('www.','')
            if domainName.find('/') > -1:
                domainName = domainName[0:domainName.find('/')]
            DNfound = False
            IMpath = 'path='+configPath+'/img/domainICO/Icon.png;circular=True;'
            for keyy in self.domainAllList:
                for i in self.domainAllList[keyy]:
                    if i[0] == domainName:
                        IMpath = i[1]
                        DNfound = True
                        break
                if DNfound:
                    break
            fullListL.append(newURL)
            fullListIC.append(IMpath)
        for i in range(len(fullListIC),8):
            fullListIC.append(style('default5')+'circular=True;')
        for i in range(len(KWResult),4):
            KWResult.append('')

        final = [KWResult,fullListIC,fullListL]
        if pointT:
            self.AllSearchKeywords[imp] = final
            self.keywordUpdateFromApp()
            self.reviseKeywords()
            self.restoreFlipThrougnmenuKeywords(pointT)
            return
        else:
            with open(configPath+'/access/keywords.txt','a+') as keywords:
                keywords.write('<--DOSIEx-->'.join(final[0])+'<--DOSIEy-->'+'<--DOSIEx-->'.join(final[1])+'<--DOSIEy-->'+'<--DOSIEx-->'.join(final[2])+'\n<--DOSIEend-->\n')
            self.reviseKeywords()
        for i in range(5,13):
            Lnn = self.Synx.getChild(Lks[i - 5])
            Lnn.delete('1.0',END)
            Lnn.insert(INSERT,'URL '+str(i - 4)+'...')
            if i < 9:
                kww = self.Synx.getChild(Kws[i - 5])
                kww.delete('1.0',END)
                kww.insert(INSERT,'Keyword '+str(i - 4)+'...')

    def KeyworDSettings(self,imp=False,point=False):
        if point:
            self.closeMenuFrames()
            self.menuFrames('re')
        self.Synx.layout(parent='menuFrames0',child='KeyworDSettings',widget=tk.LabelFrame,sectionN=13,rowN=1,style=style('Wbg'),widthR='100',heightR='5:6:6:6:6:6:6:6:6:6:6:6:6',marginYR='0:2:2:2:2:2:2:2:2:2:2:2:2')
        self.renameTopLab('Keyword Settings')
        self.Synx.layout(parent='KeyworDSettings0',child='keywFTags',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'text=play;anchor=w;',marginXR='50:1')
        self.Synx.affect(child='keywFTags',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.Synx.affect(child='KeyworDSettings',point=[1],pointSet=[{'style':'text=Keyword List;font=Helvetica 11 bold;'}])
        self.Synx.layout(parent='KeyworDSettings2',child='KwywordListText',widget=tk.Text,resolveWH=True,sectionN=2,rowN=2,style=style('Wbg')+'fg=#0000cd;',widthR='78:78',heightR='100:100')
        self.Synx.getChild('KwywordListText1').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('KeyworDSettings1'),'w',52),0))
        self.Synx.layout(parent='KeyworDSettings3',child='KwywordListTextB',widget=tk.Text,resolveWH=True,sectionN=2,rowN=2,style=style('Wbg')+'fg=#0000cd;',widthR='78:78',heightR='100:100')
        self.Synx.getChild('KwywordListTextB1').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('KeyworDSettings1'),'w',52),0))
        if point:
            if point[0] == 'view':
                self.Synx.getChild('KwywordListText0').insert(INSERT,self.AllSearchKeywords[imp][0][0])
                self.Synx.getChild('KwywordListText1').insert(INSERT,self.AllSearchKeywords[imp][0][1])
                self.Synx.getChild('KwywordListTextB0').insert(INSERT,self.AllSearchKeywords[imp][0][2])
                self.Synx.getChild('KwywordListTextB1').insert(INSERT,self.AllSearchKeywords[imp][0][3])
                self.Synx.getChild('KwywordListText0').configure(state='disabled')
                self.Synx.getChild('KwywordListText1').configure(state='disabled')
                self.Synx.getChild('KwywordListTextB0').configure(state='disabled')
                self.Synx.getChild('KwywordListTextB1').configure(state='disabled')
            elif point[0] == 'edit':
                fgm = 0
                for i in range(len(self.AllSearchKeywords[imp][0])):
                    ddx = ''
                    if i == 2:
                        fgm = 0
                        ddx = 'B'
                    if i == 3:
                        fgm = 1
                        ddx = 'B'
                    if self.AllSearchKeywords[imp][0][i]:
                        self.Synx.getChild('KwywordListText'+ddx+str(fgm)).insert(INSERT,self.AllSearchKeywords[imp][0][i])
                    else:
                        self.Synx.getChild('KwywordListText'+ddx+str(fgm)).insert(INSERT,'Keyword '+str(i)+'...')
                    fgm += 1
        else:
            self.Synx.getChild('KwywordListText0').insert(INSERT,'Keyword 1...')
            self.Synx.getChild('KwywordListText1').insert(INSERT,'Keyword 2...')
            self.Synx.getChild('KwywordListTextB0').insert(INSERT,'Keyword 3...')
            self.Synx.getChild('KwywordListTextB1').insert(INSERT,'Keyword 4...')
        self.Synx.affect(child='KeyworDSettings',point=[4],pointSet=[{'style':'text=URL List;font=Helvetica 11 bold;labelanchor=sw;'}])
        for i in range(5,13):
            self.Synx.layout(parent='KeyworDSettings'+str(i),child='LinkListTextB'+str(i),widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'fg=#0000cd;',widthR='160',heightR='45')
            self.Synx.layout(parent='KeyworDSettings'+str(i),child='LinkListTextBauto'+str(i),widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='97',heightR='40',marginYR='50')
            self.Synx.getChild('LinkListTextB'+str(i)+'0').bind('<Key>',lambda event,widget='LinkListTextB'+str(i)+'0',enter='LinkListTextBauto'+str(i)+'0',mapp='searchLinks':self.autoComplete(widget=widget,enter=enter,mapp=mapp))
            if point:
                if i - 5 < len(self.AllSearchKeywords[imp][2]):
                    if point[0] == 'view':
                        self.Synx.getChild('LinkListTextB'+str(i)+'0').insert(INSERT,self.AllSearchKeywords[imp][2][i - 5])
                        self.Synx.getChild('LinkListTextB'+str(i)+'0').configure(state='disabled')
                    elif point[0] == 'edit':
                        self.Synx.getChild('LinkListTextB'+str(i)+'0').insert(INSERT,self.AllSearchKeywords[imp][2][i - 5])
                else:
                    if point[0] == 'edit':
                        self.Synx.getChild('LinkListTextB'+str(i)+'0').insert(INSERT,'URL '+str(i - 4)+'...')
                    elif point[0] == 'view':
                        self.Synx.getChild('LinkListTextB'+str(i)+'0').configure(state='disabled')
            else:
                self.Synx.getChild('LinkListTextB'+str(i)+'0').insert(INSERT,'URL '+str(i - 4)+'...')
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('Ctrlbutt2').configure(text='')
        self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        if point:
            if point[0] == 'view' or point[0] == 'edit':
                if point[0] == 'edit':
                    self.Synx.getChild('Ctrlbutt3').configure(text='Save')
                    self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.saveNewKeywords(imp=imp,pointT=point[1]))
                else:
                    self.Synx.getChild('Ctrlbutt3').configure(text='')
                    self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
                self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.restoreFlipThrougnmenuKeywords(point[1]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Save')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.saveNewKeywords())

    def renameDOmainCat(self,do,name,key,config,button):
        if do == 'rename':
            newName = self.Synx.getChild(name).get('1.0',END).replace('\n','').strip()
            if len(newName) > 0:
                newName = newName.replace(' ','_')
                self.domainAllList[newName] = self.domainAllList.pop(key)
                self.updateFromAppToDomainFile()
                self.reviseDomains()
                self.Synx.getChild(config).configure(text=newName.replace('_',' '))
                self.Synx.getChild(name).delete('1.0',END)
                self.Synx.getChild(name).insert(INSERT,'New Name...')
                self.Synx.getChild(button).bind('<Button- 1>',lambda event,do=do,name=name,key=newName,config=config,button=button:self.renameDOmainCat(do,name,key,config,button))
            else:
                messagebox.showerror("Rename Domain Category", "Please make sure you type in a name")
        elif do == 'delete':
            var = tk.messagebox.askyesnocancel ('Delete Category','Are you sure? All items in it will be deleted as well.')
            if var:
                self.domainAllList.pop(key)
                self.updateFromAppToDomainFile()
                self.reviseDomains()
                self.Synx.getChild(config).configure(text='')
                self.Synx.getChild(name).delete('1.0',END)
                self.Synx.getChild(name).configure(state='disabled')
                self.Synx.getChild(config[0:-1]+'1').configure(text='')
                self.Synx.getChild(button).configure(text='',bg='#ffffff')
                self.Synx.getChild(button).bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild(button[0:-1]+'4').configure(text='',bg='#ffffff')
                self.Synx.getChild(button[0:-1]+'4').bind('<Button- 1>',lambda event:self.backHold())
            else:
                pass
        elif do == 'saveNew':
            newURL = self.Synx.getChild(name).get('1.0',END).replace('\n','').strip()
            keyN = self.Synx.getChild(key).get('1.0',END).replace('\n','').strip()
            if len(newURL) > 0 and newURL.find(' ') < 0:
                if len(keyN) < 1:
                    messagebox.showerror("Add Link To Category", "Please type in a category name")
                else:
                    try:
                        category = self.domainAllList[keyN.replace(' ','_')]
                        NNew = 'exist'
                    except:
                        NNew = tk.messagebox.askyesnocancel("Add Link To Category", "Category doesnt exist! A new category will be created. Continue?")
                    if NNew == 'exist':
                        if 'https://' not in newURL and 'http://' not in newURL:
                            newURL = 'http://'+newURL
                        domainName = newURL[newURL.find('//') + 2:].replace('www.','')
                        if domainName.find('/') > -1:
                            domainName = domainName[0:domainName.find('/')]
                        DNfound = False
                        IMpath = 'path='+configPath+'/img/domainICO/Icon.png;circular=True;'
                        for keyy in self.domainAllList:
                            for i in self.domainAllList[keyy]:
                                if i[0] == domainName:
                                    IMpath = i[1]
                                    DNfound = True
                                    break
                            if DNfound:
                                break
                        self.domainAllList[keyN.replace(' ','_')].append([domainName,IMpath,newURL])
                        self.updateFromAppToDomainFile()
                        self.reviseDomains()
                        self.Synx.getChild(name).delete('1.0',END)
                        self.Synx.getChild(key).delete('1.0',END)
                        self.Synx.getChild(name).insert(INSERT,'Type URL...')
                        self.Synx.getChild(key).insert(INSERT,'Type Category...')
                    elif NNew:
                        if 'https://' not in newURL and 'http://' not in newURL:
                            newURL = 'http://'+newURL
                        domainName = newURL[newURL.find('//') + 2:].replace('www.','')
                        if domainName.find('/') > -1:
                            domainName = domainName[0:domainName.find('/')]
                        DNfound = False
                        IMpath = 'path='+configPath+'/img/domainICO/Icon.png;circular=True;'
                        for keyy in self.domainAllList:
                            for i in self.domainAllList[keyy]:
                                if i[0] == domainName:
                                    IMpath = i[1]
                                    DNfound = True
                                    break
                            if DNfound:
                                break
                        self.domainAllList[keyN.replace(' ','_')] = []
                        self.domainAllList[keyN.replace(' ','_')].append([domainName,IMpath,newURL])
                        self.updateFromAppToDomainFile()
                        self.reviseDomains()
                        self.Synx.getChild(name).delete('1.0',END)
                        self.Synx.getChild(key).delete('1.0',END)
                        self.Synx.getChild(name).insert(INSERT,'Type URL...')
                        self.Synx.getChild(key).insert(INSERT,'Type Category...')
                    else:
                        pass
            else:
                messagebox.showerror("Add Link To Category", "Please make sure you type in a valid URL")

    def categorySettingsFlip(self,rge):
        frameIndx = 3
        done = False
        isat = 0
        for i in range(rge[0],rge[1]):
            if not done:
                isat = i - 2
                self.Synx.affect(child='categorySettingsLine'+str(frameIndx),point=[0,1,3,4],pointSet=[{'style':'text='+self.MarkCategory[i - 3].replace('_',' ')+';'},{'style':'text=Items\n('+str(len(self.domainAllList[self.MarkCategory[i - 3]]))+');'},{'style':'text=Rename\n;bg=#0000cd;fg=#ffffff;'},{'style':'text=Delete\n;bg=#0000cd;fg=#ffffff;'}])
                self.Synx.getChild('categorySettingsLineText'+str(frameIndx)+'0').configure(state='normal')
                self.Synx.getChild('categorySettingsLineText'+str(frameIndx)+'0').delete('1.0',END)
                self.Synx.getChild('categorySettingsLineText'+str(frameIndx)+'0').insert(INSERT,'New Name...')
                self.Synx.getChild('categorySettingsLine'+str(frameIndx)+'3').bind('<Button- 1>',lambda event,do='rename',name='categorySettingsLineText'+str(frameIndx)+'0',key=self.MarkCategory[i - 3],config='categorySettingsLine'+str(frameIndx)+'0',button='categorySettingsLine'+str(frameIndx)+'3':self.renameDOmainCat(do,name,key,config,button))
                self.Synx.getChild('categorySettingsLine'+str(frameIndx)+'4').bind('<Button- 1>',lambda event,do='delete',name='categorySettingsLineText'+str(frameIndx)+'0',key=self.MarkCategory[i - 3],config='categorySettingsLine'+str(frameIndx)+'0',button='categorySettingsLine'+str(frameIndx)+'3':self.renameDOmainCat(do,name,key,config,button))
                if i - 2 >= len(self.MarkCategory):
                    done = True
            else:
                self.Synx.affect(child='categorySettingsLine'+str(frameIndx),point=[0,1,3,4],pointSet=[{'style':'text=;'},{'style':'text=;'},{'style':'text=;bg=#ffffff;fg=#ffffff;'},{'style':'text=;bg=#ffffff;fg=#ffffff;'}])
                self.Synx.getChild('categorySettingsLineText'+str(frameIndx)+'0').delete('1.0',END)
                self.Synx.getChild('categorySettingsLineText'+str(frameIndx)+'0').configure(state='disabled')
                self.Synx.getChild('categorySettingsLine'+str(frameIndx)+'3').bind('<Button- 1>',lambda event:self.backHold())
                self.Synx.getChild('categorySettingsLine'+str(frameIndx)+'4').bind('<Button- 1>',lambda event:self.backHold())
            frameIndx += 1
        if not done:
            self.Synx.getChild('Ctrlbutt3').configure(text='Next')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.categorySettingsFlip([i + 1,i + 9]))
        else:
            self.Synx.getChild('Ctrlbutt3').configure(text='Done')
            self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())
        if rge[0] < 4:
            self.Synx.getChild('Ctrlbutt2').configure(text='')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        else:
            self.Synx.getChild('Ctrlbutt2').configure(text='Previous')
            self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.categorySettingsFlip([rge[0] - 8,rge[1] - 8]))
        self.Synx.getChild('cateSettFTags2').configure(text=str(isat)+'/'+str(len(self.MarkCategory)))

    def categorySettings(self):
        self.Synx.layout(parent='menuFrames0',child='categorySettings',widget=tk.LabelFrame,sectionN=11,rowN=1,style=style('Wbg'),widthR='100',heightR='5:8:5:8:8:8:8:8:8:8:8',marginYR='0:2:1:5:2:2:2:2:2:2:2')
        self.renameTopLab('Category Settings')
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.layout(parent='categorySettings0',child='cateSettFTags',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg')+'text=play;anchor=w;',marginXR='50:1')
        self.Synx.affect(child='cateSettFTags',point=[0,1,2],pointSet=[{'style':'width=50;height=1;text=;fg=#7d7d7d;'},{'style':'width=13;height=1;text=Count;fg=#7d7d7d;'},{'style':'width=16;height=1;text=0/0;fg=#0000cd;'}])
        self.Synx.layout(parent='categorySettings1',child='categorySettingsLink',widget=tk.Text,resolveWH=True,sectionN=2,rowN=2,style=style('Wbg')+'fg=#0000cd;',widthR='110:48',heightR='100:100')
        self.Synx.getChild('categorySettingsLink1').grid(padx=(self.Synx.child_dimensions(self.Synx.getChild('categorySettings1'),'w',70),0))
        self.Synx.layout(parent='categorySettings2',child='categorySettingsButton',widget=tk.Button,resolveWH=True,sectionN=2,rowN=2,style=style('Wbg'),widthR='1:27',marginXR='83',heightR='100:100')
        self.Synx.affect(child='categorySettingsButton',point=[1],pointSet=[{'style':'text=Save;bg=#0000cd;fg=#ffffff;'}])
        self.Synx.getChild('categorySettingsLink0').insert(INSERT,'Type URL...')
        self.Synx.getChild('categorySettingsLink1').insert(INSERT,'Type Category...')
        self.Synx.getChild('categorySettingsButton1').bind('<Button- 1>',lambda event,do='saveNew',name='categorySettingsLink0',key='categorySettingsLink1',config=None,button=None:self.renameDOmainCat(do,name,key,config,button))
        for i in range(3,11):
            self.Synx.layout(parent='categorySettings'+str(i),child='categorySettingsLine'+str(i),widget=tk.LabelFrame,sectionN=5,rowN=5,style=style('Wbg'),widthR='30:13:30:12:12',heightR='100:100:100:40:40',marginYR='0:0:0:30:30')
            self.Synx.affect(child='categorySettingsLine'+str(i),point=[0,1,3,4],pointSet=[{'style':'text=;'},{'style':'text=;labelanchor=n;'},{'style':'text=;labelanchor=n;bg=#ffffff;fg=#ffffff;'},{'style':'text=;labelanchor=n;bg=#ffffff;fg=#ffffff;'}])
            self.Synx.layout(parent='categorySettingsLine'+str(i)+'2',child='categorySettingsLineText'+str(i),widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'fg=#0000cd;state=disabled;',widthR='155',heightR='100')
        if len(self.MarkCategory) < 1:
            return
        self.categorySettingsFlip([3,11])


    def searchSettings(self):
        self.Synx.layout(parent='menuFrames0',child='searchSettings',widget=tk.LabelFrame,sectionN=10,rowN=1,style=style('Wbg'),widthR='100',heightR='8:8:8:8:8:8:8:8:8:8',marginYR='0:2:2:2:2:2:2:2:2:2')
        self.renameTopLab('Search Settings')
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('Ctrlbutt2').configure(text='')
        self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('Ctrlbutt3').configure(text='')
        self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())

        self.Synx.layout(parent='searchSettings0',child='RelevancePerLab',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'text=Minimum Relevance:;font=Helvetica 11 bold;anchor=w;',widthR='100',heightR='50',marginYR='35')
        self.Synx.layout(parent='searchSettings1',child='RelevancePerLabTabs',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='90:8')
        self.Synx.layout(parent='RelevancePerLabTabs0',child='relevanceFullBar',widget=tk.Label,sectionN=2,rowN=2,style=style(),rounded=style('default4'),widthR='97:2',heightR='15:30',marginYR='35:27')
        self.Synx.affect(child='RelevancePerLabTabs',point=[1],pointSet=[{'style':'text=0%;'}])
        self.Synx.affect(child='relevanceFullBar',point=[1],pointSet=[{'rounded':style('pin')}])
        self.Synx.getChild('relevanceFullBar0').bind('<Button- 1>',lambda event:self.shiftPin(event,'relevanceFullBar0','relevanceFullBar1','RelevancePerLabTabs1'))

        self.Synx.layout(parent='searchSettings2',child='SearchCompleteLims',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'text=Completion Limit:;font=Helvetica 11 bold;anchor=w;',widthR='100',heightR='50',marginYR='35')
        self.Synx.layout(parent='searchSettings3',child='SearchCompleteLimsRel',widget=tk.LabelFrame,sectionN=3,rowN=3,style=style('Wbg'),widthR='20:70:8')
        self.Synx.affect(child='SearchCompleteLimsRel',point=[0,2],pointSet=[{'style':'text=Minimum Relevance;'},{'style':'text=0%;'}])
        self.Synx.layout(parent='SearchCompleteLimsRel1',child='SearchCompleteLimsRelBarR',widget=tk.Label,sectionN=2,rowN=2,style=style(),rounded=style('default4'),widthR='97:2',heightR='15:30',marginYR='35:27')
        self.Synx.affect(child='SearchCompleteLimsRelBarR',point=[1],pointSet=[{'rounded':style('pin')}])
        self.Synx.getChild('SearchCompleteLimsRelBarR0').bind('<Button- 1>',lambda event:self.shiftPin(event,'SearchCompleteLimsRelBarR0','SearchCompleteLimsRelBarR1','SearchCompleteLimsRel2'))

        self.Synx.layout(parent='searchSettings4',child='SearchCompleteLimsDom',widget=tk.LabelFrame,sectionN=3,rowN=3,style=style('Wbg'),widthR='20:70:8')
        self.Synx.affect(child='SearchCompleteLimsDom',point=[0,2],pointSet=[{'style':'text=Domain Limit;'},{'style':'text=0;'}])
        self.Synx.layout(parent='SearchCompleteLimsDom1',child='SearchCompleteLimsDomBarR',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style()+'fg=#0000cd;',widthR='140',heightR='80',marginYR='17')
        self.Synx.getChild('SearchCompleteLimsDomBarR0').insert('1.0','1 - 100')
        self.Synx.getChild('SearchCompleteLimsDomBarR0').bind('<Key>',lambda event:self.setConfigTxT(event,'SearchCompleteLimsDomBarR0','SearchCompleteLimsDom2'))

        self.Synx.layout(parent='searchSettings6',child='IndivDomainLims',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'text=Domain Limits:;font=Helvetica 11 bold;anchor=w;',widthR='100',heightR='50',marginYR='35')
        self.Synx.layout(parent='searchSettings7',child='IndivDomainLimsLimsRel',widget=tk.LabelFrame,sectionN=3,rowN=3,style=style('Wbg'),widthR='20:70:8')
        self.Synx.affect(child='IndivDomainLimsLimsRel',point=[0,2],pointSet=[{'style':'text=Minimum Relevance;'},{'style':'text=0%;'}])
        self.Synx.layout(parent='IndivDomainLimsLimsRel1',child='IndivDomainLimsRelBarR',widget=tk.Label,sectionN=2,rowN=2,style=style(),rounded=style('default4'),widthR='97:2',heightR='15:30',marginYR='35:27')
        self.Synx.affect(child='IndivDomainLimsRelBarR',point=[1],pointSet=[{'rounded':style('pin')}])
        self.Synx.getChild('IndivDomainLimsRelBarR0').bind('<Button- 1>',lambda event:self.shiftPin(event,'IndivDomainLimsRelBarR0','IndivDomainLimsRelBarR1','IndivDomainLimsLimsRel2'))

        self.Synx.layout(parent='searchSettings8',child='IndivDomainLimsLimsDom',widget=tk.LabelFrame,sectionN=3,rowN=3,style=style('Wbg'),widthR='20:70:8')
        self.Synx.affect(child='IndivDomainLimsLimsDom',point=[0,2],pointSet=[{'style':'text=Domain Limit;'},{'style':'text=0;'}])
        self.Synx.layout(parent='IndivDomainLimsLimsDom1',child='IndivDomainLimsLimsDomBarR',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style()+'fg=#0000cd;',widthR='140',heightR='80',marginYR='17')
        self.Synx.getChild('IndivDomainLimsLimsDomBarR0').insert('1.0','1 - 100')
        self.Synx.getChild('IndivDomainLimsLimsDomBarR0').bind('<Key>',lambda event:self.setConfigTxT(event,'IndivDomainLimsLimsDomBarR0','IndivDomainLimsLimsDom2'))

        self.Synx.layout(parent='searchSettings9',child='IndivDomainLimsLimsinfoT',widget=tk.LabelFrame,sectionN=3,rowN=3,style=style('Wbg'),widthR='20:70:8')
        self.Synx.affect(child='IndivDomainLimsLimsinfoT',point=[0,2],pointSet=[{'style':'text=Info Tab Limit;'},{'style':'text=0;'}])
        self.Synx.layout(parent='IndivDomainLimsLimsinfoT1',child='IndivDomainLimsLimsinfoTDomBarR',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,style=style()+'fg=#0000cd;',widthR='140',heightR='80',marginYR='17')
        self.Synx.getChild('IndivDomainLimsLimsinfoTDomBarR0').insert('1.0','1 - 100')
        self.Synx.getChild('IndivDomainLimsLimsinfoTDomBarR0').bind('<Key>',lambda event:self.setConfigTxT(event,'IndivDomainLimsLimsinfoTDomBarR0','IndivDomainLimsLimsinfoT2'))
        with open(configPath+'/config/SS_Relevance.txt','r') as SS_Relevance:
            self.Synx.getChild('RelevancePerLabTabs1').configure(text=SS_Relevance.read()+'%')
        with open(configPath+'/config/SS_CL_Relevance.txt','r') as SS_Relevance:
            self.Synx.getChild('SearchCompleteLimsRel2').configure(text=SS_Relevance.read()+'%')
        with open(configPath+'/config/SS_CL_DomainLim.txt','r') as SS_Relevance:
            self.Synx.getChild('SearchCompleteLimsDom2').configure(text=SS_Relevance.read())
        with open(configPath+'/config/SS_DL_Relevance.txt','r') as SS_Relevance:
            self.Synx.getChild('IndivDomainLimsLimsRel2').configure(text=SS_Relevance.read()+'%')
        with open(configPath+'/config/SS_DL_DomainLim.txt','r') as SS_Relevance:
            self.Synx.getChild('IndivDomainLimsLimsDom2').configure(text=SS_Relevance.read())
        with open(configPath+'/config/SS_DL_ITL.txt','r') as SS_Relevance:
            self.Synx.getChild('IndivDomainLimsLimsinfoT2').configure(text=SS_Relevance.read())

    def downloadableFILES(self):
        with open(configPath+'/access/downloadableFiles.txt','r') as downloadableFiles:
            self.selectedFilesFound = []
            downloadableFiles = downloadableFiles.read().split('\n<--DOSIEy-->\n')[0:-1]
            for i in downloadableFiles:
                self.selectedFilesFound.append(i.split('<--DOSIEx-->'))

    def DownloadProgress(self):
        self.renameTopLab('Downloads')
        self.Synx.layout(parent='menuFrames0',child='downloadSpace',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Wbg'),widthR='48:48',heightR='40:40')
        self.Synx.layout(parent='downloadSpace0',child='downloadSpaceDP',widget=tk.Label,sectionN=1,rowN=1,style=style('Wbg'),rounded=style(self.downloadsAvail[0]),widthR='100',heightR='100')
        self.Synx.affect(child='downloadSpace',point=[1],pointSet=[{'style':'text=\n\n\n\n'+self.downloadsAvail[2]+';fg=#0000cd;labelanchor=n;font=Helvetica 11 bold;'}])
        self.Synx.layout(parent='menuFrames0',child='downloadSpaceInfo',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='48:48',marginYR='50')
        self.Synx.layout(parent='downloadSpaceInfo0',child='downloadSpaceInfoList',widget=tk.LabelFrame,sectionN=8,rowN=2,style=style('Wbg'),widthR='15:80',heightR='10:10:10:10:10:10:10:10',marginYR='0:0:3:3:7:7:2:2')
        self.Synx.affectGroup(group='column',child='downloadSpaceInfoList',rows=2,columns=4,point=[0,1],depth=4,styleX=[{'style':'text=Progress:;fg=#0000cd;'},{'style':'text=;fg=#0000cd;'},{'style':'text=File Format:;fg=#0000cd;'},{'style':'text=File Size:;fg=#0000cd;'},{'style':'text='+self.downloadsAvail[3]+';fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'},{'style':'text='+self.downloadsAvail[6]+';fg=#7d7d7d;'},{'style':'text='+self.downloadsAvail[4]+';fg=#7d7d7d;'}])
        self.Synx.layout(parent='downloadSpaceInfo0',child='downloadSpaceInfoListBar',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Bbg'),widthR='0',heightR='10',marginYR='12')
        self.Synx.getChild('downloadSpaceInfoListBar0').configure(width=self.Synx.child_dimensions(self.Synx.getChild('downloadSpaceInfo0'),'w',self.downloadsAvail[5]))
        
    def initializeNewSearch(self,text,source,kwkw=False,wtg=None):
        global SEARCH_TYPE
        self.fronBackBegin = True
        self.cleanUp(cache=True)
        self.DownloaDableFiles = 0
        self.Synx.getChild('StatusButtons'+str(1)).configure(text='Found Files ('+str(self.DownloaDableFiles)+')')
        self.connectOUT('FOCUS__',[])
        if kwkw:
            say = text
        else:
            say = self.Synx.getChild(text).get('1.0',END).replace('\n','').strip()
            if 'wikipedia.org' in source[0]:
                if source[0][-1:] == '/':
                    source[0] = source[0] + say.replace(' ','_')
                else:
                    source[0] = source[0] + '/' + say.replace(' ','_')
        if wtg:
            SEARCH_TYPE = wtg
        self.connectOUT(say,source)
        self.connectOUT('FOCUS_OUT__',[])
        self.closeMenuFrames()

    def endOptions(self):
        self.Synx.getChild('Ctrlbutt0').configure(text='')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('Ctrlbutt1').configure(text='')
        self.Synx.getChild('Ctrlbutt1').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('Ctrlbutt2').configure(text='')
        self.Synx.getChild('Ctrlbutt2').bind('<Button- 1>',lambda event:self.backHold())
        self.Synx.getChild('Ctrlbutt3').configure(text='')
        self.Synx.getChild('Ctrlbutt3').bind('<Button- 1>',lambda event:self.backHold())

    def closeMenuFrames(self):
        self.Synx.getChild('menuFrames0').destroy()
        self.Synx.delFromSynx('menuFrames0')
        self.renameTopLab('Home')
        self.endOptions()
        self.Synx.getChild('searchE0').delete('1.0',END)
        self.Synx.getChild('searchE0').insert(INSERT,'Search Something...')
        self.Synx.getChild('searchE0').bind('<Key>',lambda event:self.searchSomething(''))

    def menuFrames(self,index):
        try:
            mom = self.Synx.getChild('menuFrames0')
            for widget in mom.winfo_children():
                widget.destroy()
        except KeyError:
            self.Synx.layout(parent='activity2',child='menuFrames',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='100')
        lst = [0,3,6,9,12]
        for i in range(len(lst)):
            if lst[i] == index:
                self.Synx.getChild('navBut'+str(lst[i])).configure(bg='#0000cd')
            else:
                self.Synx.getChild('navBut'+str(lst[i])).configure(bg='#ffffff')
        if index == 0:
            self.menuDomains()
        elif index == 3:
            self.menuKeywords()
        elif index == 6:
            self.menuHistory()
        elif index == 9:
            self.menuMedia()
        elif index == 12:
            self.menuFolders()
        elif index == 13:
            self.homeSpace()
            self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
            self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())
            self.homeLinkInpArr = []
        elif index == 14:
            self.chooseDomainToAdd()
        elif index == 15:
            self.downloadableFILES()
            self.discoveredMediaFiles()
        elif index == 16:
            self.searchSettings()
        elif index == 17:
            self.categorySettings()
        elif index == 18:
            self.KeyworDSettings()
        elif index == 19:
            self.DownloadProgress()
        self.Synx.getChild('Ctrlbutt0').configure(text='CLOSE')
        self.Synx.getChild('Ctrlbutt0').bind('<Button- 1>',lambda event:self.closeMenuFrames())

    def showStatusTab(self,comand):
        if comand == 'show':
            self.Synx.getChild('operationStatus0').grid()
            self.Synx.getChild('tabText0').bind('<Button- 1>',lambda event:self.showStatusTab('remove'))
            self.Synx.getChild('tabTextB0').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('tabText0').configure(fg='#000000')
            self.Synx.getChild('tabTextB0').configure(fg='#0000ff')
        else:
            self.Synx.getChild('operationStatus0').grid_remove()
            self.Synx.getChild('tabText0').bind('<Button- 1>',lambda event:self.backHold())
            self.Synx.getChild('tabTextB0').bind('<Button- 1>',lambda event:self.showStatusTab('show'))
            self.Synx.getChild('tabText0').configure(fg='#0000ff')
            self.Synx.getChild('tabTextB0').configure(fg='#000000')

    def searchSomething(self,tag):
        if tag == 'SearchDomainCategory':
            arr = self.DomainListedCategories
            arrenter = self.DomainListedCategories
        elif tag == 'SearchKeywords':
            arr = self.KeywordsAuto
            arrenter = self.KeywordsAuto
        elif tag == 'SearchMedia':
            arr = self.ViewMediaListAuto
            arrenter = self.ViewMediaListAuto
        elif tag == 'SearchFolders':
            arr = self.SavedFoldersListName
            arrenter = self.SavedFoldersListName
        elif tag == '':
            return
        
        write = self.Synx.getChild('searchE0').get('1.0',END)
        for i in range(len(arr)):
            if (write[0:-1] + arr[i][len(write[0:-1]):]).lower() == arr[i].lower():
                self.Synx.getChild('searchEAut0').configure(text = write[0:-1] + arr[i][len(write[0:-1]):])
                self.Synx.getChild('searchEAut0').bind('<Button- 1>',lambda event, widget = 'searchE0', enter = 'searchEAut0', text = arrenter[arr.index(write[0:-1] + arr[i][len(write[0:-1]):])]:self.acceptAutoComplete(widget,enter,text))
                self.Synx.getChild('searchE0').bind('<Return>',lambda event:self.doTheSearching(tag,write[0:-1] + arr[i][len(write[0:-1]):]))
                self.Synx.getChild('searchEAut0').update()
                return
        self.Synx.getChild('searchEAut0').configure(text = '')
        self.Synx.getChild('searchEAut0').bind('<Button- 1>',lambda event, X='':self.backHold())
        self.Synx.getChild('searchE0').bind('<Return>',lambda event:self.doTheSearching(''))

    def doTheSearching(self,tag,point=None):
        self.Synx.getChild('searchE0').delete('1.0',END)
        if tag == 'SearchDomainCategory':
            self.Synx.getChild('searchE0').insert(INSERT,'Search Category...')
            self.renameTopLab('Category: '+point+'')
            self.Synx.affect(child='dFTags',point=[0],pointSet=[{'style':'text='+point+';'}])
            self.domainNav(point.replace(' ','_'),[1,6])
        elif tag == 'SearchKeywords':
            self.Synx.getChild('searchE0').insert(INSERT,'Search Keywords...')
            sm = self.KeywordsAutoIndex[self.KeywordsAuto.index(point)]
            self.flipThrougnmenuKeywords([sm + 1,sm + 6])
        elif tag == 'SearchMedia':
            self.Synx.getChild('searchE0').insert(INSERT,'Search Media...')
            self.listMenuMedia([self.ViewMediaListAuto.index(point),self.ViewMediaListAuto.index(point) + 9])
        elif tag == 'SearchFolders':
            self.Synx.getChild('searchE0').insert(INSERT,'Search Media...')
            self.FlipThrougnFolderList([self.SavedFoldersListName.index(point), self.SavedFoldersListName.index(point) + 36])
    

    def run(self):
        win=tk.Tk()
        self.root = win
        win.title('Dosie')
        window_width = win.winfo_screenwidth()
        window_height = win.winfo_screenheight()
        win.minsize(width=800,height=600)
        win.config(bg='#ffffff')
        win.geometry(str(window_width)+'x'+str(window_height))

        self.root.protocol('WM_DELETE_WINDOW',self.quitDosie)

        icon=PhotoImage(file=configPath+'/logo.png')
        win.tk.call('wm','iconphoto',win._w,icon)
        win.columnconfigure(0,minsize=400,weight=900)


        shareWithSynx('win',win)
        Synx = self.Synx('win')

        
        
        
        #___LAYOUT_______________________
        Synx.layout(child='firstDiv',widget=tk.LabelFrame,sectionN=3,rowN=3,style=style(),widthR='15:55:25',marginYR='1:1:1',heightR='96:96:96')
        #LOADING PAGE____
        Synx.layout(child='welcomePage',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Bbg'),widthR='100',heightR='100')
        Synx.layout(parent='welcomePage0',child='welcomePageTT',widget=tk.Label,sectionN=4,rowN=2,style=style('Bbg'),rounded=style('default4'),widthR='1:20',heightR='2:20:2:2',marginXR='40',marginYR='30:30:5:5')
        Synx.affect(child='welcomePageTT',point=[1,3],pointSet=[{'rounded':style('DlogoR2')},{'rounded':style('load')}])
        #LOADING PAGE____
        Synx.layout(parent='firstDiv0',child='navs',widget=tk.LabelFrame,sectionN=4,rowN=1,style=style('Wbg'),widthR='100',marginYR='1:1:3:23',heightR='6:6:50:10')
        Synx.getChild('firstDiv0').grid(padx=(Synx.child_dimensions(win,'w',0.5),0))

        Synx.layout(parent='navs0',child='theApp',widget=tk.Button,sectionN=2,rowN=2,style=style(),rounded=style('DlogoR'),widthR='25:70',heightR='90:90')
        Synx.affect(child='theApp',point=[1],pointSet=[{'style':style('Dtext')}])

        Synx.layout(parent='navs1',child='blueB',widget=tk.Button,sectionN=1,rowN=1,style=style(),rounded=style('blueBr'),widthR='100',heightR='100')
        
        Synx.layout(parent='navs2',child='navBut',widget=tk.Button,sectionN=15,rowN=3,style=style('Wbg'),rounded=style('default4'),widthR='2:25:55',heightR='10:10:10:10:10:10:10:10:10:10:10:10:10:10:10')
        Synx.affect(child='navBut',point=[6],pointSet=[{'style':style('navClick')}])
        Synx.affectGroup(group='column',child='navBut',rows=3,columns=5,point=[1],depth=5,styleX=[{'rounded':style('domains')},{'rounded':style('keywords')},{'rounded':style('history')},{'rounded':style('media')},{'rounded':style('folders')}])
        Synx.affectGroup(group='column',child='navBut',rows=3,columns=5,point=[2],depth=5,styleX=[{'style':style('butCnv')+'text=Domains;'},{'style':style('butCnv')+'text=Keywords;'},{'style':style('butCnv')+'text=History;'},{'style':style('butCnv')+'text=Media;'},{'style':style('butCnv')+'text=Folders;'}])
        Synx.layout(parent='navs3',child='navBottom',widget=tk.Label,sectionN=1,rowN=1,style=style('Wbg'),rounded=style('nBott'),widthR='100',heightR='100')
        Synx.layout(parent='navs3',child='navBottomTxt',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg')+'text=;labelanchor=n;font=Helvetica 7 bold;',widthR='24',heightR='20',marginYR='40')
        Synx.getChild('navBottomTxt0').grid(padx=(Synx.child_dimensions(Synx.getChild('navs3'),'w',37),0))
        Synx.getChild('navBut2').bind('<Button- 1>',lambda event:self.menuFrames(0))
        Synx.getChild('navBut5').bind('<Button- 1>',lambda event:self.menuFrames(3))
        Synx.getChild('navBut8').bind('<Button- 1>',lambda event:self.menuFrames(6))
        Synx.getChild('navBut11').bind('<Button- 1>',lambda event:self.menuFrames(9))
        Synx.getChild('navBut14').bind('<Button- 1>',lambda event:self.menuFrames(12))


        Synx.layout(parent='firstDiv1',child='activity',widget=tk.LabelFrame,sectionN=4,rowN=1,style=style(),widthR='100',marginYR='1:1:2:3',heightR='5:5:73:10')
        Synx.layout(parent='activity0',child='topIndx',widget=tk.Label,sectionN=3,rowN=3,style=style('Wbg'),rounded=style('default5'),widthR='5:30:30',marginXR='1:33',heightR='90:90:90')
        Synx.affect(child='topIndx',point=[0,1],pointSet=[{'rounded':style('topIndL')},{'style':style('topIndLT')}])
        Synx.getChild('topIndx1').bind('<Button- 1>',lambda event:self.menuFrames(13))
        Synx.layout(parent='topIndx2',child='searchE',widget=tk.Text,resolveWH=True,sectionN=1,rowN=1,widthR='165',heightR='50',style='fg=#7d7d7d;bd=0;')
        Synx.getChild('searchE0').insert(END,'Search Something...')
        Synx.getChild('searchE0').bind('<Key>',lambda event:self.searchSomething(''))
        Synx.layout(parent='topIndx2',child='searchEAut',widget=tk.LabelFrame,sectionN=1,rowN=1,widthR='100',heightR='50',style=style('Wbg')+'fg=#0000cd;text=;',marginYR='50')

        Synx.layout(parent='activity1',child='process',widget=tk.Label,sectionN=5,rowN=5,style=style('Wbg'),rounded=style('default5'),widthR='60:5:5:5:5',marginXR='17:1:1:1',heightR='90:98:98:98:98')
        Synx.layout(parent='process0',child='processName',widget=tk.Label,sectionN=1,rowN=1,widthR='7',heightR='1',style='font=Helvetica 19 bold;text=Home;anchor=w;bg=#ffffff;')

        Synx.layout(parent='activity2',child='Mresults1',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Dbg'),widthR='61:36',heightR='48:48',marginYR='1:1')
        Synx.layout(parent='activity2',child='Mresults2',widget=tk.LabelFrame,sectionN=2,rowN=2,style=style('Dbg'),widthR='36:61',heightR='48:48',marginYR='51:51')

        Synx.layout(parent='activity3',child='ongoingCtrl',widget=tk.LabelFrame,style='padx=1;pady=1;',sectionN=2,rowN=1,widthR='100',heightR='45:45',marginYR='1:5')
        Synx.affect(child='ongoingCtrl',point=[0,1],pointSet=[{'style':style('Wbg')},{'style':style('Bbg')}])

        Synx.layout(parent='ongoingCtrl0',child='Ctrlbutt',widget=tk.Button,style=style()+'fg=#0000cd;',sectionN=4,rowN=4,widthR='2:2:2:2',marginXR='25:25:25',heightR='1:1:1:1',marginYR='1:1:1:1')
        Synx.layout(parent='ongoingCtrl1',child='Ctrlbutt2R',widget=tk.Button,style=style('default2')+'bg=#000080;fg=#ffffff;',rounded=style('default4'),sectionN=4,rowN=4,widthR='7:2:2:2',marginXR='23:35:15',heightR='70:1:1:1',marginYR='14:14:14:14')
        Synx.affect(child='Ctrlbutt2R',point=[0,1,2,3],pointSet=[{'style':'text=;','rounded':style('ctrlCnrOP')},{'style':'image=;text=Downloads;'},{'style':'image=;text=Back;'},{'style':'image=;text=Forward;'}])
        Synx.getChild('Ctrlbutt2R0').configure(command=self.CurrentSearchResults)
        Synx.getChild('Ctrlbutt2R1').bind('<Button- 1>',lambda event:self.menuFrames(19))

        Synx.layout(parent='firstDiv2',child='operations',widget=tk.LabelFrame,sectionN=3,rowN=1,style=style(),widthR='100',marginYR='1:8:2',heightR='5:5:79')

        Synx.layout(parent='operations0',child='settings',widget=tk.Label,sectionN=3,rowN=3,style=style(),rounded=style('default5'),widthR='13:13:13',marginXR='58:2',heightR='99:99:99')
        Synx.affect(child='settings',point=[0,1,2],pointSet=[{'rounded':style('settings1')},{'rounded':style('settings2')},{'rounded':style('settings3')}])
        Synx.getChild('settings0').grid(padx=(Synx.child_dimensions(Synx.getChild('operations0'),'w',56),0))
        Synx.getChild('settings0').bind('<Button- 1>',lambda event:self.menuFrames(16))
        Synx.getChild('settings1').bind('<Button- 1>',lambda event:self.menuFrames(17))
        Synx.getChild('settings2').bind('<Button- 1>',lambda event:self.menuFrames(18))

        Synx.layout(parent='operations1',child='tabNav',widget=tk.Label,sectionN=2,rowN=2,style=style(),rounded=style('default6'),widthR='45:45',heightR='99:99')
        Synx.layout(parent='tabNav0',child='tabText',widget=tk.Button,resolveWH=True,sectionN=1,rowN=1,style=style()+'text=OPERATIONS;fg=#0000cd;',widthR='100',heightR='80')
        Synx.layout(parent='tabNav1',child='tabTextB',widget=tk.Button,resolveWH=True,sectionN=1,rowN=1,style=style()+'text=STATUS;fg=#000000;',widthR='50',heightR='80')


        Synx.layout(parent='operations2',child='Dfigs',widget=tk.Label,sectionN=2,rowN=2,style=style(),rounded=style('default4'),widthR='47:47',heightR='40:40')
        Synx.affect(child='Dfigs',point=[0,1],pointSet=[{'rounded':style('default5')},{'rounded':style('relev')}])
        Synx.layout(parent='Dfigs0',child='timer',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style()+'text=0m 0s;fg=#0000cd;bg=#f0f0f0;',widthR='130',heightR='20',marginYR='50')
        Synx.layout(parent='Dfigs1',child='RelevancePer',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style()+'text=0%;fg=#ffffff;bg=#44464A;font=Helvetica 15 bold;',widthR='100',heightR='20',marginYR='40')
        Synx.getChild('RelevancePer0').grid(padx=(Synx.child_dimensions(Synx.getChild('Dfigs1'),'w',30),0))
        Synx.getChild('RelevancePer0').configure(width=5,height=2)


        Synx.layout(parent='operations2',child='Dnumbs',widget=tk.LabelFrame,sectionN=2,rowN=1,style=style(),widthR='100',heightR='15:43',marginYR='40:2')
        Synx.layout(parent='Dnumbs0',child='DomainP',widget=tk.LabelFrame,sectionN=3,rowN=1,style=style(),widthR='100',heightR='20:20:20',marginYR='0:10:10')
        Synx.affect(child='DomainP',point=[0,1,2],pointSet=[{'style':'fg=#0000cd;'},{'style':'fg=#7d7d7d;'},{'style':'fg=#7d7d7d;'}])
        Synx.layout(parent='Dnumbs1',child='doneDm',widget=tk.LabelFrame,sectionN=10,rowN=2,style=style(),widthR='65:30',marginYR='0:0:5:5:5:5:5:5:5:5')
        Synx.affectGroup(group='column',child='doneDm',rows=2,columns=5,point=[0,1],depth=5,style=[{'style':'fg=#7d7d7d;'},{'style':'fg=#0000cd;'}])

        Synx.layout(parent='operations2',child='operationStatus',widget=tk.LabelFrame,sectionN=1,rowN=1,style=style('Wbg'),widthR='100',heightR='98')
        Synx.layout(parent='operationStatus0',child='statusPlc',widget=tk.LabelFrame,sectionN=8,rowN=2,style=style('Wbg'),widthR='45:45',heightR='5:5:5:5:5:5:5:5',marginYR='3:3:3:3:3:3:3:3')
        Synx.affect(child='statusPlc',point=[0,1,2,3,4,5,6,7],pointSet=[{'style':'text=Stack count;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'},{'style':'text=Accessed Links;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'},{'style':'text=Status;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'},{'style':'text=New Domains Found;fg=#7d7d7d;'},{'style':'text=;fg=#0000cd;'}])
        Synx.layout(parent='operationStatus0',child='newDomainsFound',widget=tk.Label,sectionN=10,rowN=2,style=style('Wbg'),rounded=style('default5'),widthR='10:85',heightR='6:5:6:5:6:5:6:5:6:5',marginYR='40:40:3:4:3:4:3:3:3:4')
        Synx.layout(parent='operationStatus0',child='StatusButtons',widget=tk.Button,resolveWH=True,sectionN=3,rowN=3,style=style('Bbg')+'text=clicking;fg=#ffffff;',widthR='58:58:58',heightR='7:7:7',marginYR='93:93:93',marginXR='1:1')
        Synx.layout(parent='statusPlc5',child='StateInfo',widget=tk.Label,resolveWH=True,sectionN=1,rowN=1,style=style('Wbg')+'text=;fg=#0000cd;anchor=nw;wraplength=155;',widthR='180',heightR='140')
        padAr = [0,23,46]
        nameingAr = ['Add Domain','Found Files (0)','End Search']
        for i in range(3):
            if i > 0:
                Synx.getChild('StatusButtons'+str(i)).grid(padx=(Synx.child_dimensions(Synx.getChild('operationStatus0'),'w',padAr[i]),0))
            if i == 2:
                Synx.getChild('StatusButtons'+str(i)).configure(text=nameingAr[i],fg='#00ffff')
                Synx.getChild('StatusButtons'+str(i)).bind('<Button- 1>',lambda event:self.CancelSearch())
            else:
                Synx.getChild('StatusButtons'+str(i)).configure(text=nameingAr[i])
            if i == 0:
                Synx.getChild('StatusButtons'+str(i)).bind('<Button- 1>',lambda event,Px=14:self.menuFrames(Px))
            elif i == 1:
                Synx.getChild('StatusButtons'+str(i)).bind('<Button- 1>',lambda event,Pxj=15:self.menuFrames(Pxj))
        Synx.affectGroup(group='column',child='newDomainsFound',rows=2,columns=5,point=[1],depth=5,style=[{'style':'image=;width=38;height=2;text=;fg=#0000cd;anchor=w;'}])

        
        self.TXchild = Synx.getChild('DomainP2')
        self.TrackPos = algo.trackSectionPosition()
        self.RelevanceSP = Synx.getChild('Dfigs1')
        self.RelevanceSPC = Synx.getChild('RelevancePer0')
        self.probeTimer = Synx.getChild('timer0')
        self.Synx = Synx

        

        self.showStatusTab('remove')
        #___LAYOUT_______________________

        self.root.mainloop()





DosieGUI = DosieGUI()


time.sleep(8)
var = DosieGUI.dosome()
Crawler = crawler(var[0],var[1],var[2],var[3],var[4],var[5])


TKclown = tk.Tk()
PSTtime = None
def communicationThread():
    global communicateSIGNAL
    global COMMUNICATE_WITH
    global THREADSIGNAL
    global PSTtime
    if communicateSIGNAL:
        THREADSIGNAL = True
        #print('ive ended')
        TKclown.after_cancel(PSTtime)
        Crawler.query(communicateSIGNAL,COMMUNICATE_WITH)
        communicateSIGNAL = False
    if THREADSIGNAL:
        THREADSIGNAL = True
        #print('ive ended')
        TKclown.after_cancel(PSTtime)
    else:
        PSTtime = TKclown.after(100,communicationThread)
        #print('im going')
    THREADSIGNAL = False

TKclown.withdraw()
TKclown.mainloop()
