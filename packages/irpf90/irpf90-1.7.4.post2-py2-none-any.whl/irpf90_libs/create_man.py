#!/usr/bin/env python2
#   IRPF90 is a Fortran90 preprocessor written in Python for programming using
#   the Implicit Reference to Parameters (IRP) method.
#   Copyright (C) 2009 Anthony SCEMAMA 
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#   Anthony Scemama
#   LCPQ - IRSAMC - CNRS
#   Universite Paul Sabatier
#   118, route de Narbonne      
#   31062 Toulouse Cedex 4      
#   scemama@irsamc.ups-tlse.fr


from variable  import Variable
from variables import variables
from subroutine  import Sub
from subroutines import subroutines
from irpf90_t  import *
from util import *


def do_print_short(file,var):
  assert type(var) == Variable
  print >>file, "%s : %s :: %s %s"%( \
   var.line.filename[0].ljust(35),
   var.type.ljust(30),
   var.name.ljust(25),
   build_dim(var.dim) )

######################################################################
def process_doc(file,line):
  assert type(line) == str
  line = line.strip()
  if line == "":
    line = ".br"
  print >>file, line

######################################################################
def process_deps(file,l):
  assert type(l) == list
  for v in l:
    print >>file, "%s\n.br"%(v,)

######################################################################
def process_types(file,var):
  assert type(var) == Variable
  vars = [var.name] + var.others
  for var in vars:
    name = var
    var = variables[var]
    Type = var.type
    dim = build_dim(var.dim)
    print >>file, "%s\t:: %s\t%s"%(Type,name,dim)

######################################################################
def do_print(var):
  assert type(var) == Variable
  filename = var.line.filename[0]
  name = var.name
  file = open("%s%s.l"%(mandir,var.name), "w")
  print >>file, '.TH "IRPF90 entities" l %s "IRPF90 entities" %s'%(name,name)
  if var.same_as != var.name:
    var = variables[var.same_as]
  print >>file, ".SH Declaration"
  print >>file, ".nf"
  process_types(file,var)
  print >>file, ".ni"
  if var.doc != []:
   print >>file, ".SH Description"
   for l in var.doc:
     process_doc(file,l)
  print >>file, ".SH File\n.P"
  print >>file, filename
  if var.needs != []:
    var.needs.sort()
    print >>file, ".SH Needs"
    process_deps(file,var.needs)
  if var.needed_by != []:
    var.needed_by.sort()
    print >>file, ".SH Needed by"
    process_deps(file,var.needed_by)
  print >>file, ".SH Instability factor"
  fo = len(var.children)
  fi = len(var.parents)
  print >>file, "%5.1f %%"%(100.* (fi / (fi+fo+.000001) ))
  print >>file, ".br"
  file.close()

######################################################################
def process_declaration_subroutine(file, sub):
  print >>file, sub.line.text.split('!')[0].strip()

# for line in sub.text:
######################################################################
def do_print_subroutines(sub):
  assert type(sub) == Sub
  filename = sub.line.filename
  name = sub.name
  file = open("%s%s.l"%(mandir,sub.name), "w")
  print >>file, '.TH "IRPF90 entities" l %s "IRPF90 entities" %s'%(name,name)
  print >>file, ".SH Declaration"
  print >>file, ".nf"
  process_declaration_subroutine(file,sub)
  print >>file, ".ni"
  if sub.doc != []:
   print >>file, ".SH Description"
   for l in sub.doc:
     process_doc(file,l)
  print >>file, ".SH File\n.P"
  print >>file, filename
  if sub.needs != []:
    sub.needs.sort()
    print >>file, ".SH Needs"
    process_deps(file,sub.needs)
  if sub.called_by != []:
    sub.called_by.sort()
    print >>file, ".SH Called by"
    process_deps(file,sub.called_by)
  if sub.calls != []:
    sub.calls.sort()
    print >>file, ".SH Calls"
    process_deps(file,sub.calls)
  if sub.touches != []:
    sub.touches.sort()
    print >>file, ".SH Touches"
    process_deps(file,sub.touches)
  print >>file, ".SH Instability factor"
  fo = len(sub.needs)+len(sub.calls)+len(sub.touches)
  fi = len(sub.called_by)
  print >>file, "%5.1f %%"%(100.* (fi / (fi+fo+.000001) ))
  print >>file, ".br"
  file.close()

######################################################################
def run():
  import parsed_text
  import os,sys
  pid1 = os.fork()
  if pid1 == 0:
    for v in variables.values():
      do_print(v)
    for s in subroutines.values():
      do_print_subroutines(s)
    sys.exit(0)

  pid2 = os.fork()
  if pid2 == 0:
    tags = []
    l = variables.keys()
    file = open("irpf90_entities","w")
    l.sort()
    for v in l:
      do_print_short(file,variables[v])
      line = variables[v].line
#     tags.append( '%s\t%s\t/%s/;"\n'%(v,line.filename[0],line.text.split('!')[0].strip()) )
      tags.append( '%s\t%s\t%d\n'%(v,line.filename[0],line.i) )
    file.close()
    l = subroutines.keys()
    for v in l:
      line = subroutines[v].line
#     tags.append('%s\t%s\t/%s/;"\n'%(v,line.filename,line.text.split('!')[0].strip()))
      tags.append('%s\t%s\t%d\n'%(v,line.filename,line.i))
    tags.sort()
    file = open("tags","w")
    for line in tags:
      file.write(line)
    file.close()
    sys.exit(0)

  os.waitpid(pid1,0)
  os.waitpid(pid2,0)

######################################################################
if __name__ == '__main__':
  run()
