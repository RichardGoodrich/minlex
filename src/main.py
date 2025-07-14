#! /usr/bin/python
this_author  = "1to9only"
this_program = "minlex.py"
this_version = "1.00"
import os, sys, optparse

# source attribution:
#
# minlex.py is my modifications to canonical.py to calculate MINimal LEXicographical sudoku grids
#
# I found canonical.py in RichardGoodrich's BigSdk package downloaded from here:
# https://www.dropbox.com/scl/fo/usiwk90hd14b405ry2h9y/h?rlkey=tn0oygefkwmi5g3lnlfxsjtyq&dl=0
#
# In http://forum.enjoysudoku.com/minimal-lexographic-sudoku-string-help-t42404.html#p344128
# RichardGoodrich wrote:
#   'SO, on "canonical.py" I got that maybe 10 years ago from a very bright German fellows named Moritz Lentz.'
#   'I have not been back in contact since.'
#
# I have modified (a lot!) and reformatted minlex.py code to my liking!!
#
# Usage: minlex.py [puzzle string|puzzles file]
#
# Examples:
# minlex.py 000000075000080094000500600010000200000900057006003040001000023080000006063240000
# minlex.py 8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..
# minlex.py 812753649943682175675491283154237896369845721287169534521974368438526917796318452
# minlex.py puzzles.txt
#
# Results:
# ..............1.23....2.14.....4......3....5..6.7...8..2...8...6.59..4.29.765.8..
# ........1.....2.3...4.5.6.....6..7....678.....3...9.....8...5...9...7.1.12.....9.
# 123456789457189236698723415285914367761532948934867152346278591579641823812395674

#
# this section programatically creates the permutations table, 6x6x6x6 = 1296 rows/colums permutations
# it makes the program SLOWER! the section can be replaced by the full perm[] table from canonical.py
#

perm = []
PERMS = [ [ 0, 1, 2], [ 0, 2, 1], [ 1, 0, 2], [ 1, 2, 0], [ 2, 0, 1], [ 2, 1, 0]]
for i in range( 6):
   for j in range( 6):
      for k in range( 6):
         for l in range( 6):
            perm.append( [ PERMS[i][0]*3+PERMS[j][0], PERMS[i][0]*3+PERMS[j][1], PERMS[i][0]*3+PERMS[j][2],
                           PERMS[i][1]*3+PERMS[k][0], PERMS[i][1]*3+PERMS[k][1], PERMS[i][1]*3+PERMS[k][2],
                           PERMS[i][2]*3+PERMS[l][0], PERMS[i][2]*3+PERMS[l][1], PERMS[i][2]*3+PERMS[l][2]])

# end section

def perm_copy( sudoku, canon, i, j):
   map_ = [ 0, -1, -1, -1, -1, -1, -1, -1, -1, -1]
   next_map = 1
   for y in range( 9):
      for x in range( 9):
         a = sudoku[ perm[ i][ y]][ perm[ j][ x]]
         if map_[ a] == -1:
            map_[ a] = next_map
            next_map += 1
         canon[ y*9+x] = map_[ a]

def compare_and_update( sudoku, canon, i, j):
   map_ = [ 0, -1, -1, -1, -1, -1, -1, -1, -1, -1]
   next_map = 1
   for y in range( 9):
      for x in range( 9):
         a = sudoku[ perm[ i][ y]][ perm[ j][ x]]
         if map_[ a] == -1:
            map_[ a] = next_map
            next_map += 1
         if map_[ a] < canon[ y*9+x]:
            perm_copy( sudoku, canon, i, j)
            return
         elif map_[ a] > canon[ y*9+x]:
            return

def canonical_form( line):
   sudoku = [ [ 0 for __ in range( 9)] for _ in range( 9)]
   for i in range( 81):
      sudoku[ i//9][ i%9] = int( line[ i])
   canon = [ 9 for _ in range( 81)]
   for i in range( 81):
      canon[ i] = sudoku[ i//9][ i%9]
   transposed = [ [ 0 for __ in range( 9)] for _ in range( 9)]
   for y in range( 9):
      for x in range( 9):
         transposed[ y][ x] = sudoku[ x][ y]
   for i in range( 1296):
      for j in range( 1296):
         compare_and_update( sudoku, canon, i, j)
         compare_and_update( transposed, canon, i, j)
   return canon

def main():
   parser = optparse.OptionParser()
   argc, argv = parser.parse_args()

   input = ''
   if len( argv) == 1:
      input = argv[ 0]
   if input == '':
      print( 'nothing to do!')
      exit( 0)

   if len( input) == 81:
      input = input.replace( '.', '0')
      canon = ''.join( [ str(i) for i in canonical_form( input)])
      canon = canon.replace( '0', '.')
      print( canon)
      exit( 0)

   isfile = os.path.isfile( input)
   if not isfile:
      print( input + ' not found!')
      exit( 0)

   f = open( input,'r')
   for line in f:
      line = line.replace( '\x0a', '')
      line = line.replace( '\x0d', '')
      if len( line) >= 81:
         line = line.replace( '.', '0')
         canon = ''.join( [ str(i) for i in canonical_form( line)])
         canon = canon.replace( '0', '.')
         print( canon)

   f.close()

   return 0

if __name__ == "__main__":
   sys.exit( main())

