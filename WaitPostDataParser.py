# This program can load WaitPost.db and to read
# Author    : Kang-Min Wang ( Aminzai )
# Mail      : lagunawang --AT-- Gmail.com
# Date      : Wed Oct  7 14:00:27 CST 2009

#import optparse
import pickle
import os

#parser = optparse.OptionParser()
#parser.add_option( '-f' , '--file' , dest='filename' , default='WaitPostBak.db' , help='Input file, Default file is "WaitPostBak.db"' )
#args = ['-f' , 'foo.txt']
#(options, args) = parser.parse_args(args)
#a = parser.parse_args(args)
#print args

if os.path.exists( 'WaitPostBak.db' ):
  file  = open( 'WaitPostBak.db' , 'rb')
  data = pickle.load( file )

  for i in data:
    print i
else:
  print 'file not find!!'

