include "globals.mzn";
% PARAMETERS %
% paper roll dimensions
int: w;
int: h;

% number of necessary pieces of paper
int: n_pieces;
set of int: NPIECES = 1..n_pieces;

% dimension of pieces of paper
array[NPIECES, 1..2] of int: size; 

% axes
int: x = 1;
int: y = 2;

% VARIABLE %
% coordinates of the left bottom corner
array[NPIECES, 1..2] of var int: coordinates; 

% CONSTRAINTS %
% set the domain of the pieces value
constraint 
  forall(i in NPIECES)
    ((coordinates[i,x] >= 0 /\ coordinates[i,x] < w) /\ 
     (coordinates[i,y] >= 0 /\ coordinates[i,y] < h));

% non-overlapping constraint
/* predicate diffn
 * Constrains rectangles i , given by their origins ( x [ i ], y [ i ]) and sizes ( dx [ i ], dy [ i ]), to be non-overlapping. Zero-width rectangles can still not overlap with any other rectangle.
 */
constraint
  diffn(coordinates[..,x],coordinates[..,y], size[..,x], size[..,y]);
/*
For the non-overlapping constraint I also tried:
 * array[NPIECES, 1..2] of var 0..max([w, h])-1: q;
 * constraint diffn_k(q,size);
 *
 * constraint geost_nonoverlap_k(coordinates[..,x],size[..,x],coordinates[..,y],size[..,y]);
 *
 * but both the predicates fail with 40x40 paper size
*/

% each piece must fit in the paper roll
constraint 
  forall(i in NPIECES)
    (((size[i,x] + coordinates[i,x]) <= w) /\
     ((size[i,y] + coordinates[i,y]) <= h));


% implied cumulative constraints 
/* predicate cumulative
 * Requires that a set of pieces of paper given by left bottom corner (coordinates), size along the x axis, and size along the y axis, never require more than a global resource bound (width or height) at any one time.
 */
constraint 
  cumulative(coordinates[..,y], size[..,y], size[..,x], w)::domain;
constraint 
  cumulative(coordinates[..,x], size[..,x], size[..,y], h)::domain;

% search
ann:search_ann;
% Choose the variable with the largest domain
search_ann = int_search(coordinates, first_fail, indomain_split); 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GUARDA QUALE ANNOTAZIONE SCEGLIERE %%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%https://www.minizinc.org/doc-2.4.3/en/lib-annotations.html?highlight=first_fail

% Choose the variable with largest domain, divided by the number of attached constraints weighted by how often they have caused failure
%search_ann = int_search(coordinates, dom_w_deg, indomain_split);
% Choose the variable with the smallest domain, breaking ties using the number of attached constraints
%search_ann = int_search(coordinates, most_constrained, indomain_split);
solve :: search_ann satisfy;

output [
  "width: ",show(w), " height: ", show(h), "\n",
  "dimension x:",show(size[..,x]), "\n",
  "dimension y:",show(size[..,y]), "\n",
  "origin x:",show(coordinates[..,x]), "\n",
  "origin y:",show(coordinates[..,y]), "\n",
  "==========================="
];
output [
  " required output:\n",
  show(w), " ", show(h), "\n",
  show(n_pieces), "\n",
];
output[
  show(size[i,x]) ++ " " ++ show(size[i,y]) ++ "  " ++ show(coordinates[i,x]) ++ " " ++ show(coordinates[i,y]) ++ "\n" | i in NPIECES
];