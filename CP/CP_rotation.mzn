include "globals.mzn";

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

% coordinates of the left bottom corner
array[NPIECES, 1..2] of var int: coordinates; 

% CONSTRAINTS %
% set the domain of the pieces value
constraint 
  forall(i in NPIECES)
    ((coordinates[i,x] >= 0 /\ coordinates[i,x] < w) /\ 
     (coordinates[i,y] >= 0 /\ coordinates[i,y] < h));


/*
Parameters:
- k: the number of dimensions
- rect_size: the size of each box in k dimensions
- rect_offset: the offset of each box from the base position in k dimensions
- shape: the set of rectangles defining the i -th shape.
- x: the base position of each object. x [ i , j ] is the position of object i in. dimension j 
- kind: the shape used by each object.
*/

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