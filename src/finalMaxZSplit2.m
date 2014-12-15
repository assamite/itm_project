function [I] = finalMaxZSplit2(threshold)
% Split data by dividing by the curve fitted to the points around the 
% maximum value of Z (second column in side data).

fid = fopen('../sdata/final.sdat');
ret = fscanf(fid, '%f %f\n', [2, 20000]);
fclose(fid);
Z = transpose(ret(2, :));
Y = transpose(ret(1, :));
fid = fopen('../data/final.dat');
X = fscanf(fid, '%f\n');
fclose(fid);

mz = max(Z);
zindeces = zeros(size(Z));
n = size(Z);
n = n(1);

for i=1:n
  z = Z(i);
  if mz - z < threshold
    zindeces(i) = 1;
  end;
end;

I = find(zindeces);

YI = Y(I);
ZI = Z(I);
XI = X(I);
YZX = [YI, ZI, XI];

[xData, yData] = prepareCurveData( YI, XI );
% Set up fittype and options.
ft = fittype( 'poly2' );
% Fit model to data.
[fr, gof] = fit( xData, yData, ft );
[SY, SZ] = meshgrid(-4:0.1:4, -4:0.5:1.5);
SX = reshape(fr(SY),size(SY));
figure
scatter3(Y,Z,X,4, 'k','s', 'filled');
hold on;
surf(SY,SZ,SX, gradient(SX));
xlabel('Y');
ylabel('Z');
zlabel('X');