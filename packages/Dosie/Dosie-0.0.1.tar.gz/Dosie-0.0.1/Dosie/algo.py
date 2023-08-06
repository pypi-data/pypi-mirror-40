import re

class trackSectionPosition():
    def __init__(self):
        pass
    parentName = ''
    parentIndicate = 0

    def reset(self):
        self.parentName = ''
        self.parentIndicate = 0
    
    indicateParent = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

    def nameParent(self):
        if(self.parentIndicate == 26):
            self.parentIndicate = 0
            self.parentName += self.indicateParent[self.parentIndicate]
        else:
            self.parentName = self.parentName[0:-1] + self.indicateParent[self.parentIndicate]
        self.parentIndicate += 1

class elementBody(trackSectionPosition):
    opened = '<div '
    opened2 = '<div>'
    closed = '</div>'
    Eopen = ''
    Eclose = ''
    Dopen = 0
    whoOpened = 0
    openIndicate = 0
    
    whatString = ""
    ifFound = False
    querSize = 0
    pointDist = 0
    PartIndex = 0
    u_Query = ''
    full_find = []
    YesParts = []
    confYesParts = []
    sectionNameing = []

    def __init__(self,userQuery):
        trackSectionPosition.__init__(self)
        self.querSize = len(userQuery) * 4
        self.u_Query = userQuery

    def initQuery(self,userQuery):
        self.querSize = len(userQuery) * 4
        self.u_Query = userQuery

    def reset(self):
        self.Eopen = ''
        self.Eclose = ''
        self.Dopen = 0
        self.whoOpened = 0
        self.openIndicate = 0
    
        self.whatString = ""
        self.ifFound = False
        self.querSize = 0
        self.pointDist = 0
        self.PartIndex = 0
        self.u_Query = ''
        self.full_find = []
        self.YesParts = []
        self.confYesParts = []
        self.sectionNameing = []

    def setEopen(self,a):
        if(self.ifFound == True):
            self.whatString += a
        self.Eopen += a
        lt = len(self.Eopen)
        if(self.opened[0:lt] == self.Eopen):
            self.setOpen()
        elif(self.opened2[0:lt] == self.Eopen):
            self.setOpen()
        else:
            self.Eopen = ''

    def remove_tags(self,text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)

    def set_in(self,clean,tag,img = False):
        self.pointDist += 1
        yhParts = self.YesParts
        said = self.u_Query.split(' ')
        for i in range(len(said)):
            if img == False:
                if tag == 'a':
                    if (' '+clean+' ').lower().find(said[i].lower()) > -1 and '/search?client=' not in clean and 'webcache.googleusercontent' not in clean and 'support.google' not in clean and '/search?q=' not in clean and 'www.google.com/intl' not in clean:
                        if clean not in self.confYesParts:
                            yhParts.append([tag,self.pointDist,clean])
                            self.confYesParts.append(clean)
                else:
                    if (' '+clean+' ').lower().find(' '+said[i].lower()+' ') > -1 and '/search?client=' not in clean and 'webcache.googleusercontent' not in clean and 'support.google' not in clean and '/search?q=' not in clean and 'www.google.com/intl' not in clean:
                        if clean not in self.confYesParts:
                            yhParts.append([tag,self.pointDist,clean])
                            self.confYesParts.append(clean)
            else:
                if (' '+clean+' ').lower().find(said[i].lower()) > -1 and '/search?client=' not in clean and 'webcache.googleusercontent' not in clean and 'support.google' not in clean and '/search?q=' not in clean and 'www.google.com/intl' not in clean:
                    if clean not in self.confYesParts:
                        yhParts.append([tag,self.pointDist,clean])
                        self.confYesParts.append(clean)

    def getClean(self,st,tag,pos):
        see = '<'+tag+' '
        seeT = '<'+tag+'>'
        tfg = False
        if(st.find(see) > -1):
            if(st.find(seeT) > -1):
                if(st.find(seeT) < st.find(see)):
                    first = st.find(seeT)
                    tgg = seeT
                else:
                    first = st.find(see)
                    tgg = see
                    tfg = True
            else:
                first = st.find(see)
                tgg = see
                tfg = True
        else:
            first = st.find(seeT)
            tgg = seeT

        ele = st[0:pos]
        Href = ''
        if tag == 'a':
            src = re.findall('href="(.+?)"',ele)
            if src:
                Href = src[0]+' ~||~ '
        before = ele[first + len(tgg):]
        if(tfg == True):
            before = '<div'+before+'</div>'
        clean = self.remove_tags(before)
        #if(indx < 3):
        #    itt = 0
        #else:
        #    itt = indx - 2
        self.set_in(Href+clean,tag)
        return st[pos + len('</'+tag+'>'):]

    def elements(self,st):
        while len(st) > 0:
            h1 = st.find('</h1>')
            if(h1 < 0):
                h1 = len(st)
            h2 = st.find('</h2>')
            if(h2 < 0):
                h2 = len(st)
            h3 = st.find('</h3>')
            if(h3 < 0):
                h3 = len(st)
            p = st.find('</p>')
            if(p < 0):
                p = len(st)
            a = st.find('</a>')
            if(a < 0):
                a = len(st)
            td = st.find('</td>')
            if(td < 0):
                td = len(st)
            li = st.find('</li>')
            if(li < 0):
                li = len(st)
            if(h1 == len(st) and h2 == len(st) and h3 == len(st) and p == len(st) and a == len(st) and td == len(st) and li == len(st)):
                if(st.find('<script ') > -1):
                    st = ''
                else:
                    var_Headdings1 = re.findall('<img (.+?)>',st)
                    for j in range(len(var_Headdings1)):
                        st = st.replace('<img '+var_Headdings1[j]+'>','')
                        src = re.findall('src="(.+?)"',var_Headdings1[j])
                        if src:
                            self.set_in(src[0],'img',True)
                    try1 = '<div '+st+'</div>'
                    try2 = '<div>'+st+'</div>'
                    st1 = self.remove_tags(try1)
                    st2 = self.remove_tags(try2)
                    if(len(st1) > 0):
                        st = st1
                    else:
                        st = st2
                self.set_in(st,'plane')
                st = '';
            else:
                if(st.find('<script ') > -1):
                    st = ''
                else:
                    mann = ['h1','h2','h3','p','a','td','li']
                    mnn2 = [h1,h2,h3,p,a,td,li]
                    max_value = min(mnn2)
                    max_index = mnn2.index(max_value)
                    st = self.getClean(st,mann[max_index],max_value)

    def updateSetContent(self):
        if((self.whatString).startswith('<div>') or (self.whatString).startswith('<div ')):
            self.whatString = self.whatString[len('<div>'):]
        self.whatString = self.whatString[0:-5]
        self.whatString = (self.whatString).strip()
        if((self.whatString).endswith('<')):
            self.whatString = self.whatString[0:-1]
        self.whatString = (self.whatString).strip()
        if(len(self.whatString) > 0 and self.whatString != '>'):
            pass
        self.elements(self.whatString)
        self.whatString = ""

    def setOpen(self):
        if(self.Eopen == '<div ' or self.Eopen == '<div>'):
            self.updateSetContent()
            self.ifFound = True
            self.whoOpened += 1
            self.openIndicate += 1
            self.Dopen += 1
            self.Eopen = ''

    def setEclose(self,a):
        self.Eclose += a
        lt = len(self.Eclose)
        if(self.closed[0:lt] == self.Eclose):
            self.setClose()
        else:
            self.Eclose = ''

    def setClose(self):
        if(self.Eclose == '</div>'):
            self.updateSetContent()
            self.ifFound = False
            self.openIndicate = 0
            self.Dopen -= 1
            self.Eclose = ''
            if(self.Dopen == 0):
                var_ctn = False
                for i in range(len(self.YesParts)):
                    if self.YesParts[i]:
                        self.full_find.append(self.YesParts)
                        var_ctn = True
                        self.PartIndex += 1
                        break
                if(var_ctn == True):
                    self.sectionNameing.append([True,self.parentName,(self.PartIndex - 1)])
                else:
                    self.sectionNameing.append([False,self.parentName,0])
                self.YesParts = []
                self.confYesParts = []
                self.nameParent()

class Into_Perspective():
    plaque = []
    passStr = ''
    spacNum = 0

    def reset(self):
        self.passStr = ''
        self.plaque = []
        self.spacNum = 0
    
    def Tabs(self,arr):
        self.reset()
        for i in range(len(arr)):
            if i == 0:
                spacNum = arr[i][1]
            if arr[i][1] - spacNum < 4:
                tagType = arr[i][0]
                if tagType != 'space':
                    self.passStr += '<'+tagType+'> '+arr[i][2]+' </'+tagType+'><-||DOSIE||->\n'
                else:
                    self.passStr += '<'+tagType+'> '+arr[i][2]+' </'+tagType+'><-||DOSIE||->\n'
            else:
                self.plaque.append(self.passStr)
                self.passStr = ''
                tagType = arr[i][0]
                if tagType != 'space':
                    self.passStr += '<'+tagType+'> '+arr[i][2]+' </'+tagType+'><-||DOSIE||->\n'
                else:
                    self.passStr += '<'+tagType+'> '+arr[i][2]+' </'+tagType+'><-||DOSIE||->\n'
                spacNum = arr[i][1]
        return self.plaque
