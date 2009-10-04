#!/usr/bin/env python
## -*- coding: utf-8 -*-
# encoding uft-8
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Thu Oct  1 11:05:15 CST 2009
import plurkapi
import sys
import os
import RSS_Reader
import time
import pickle
import random
try:
  import lxml.html as lhtml
except:
  print "Warring: Can't import lxml.html, That will can't use tinyURL"
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

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

  def Backup_Wait_Post_To_File( self , data ):
    file = open( 'WaitPostBak.db' , 'wb' )
    pickle.dump( data , file )
    file.close()

  def Restore_Wait_Post_From_File( self ):
    file = open( 'WaitPostBak.db' , 'rb' )
    data = pickle.load( file )
    file.close()
    return data
  
  def BuildTinyURL( self , url ):
    tinyapiurl = "http://tinyurl.com/api-create.php?url="
    try:
      tinyurl = lhtml.parse(tinyapiurl+url).xpath("//body")[0].text_content()
    except:
      return url
    return tinyurl

  def BeFrineds( self ):
    """Auto Add friend ,if have anybody want be friend"""
    alerts = self.Client.getAlerts()
    if not alerts > 0 :
      self.Client.befriend( alerts )
  
  def ResizePost( self , data ):
    print 'Length:', len( data )
    if len( data ) > 130 :
      resizedata = data[0:130] + '..)'
      print 'Resize Post: ' + resizedata
      print 'Resized Length: ' + len( resizedata )
      return resizedata 
    else:
      return data

  def mainRun( self ):
    """Main Function"""
    rets = self.rss.Read_RSS_Source()
    self.WaitPost = []
    #Reload File
    if os.path.exists( 'WaitPostBak.db' ):
      RestoreData = self.Restore_Wait_Post_From_File()
      print "Restore Data & Post to Plurk"
      for y in range( 0 , len( RestoreData ) ):
        self.Backup_Wait_Post_To_File( RestoreData )
        PostData = RestoreData.pop()
        print 'Restore & Post:',PostData
        while 1:
          try:
            self.Client.addPlurk( lang='tr_ch', qualifier = 'says' , content = self.ResizePost( PostData ) )
          except:
            print "Plurk raise error!!,We will retry....."
            DelayTime = random.randint( 30 , 60 )
            print 'Delay Time:', DelayTime
            time.sleep( DelayTime )
          else:
            break

    #Get all data
    for i in range( 0 , len( rets ) ):
      source_Title = rets[i][0] 
      for j in range ( 0 , len( rets[i][1] ) ):
        if j > 10 : #Control Max Data
          break
        item = rets[i][1][j]
        title = item.find('title').text.strip().encode('utf-8')
        link = self.BuildTinyURL( item.find('link').text.strip().encode('utf-8') )
        data = '[' + source_Title + '] ' + link + ' (' + title + ') '

        if j == 0:
          self.newestTitle = title
          print 'The Newest Title:',title

        if self.rss.Check_Last_RSS_Data( [ source_Title , title ] ) :
          print 'Found:',data
          break
        self.WaitPost.append( data )

      self.rss.Save_Last_RSS_Data( [ source_Title , self.newestTitle ] )

    for x in range( 0 , len( self.WaitPost ) ):
      self.Backup_Wait_Post_To_File( self.WaitPost )
      PostData = self.WaitPost.pop()
      print 'Post:',PostData
      while 1:
        try:
          self.Client.addPlurk( lang='tr_ch', qualifier = 'says' , content = self.ResizePost( PostData ) )
        except:
          print "Plurk raise error!!,We will retry....."
          DelayTime = random.randint( 30 , 60 )
          print 'Delay Time:', DelayTime
          time.sleep( DelayTime )
        else:
          break
      DelayTime = random.randint( 30 , 60 )
      print 'Delay Time:', DelayTime
      time.sleep( DelayTime )
          
if __name__ == '__main__' :
  bot = PlurkBot()

  #daily_run
  daily_run = LoopingCall( bot.mainRun )
  daily_run.start( 21600.0 )

  #be Friends
  beFriends = LoopingCall( bot.BeFrineds )
  beFriends.start( 3600.0 )

  reactor.run()
