set of PARTS: group_selected = { cBBa_C0040 };

% All parts in group_selected in sequence 
constraint
  forall(p in group_selected)
      (exists(i in POSITION)(sequence[i,name] == p));
