include "table.mzn";
include "data.dzn";

int: max_parts;
int: substring_length;
set of int: substring_index;
set of int: combined_index;

array[int] of -2..2: site_1;
array[int] of -2..2: site_2;

enum PARTS;
enum FEATURE;
      
array[PARTS, FEATURE] of int: data;
set of PARTS: group_regulatory;
set of PARTS: group_rbs;
set of PARTS: group_coding;
set of PARTS: group_terminator;
set of PARTS: null;


predicate valid_order(var int: i_first, var int: i_second) =
  let { 
    var int: first = to_enum(PARTS, i_first); 
    var int: second = to_enum(PARTS, i_second); 
  } in
  ((first in group_regulatory /\ (second in group_regulatory \/ second in group_rbs)) \/
  (first in group_rbs /\ second in group_coding) \/
  (first in group_coding /\ (second in group_coding \/ second in group_terminator)) \/
  (first in group_terminator /\ (second in group_terminator \/ second in null)) \/
  (first in null /\ second in null));
  
predicate in_sequence(var PARTS: p) = 
  exists(i in POSITION)(sequence[i,name] == p);

predicate contains_restriction_site(array[int] of var int: end, array[int] of var int: start, array[int] of var int: site) = 
  let {
    array[combined_index] of var -2..2: combined = array1d(combined_index, end ++ start);
    var int: site_length = length(site);
  } in
  exists(i in 0..substring_length)(forall(j in 1..site_length)(combined[i+j] == site[j]));


set of int: POSITION = 1..max_parts;
array[POSITION, FEATURE] of var int: sequence;
constraint forall(i in POSITION)(table(sequence[i,..], data));
var set of PARTS: group_selected;

% All parts in sequence in group_selected
constraint forall(i in POSITION)(sequence[i,name] in group_selected);
% All parts in group_selected in sequence
constraint forall(p in group_selected)(in_sequence(p));

% First part in sequence must be promotor
constraint sequence[1,name] in group_regulatory;
% Last part either terminator or null (preceeded by terminator)
constraint sequence[max(POSITION),name] in group_terminator \/ sequence[max(POSITION),name] in null;
constraint forall(i in POSITION where i != max(POSITION))(valid_order(sequence[i,name], sequence[i+1,name]));
constraint forall(i in POSITION where i != max(POSITION))(not contains_restriction_site(sequence[i, l1..lend], sequence[i+1, f1..fend], site_2));

var int: total_a = sum(sequence[..,a]);
var int: total_t = sum(sequence[..,t]);
var int: total_g = sum(sequence[..,g]);
var int: total_c = sum(sequence[..,c]);

var int: a_t_diff = if total_a > total_t then total_a - total_t else total_t - total_a endif;
var int: g_c_diff = if total_g > total_c then total_g - total_c else total_c - total_g endif; 
var int: at_gc_diff = if a_t_diff > g_c_diff then a_t_diff - g_c_diff else g_c_diff - a_t_diff endif;
constraint a_t_diff < 20;
constraint g_c_diff < 20;
solve minimize (at_gc_diff);

output["A-T diff: " ++ show(a_t_diff) ++ ", G-C diff: " ++ show(g_c_diff) ++ ", AT-GC diff: " ++ show(at_gc_diff) ++ "\nSequence: "];
output[show(to_enum(PARTS, sequence[i,name])) ++ " " | i in POSITION];
