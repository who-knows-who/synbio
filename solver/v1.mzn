include "table.mzn";
include "alldifferent.mzn";

predicate valid_order(var PARTS: first, var PARTS: second) =
  ((first in group_regulatory /\ (second in group_regulatory \/ second in group_rbs)) \/
  (first in group_rbs /\ second in group_coding) \/
  (first in group_coding /\ (second in group_regulatory \/  second in group_coding \/ second in group_terminator)) \/
  (first in group_terminator /\ (second in group_terminator \/ second in null)) \/
  (first in null /\ second in null));
  
predicate in_sequence(var PARTS: p) = 
  exists(i in POSITION)(sequence[i] == p);
  
enum PARTS;
enum FEATURE = {name, a, t, g, c};
array[PARTS, FEATURE] of int: data;

set of PARTS: group_regulatory;
set of PARTS: group_rbs;
set of PARTS: group_coding;
set of PARTS: group_terminator;
set of PARTS: null;

int: max_parts;
set of int: POSITION = 1..max_parts;
array[POSITION] of var PARTS: sequence;
var set of PARTS: group_selected;

% All parts in sequence in group_selected
constraint forall(i in POSITION)(sequence[i] in group_selected);
% All parts in group_selected in sequence
constraint forall(p in group_selected)(in_sequence(p));

% First part in sequence must be promotor
constraint sequence[1] in group_regulatory;
% Last part either terminator or null (preceeded by terminator)
constraint sequence[max(POSITION)] in group_terminator \/ sequence[max(POSITION)] in null;
constraint forall(i in POSITION where i != max(POSITION))(valid_order(sequence[i], sequence[i+1]));

var int: total_a = sum(part in group_selected)(data[part,a]);
var int: total_t = sum(part in group_selected)(data[part,t]);
var int: total_g = sum(part in group_selected)(data[part,g]);
var int: total_c = sum(part in group_selected)(data[part,c]);

var int: a_t_diff = if total_a > total_t then total_a - total_t else total_t - total_a endif;
var int: g_c_diff = if total_g > total_c then total_g - total_c else total_c - total_g endif; 
var int: at_gc_diff = if a_t_diff > g_c_diff then a_t_diff - g_c_diff else g_c_diff - a_t_diff endif;
solve minimize (a_t_diff + g_c_diff + at_gc_diff);

output["A-T diff: " ++ show(a_t_diff) ++ " G-C diff: " ++ show(g_c_diff) ++ " AT-GC diff: " ++ show(at_gc_diff) ++ "\n"];
output[show(to_enum(PARTS,sequence[i])) ++ " " | i in POSITION];
