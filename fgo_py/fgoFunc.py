###################################################################################################################################################
#                                                                                                                                                 #
#                                                                                                                                                 #
#    YYYYYYY       YYYYYYY     LLLLLLLLLLL                     SSSSSSSSSSSSSSS      FFFFFFFFFFFFFFFFFFFFFF     MMMMMMMM               MMMMMMMM    #
#    Y:::::Y       Y:::::Y     L:::::::::L                   SS:::::::::::::::S     F::::::::::::::::::::F     M:::::::M             M:::::::M    #
#    Y:::::Y       Y:::::Y     L:::::::::L                  S:::::SSSSSS::::::S     F::::::::::::::::::::F     M::::::::M           M::::::::M    #
#    Y::::::Y     Y::::::Y     LL:::::::LL                  S:::::S     SSSSSSS     FF::::::FFFFFFFFF::::F     M:::::::::M         M:::::::::M    #
#    YYY:::::Y   Y:::::YYY       L:::::L                    S:::::S                   F:::::F       FFFFFF     M::::::::::M       M::::::::::M    #
#       Y:::::Y Y:::::Y          L:::::L                    S:::::S                   F:::::F                  M:::::::::::M     M:::::::::::M    #
#        Y:::::Y:::::Y           L:::::L                     S::::SSSS                F::::::FFFFFFFFFF        M:::::::M::::M   M::::M:::::::M    #
#         Y:::::::::Y            L:::::L                      SS::::::SSSSS           F:::::::::::::::F        M::::::M M::::M M::::M M::::::M    #
#          Y:::::::Y             L:::::L                        SSS::::::::SS         F:::::::::::::::F        M::::::M  M::::M::::M  M::::::M    #
#           Y:::::Y              L:::::L                           SSSSSS::::S        F::::::FFFFFFFFFF        M::::::M   M:::::::M   M::::::M    #
#           Y:::::Y              L:::::L                                S:::::S       F:::::F                  M::::::M    M:::::M    M::::::M    #
#           Y:::::Y              L:::::L         LLLLLL                 S:::::S       F:::::F                  M::::::M     MMMMM     M::::::M    #
#           Y:::::Y            LL:::::::LLLLLLLLL:::::L     SSSSSSS     S:::::S     FF:::::::FF                M::::::M               M::::::M    #
#        YYYY:::::YYYY         L::::::::::::::::::::::L     S::::::SSSSSS:::::S     F::::::::FF                M::::::M               M::::::M    #
#        Y:::::::::::Y         L::::::::::::::::::::::L     S:::::::::::::::SS      F::::::::FF                M::::::M               M::::::M    #
#        YYYYYYYYYYYYY         LLLLLLLLLLLLLLLLLLLLLLLL      SSSSSSSSSSSSSSS        FFFFFFFFFFF                MMMMMMMM               MMMMMMMM    #
#                                                                                                                                                 #
#        又有人想教yls做游戏? 我不是我没有,我已经帮他做了                                                                                         #
#                                                                                                                                                 #
###################################################################################################################################################
'Full-automatic FGO Script'
__author__='hgjazhgj'
import logging,os,re,threading,time,cv2,numpy,win32con,win32file
from subprocess import check_call
from airtest.core.android.android import Android
from airtest.core.android.constant import CAP_METHOD,ORI_METHOD,TOUCH_METHOD
(lambda logger:(logger.setLevel(logging.WARNING),logger)[-1])(logging.getLogger('airtest')).handlers[0].formatter.datefmt='%H:%M:%S'
(lambda logger:(logger.setLevel(logging.INFO),logger.addHandler((lambda handler:(handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s]<%(name)s> %(message)s','%H:%M:%S')),handler)[-1])(logging.StreamHandler()))))(logging.getLogger('fgo'))
logger=logging.getLogger('fgo.Func')
IMG_APEMPTY=cv2.imread('fgoImage/apempty.png')
IMG_ATTACK=cv2.imread('fgoImage/attack.png')
IMG_BEGIN=cv2.imread('fgoImage/begin.png')
IMG_BATTLEBEGIN=cv2.imread('fgoImage/battlebegin.png')
IMG_BATTLECONTINUE=cv2.imread('fgoImage/battlecontinue.png')
IMG_BOUND=cv2.imread('fgoImage/bound.png')
IMG_BOUNDUP=cv2.imread('fgoImage/boundup.png')
IMG_CARDSEALED=cv2.imread('fgoImage/cardsealed.png')
IMG_CHOOSEFRIEND=cv2.imread('fgoImage/choosefriend.png')
IMG_END=cv2.imread('fgoImage/end.png')
IMG_FAILED=cv2.imread('fgoImage/failed.png')
IMG_GACHA=cv2.imread('fgoImage/gacha.png')
IMG_HOUGUSEALED=cv2.imread('fgoImage/hougusealed.png')
IMG_JACKPOT=cv2.imread('fgoImage/jackpot.png')
IMG_LISTEND=cv2.imread('fgoImage/listend.png')
IMG_LISTNONE=cv2.imread('fgoImage/listnone.png')
IMG_NOFRIEND=cv2.imread('fgoImage/nofriend.png')
IMG_PARTYINDEX=cv2.imread('fgoImage/partyindex.png')
IMG_STAGE=[cv2.imread(f'fgoImage/stage{i}.png')for i in range(1,4)]
IMG_STAGETOTAL=[cv2.imread(f'fgoImage/total{i}.png')for i in range(1,4)]
IMG_STILL=cv2.imread('fgoImage/still.png')
partyIndex=0
skillInfo=[[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]],[[0,0,0],[0,0,0],[0,0,0]]]
houguInfo=[[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]]
dangerPos=[0,0,1]
friendPos=4
masterSkill=[[0,0,0],[0,0,0],[0,0,0,0]]
terminateFlag=False
suspendFlag=False
tobeTerminatedFlag=-1
def sleep(x,part=.1):
    timer=time.time()+x-part
    while True:
        while suspendFlag and not terminateFlag:time.sleep(.1)
        if terminateFlag:exit(0)
        if time.time()>=timer:break
        time.sleep(part)
    time.sleep(max(0,timer+part-time.time()))
class Fuse:
    def __init__(self,fv=400,show=3,name='',logsize=16):
        self.__value=0
        self.__max=fv
        self.show=show
        self.name=name
        self.logsize=logsize
        self.log=[None for i in range(self.logsize)]
        self.logptr=0
    @property
    def value(self):return self.__value
    @property
    def max(self):return self.__max
    def increase(self):
        if self.__value>self.__max:
            logger.warning(f'Fused {self.name}')
            self.save()
            exit(0)
        self.__value+=1
        return self
    def reset(self):
        if self.__value>self.show:logger.debug(f'Fuse {self.name} {self.__value}')
        self.__value=0
        if id(check)!=id(self.log[(self.logptr-1)%self.logsize]):
            self.log[self.logptr]=check
            self.logptr=(self.logptr+1)%self.logsize
        return self
    def save(self):
        for i in range(16):
            self.log[(i+self.logptr)%self.logsize].save(f'fuselog{i:02}.jpg')
        check.save()
fuse=Fuse()
class DirListener:
    def __init__(self,dir):
        self.hDir=win32file.CreateFile(dir,win32con.GENERIC_READ,win32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRITE|win32con.FILE_SHARE_DELETE,None,win32con.OPEN_EXISTING,win32con.FILE_FLAG_BACKUP_SEMANTICS,None)
        self.msg=[]
        self.lock=threading.Lock()
        self.ren=''
        def f():
            while True:self.add(win32file.ReadDirectoryChangesW(self.hDir,0x1000,False,win32con.FILE_NOTIFY_CHANGE_FILE_NAME|win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,None,None))
        threading.Thread(target=f,daemon=True,name='DirListener').start()
    def add(self,x):
        def onCreated(file):
            for i in range(len(self.msg)-1,-1,-1):
                if self.msg[i][1]!=file:continue
                if self.msg[i][0]==2:
                    self.msg[i][0]=3
                    return
                break
            self.msg.append([1,file])
        def onDeleted(file):
            for i in range(len(self.msg)-1,-1,-1):
                if self.msg[i][1]!=file:continue
                if self.msg[i][0]==1:
                    del self.msg[i]
                    return
                if self.msg[i][0]==3:
                    del self.msg[i]
                    break
                temp=self.msg[i-1][1]
                del self.msg[i-1:i+1]
                onDeleted(temp)
                return
            self.msg.append([2,file])
        def onUpdated(file):
            for i in range(len(self.msg)-1,-1,-1):
                if self.msg[i][1]!=file:continue
                if self.msg[i][0]==1or self.msg[i][0]==3:return
                if self.msg[i][0]==5:
                    temp=self.msg[i-1][1]
                    del self.msg[i-1:i+1]
                    onDeleted(temp)
                    onCreated(file)
                    return
                break
            self.msg.append([3,file])
        def onRenamedFrom(file):self.ren=file
        def onRenamedTo(file):
            for i in range(len(self.msg)-1,-1,-1):
                if self.msg[i][1]==file:break
                if self.msg[i][1]==self.ren:
                    if self.msg[i][0]==1:
                        del self.msg[i]
                        onCreated(file)
                        return
                    if self.msg[i][0]==3:
                        self.msg[i][0]=2
                        onCreated(file)
                        return
                    if self.msg[i][0]==5:
                        self.ren=self.msg[i-1][1]
                        del self.msg[i-1:i+1]
                        if self.ren==file:return
                    break
            self.msg+=[[4,self.ren],[5,file]]
        with self.lock:
            for i in x:{1:onCreated,2:onDeleted,3:onUpdated,4:onRenamedFrom,5:onRenamedTo}.get(i[0],lambda _:None)(i[1])
    def get(self):
        with self.lock:
            ans=self.msg
            self.msg=[]
        return ans
class ImageListener(dict):
    def __init__(self,path,ends='.png'):
        super().__init__((file[:-len(ends)],cv2.imread(path+file))for file in os.listdir(path)if file.endswith(ends))
        self.path=path
        self.ends=ends
        self.listener=DirListener(path)
    def flush(self):
        lastAction=0
        oldName=None
        def onCreated(name):self[name]=cv2.imread(self.path+name+self.ends)
        def onDeleted(name):del self[name]
        def onUpdated(name):self[name]=cv2.imread(self.path+name+self.ends)
        def onRenamedFrom(name):
            nonlocal oldName
            if oldName is not None:del self[oldName]
            oldName=name
        def onRenamedTo(name):self[name]=self[oldName]if lastAction==4else cv2.imread(self.path+name+self.ends)
        for action,name in((action,file[:-len(self.ends)])for action,file in self.listener.get()if file.endswith(self.ends)):
            {1:onCreated,2:onDeleted,3:onUpdated,4:onRenamedFrom,5:onRenamedTo}.get(action,lambda _:None)(name)
            lastAction=action
        if oldName is not None:del self[oldName]
friendImg=ImageListener('fgoImage/friend/')
mailFilterImg=ImageListener('fgoImage/mailfilter/')
class Base(Android):
    def __init__(self,serialno=None):
        self.lock=threading.Lock()
        if serialno is None:
            self.serialno=None
            return
        try:super().__init__(serialno,cap_method=CAP_METHOD.JAVACAP,ori_method=ORI_METHOD.ADB,touch_method=TOUCH_METHOD.MAXTOUCH)
        except:self.serialno=None
        else:
            self.render=[round(i)for i in self.get_render_resolution(True)]
            self.scale,self.border=(1080/self.render[3],(round(self.render[2]-self.render[3]*16/9)>>1,0))if self.render[2]*9>self.render[3]*16else(1920/self.render[2],(0,round(self.render[3]-self.render[2]*9/16)>>1))
            self.maxtouch.install_and_setup()
            self.key={c:[round(p[i]/self.scale+self.border[i]+self.render[i])for i in range(2)]for c,p in{
                '\x70':(790,74),'\x71':(828,74),'\x72':(866,74),'\x73':(903,74),'\x74':(940,74),'\x75':(978,74),'\x76':(1016,74),'\x77':(1053,74),'\x78':(1091,74),'\x79':(1128,74),#VK_F1..10
                '1':(277,640),'2':(598,640),'3':(974,640),'4':(1312,640),'5':(1651,640),'6':(646,304),'7':(976,304),'8':(1267,304),'0':(1819,367),
                'Q':(1800,475),'W':(1360,475),'E':(1493,475),'R':(1626,475),'T':(210,540),'Y':(510,540),'U':(810,540),'I':(1110,540),'O':(1410,540),'P':(1710,540),'\xDC':(1880,40),#\ VK_OEM_5
                'A':(109,860),'S':(244,860),'D':(385,860),'F':(582,860),'G':(724,860),'H':(861,860),'J':(1056,860),'K':(1201,860),'L':(1336,860),'\xBA':(1247,197),#; VK_OEM_1
                'Z':(960,943),'X':(259,932),'B':(495,480),'N':(248,1041),'M':(1200,1000),
                ' ':(1846,1030),
                '\x64':(70,221),'\x65':(427,221),'\x66':(791,221),'\x67':(70,69),'\x68':(427,69),'\x69':(791,69),#VK-NUMPAD4..9
                }.items()}
    def touch(self,p):
        with self.lock:super().touch([round(p[i]/self.scale+self.border[i]+self.render[i])for i in range(2)])
    # def swipe(self,rect,duration=.15,steps=2,fingers=1):
    #     with self.lock:super().swipe(*[[round(rect[i<<1|j]/self.scale)+self.border[j]+self.render[j]for j in range(2)]for i in range(2)],duration,steps,fingers)
    def swipe(self,rect):#if this doesn't work, use the above one instead
        p1,p2=[numpy.array(self._touch_point_by_orientation([rect[i<<1|j]/self.scale+self.border[j]+self.render[j]for j in range(2)]))for i in range(2)]
        vd=p2-p1
        lvd=numpy.linalg.norm(vd)
        vd/=.2*self.scale*lvd
        vx=numpy.array([0.,0.])
        def send(method,pos):self.maxtouch.safe_send(' '.join((method,'0',*[str(i)for i in self.maxtouch.transform_xy(*pos)],'50\nc\n')))
        with self.lock:
            send('d',p1)
            time.sleep(.01)
            for _ in range(2):
                send('m',p1+vx)
                vx+=vd
                time.sleep(.02)
            vd*=5
            while numpy.linalg.norm(vx)<lvd:
                send('m',p1+vx)
                vx+=vd
                time.sleep(.008)
            send('m',p2)
            time.sleep(.35)
            self.maxtouch.safe_send('u 0\nc\n')
            time.sleep(.02)
    def press(self,c):
        with self.lock:super().touch(self.key[c])
    def snapshot(self):return cv2.resize(super().snapshot()[self.render[1]+self.border[1]:self.render[1]+self.render[3]-self.border[1],self.render[0]+self.border[0]:self.render[0]+self.render[2]-self.border[0]],(1920,1080),interpolation=cv2.INTER_CUBIC)
base=Base()
def doit(pos,wait):[(base.press(i),sleep(j*.001))for i,j in zip(pos,wait)]
check=None
class Check:
    def __init__(self,forwordLagency=.01,backwordLagency=0):
        sleep(forwordLagency)
        self.im=base.snapshot()
        global check
        check=self
        fuse.increase()
        sleep(backwordLagency)
    def compare(self,img,rect=(0,0,1920,1080),threshold=.05):return threshold>cv2.minMaxLoc(cv2.matchTemplate(self.im[rect[1]:rect[3],rect[0]:rect[2]],img,cv2.TM_SQDIFF_NORMED))[0]and fuse.reset()
    def select(self,img,rect=(0,0,1920,1080)):return numpy.argmin([cv2.minMaxLoc(cv2.matchTemplate(self.im[rect[1]:rect[3],rect[0]:rect[2]],i,cv2.TM_SQDIFF_NORMED))[0]for i in img])
    def tap(self,img,rect=(0,0,1920,1080),threshold=.05):return(lambda loc:loc[0]<threshold and(base.touch((rect[0]+loc[2][0]+(img.shape[1]>>1),rect[1]+loc[2][1]+(img.shape[0]>>1))),fuse.reset())[1])(cv2.minMaxLoc(cv2.matchTemplate(self.im[rect[1]:rect[3],rect[0]:rect[2]],img,cv2.TM_SQDIFF_NORMED)))
    def save(self,name=''):
        cv2.imwrite(time.strftime('%Y-%m-%d_%H.%M.%S',time.localtime())+'.jpg'if name==''else name,self.im)
        return self
    def show(self):
        cv2.imshow('Check Screenshot - Press S to save',cv2.resize(self.im,(0,0),fx=.4,fy=.4))
        if cv2.waitKey()==ord('s'):self.save()
        cv2.destroyAllWindows()
        return self
    def isAddFriend(self):return self.compare(IMG_END,(243,863,745,982))
    def isApEmpty(self):return self.compare(IMG_APEMPTY,(906,897,1017,967))
    def isBattleBegin(self):return self.compare(IMG_BATTLEBEGIN,(1673,959,1899,1069))
    def isBattleContinue(self):return self.compare(IMG_BATTLECONTINUE,(1072,805,1441,895))
    def isBattleFailed(self):return self.compare(IMG_FAILED,(277,406,712,553))
    def isBattleFinished(self):return(self.compare(IMG_BOUND,(112,250,454,313))or self.compare(IMG_BOUNDUP,(987,350,1468,594)))
    def isBegin(self):return self.compare(IMG_BEGIN,(1630,950,1919,1079))
    def isChooseFriend(self):return self.compare(IMG_CHOOSEFRIEND,(1249,324,1387,382))
    def isGacha(self):return self.compare(IMG_GACHA,(973,960,1312,1052))
    def isHouguReady(self):return[not any(self.compare(j,(470+346*i,258,768+346*i,387),.3)for j in(IMG_HOUGUSEALED,IMG_CARDSEALED))and(numpy.mean(self.im[1019:1026,217+478*i:235+478*i])>55or numpy.mean(Check(.2).im[1019:1026,217+478*i:235+478*i])>55)for i in range(3)]
    def isListEnd(self,pos):return any(self.compare(i,(pos[0]-30,pos[1]-20,pos[0]+30,pos[1]+1),.25)for i in(IMG_LISTEND,IMG_LISTNONE))
    def isNextJackpot(self):return self.compare(IMG_JACKPOT,(1556,336,1859,397))
    def isNoFriend(self):return self.compare(IMG_NOFRIEND,(369,545,1552,797),.1)
    def isSkillReady(self):return[[not self.compare(IMG_STILL,(54+476*i+132*j,897,83+480*i+141*j,927),.1)for j in range(3)]for i in range(3)]
    def isTurnBegin(self):return self.compare(IMG_ATTACK,(1567,932,1835,1064))
    def getABQ(self):return[-1if self.compare(IMG_CARDSEALED,(43+386*i,667,345+386*i,845),.3)else(lambda x:x.index(max(x)))([numpy.mean(self.im[771:919,108+386*i:318+386*i,j])for j in(2,1,0)])for i in range(5)]
    def getPartyIndex(self):return cv2.minMaxLoc(cv2.matchTemplate(self.im[58:92,768:1152],IMG_PARTYINDEX,cv2.TM_SQDIFF_NORMED))[2][0]//37+1
    def getPortrait(self):return[self.im[640:740,195+480*i:296+480*i]for i in range(3)]
    def getStage(self):return self.select(IMG_STAGE,(1296,20,1342,56))+1
    def getStageTotal(self):return self.select(IMG_STAGETOTAL,(1325,20,1372,56))+1
def gacha():
    while fuse.value<30:
        if Check(.1).isGacha():doit('MK',(200,2700))
        base.press('\xDC')
def jackpot():
    while fuse.value<70:
        if Check().isNextJackpot():doit('0JJ',(600,1800,0))
        for _ in range(40):base.press('2')
def mailFiltering():
    mailFilterImg.flush()
    while not Check(1).isListEnd((1406,1079)):
        if not any(check.tap(i[1],threshold=.016)for i in mailFilterImg.items()):base.swipe((400,900,400,300))
def chooseFriend():
    refresh=False
    while not Check(.2).isChooseFriend():
        if check.isNoFriend():
            if refresh:sleep(10)
            doit('\xBAJ',(500,1000))
            refresh=True
    friendImg.flush()
    if not friendImg:
        time.sleep(.2)
        return base.press('8')
    while True:
        timer=time.time()
        while True:
            for i in(i[0]for i in friendImg.items()if check.tap(i[1])):
                skillInfo[friendPos],houguInfo[friendPos]=(lambda r:(lambda p:([[skillInfo[friendPos][i][j]if p[i*3+j]=='x'else int(p[i*3+j])for j in range(3)]for i in range(3)],[houguInfo[friendPos][i]if p[i+9]=='x'else int(p[i+9])for i in range(2)]))(r.group())if r else(skillInfo[friendPos],houguInfo[friendPos]))(re.search('[0-9x]{11}$',i))
                return logger.info(f'Friend {i}')
            if check.isListEnd((1860,1064)):break
            base.swipe((800,900,800,300))
            Check(.3)
        if refresh:sleep(max(0,timer+10-time.time()))
        doit('\xBAJ',(500,1000))
        refresh=True
        while not Check(.2).isChooseFriend():
            if check.isNoFriend():
                sleep(10)
                doit('\xBAJ',(500,1000))
def battle():
    turn,stage,stageTurn,servant=0,0,0,[0,1,2]
    while True:
        if Check(0,.1).isTurnBegin():
            turn+=1
            stage,stageTurn=(lambda x:[x,stageTurn+1if stage==x else 1])(Check(.5).getStage())
            skill,newPortrait=check.isSkillReady(),check.getPortrait()
            if turn==1:stageTotal=check.getStageTotal()
            else:servant=(lambda m,p:[m+p.index(i)+1if i in p else servant[i]for i in range(3)])(max(servant),[i for i in range(3)if servant[i]<6and cv2.matchTemplate(newPortrait[i],portrait[i],cv2.TM_SQDIFF_NORMED)[0][0]>.04])
            if stageTurn==1and dangerPos[stage-1]:doit(('\x69\x68\x67\x66\x65\x64'[dangerPos[stage-1]-1],'\xDC'),(250,500))
            portrait=newPortrait
            logger.info(f'{turn} {stage} {stageTurn} {servant}')
            for i,j in((i,j)for i in range(3)if servant[i]<6for j in range(3)if skill[i][j]and skillInfo[servant[i]][j][0]and min(skillInfo[servant[i]][j][0],stageTotal)<<8|skillInfo[servant[i]][j][1]<=stage<<8|stageTurn):
                doit(('ASD','FGH','JKL')[i][j],(300,))
                if skillInfo[servant[i]][j][2]:doit('234'[skillInfo[servant[i]][j][2]-1],(300,))
                sleep(2.3)
                while not Check().isTurnBegin():pass
            for i in(i for i in range(3)if stage==min(masterSkill[i][0],stageTotal)and stageTurn==masterSkill[i][1]):
                doit(('Q','WER'[i]),(300,300))
                if masterSkill[i][2]:doit('234'[masterSkill[i][2]-1],(300,))
                sleep(2.3)
                while not Check().isTurnBegin():pass
            doit(' ',(2350,))
            doit((lambda c,h:['678'[i]for i in sorted((i for i in range(3)if h[i]),key=lambda x:-houguInfo[servant[x]][1])]+['12345'[i]for i in sorted(range(5),key=(lambda x:c[x]<<1&2|c[x]>>1&1)if any(h)else(lambda x:-1if c[x]!=-1and c.count(c[x])>=3else c[x]<<1&2|c[x]>>1&1))])(Check().getABQ(),[servant[i]<6and j and houguInfo[servant[i]][0]and stage>=min(houguInfo[servant[i]][0],stageTotal)for i,j in zip(range(3),check.isHouguReady())]),(270,270,2270,1270,6000))
        elif check.isBattleFinished():
            logger.info('Battle Finished')
            return True
        elif check.isBattleFailed():
            logger.warning('Battle Failed')
            return False
def main(appleCount=0,appleKind=0,battleFunc=battle):
    apple,battle=0,0
    def eatApple():
        if Check(.7,.3).isApEmpty():
            nonlocal apple,appleCount
            if apple==appleCount:
                logger.info('Ap Empty')
                base.press('Z')
                return True
            else:
                apple+=1
                logger.info(f'Apple {apple}')
                doit(('W4K8'[appleKind],'L'),(400,1200))
                return False
    global tobeTerminatedFlag
    while True:
        while True:
            if Check(.3,.3).isBegin():
                if not tobeTerminatedFlag:return
                tobeTerminatedFlag-=1
                base.press('8')
                if eatApple():return
                chooseFriend()
                while not Check(.1).isBattleBegin():pass
                if partyIndex and check.getPartyIndex()!=partyIndex:doit(('\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79'[partyIndex-1],' '),(1000,400))
                doit(' 8',(800,10000))
                break
            if check.isBattleContinue():
                if not tobeTerminatedFlag:return base.press('F')
                tobeTerminatedFlag-=1
                base.press('K')
                if eatApple():return
                chooseFriend()
                break
            if check.isAddFriend():base.press('X')
            base.press(' ')
        battle+=1
        logger.info(f'Battle {battle}')
        doit('    ',(200,200,200,200))if battleFunc()else doit('BIJ',(500,500,500))
def userScript():
    while not Check(0,.2).isTurnBegin():pass
    #                            S    2    D    F    2    G   H    2   J   2    K    L    2   Q   E   2     _   6   5    4
    doit('S2DF2GH2J2KL2QE2 654',(350,3000,3000,350,3000,3000,350,3000,350,3000,3000,350,3000,300,350,3000,2400,350,350,10000))
    while not Check(0,.2).isBattleFinished():assert not check.isTurnBegin()
    return True
