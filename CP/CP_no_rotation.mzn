include "globals.mzn";
% PARAMETERS %
% paper roll dimensions
int: w;
int: h;

% number of necessary pieces of paper
int: n_pieces;
set of int: NPIECES = 1..n_pieces;

% dimension of pieces of paper
array[NPIECES, 1..2] of int: rectangles; 

% axes
int: x = 1;
int: y = 2;

% VARIABLE %
% coordinates of the left bottom corner
array[NPIECES, 1..2] of var int: coordinates; 

% CONSTRAINTS %

%% Defining the domain of the problem

% bound the pieces origin within the paper rolls limits
constraint 
  forall(i in NPIECES)
    ((coordinates[i,x] >= 0 /\ coordinates[i,x] < w) /\ 
     (coordinates[i,y] >= 0 /\ coordinates[i,y] < h));
     
% bound the pieces dimension within the paper rolls limits
constraint 
  forall(i in NPIECES)
    (((rectangles[i,x] + coordinates[i,x]) <= w) /\
     ((rectangles[i,y] + coordinates[i,y]) <= h));

%% non-overlapping constraint
/* predicate diffn
 * Constrains rectangles i , given by their origins ( x [ i ], y [ i ]) 
 * and sizes ( dx [ i ], dy [ i ]), to be non-overlapping. Zero-width 
 * rectangles can still not overlap with any other rectangle.
 */
constraint
  diffn(coordinates[..,x],coordinates[..,y], rectangles[..,x], rectangles[..,y]);
/*
For the non-overlapping constraint I also tried:
 * array[NPIECES, 1..2] of var 0..max([w, h])-1: q;
 * constraint diffn_k(q,size);
 *
 * constraint geost_nonoverlap_k(coordinates[..,x],size[..,x],coordinates[..,y],size[..,y]);
 *
 * but both the predicates fail with 40x40 paper size
*/


%% implied cumulative constraints 
/* predicate cumulative
 * Requires that a set of pieces of paper given by left bottom corner (coordinates), size along
 * the x axis, and size along the y axis, never require more than a global resource bound
 * (width or height) at any one time.
 */
constraint 
  cumulative(coordinates[..,y], rectangles[..,y], rectangles[..,x], w)::domain;
constraint 
  cumulative(coordinates[..,x], rectangles[..,x], rectangles[..,y], h)::domain;
/*built-in annotation "domain" which instructs the solver to use the domain propagating version of cumulative*/

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
  "dimension x:",show(rectangles[..,x]), "\n",
  "dimension y:",show(rectangles[..,y]), "\n",
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
  show(rectangles[i,x]) ++ " " ++ show(rectangles[i,y]) ++ "  " ++ show(coordinates[i,x]) ++ " " ++ show(coordinates[i,y]) ++ "\n" | i in NPIECES
];