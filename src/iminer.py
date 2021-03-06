#!/usr/bin/env python
'''
Created on Apr 16, 2010

@author: kling
'''
import threading, os, sys
from image_loader import flickr, storage
from optparse import OptionParser, OptionGroup


usage = """usage: %prog -f [options] tag1 [tag2, ...]
%prog -a REPOSITORY"""

parser = OptionParser(usage=usage)

parser.add_option('-f', '--fetch', action='store_true', dest='fetch', 
                  default='true', help='fetch images corresponding to the tags')

parser.add_option('-a', '--analyze', action='store_true', dest='analyze', 
                  help='analyze the data in specified repository')

group = OptionGroup(parser, 'Mining options', 'These options are valid in combination with the mining option:')
group.add_option('-p','--pages', action='store', type='int', dest='pages',
                  default=1,
                  help='number of pages to get the images from [default: %default]')

group.add_option('-d', '--dir', action='store', type='string', dest='directory',
                  default=os.path.join(os.path.expanduser('~'), 'flickr-analysis'), metavar='DIR',
                  help='the destination directory [default: %default]')

parser.add_option_group(group)


(options, args) = parser.parse_args()


if options.fetch:   # Fetch data from Flickr
    if not args:
        parser.error("at least one tag is required")
        
        destination_dir = os.path.abspath(options.directory)
        if os.listdir(destination_dir):
            sys.exit("Destination directory has to be empty!")

total = 0
storage.FileStorage(options.directory)

class Mythread(threading.Thread):
    
    def __init__(self, tag):
        self.tag = tag
        
        threading.Thread.__init__(self)
        
    def run(self):
        from image_loader import storage
        storage = storage.FileStorage(options.directory)
        print 'Fetching information for tag %r...' % name
        tag = flickr.Tag(self.tag)
        photos = tag.get_thumbs(options.pages)
        print '%s: %i images fetched.' % (self.tag, len(photos))
        print '%s : saving to: %s' % (self.tag, storage.dir)
        storage.save(tag)
        print '%s: done.' % self.tag

for name in args:
    Mythread(name).start()



    