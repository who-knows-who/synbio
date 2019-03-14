array[int] of -2..2: site_1 = [-1,1,1,-2,2];

constraint
  forall(i in POSITION where i!= max(POSITION))
      (not contains_restriction_site(
          sequence[i, l1..lend],
          sequence[i+1, f1..fend],
          site_1));

