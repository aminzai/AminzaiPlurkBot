#!/usr/bin/env python
## -*- coding: utf-8 -*-
# encoding uft-8
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Thu Oct  1 11:05:15 CST 2009

# By System
import sys
import os
import time
import pickle
import random
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
# By local
import plurkapi
import RSS_Reader
from ShortUrlGen import ShortURL as sUrl

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
    """Save a backup file to disk"""
    file = open( 'WaitPostBak.db' , 'wb' )
    pickle.dump( data , file )
    file.close()

  def Restore_Wait_Post_From_File( self ):
    """Restore the backup file"""
    file = open( 'WaitPostBak.db' , 'rb' )
    data = pickle.load( file )
    file.close()
    return data

  def Restore_Post( self , PostData , WaitPost ):
    """Get the new post data & save back to file"""
    WaitPost.append( PostData )
    random.shuffle( WaitPost )
    returnPostDat = WaitPost.pop()
    self.Backup_Wait_Post_To_File( WaitPost )
    return returnPostDat
  def BeFrineds( self ):
    """Auto Add friend ,if have anybody want be friend"""
    alerts = self.Client.getAlerts()
    if not alerts > 0 :
      self.Client.befriend( alerts )
  
  def ResizePost( self , data , max = 110 , min = 40):
    """Cut Post length"""
    if len( data ) > max :
      return data[0:max-5] + '...'
    elif len( data ) < min :
      return data  + ' ' +str( random.random() )[ random.randint( 2 , 5 ) : -1  ]
    else:
      return data

  def PostDataGen( self , item ):
    """Generator the post data via some post style"""
    title = item.find('title').text.strip().encode('utf-8')
    su = sUrl()
    link = su.Random_Short_Url_Gen( item.find('link').text.strip().encode('utf-8') )
    rand_style = random.randint( 0 , 4 )
    if rand_style == 0 :
       return link + ' (' + self.ResizePost( title , 160 , 100) + ') '
    elif rand_style == 1 :
       return self.ResizePost( title , 160 , 100 ) + ' ' + link + ' '
    elif rand_style == 2 :
       return self.ResizePost( title , 160 , 100 ) + ' ' + link + ' (**連結**)'
    elif rand_style == 3 :
       return link + ' (**連結**)' + self.ResizePost( title , 150 , 100 )
    elif rand_style == 4 :
       return link + ' ' + self.ResizePost( title , 160 , 100 )

  def mainRun( self ):
    """Main Function"""
    rets = self.rss.Read_RSS_Source()
    self.WaitPost = []
    #Reload File
    if os.path.exists( 'WaitPostBak.db' ):
      RestoreData = self.Restore_Wait_Post_From_File()
      print "Restore Data & Post to Plurk"
      DelayTime = random.randint( 60 , 166 )
      print 'Delay Time(Jump 10~11min):', DelayTime
      time.sleep( DelayTime )
      for y in range( 0 , len( RestoreData ) ):
        random.shuffle( RestoreData )
        self.Backup_Wait_Post_To_File( RestoreData )
        PostData = RestoreData.pop()
        while 1:
          try:
            print 'Restore & Post:',PostData
            self.Client.addPlurk( lang='tr_ch', qualifier = 'says' , content = PostData )
          except:
            print "Plurk raise error!!,We will retry....."
            tmp = []
            PostData = PostData + '..'
            tmp.append( PostData )
            tmp.extend( RestoreData )
            RestoreData = tmp
            PostData = RestoreData.pop()
            self.Backup_Wait_Post_To_File( RestoreData )
            DelayTime = random.randint( 50 , 160 )
            print 'Delay Time(Jump 10~11min):', DelayTime
            time.sleep( DelayTime )
          else:
            DelayTime = random.randint( 60 , 170 )
            print 'Delay Time:', DelayTime
            time.sleep( DelayTime )
            break
        if ( y % 4 ) == 3:
          DelayTime = random.randint( 1800 , 3800 )
          print '(Long time Delay)Delay Time:', DelayTime
          time.sleep( DelayTime )

    #Get all data
    for i in range( 0 , len( rets ) ):
      for j in range ( 0 , len( rets[i][1] ) ):
        source_Title = rets[i][0] 
        if j > 3 : #Control Max Data
          break
        item = rets[i][1][j]
        data = self.PostDataGen( item )

        if j == 0:
          self.newestTitle = data
          print source_Title + 'The Newest Title:',data
          self.rss.Save_Last_RSS_Data( [ source_Title , self.newestTitle ] )

        if self.rss.Check_Last_RSS_Data( [ source_Title , data ] ) :
          print 'Found:',data
          break
        self.WaitPost.append( data )


    random.shuffle( self.WaitPost )

    for x in range( 0 , len( self.WaitPost ) ):
      random.shuffle( self.WaitPost )
      self.Backup_Wait_Post_To_File( self.WaitPost )
      PostData = self.WaitPost.pop()
      while 1:
        try:
          print 'Post:',PostData
          self.Client.addPlurk( lang='tr_ch', qualifier = 'says' , content = PostData )
        except:
          print "Plurk raise error!!,We will retry....."
          DelayTime = random.randint( 60 , 170 )
          print 'Delay Time:', DelayTime
          time.sleep( DelayTime )
          tmp = []
          PostData = PostData + '..'
          tmp.append( PostData )
          tmp.extend( self.WaitPost )
          self.WaitPost = tmp
          PostData = self.WaitPost.pop()
          self.Backup_Wait_Post_To_File( self.WaitPost )
        else:
          DelayTime = random.randint( 60 , 170 )
          print 'Delay Time:', DelayTime
          time.sleep( DelayTime )
          break
      if ( y % 4 ) == 3:
        DelayTime = random.randint( 1800 , 3800 )
        print '(Long time Delay)Delay Time:', DelayTime
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
