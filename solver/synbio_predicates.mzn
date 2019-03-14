predicate valid_order(var int: i_first, var int: i_second) =
  let { 
    var int: first = to_enum(PARTS, i_first); 
    var int: second = to_enum(PARTS, i_second); 
  } in
  ((first in group_regulatory /\ (second in group_regulatory \/ second in group_rbs)) \/
  (first in group_rbs /\ second in group_coding) \/
  (first in group_coding /\ (second in group_rbs \/ second in group_terminator)) \/
  (first in group_terminator /\ (second in group_terminator \/ second in null)) \/
  (first in null /\ second in null));

predicate contains_restriction_site(array[int] of var int: end, array[int] of var int: start, array[int] of var int: site) = 
  let {
    array[combined_index] of var -2..2: combined = array1d(combined_index, end ++ start);
    var int: site_length = length(site);
  } in
  exists(i in 0..substring_length)(forall(j in 1..site_length)(combined[i+j] == site[j]));
