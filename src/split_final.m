function [YZX1, YZX2, indeces] = split_final(Y, Z, X)
% Split final.dat and final.sdat into two sets divided by fitted plane.

indeces = zeros(size(Y));
plane = final_fit(Y,Z,X,false);
rows = size(Y);
rows = rows(1);
for i = 1:rows
  y = Y(i);
  z = Z(i);
  x = X(i);
  if plane(y, z) > x && z > -1.5
     indeces(i) = 1;
  end;
end;

I = find(indeces);
YZX = [Y, Z, X];
YZX2 = YZX(indeces == true, :);
YZX1 = YZX(indeces == false, :);

