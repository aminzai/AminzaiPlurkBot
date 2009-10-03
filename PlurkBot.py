#!/usr/bin/env python
## -*- coding: utf-8 -*-
# encoding uft-8
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Thu Oct  1 11:05:15 CST 2009
import plurkapi
import sys
import RSS_Reader
import time
from twisted.internet import reactor,task

class PlurkBot:
  """That is a plurk bot,that can query a lot of rss resource from internet """
  def __init__( self ):
    self.Client = plurkapi.PlurkAPI()
    username , password =  self.GetPlurkAccountInf()
    
    if self.Client.login( username , password ) == False:
      print "ERROR: Can't Login in to Plurk"
      sys.exit()
    else:
      print "Login Succeed!!"
    #Setup RSS Data
    self.rss = RSS_Reader.RSS_Reader()

  def GetPlurkAccountInf( self ):
    """Get Plurk Account information via account.inf """
    try:
      AccountFile = open ( 'account.inf' , 'r' )
    except:
      print "ERROR: Can't not open 'account.inf'!!"
      sys.exit()

    # AccountInf's data type [ 'username' , 'password' ]
    AccountInf = AccountFile.readline().rstrip().split()
    return AccountInf 
  
  def BuildTinyURL( self , url ):
    tinyapiurl = "http://tinyurl.com/api-create.php?url="
    try:
      tinyurl = lhtml.parse(tinyapiurl+url).xpath("//body")[0].text_content()
    except:
      return url
    return tinyurl

  def BeFrineds( self ):
    """Auto Add friend ,if have anybody want be friend"""
    if len( self.Client.getAlerts() ):
      Client.befriend( alerts )

  def mainRun( self ):
    """Main Function"""
    rets = self.rss.Read_RSS_Source()
    for i in range( 0 , len( rets ) ):
      for j in range ( 0 , len( rets[i][1] ) ):
        source_Title = '[' + rets[i][0] + ']'
        item = rets[i][1][j]
        title = item.find('title').text.strip().encode('utf-8')
        link = self.BuildTinyURL( item.find('link').text.strip().encode('utf-8') )
        data = source_Title +' ' + link + ' (' + title + ') '
        print data

        if self.rss.Check_Last_RSS_Data( [ rets[i][0] , title ] ) :
          print "Found:", data
          break
        
        self.Client.addPlurk( lang='tr_ch', qualifier = 'says' , content = data )

        time.sleep(60*j)

        if j == 0:
          self.rss.Save_Last_RSS_Data( [ rets[i][0] , title ] )
          
if __name__ == '__main__' :
  bot = PlurkBot()

  #daily_run
  daily_run = task.LoopingCall( bot.mainRun() )
  daily_run.start( 300 )

  #be Friends
  beFriends = task.LoopingCall( bot.BeFrineds() )
  beFriends.start( 600 )

  reactor.run()
