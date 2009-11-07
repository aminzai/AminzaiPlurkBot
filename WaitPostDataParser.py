#!/usr/bin/env python
#================================================
# This program can load WaitPost.db and to read
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Wed Oct  7 14:00:27 CST 2009
#=================================================

#import optparse
import pickle
import os
import sys

import readline, threading
import time

###### Function
class write(threading.Thread):
    def __init__ (self, s):
        threading.Thread.__init__(self)
        self.s = s

    def run(self):
        time.sleep(.01)
        readline.insert_text(self.s)
        readline.redisplay()

def LoadData():
  if not os.path.exists( 'WaitPostBak.db' ):
    print 'file not find!!'
    sys.exit()
  else:
    File  = open( 'WaitPostBak.db' , 'rb')
    RawData = pickle.load( File )
    File.close()
    return RawData

def EditData( data , num ):
    write( data[ int( num ) ] ).start()
    data[ int( num ) ] = raw_input( "Edit: " )

def SaveData( data ):
  if len( data ) == 0 :
    os.system( 'rm -f WaitPostBak.db' )
  else:
    tmp = []
    for i in data.keys():
      tmp.append( data[ i ] )
    FileOut  = open( 'WaitPostBak.db' , 'wb')
    pickle.dump( tmp , FileOut )
    FileOut.close()

def Functions( data , cmd ):
  try:
    if data.has_key( int( cmd[0] ) ):
      del data[ int( cmd ) ]
      return data
  except ValueError:
    pass

  if cmd[0] == 's':
    SaveData( data )
  if cmd[0] == 'e':
    EditData( data , cmd[1] )
  elif cmd[0] == 'w':
    SaveData( data )
    sys.exit()
  elif cmd[0] == 'q':
    print 'Bye!!'
    sys.exit()
  elif cmd[0] == 'h':
    print """
    h : help
    e : edit Data  Ex: e1
    s : Write backup to backup file
    w : Write backup to backup file, and quit
    q : quit without save
    """
    print 'Press any key to continue'
    raw_input()
  else:
    print 'Please type the right command, or type \"h\" to get help'
    print 'Press any key to continue'
    raw_input()
  return data

def PrintData( data ):
  for i in data.keys():
    print i , data[ i ]

#####  Main Run
RawData = LoadData()
data = {}

for i in range( len( RawData ) ):
  data[ i ] =  RawData[ i ]

while 1:
  PrintData( data )
  print '='*40
  cmd = raw_input('Type num to del item, or type h to get help:')
  data = Functions( data , cmd )
  print '='*40
