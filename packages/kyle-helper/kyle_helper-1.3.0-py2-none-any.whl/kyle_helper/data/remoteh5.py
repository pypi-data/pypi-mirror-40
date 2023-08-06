#import subprocess
from hashlib import sha512
from kyle_helper.data.utility import rsync

def copy_remote_h5(h5file, cache_dir='/tmp', offline=False):
   h = sha512()
   h.update(h5file)
   hh = h.hexdigest()
   tmpfile = cache_dir + "/{}.h5".format(hh)
   if not offline:
       rsync("av", h5file, tmpfile)
   #subprocess.call(['rsync', '-avP', h5file, tmpfile])
   return tmpfile

