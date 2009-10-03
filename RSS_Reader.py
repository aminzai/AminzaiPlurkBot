#!/usr/bin/env python
### -*- coding: utf-8 -*-
# encoding: utf-8
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Wed Sep 30 11:23:52 CST 2009

from lxml import etree
import sys
import os
import pickle

class RSS_Reader:
  """Read RSS file"""
  def __init__( self , filename = 'rss_source.inf' ):
    self.Set_RSS_source_file( filename )
    #self.Read_RSS_Source()

  def Set_RSS_source_file( self , filename ):
    """Set RSS Source file name"""
    self.filename = filename

  def Get_RSS_source_file( self ):
    """Get RSS Source file name"""
    return self.filename

  def Save_Last_RSS_Data( self , data ):
    """Save Last RSS Data to a file"""
    tmp = self.Read_Last_RSS_Data()
    tmp[ data[0] ] = data[1]
    f = open( 'LastRSSData.db' , 'wb' )
    pickle.dump( tmp , f ) 
    f.close()

  def Read_Last_RSS_Data( self ):
    """Read the last RSS Data from pickle file"""
    try:
      f = open( 'LastRSSData.db' , 'rb' )
    except IOError:
      os.system('touch LastRSSData.db')
    
    try:
      data = pickle.load( f )
    except EOFError:
      f.close()
      f = open( 'LastRSSData.db' , 'wb' )
      pickle.dump( {'RSS':'Start'} , f )
      f.close()
      f = open( 'LastRSSData.db' , 'rb' )
      data = pickle.load( f )
    except UnboundLocalError:
      f.close()
      f = open( 'LastRSSData.db' , 'wb' )
      pickle.dump( {'RSS':'Start'} , f )
      f.close()
      f = open( 'LastRSSData.db' , 'rb' )
      data = pickle.load( f )
    f.close()
    
    return data


  def Check_Last_RSS_Data( self , check_data ):
    """ That will open LastRSSData.db to check """
    check = self.Read_Last_RSS_Data()
    if check.has_key( check_data[0] ):
      if check[ check_data[0] ] == check_data[1]:
        return False
      else:
        return True
    else:
        return False

  def Read_RSS_Source( self ):
    """Read RSS by RSS source file"""
    try: 
      file = open( self.Get_RSS_source_file() , 'r' )
    except:
      print ("ERROR:Can't not open RSS source file!")
      sys.exit()

    # source data type [ 'Tilte' , 'URL']
    source = [ x.rstrip().split() for x in file.readlines() if not x[0] == '#' ]

    rets = []
    for i in range( 0 , len( source ) ):
      try:
        rets.append( [ source[i][0] , etree.parse( source[i][1] ).xpath('//item') ] )
      except:
        continue

    #print rets[0][1]
    file.close()
    return rets

## Test Function 
if __name__ == '__main__' :
  x = RSS_Reader()
  print x.Read_RSS_Source()
