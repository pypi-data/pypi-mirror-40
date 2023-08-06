from uuid import uuid4
import subprocess
import logging
import numpy as np

def excel_to_array(s_, header_rows=1, return_header_dict=False):
    """Takes a multi-line, tab-delimited string (e.g. copied from
    Microsoft Excel and converts it to a numpy array.

    Args:
        s_ (string): A string representation of the data.
            Can include a header and whitespace at the
            beginning and end.
        header_rows (int): default 1.  Number of initial rows
            to consider the header
        return_header_dict (boolean): Whether or not to return a dictionary
            of the header keys/indices, e.g.  hd['x'] == 0


        

    """



    s_ = s_.rstrip().lstrip()
    tmpfile = "/tmp/{}".format(uuid4())
    with open(tmpfile, 'w') as F:
        F.write(s_)

    a = np.genfromtxt(tmpfile, delimiter="\t", dtype=np.float32)
    if not(np.all(np.isnan(a[0,:]))) and header_rows==1:
        logging.warning("Not all elements in the first line were interpreted as strings.  Are you sure the default header_rows=1 is what you want?")
    a = a[header_rows:,:]
    header = np.genfromtxt(tmpfile, delimiter="\t", skip_footer=len(a), dtype=np.str)
    if return_header_dict:
        hd = {}
        for i, head in enumerate(header):
            hd[head] = i
        return header, a, hd
    else:
        return header, a

def spreadsheet_to_array(*args, **kwargs):
    return excel_to_array(*args, **kwargs)



def rsync(flags='a', source=None, destination=None):
   assert source is not None and destination is not None, "Source and destination must be specified"

   if 'v' in flags:
       print("RSYNC:source:{}".format(source))
       print("RSYNC:destination:{}".format(destination))
   p = subprocess.Popen(["rsync","-"+flags, source, destination], stdout=subprocess.PIPE, bufsize=1)
   for line in iter(p.stdout.readline, b''):
       print (line,)
   p.stdout.close()
   p.wait()
   return 1-p.returncode


