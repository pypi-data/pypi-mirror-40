import tkinter as tk
from PIL import ImageTk
from PIL import Image
from PIL import ImageDraw
import os, shutil
import random
import string
import ntpath

PhotoImage = tk.PhotoImage

configPath = os.path.dirname(__file__)



def shareWithSynx(a,b):
    globals()[a] = b

class Synx():
    root = False
    SynxWHresolve = ''
    baseWidthV = ''
    mediaPath = configPath+'\\media\\gen'
    
    def __init__(self,root):
        self.root = globals()[root]
        self.SynxWHresolve = PhotoImage(file=configPath+'/media/vv.png')
        self.cleanUp()

    def cleanUp(self):
        folder = configPath+'/media/gen/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                #print(e)
                pass

    def delFromSynx(self,var):
        try:
            foo = win.call(self.getChild(var).cget('image'), 'cget', '-file')
            os.unlink(foo)
        except:
            pass
        globals()[var].destroy()
        globals()[var] = None
        del globals()[var]

    def getChild(self,child):
        return globals()[child]

    def affectPlus1(self,point,pointSet,child):
        for i in range(len(point)):
            wid = globals()[child+str(point[i])]
            apply = pointSet[i]
            for key in apply:
                if key == 'style':
                    self.styling(apply[key],wid)
                elif key == 'rounded':
                    defArgs = self.properties(apply[key])
                    widgitIMG = self.rounded(**defArgs)
                    widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                    globals()[child+'widgit'+randP+'Imaged' + str(i)] = PhotoImage(file=widgitIMG)
                    wid.configure(image=globals()[child+'widgit'+randP+'Imaged' + str(i)])
                    wid._image_ref = globals()[child+'widgit'+randP+'Imaged' + str(i)]

    def affectPlus2(self,child,fromTo,style,rounded):
        for i in range(fromTo[0],fromTo[1]):
            wid = globals()[child+str(i)]
            if style != '':
                self.styling(style,wid)
            if rounded != '':
                defArgs = self.properties(rounded)
                widgitIMG = self.rounded(**defArgs)
                widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                globals()[child+'widgit'+randP+'Imageq' + str(i)] = PhotoImage(file=widgitIMG)
                wid.configure(image=globals()[child+'widgit'+randP+'Imageq' + str(i)])
                wid._image_ref = globals()[child+'widgit'+randP+'Imageq' + str(i)]

    def affect(self,child='',fromTo='',style='',rounded='',point='',pointSet=''):
        if isinstance(point,list) and isinstance(fromTo,tuple):
            self.affectPlus2(child,fromTo,style,rounded)
            if isinstance(pointSet,list):
                self.affectPlus1(point,pointSet,child)
        elif isinstance(point,list) and not isinstance(fromTo,tuple):
            if isinstance(pointSet,list):
                self.affectPlus1(point,pointSet,child)
        elif isinstance(fromTo,tuple):
            self.affectPlus2(child,fromTo,style,rounded)

    def affectGroup(self,group='',child='',rows=0,columns=0,point=[0],depth=0,style='',styleX=''):
        Cp = 0
        index = 0
        StyleEvery = 0
        if group == 'column':
            maskRow = rows
            maskColumn = columns
            columns = maskRow
            rows = maskColumn
        if group == 'row' or group == 'column':
            for i in range(columns):
                if Cp == len(point):
                    return
                if i == point[Cp]:
                    if group == 'column':
                        start = point[Cp]
                    else:
                        start = index
                    for j in range(depth):
                        wid = globals()[child + str(start)]
                        if isinstance(style,list):
                            for key in style[Cp]:
                                if key == 'style':
                                    self.styling(style[Cp][key],wid)
                                elif key == 'rounded':
                                    defArgs = self.properties(style[Cp][key])
                                    widgitIMG = self.rounded(**defArgs)
                                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                                    widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                                    globals()[child+'widgitImagez' + str(i) + str(j) + str(randP)] = PhotoImage(file=widgitIMG)
                                    wid.configure(image=globals()[child+'widgitImagez' + str(i) + str(j) + str(randP)])
                                    wid._image_ref = globals()[child+'widgitImagez' + str(i) + str(j) + str(randP)]
                        elif isinstance(styleX,list):
                            for key in styleX[StyleEvery]:
                                if key == 'style':
                                    self.styling(styleX[StyleEvery][key],wid)
                                elif key == 'rounded':
                                    defArgs = self.properties(styleX[StyleEvery][key])
                                    widgitIMG = self.rounded(**defArgs)
                                    widgitIMG = self.fitImage(self.child_dimensions(wid,'w',100),widgitIMG,100)
                                    randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                                    globals()[child+'widgitImagev' + str(i) + str(j) + str(randP)] = PhotoImage(file=widgitIMG)
                                    wid.configure(image=globals()[child+'widgitImagev' + str(i) + str(j) + str(randP)])
                                    wid._image_ref = globals()[child+'widgitImagev' + str(i) + str(j) + str(randP)]
                        StyleEvery += 1
                        if group == 'column':
                            start += columns
                        else:
                            start += 1
                    Cp += 1
                index += rows

    def properties(self,rules):
        rules = rules[0:-1]
        rules = dict(e.split('=') for e in rules.split(';'))
        return rules

    def styling(self,rules,child):
        rules = rules[0:-1]
        rules = dict(e.split('=') for e in rules.split(';'))
        child.configure(**rules)

    def fitImage(self,parentSZ,path,per):
        basewidth = parentSZ
        basewidth = round((per / 100) * basewidth)
        img = Image.open(path)
        randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
        base = ntpath.basename(path)
        path = configPath+'/media/gen/'+randP+base
        img.save(path)
        img = Image.open(path)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        pathNew = path
        img.save(pathNew)
        return pathNew

    def borderRadius(self,im,rad):
        rad = int(rad)
        width, height = im.size
        rad = round((rad / 100) * height)
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def circular(self,im):
        im = im.resize((im.size[1], im.size[1]))
        bigsize = (im.size[0] * 3, im.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        im.putalpha(mask)
        return im

    def rounded(self,path='',background='',rad=10,circular=False):
        if circular == False:
            self.baseWidthV = True
        else:
            self.baseWidthV = False
        if path == '':
            if len(list(background)) < 3:
                if circular == False:
                    useMMx = configPath+'/media/vv2.png'
                else:
                    useMMx = configPath+'/media/vv.png'
                im = Image.open(useMMx)
                pixelMap = im.load()
                img = Image.new( im.mode, im.size)
                pixelsNew = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        pixelsNew[i,j] = (255,255,255,255)
                try:
                    rad = int(rad)
                    img = self.borderRadius(img,rad)
                except ValueError:
                    img = self.circular(img)
                randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                base = ntpath.basename(useMMx)
                pathNew = configPath+'/media/gen/'+randP+base
                img.save(pathNew)
                return pathNew
            else:
                if circular == False:
                    useMMx = configPath+'/media/vv2.png'
                else:
                    useMMx = configPath+'/media/vv.png'
                background = background.lstrip('#')
                background = tuple(int(background[i:i+2], 16) for i in (0, 2 ,4))
                im = Image.open(useMMx)
                pixelMap = im.load()
                img = Image.new( im.mode, im.size)
                pixelsNew = img.load()
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        pixelsNew[i,j] = background
                if circular == False:
                    rad = int(rad)
                    img = self.borderRadius(img,rad)
                else:
                    img = self.circular(img)
                randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
                base = ntpath.basename(useMMx)
                pathNew = configPath+'/media/gen/'+randP+base
                img.save(pathNew)
                return pathNew
        else:
            img = Image.open(path)
            if circular == False:
                rad = int(rad)
                img = self.borderRadius(img,rad)
            else:
                img = self.circular(img)
            randP = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
            base = ntpath.basename(path).split('.')[0]+'.png'
            pathNew = configPath+'/media/gen/'+randP+base
            img.save(pathNew)
            return pathNew

    def child_dimensions(self,parent,side,val):
        self.root.update()
        if side == 'w':
            side = parent.winfo_width()
        else:
            side = parent.winfo_height()
        return round((val / 100) * side)

    def resolveSize(self,parent,side,val):
        SynxResolve = tk.Label(self.root,width=1,height=1)
        SynxResolve.grid(column=0,row=0,pady=(2000,0))
        self.root.update()
        if side == 'w':
            width = SynxResolve.winfo_width()
            parentWidth = parent.winfo_width()
            pixWidth = ((width / parentWidth) * 100)
            fin = round((val / pixWidth) * 1)
        else:
            height = SynxResolve.winfo_height()
            parentHeight = parent.winfo_height()
            pixHeight = ((height / parentHeight) * 100)
            fin = round((val / pixHeight) * 1)
        SynxResolve.grid_forget()
        self.root.update()
        return fin

    def layoutWaMa(self,parent,ratioX,rowN):
        padxR = []
        widthxR = []
        widthxResolve = []
        pad = 0
        for i in range(len(ratioX)):
            ratioX[i] = int(ratioX[i])
            padxX = self.child_dimensions(parent,'w',ratioX[i])
            padxR.append(padxX)
            pad += ratioX[i]
        width = 100 - pad
        width = width / rowN
        resolveWval = self.resolveSize(parent,'w',width)
        width = self.child_dimensions(parent,'w',width)
        for i in range(rowN):
            widthxR.append(width)
            widthxResolve.append(resolveWval)
        return [padxR,widthxR,widthxResolve]

    def layoutWsMa(self,parent,widthR):
        widthxR = []
        widthxResolve = []
        widthX = widthR.split(':')
        widthM = 0
        for i in range(len(widthX)):
            widthX[i] = int(widthX[i])
            resolveWval = self.resolveSize(parent,'w',widthX[i])
            width = self.child_dimensions(parent,'w',widthX[i])
            widthxR.append(width)
            widthxResolve.append(resolveWval)
            widthM += widthX[i]
        return [widthM,widthxR,widthxResolve]
        

    def layout(self,parent='win',child='',widget=tk.LabelFrame,sectionN=1,rowN=1,marginXR='auto',widthR='auto',heightR='auto',marginYR='auto',MXdef=5,resolveWH=False,style='',rounded='XXXX'):
        globals()[child] = ''
        parent = globals()[parent]
        row = 0
        tick = True
        padxR = []
        widthxR = []
        widthxResolve = []
        heightxResolve = []
        heightxR = []
        heightPad = []

        
        
        for i in range(sectionN):
            if tick:
                row += 1
                tick = False
            elif (i + 1) % rowN == 0:
                tick = True
        
        if widthR == 'auto':
            if marginXR == 'auto':
                marginXR = ''
                for i in range(rowN - 1):
                    marginXR += str(MXdef)+':'
                marginXR = marginXR[0:-1]
                ratioX = marginXR.split(':')
                WaMaRET = self.layoutWaMa(parent,ratioX,rowN)
                padxR = WaMaRET[0]
                widthxR = WaMaRET[1]
                widthxResolve = WaMaRET[2]
            else:
                ratioX = marginXR.split(':')
                WaMaRET = self.layoutWaMa(parent,ratioX,rowN)
                padxR = WaMaRET[0]
                widthxR = WaMaRET[1]
                widthxResolve = WaMaRET[2]
        else:
            if marginXR == 'auto':
                if rowN == 1:
                    rowNX = 2
                else:
                    rowNX = rowN
                widthX = widthR.split(':')
                WsMaRES = self.layoutWsMa(parent,widthR)
                widthM = WsMaRES[0]
                widthxR = WsMaRES[1]
                widthxResolve = WsMaRES[2]
                pmx = 100 - widthM
                pmx = pmx / (rowNX - 1)
                marginXR = ''
                for i in range(rowNX - 1):
                    marginXR += str(round(pmx))+':'
                marginXR = marginXR[0:-1]
                ratioX = marginXR.split(':')
                for i in range(len(ratioX)):
                    ratioX[i] = int(ratioX[i])
                    padxX = self.child_dimensions(parent,'w',ratioX[i])
                    padxR.append(padxX)
            else:
                pad = 0
                ratioX = marginXR.split(':')
                for i in range(len(ratioX)):
                    ratioX[i] = int(ratioX[i])
                    padxX = self.child_dimensions(parent,'w',ratioX[i])
                    padxR.append(padxX)
                    pad += ratioX[i]
                widthX = widthR.split(':')
                WsMaRES = self.layoutWsMa(parent,widthR)
                widthM = WsMaRES[0]
                widthxR = WsMaRES[1]
                widthxResolve = WsMaRES[2]
        
        #____HEIGHTS___________________________________________________________
                    
        if heightR == 'auto':
            if marginYR == 'auto':
                Hpad = MXdef * (row - 1)
                Hpadp = self.child_dimensions(parent,'h',MXdef)
                Hleft = 100 - Hpad
                resolveHval = self.resolveSize(parent,'h',(Hleft / row))
                heigthH = self.child_dimensions(parent,'h',(Hleft / row))
                for i in range(sectionN):
                    if i <= (rowN - 1):
                        heightPad.append([0,heigthH])
                        heightxResolve.append([0,resolveHval])
                    else:
                        heightPad.append([Hpadp,heigthH])
                        heightxResolve.append([Hpadp,resolveHval])
            else:
                marginYR = marginYR.split(':')
                for i in range(len(marginYR)):
                    marginYR[i] = int(marginYR[i])
                    Hpad = marginYR[i] * (row - 1)
                    HpadP = self.child_dimensions(parent,'h',marginYR[i])
                    Hleft = 100 - Hpad
                    resolveHval = self.resolveSize(parent,'h',(Hleft / row))
                    heigthH = self.child_dimensions(parent,'h',(Hleft / row))
                    heightPad.append([HpadP,heigthH])
                    heightxResolve.append([HpadP,resolveHval])
        else:
            if marginYR == 'auto':
                heightR = heightR.split(':')
                for i in range(len(heightR)):
                    heightR[i] = int(heightR[i])
                    resolveHval = self.resolveSize(parent,'h',heightR[i])
                    heigthH = self.child_dimensions(parent,'h',heightR[i])
                    if i <= (rowN - 1):
                        heightPad.append([0,heigthH])
                        heightxResolve.append([0,resolveHval])
                    else:
                        Hpad = MXdef * (row - 1)
                        HpadP = self.child_dimensions(parent,'h',MXdef)
                        heightPad.append([HpadP,heigthH])
                        heightxResolve.append([HpadP,resolveHval])
            else:
                marginYR = marginYR.split(':')
                heightR = heightR.split(':')
                for i in range(len(marginYR)):
                    marginYR[i] = int(marginYR[i])
                    Hpad = marginYR * (row - 1)
                    HpadP = self.child_dimensions(parent,'h',marginYR[i])
                    heightR[i] = int(heightR[i])
                    resolveHval = self.resolveSize(parent,'h',heightR[i])
                    heigthH = self.child_dimensions(parent,'h',heightR[i])
                    heightPad.append([HpadP,heigthH])
                    heightxResolve.append([HpadP,resolveHval])
        indx = 0
        compact = []
        for i in range(rowN):
            compact.append(0)
        for i in range(len(heightPad)):
            mock = heightPad[i][0]
            heightPad[i][0] = heightPad[i][0] + compact[indx]
            compact[indx] += mock + heightPad[i][1]
            if (i + 1) % rowN == 0:
                indx = 0
            else:
                indx += 1

        padx = 0
        pdrC = 0
        widC = 0
        for i in range(sectionN):
            if resolveWH == True:
                useAsWidth = widthxResolve[widC]
                useAsHeight = heightxResolve[i][1]
            else:
                useAsWidth = widthxR[widC]
                useAsHeight = heightPad[i][1]
            globals()[child + str(i)] = widget(parent,width=useAsWidth,height=useAsHeight)
            globals()[child + str(i)].columnconfigure(0,minsize=widthxR[widC])
            globals()[child + str(i)].rowconfigure(0,minsize=heightPad[i][1])
            globals()[child + str(i)].grid(column=0,row=0,sticky='nw',pady=(heightPad[i][0],0),padx=(padx,0))
            if style != '':
                self.styling(style,globals()[child + str(i)])
            if rounded == 'XXXX':
                pass
            elif rounded.find('background') < 0 and rounded.find('path') < 0 and rounded.find('rad') < 0:
                widgitIMG = self.rounded()
                if self.baseWidthV == True:
                    self.fitImage(widthxR[widC],widgitIMG,100)
                else:
                    self.fitImage(heightPad[i][1],widgitIMG,100)
                globals()[child+'widgitImage' + str(i)] = PhotoImage(file=widgitIMG)
                globals()[child + str(i)].configure(image=globals()[child+'widgitImage' + str(i)])
                globals()[child + str(i)]._image_ref = globals()[child+'widgitImage' + str(i)]
            else:
                defArgs = self.properties(rounded)
                widgitIMG = self.rounded(**defArgs)
                if self.baseWidthV == True:
                    self.fitImage(widthxR[widC],widgitIMG,100)
                else:
                    self.fitImage(heightPad[i][1],widgitIMG,100)
                globals()[child+'widgitImage' + str(i)] = PhotoImage(file=widgitIMG)
                globals()[child + str(i)].configure(image=globals()[child+'widgitImage' + str(i)])
                globals()[child + str(i)]._image_ref = globals()[child+'widgitImage' + str(i)]
            if (i + 1) % rowN == 0 :
                pdrC = 0
                widC = 0
                padx = 0
            else:
                padx += widthxR[widC] + padxR[pdrC]
                pdrC += 1
                widC += 1
