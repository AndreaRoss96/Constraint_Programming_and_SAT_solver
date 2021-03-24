include "globals.mzn";

% paper roll dimensions
int: w;
int: h;

% number of necessary pieces of paper
int: n_pieces;
set of int: NPIECES = 1..n_pieces;

% number of shapes
int: n_shapes;
set of int: NPIECES_ROT = 1..n_shapes;

% dimension of pieces of paper
array[NPIECES, 1..2] of int: size; 

% axes
int: x = 1;
int: y = 2;

% coordinates of the left bottom corner
array[NPIECES, 1..2] of var int: coordinates;


% CONSTRAINTS %
% set the domain of the pieces value
constraint 
  forall(i in NPIECES)
    ((coordinates[i,x] >= 0 /\ coordinates[i,x] < w) /\ 
     (coordinates[i,y] >= 0 /\ coordinates[i,y] < h));

/*
-- geost_bb -- https://www.minizinc.org/doc-2.5.3/en/lib-globals.html#index-97
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
- l: is an array of lower bounds, l [ i ] is the minimum bounding box for all objects in dimension i .
- u: is an array of upper bounds, u [ i ] is the maximum bounding box for all objects in dimension i 
*/
int: k = 2;
array[NPIECES_ROT, 1..k] set of int: rect_size;
array[] set of int: rect_offset; % è uguale a prima ?
array[int] of NPIECES_ROT: shape;
???: x;
???: kind;
[0,0] : l;
[w,h] : u


/*
A global non-overlap constraint for 2 dimensional objects. It enforces that no two objects overlap and zero-length objects do not appear in the middle of other objects.
- x1: first coordinate of each object
- w2: width in first dimension for each object
- x2: second coordinate of each object
- w2: width in second dimension for each object
*/
constraint 
 geost_nonoverlap_k(coordinates[..,x],size[..,x],coordinates[..,y],size[..,y]);

/*
cosa fa lui?
praticamente non considera soltanto i rettangoli, ma anche le "forme", ovvero i rettangoli non quadrati e che quindi possono essere ruotati
*/