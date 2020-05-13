belief network "unknown"
node Burglary {
  type : discrete [ 2 ] = { "True", "False" };
}
node Earthquake {
  type : discrete [ 2 ] = { "True", "False" };
}
node Alarm {
  type : discrete [ 2 ] = { "True", "False" };
}
node JohnCalls {
  type : discrete [ 2 ] = { "True", "False" };
}
node MaryCalls {
  type : discrete [ 2 ] = { "True", "False" };
}
probability ( Burglary ) {
   0.01, 0.99;
}
probability ( Earthquake ) {
   0.02, 0.98;
}
probability ( Alarm | Burglary, Earthquake ) {
  (0, 0) : 0.95, 0.05;
  (1, 0) : 0.29, 0.71;
  (0, 1) : 0.94, 0.06;
  (1, 1) : 0.001, 0.999;
}
probability ( JohnCalls | Alarm ) {
  (0) : 0.9, 0.1;
  (1) : 0.05, 0.95;
}
probability ( MaryCalls | Alarm ) {
  (0) : 0.7, 0.3;
  (1) : 0.01, 0.99;
}
