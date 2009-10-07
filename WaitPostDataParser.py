# This program can load WaitPost.db and to read
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Wed Oct  7 14:00:27 CST 2009

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

if not os.path.exists( 'WaitPostBak.db' ):
  print 'file not find!!'
  sys.exit()
else:
  file  = open( 'WaitPostBak.db' , 'rb')
  RawData = pickle.load( file )

data = {}

for i in range( len( RawData ) ):
  data[ i ] =  RawData[ i ]

while 1:
 for i in data.keys():
   print i , data[ i ]
 DelNum = raw_input('Type num to del item, or type q to quit:')
 if DelNum == 'q':
   print 'Bye!'
   sys.exit()
 else:
   del data[ DelNum ]
