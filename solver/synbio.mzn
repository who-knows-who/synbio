include "table.mzn";
include "synbio_predicates.mzn";
include "synbio_restriction.mzn";
include "synbio_selected.mzn";
include "data.dzn";

% Used for combining to find substrings
int: substring_length;
set of int: substring_index = 1..substring_length;
set of int: combined_index = 1..2*substring_length;

% Allows indexing by name
enum PARTS;
enum FEATURE;

% Instantiate part data from data file
array[PARTS, FEATURE] of int: data;
set of PARTS: group_regulatory;
set of PARTS: group_rbs;
set of PARTS: group_coding;
set of PARTS: group_terminator;
set of PARTS: null;

% Instantiate user inputs from data file
% MiniZinc doesn't like variable arrays
int: max_parts;
set of int: POSITION = 1..max_parts;

% Stores data on part at each position in sequence
array[POSITION, FEATURE] of var int: sequence;
% Each row much come from the data table
constraint forall(i in POSITION)(table(sequence[i,..], data));

% First part in sequence must be promotor
constraint sequence[1,name] in group_regulatory;

% Last part either terminator or null (preceeded by terminator)
constraint sequence[max(POSITION),name] in group_terminator \/ sequence[max(POSITION),name] in null;

% Parts must be in valid order
constraint forall(i in POSITION where i != max(POSITION))(valid_order(sequence[i,name], sequence[i+1,name]));


%%%%% MINIMISATION - Based on Chargaff's Second Parity Law%%%%%
var int: total_a = sum(sequence[..,a]);
var int: total_t = sum(sequence[..,t]);
var int: total_g = sum(sequence[..,g]);
var int: total_c = sum(sequence[..,c]);

% Find difference between a t and g c
var int: a_t_diff = if total_a > total_t then total_a - total_t else total_t - total_a endif;
var int: g_c_diff = if total_g > total_c then total_g - total_c else total_c - total_g endif; 

% Difference shouldn't be greater than 10% - could change
constraint a_t_diff < (total_a + total_t) div 10;
constraint g_c_diff < (total_g + total_c) div 10;

% Try to lower both
solve minimize (a_t_diff + g_c_diff);

% Output
output["A-T diff: " ++ show(a_t_diff) ++ ", G-C diff: " ++ show(g_c_diff) ++  "\nSequence: "];
output[show(to_enum(PARTS, sequence[i,name])) ++ " " | i in POSITION];
