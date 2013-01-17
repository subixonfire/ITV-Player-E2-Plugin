# coding: utf-8
###########################################################################
##################### By:subixonfire  www.satforum.me #####################

""" This file is part of ITV Player E2 Plugin.

    ITV Player E2 Plugin is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ITV Player E2 Plugin is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>."""
    
###########################################################################
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.InfoBar import MoviePlayer as MP_parent
from Screens.InfoBar import InfoBar
from Screens.MessageBox import MessageBox
from ServiceReference import ServiceReference
from enigma import eServiceReference, eConsoleAppContainer, ePicLoad, getDesktop, eServiceCenter, loadPic
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Pixmap import Pixmap
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from cookielib import CookieJar
import urllib, urllib2, re, time, os, random
import socket

socket.setdefaulttimeout(300) #in seconds

     

###########################################################################

class ITVplayer(Screen):
    wsize = getDesktop(0).size().width()
    hsize = getDesktop(0).size().height()
    print "wsize " + str(wsize)
    plugin_dir = os.path.dirname(os.path.realpath(__file__)) + "/"
    
    skin = """
        <screen flags="wfNoBorder" position="0,0" size=\"""" + str(wsize) + "," + str(hsize) + """\" title="ITV" >
        <ePixmap alphatest="on" pixmap=\"""" + plugin_dir + """main.png" position="0,0" size=\"""" + str(wsize) + "," + str(hsize) + """\"  zPosition="-2"/>
            <widget name="myMenu" position="235,385" size=\"""" + str(wsize - 502) + "," + str(hsize - 470) + """\" scrollbarMode="showOnDemand"/>
            <widget name="pix" position=\"""" + str((wsize /2) + 300) + """,110" size="250,350" zPosition="7"/>
        
        </screen>"""
            
    fileTitle1 = ""
    fileTitle2 = ""
    theFunc = "main"
    downDir = "/mnt/hdd"
    oldlist = []
    osdList = []
    osdList.append((_("ITV Player    (This will take some time to load.)"), "itv"))
    osdList.append((_("Help / About"), "help"))
    historyList = []
    historyInt = 0
    rtmp = ""
    
        
    def __init__(self, session):
        
       
        Screen.__init__(self, session)
        self["myMenu"] = MenuList(self.osdList)
        self['pix'] = Pixmap()
        self["myActionMap"] = ActionMap(["SetupActions","ColorActions"],
        {
        "ok": self.go,
        "cancel": self.cancel
        }, -1)
        
           
        
    
    def go(self):
    
        
        
        returnTitle = self["myMenu"].l.getCurrentSelection()[0]
        returnValue = self["myMenu"].l.getCurrentSelection()[1]
        returnIndex = self["myMenu"].getSelectedIndex()
        
        if not self.theFunc == "itv2": 
            if not returnValue == "help":
                try:
                    self.historyList[int(self.historyInt)] = [self.theFunc, self.osdList, returnIndex]
                except:    
                    self.historyList.append([self.theFunc, self.osdList, returnIndex])
                self.historyInt = self.historyInt + 1
        
        
        if self.theFunc == "main":
            if returnValue == "itv":
               
                self.oldList = self.osdList
                
                
                url = "http://www.itv.com/_data/xml/CatchUpData/CatchUp360/CatchUpMenu.xml"
    
                try:
                    req = urllib2.Request(url,)
                    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                    response = urllib2.urlopen(req)   
                    htmldoc = str(response.read())
                    response.close()
                    print htmldoc 
                except :
                    print "jebiga gethtml"
                
                
                
                
                xList = (re.compile ('<ProgrammeId>(.+?)</ProgrammeId>.+?<ProgrammeTitle>(.+?)</ProgrammeTitle>',re.DOTALL).findall(htmldoc))
                #for x in xList:
    
                    #try:    
                    #    progTitle = re.search('<ProgrammeTitle>(.*?)</ProgrammeTitle>', x).group(1)
                    #    progId = re.search('<ProgrammeId>(.+?)</ProgrammeId>', x).group(1)
                    #except:
                    #    pass
                    #self.osdList.append((_(progTitle), progId))
                self.osdList = [(x[1], x[0]) for x in xList]
                self["myMenu"].setList(self.osdList) 
                   
               
                self.theFunc = "itv"
                
            if returnValue == "help":
                self.session.open(MessageBox,_("This is a preview alpha release, no help awailable. \nThis plugin will work only for users inside UK or with a UK ip!\n\nDeveloped by: subixonfire\nGfx by: Ev0 \n\nIf you like my work feel free to donate. This will help future work on this and other plugins. "), MessageBox.TYPE_INFO)        
                        
        elif self.theFunc == "itv":
        
            self.oldList = self.osdList
            
            url = "http://www.itv.com/_app/Dynamic/CatchUpData.ashx?ViewType=1&Filter=" + returnValue + "&moduleID=115107"
    
            try:
                req = urllib2.Request(url, "GET")
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3 Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)   
                htmldoc = str(response.read())
                response.close() 
            except :
                print "jebiga gethtml"
    
            xList = (re.compile ('<h3><a href=".+?Filter=([0-9]+?)">(.+?)</a></h3>.+?<p class="date">(.+?)</p>',re.DOTALL).findall(htmldoc))
            self.osdList = [(x[1] + " " + x[2], x[0]) for x in xList]
            self["myMenu"].setList(self.osdList)
            
            self.theFunc = "itv1"
            
            
        elif self.theFunc == "itv1":
        
            self.fileTitle1 = returnTitle
            self.fileTitle2 = ""
            
            self.oldList = self.osdList
            
            soapMessage = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	  <SOAP-ENV:Body>
	    <tem:GetPlaylist xmlns:tem="http://tempuri.org/" xmlns:itv="http://schemas.datacontract.org/2004/07/Itv.BB.Mercury.Common.Types" xmlns:com="http://schemas.itv.com/2009/05/Common">
	      <tem:request>
		<itv:RequestGuid>FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF</itv:RequestGuid>
		<itv:Vodcrid>
		  <com:Id>%s</com:Id>
		  <com:Partition>itv.com</com:Partition>
		</itv:Vodcrid>
	      </tem:request>
	      <tem:userInfo>
		<itv:GeoLocationToken>
		  <itv:Token/>
		</itv:GeoLocationToken>
		<itv:RevenueScienceValue>scc=true; svisit=1; sc4=Other</itv:RevenueScienceValue>
	      </tem:userInfo>
	      <tem:siteInfo>
		<itv:Area>ITVPLAYER.VIDEO</itv:Area>
		<itv:Platform>DotCom</itv:Platform>
		<itv:Site>ItvCom</itv:Site>
	      </tem:siteInfo>
	    </tem:GetPlaylist>
	  </SOAP-ENV:Body>
	</SOAP-ENV:Envelope>
	"""%returnValue
    
            url = 'http://mercury.itv.com/PlaylistService.svc'
	
	
            req = urllib2.Request(url, soapMessage)
            req.add_header("Host","mercury.itv.com")
            req.add_header("Referer","http://www.itv.com/mercury/Mercury_VideoPlayer.swf?v=1.6.479/[[DYNAMIC]]/2")
            req.add_header("Content-type","text/xml; charset=\"UTF-8\"")
            req.add_header("Content-length","%d" % len(soapMessage))
            req.add_header("SOAPAction","http://tempuri.org/PlaylistService/GetPlaylist")    
            response = urllib2.urlopen(req)   
            htmldoc = str(response.read())
            response.close() 
    
            res = re.search('<VideoEntries>.+?</VideoEntries>', htmldoc, re.DOTALL).group(0)
            #print res

            rtmp = re.compile('(rtmp[^"]+)').findall(res)[0]
            self.rtmp = rtmp.replace('&amp;','&')
            print rtmp
            playpath = re.compile('(mp4:[^\]]+)').findall(res)
            print playpath
            
            self.osdList = []
            for x in playpath:
            
                try:    
                    y = "Quality: " + re.search('rtmpecatchup/(.+?)/', x).group(1)
                except:
                    y = "Unknown Quality"
                self.osdList.append((_(y), x))
                print x
            
            
            self["myMenu"].setList(self.osdList)
            
            
            
            self.theFunc = "itv2"
                    
        
        elif self.theFunc == "itv2":
        
            print returnValue
            returnUrl = self.rtmp + " swfurl=http://www.itv.com/mercury/Mercury_VideoPlayer.swf playpath=" + returnValue + " swfvfy=true"
            print returnUrl
            
            if returnUrl:       
                fileRef = eServiceReference(4097,0,returnUrl)
                fileRef.setData(2,10240*1024)
                fileRef.setName(self.fileTitle1)
                self.session.open(MoviePlayer, fileRef)
                     
        
           
        self["myMenu"].moveToIndex(0)        
        #print self.theFunc + " " + returnValue
        
    
    def cancel(self):
        print self.theFunc
        if self.historyInt > 0:
            self.historyInt = self.historyInt - 1
            self.theFunc = self.historyList[self.historyInt][0]
            self.osdList = self.historyList[self.historyInt][1]
            self["myMenu"].setList(self.osdList)
            self["myMenu"].moveToIndex(self.historyList[self.historyInt][2])
            
            print "#################### radiiiiii "
            
        else:    
            self.close(None)
               
###########################################################################

def main(session, **kwargs):
    
    burek = session.open(ITVplayer)
        
                  
###########################################################################    

class MoviePlayer(MP_parent):
	def __init__(self, session, service):
		self.session = session
		self.WithoutStopClose = False
		
		MP_parent.__init__(self, self.session, service)
		     

	def leavePlayer(self):
		self.is_closing = True
		self.close()

	def leavePlayerConfirmed(self, answer):
		self.is_closing = True
		self.close

	def doEofInternal(self, playing):
		if not self.execing:
			return
		if not playing :
			return
		self.leavePlayer()

	def showMovies(self):
		self.WithoutStopClose = False
		self.close()

	def movieSelected(self, service):
		self.leavePlayer(self.de_instance)

	def __onClose(self):
		if not(self.WithoutStopClose):
			self.session.nav.playService(self.lastservice)	
###########################################################################

def Plugins(**kwargs):
    return PluginDescriptor(
        name="ITV Player",
        description="Preview of the new ITV Player.",
        where = [ PluginDescriptor.WHERE_EXTENSIONSMENU, PluginDescriptor.WHERE_PLUGINMENU ],
        icon="./icon.png",
        fnc=main)


