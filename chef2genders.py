#!/usr/bin/python

'''
Creates a pdsh genders file from chef nodes 
'''

import datetime
import hashlib
import json
import subprocess

current_genders = '/etc/genders'

date = datetime.datetime.now()
new_genders = '/etc/pdsh/genders-%s%s%s%s%s%s%s' % (date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond)
gf = open(new_genders, 'w+')
print 'Getting nodes from chef...'
my_json = json.loads(subprocess.Popen(['knife', 'search', 'node', 'chef_environment:_default NOT tags:disabled', '-a', 'roles', '-f', 'json'], stdout=subprocess.PIPE).stdout.read())
nodes = my_json['rows']
for node in nodes:
  for k,v in node.iteritems():
    if len(v['roles']) > 0:
      pdsh_node = '%s %s,pdsh_rcmd_type=ssh\n' % (k, ','.join(v['roles']))
      gf.write(pdsh_node)

gf.close()

md5sum_current = hashlib.md5(open(current_genders).read()).hexdigest()
md5sum_new = hashlib.md5(open(new_genders).read()).hexdigest()

if md5sum_current != md5sum_new:
  print 'Updating the genders file'
  subprocess.call(['ln', '-fs', new_genders, current_genders])
else:
  print 'No changes were made to the genders file'
  subprocess.call(['rm', new_genders])
