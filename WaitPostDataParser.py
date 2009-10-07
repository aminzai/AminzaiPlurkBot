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
  file.close()


data = {}

for i in range( len( RawData ) ):
  data[ str( i ) ] =  RawData[ i ]

while 1:
 for i in data.keys():
   print i , data[ i ]
 DelNum = raw_input('Type num to del item, or type q to quit, type w to save & quit:')
 if DelNum == 'q':
   print 'Bye!'
   sys.exit()
 elif DelNum == 'w':
   break
 elif DelNum == '':
   continue
 else:
   del data[ DelNum ]


FileOut  = open( 'WaitPostBak.db' , 'wb')
RawData = pickle.load( FileOut )
tmp = []
for i in data.keys():
  tmp.append( data[ i ] )

pickle.dump( tmp , FileOut )

FileOut.close()
