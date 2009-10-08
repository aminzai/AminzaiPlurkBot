#!/usr/bin/env python
######
# This program can load WaitPost.db and to read
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Wed Oct  7 14:00:27 CST 2009
#####

#import optparse
import pickle
import os
import sys

#parser = optparse.OptionParser()
#parser.add_option( '-f' , '--file' , dest='filename' , default='WaitPostBak.db' , help='Input file, Default file is "WaitPostBak.db"' )
#args = ['-f' , 'foo.txt']
#(options, args) = parser.parse_args(args)
#a = parser.parse_args(args)
#print args

###### Function
def LoadData():
  if not os.path.exists( 'WaitPostBak.db' ):
    print 'file not find!!'
    sys.exit()
  else:
    File  = open( 'WaitPostBak.db' , 'rb')
    RawData = pickle.load( File )
    File.close()
    return RawData

def SaveData( data ):
  tmp = []
  for i in data.keys():
    tmp.append( data[ i ] )
  FileOut  = open( 'WaitPostBak.db' , 'wb')
  pickle.dump( tmp , FileOut )
  FileOut.close()

def Functions( data , cmd ):
  if data.has_key( cmd ):
    del data[ int( cmd ) ]
  else:
    if cmd == 's':
      SaveData( data )
    elif cmd == 'w':
      SaveData( data )
      sys.exit()
    elif cmd == 'q':
      print 'Bye!!'
      sys.exit()
    elif cmd == 'h':
      print """
      h : help 
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
  cmd = raw_input('Type num to del item, or type h to get help:')
  data = Functions( data , cmd )
