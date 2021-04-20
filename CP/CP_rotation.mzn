include "globals.mzn";

% paper roll dimensions
int: w;
int: h;
set of int : DIM = 1..2;

% axes
int: x = 1;
int: y = 2;

% pieces of paper 
int: n_pieces;
set of int: NPIECES = 1..n_pieces;

% number of shapes --> i.e. nxn is 1 shape, mxn is 2 shapes
int: n_shapes;
set of int: NPIECES_ROT = 1..n_shapes;

% dimension of pieces of paper
array[NPIECES, DIM] of int: rectangles; % used just in final print

% coordinates of the left bottom corner
array[NPIECES, DIM] of var int: coordinates;

/*-- geost_bb --
doc: https://www.minizinc.org/doc-2.5.3/en/lib-globals.html#index-97
example: https://github.com/MiniZinc/minizinc-examples/blob/master/carpet_cutting/carpet_cutting_geost.mzn

A global non-overlap constraint for k dimensional objects.
It enforces that no two objects overlap, and that all objects
fit within a global k dimensional bounding box.

Parameters:
- k: the number of dimensions
- rect_size: the size of each box in k dimensions
- rect_offset: the offset of each box from the base position in k dimensions
- shape: the set of rectangles defining the i -th shape.
- x: the base position of each object. x [ i , j ] is the position of object i in. dimension j 
- kind: the shape used by each object.
- l: is an array of lower bounds, l [ i ] is the minimum bounding box for all objects in dimension i
- u: is an array of upper bounds, u [ i ] is the maximum bounding box for all objects in dimension i 
*/
int: k = 2;
array[NPIECES_ROT, 1..k] of int : rect_size;
array[NPIECES_ROT, 1..k] of int : rect_offset;
array[int] of set of NPIECES_ROT: shape;
% x = coordinates
% index of shapes related to a paper and, eventually, its rotation
array[NPIECES] of set of int: shape_index;
array[NPIECES] of var int : kind;
array[DIM] of var int : l = [0,0];
array[DIM] of var int : u = [w,h];


% CONSTRAINTS %
% set the domain of the pieces value
constraint 
  forall(i in NPIECES)
    ((coordinates[i,x] >= 0 /\ coordinates[i,x] < w) /\ 
     (coordinates[i,y] >= 0 /\ coordinates[i,y] < h));
     

% implied cumulative constraints --> riguarda
constraint (cumulative([coordinates[i,x] | i in NPIECES ], [rect_size[kind[i],x] | i in NPIECES ], [rect_size[kind[i],y] | i in NPIECES ],h));
constraint (cumulative([coordinates[i,y] | i in NPIECES ], [rect_size[kind[i],y] | i in NPIECES ], [rect_size[kind[i],x] | i in NPIECES ],w));

% bounding constraint
constraint forall(i in NPIECES)(kind[i] in shape_index[i]); 

% non-overlap constraint for k dimensional objects
constraint
  geost_bb(k,rect_size,rect_offset, shape, coordinates, kind, l, u);

% numper of different pieces of paper
int: rect_copies;
set of int: NDIFFPIECES = 1..rect_copies;

% number of copy for each piece of paper
array[NDIFFPIECES] of int: rect_rep;

% find the starting index of each size
array[NDIFFPIECES] of int: coordinate_shapes;

% order pieces of the same size
constraint forall(i in NDIFFPIECES)(
  forall(j in 1..rect_rep[i]-1)(
    lex_greater(coordinates[coordinate_shapes[i]+j,..],coordinates[coordinate_shapes[i]+j+1,..])));

% search
ann:search_ann;
% Choose the variable with the largest domain
search_ann = int_search(coordinates, first_fail, indomain_split); 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GUARDA QUALE ANNOTAZIONE SCEGLIERE %%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%https://www.minizinc.org/doc-2.4.3/en/lib-annotations.html?highlight=first_fail

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
  "origin y:",show(coordinates[..,y]), "\n"
];
output [
  " required output:\n",
  show(w), " ", show(h), "\n",
  show(n_pieces), "\n",
];
output[
  show(rectangles[i,x]) ++ " " ++ show(rectangles[i,y]) ++ "  " ++ show(coordinates[i,x]) ++ " " ++ show(coordinates[i,y]) ++ "\n" | i in NPIECES
];