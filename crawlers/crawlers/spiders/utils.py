def remove_unicode(s):
    return s.encode('ascii', 'ignore')
# for Python 3
#      return s.encode('ascii', 'ignore').decode('utf-8')
