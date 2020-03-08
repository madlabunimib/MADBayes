belief network "unknown"
node A {
  type : discrete [ 3 ] = { "young", "adult", "old" };
}
node S {
  type : discrete [ 2 ] = { "M", "F" };
}
node E {
  type : discrete [ 2 ] = { "high", "uni" };
}
node O {
  type : discrete [ 2 ] = { "emp", "self" };
}
node R {
  type : discrete [ 2 ] = { "small", "big" };
}
node T {
  type : discrete [ 3 ] = { "car", "train", "other" };
}
probability ( A ) {
   0.3, 0.5, 0.2;
}
probability ( S ) {
   0.6, 0.4;
}
probability ( E | A, S ) {
  (0, 0) : 0.75, 0.25;
  (1, 0) : 0.72, 0.28;
  (2, 0) : 0.88, 0.12;
  (0, 1) : 0.64, 0.36;
  (1, 1) : 0.7, 0.3;
  (2, 1) : 0.9, 0.1;
}
probability ( O | E ) {
  (0) : 0.96, 0.04;
  (1) : 0.92, 0.08;
}
probability ( R | E ) {
  (0) : 0.25, 0.75;
  (1) : 0.2, 0.8;
}
probability ( T | O, R ) {
  (0, 0) : 0.48, 0.42, 0.10;
  (1, 0) : 0.56, 0.36, 0.08;
  (0, 1) : 0.58, 0.24, 0.18;
  (1, 1) : 0.70, 0.21, 0.09;
}
