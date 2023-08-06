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


import util 
from command_line import command_line

do_debug = command_line.do_debug
do_openmp = command_line.do_openmp
do_memory = command_line.do_memory

import irpf90_t

FILENAME = irpf90_t.irpdir+"irp_stack.irp.F90"

def create():

  txt = """
module irp_stack_mod
  integer, parameter            :: STACKMAX=1000
  character*(128),allocatable   :: irp_stack(:,:)
  double precision,allocatable  :: irp_cpu(:,:)
  integer,allocatable           :: stack_index(:)
  logical                       :: alloc = .False.
  integer                       :: nthread
  character*(128)               :: white = ''
end module

subroutine irp_enter(irp_where)
 use irp_stack_mod
 integer       :: ithread
 character*(*) :: irp_where
"""
  if not do_openmp:
    txt += """
   ithread = 0
"""
  else:
    txt += """
 integer, external :: omp_get_thread_num
 integer, external :: omp_get_num_threads
 ithread = omp_get_thread_num()
"""

  txt += "$1"

  if do_memory:
     txt+="""
 if (.not.alloc) then
"""
     if do_openmp:
       txt += """
 !$OMP PARALLEL
 !$OMP SINGLE
 nthread = omp_get_num_threads()
 !$OMP END SINGLE
 !$OMP END PARALLEL
"""
     else:
       txt += """
 nthread = 1
 """
     txt += """
   print *, 'Allocating irp_stack(',STACKMAX,',',0:nthread,')'
   print *, 'Allocating irp_cpu(',STACKMAX,',',0:nthread,')'
   print *, 'Allocating stack_index(',0:nthread,')'
 endif"""
  txt +="""
$2
end subroutine

subroutine irp_enter_f(irp_where)
 use irp_stack_mod
 integer       :: ithread
 character*(*) :: irp_where
 """
  if do_openmp:
    txt += """
 integer, external :: omp_get_thread_num
 integer, external :: omp_get_num_threads
 ithread = omp_get_thread_num()
"""
  else:
    txt += """
  ithread = 0
"""
  txt += """
$1
"""
  if do_memory:
    txt+="""
 if (.not.alloc) then
"""
    if do_openmp:
      txt += """
 !$OMP PARALLEL
 !$OMP SINGLE
  nthread = omp_get_num_threads()
 !$OMP END SINGLE
 !$OMP END PARALLEL
"""
    else:
      txt += """
  nthread = 1
"""
    txt +="""
  print *, 'Allocating irp_stack(',STACKMAX,',',0:nthread,')'
  print *, 'Allocating irp_cpu(',STACKMAX,',',0:nthread,')'
  print *, 'Allocating stack_index(',0:nthread,')'
 endif
"""
  txt += """
$2
end subroutine

subroutine irp_leave (irp_where)
 use irp_stack_mod
  character*(*) :: irp_where
  integer       :: ithread
  double precision :: cpu
"""
  if do_openmp:
    txt += """
 integer, external :: omp_get_thread_num
 ithread = omp_get_thread_num()
 """
  else:
    txt += """
 ithread = 0
 """
  txt += """
$3
$4
end subroutine
"""

  # $1
  if do_debug:
    s = """
 if (.not.alloc) then
 """
    if do_openmp:
      s += """
 !$OMP PARALLEL
 !$OMP SINGLE
 nthread = omp_get_num_threads()
 !$OMP END SINGLE
 !$OMP END PARALLEL
 !$OMP CRITICAL
 if (.not.alloc) then
   allocate(irp_stack(0:STACKMAX,0:nthread))
   allocate(irp_cpu(0:STACKMAX,0:nthread))
   allocate(stack_index(0:nthread))
   stack_index = 0
   alloc = .True.
 endif
 !$OMP END CRITICAL
 endif
 stack_index(ithread) = min(stack_index(ithread)+1,STACKMAX)
 irp_stack(stack_index(ithread),ithread) = irp_where"""
    else:
      s += """
 nthread = 1
 if (.not.alloc) then
   allocate(irp_stack(0:STACKMAX,1))
   allocate(irp_cpu(0:STACKMAX,1))
   allocate(stack_index(2))
   stack_index = 0
   alloc = .True.
 endif
 endif
 stack_index(1) = min(stack_index(1)+1,STACKMAX)
 irp_stack(stack_index(1),1) = irp_where"""
    if do_memory:
      txt+="""
  print *, 'Allocating irp_stack(',STACKMAX,','0:nthread,')'
  print *, 'Allocating irp_cpu(',STACKMAX,','0:nthread,')'
  print *, 'Allocating stack_index(',0:nthread,')'"""
  else:
    s = ""
  txt = txt.replace("$1",s)

  # $2
  if do_debug:
    txt = txt.replace("$2","""
  print *, ithread, ':', white(1:stack_index(ithread))//'-> ', trim(irp_where)
  call cpu_time(irp_cpu(stack_index(ithread),ithread))""")
  else:
    txt = txt.replace("$2","")

  # $3
  if do_debug:
    txt = txt.replace("$3","""
  call cpu_time(cpu)
  print *, ithread, ':', white(1:stack_index(ithread))//'<- ', &
    trim(irp_stack(stack_index(ithread),ithread)), &
    cpu-irp_cpu(stack_index(ithread),ithread)""")
  else:
    txt = txt.replace("$3","")

  # $4
  if do_debug:
    txt = txt.replace("$4","""
  stack_index(ithread) = max(0,stack_index(ithread)-1)""")
  else:
    txt = txt.replace("$4","")

  txt += """
subroutine irp_trace
 use irp_stack_mod
 integer :: ithread
 integer :: i
"""
  if do_openmp:
    txt += """
!$ integer, external :: omp_get_thread_num
!$ ithread = omp_get_thread_num()
"""
  else:
    txt += """
 ithread = 0
"""
  txt += """
 if (.not.alloc) return
 print *, 'Stack trace: ', ithread
 print *, '-------------------------'
 do i=1,stack_index(ithread)
  print *, trim(irp_stack(i,ithread))
 enddo
 print *, '-------------------------'
end subroutine
"""

  txt = txt.split('\n')
  txt = map(lambda x: x+"\n",txt)
  if not util.same_file(FILENAME, txt):
    file = open(FILENAME,'w')
    file.writelines(txt)
    file.close()


