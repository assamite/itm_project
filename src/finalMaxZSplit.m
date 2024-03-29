function [I, Y1, Z1, X1, Y0, Z0, X0] = finalMaxZSplit(threshold, save)
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
[SY, SZ] = meshgrid(-4:0.1:4, -4:0.3:1.5);
SX = reshape(fr(SY),size(SY));
figure
scatter3(Y,Z,X,5,'k','o', 'filled');
hold on;
surf(SY,SZ,SX);


indeces = zeros(size(X));

for i=1:n
  if fr(Y(i)) < X(i)
    indeces(i) = 1;
  end;
end;

I = find(indeces);
Y1 = Y(I);
Z1 = Z(I);
X1 = X(I);
Y0 = Y(indeces == false);
Z0 = Z(indeces == false);
X0 = X(indeces == false);

% DATAPOINTS ABOVE THE PLANE
[xData, yData, zData] = prepareSurfaceData( Y1, Z1, X1 );
% Set up fittype and options.
ft = fittype( 'poly55' );
% Fit model to data.
[fit1, gof1] = fit( [xData, yData], zData, ft );


% DATAPOINTS UNDER THE PLANE
[xData, yData, zData] = prepareSurfaceData( Y0, Z0, X0 );
% Set up fittype and options.
ft = fittype( 'poly55' );
% Fit model to data.
[fit2, gof2] = fit( [xData, yData], zData, ft );

if save
  fid = fopen('final_split1_coefs.txt', 'w');
  fprintf(fid, 'Linear model Poly55:\nfit2(x,y) = p00 + p10*x + p01*y + p20*x^2 + p11*x*y + p02*y^2 + p30*x^3\n+ p21*x^2*y + p12*x*y^2 + p03*y^3 + p40*x^4 + p31*x^3*y\n+ p22*x^2*y^2 + p13*x*y^3 + p04*y^4 + p50*x^5 + p41*x^4*y\n+ p32*x^3*y^2 + p23*x^2*y^3 + p14*x*y^4 + p05*y^5\n\n');
  fprintf(fid, '%f\n', fit1.p00, fit1.p10, fit1.p01, fit1.p20, fit1.p11, fit1.p02, fit1.p30, fit1.p21, fit1.p12, fit1.p03, fit1.p40, fit1.p31, fit1.p22, fit1.p13, fit1.p04, fit1.p50, fit1.p41, fit1.p32, fit1.p23, fit1.p14, fit1.p05);
  fclose(fid);
  
  fid = fopen('final_split0_coefs.txt', 'w');
  fprintf(fid, 'Linear model Poly55:\nfit2(x,y) = p00 + p10*x + p01*y + p20*x^2 + p11*x*y + p02*y^2 + p30*x^3\n+ p21*x^2*y + p12*x*y^2 + p03*y^3 + p40*x^4 + p31*x^3*y\n+ p22*x^2*y^2 + p13*x*y^3 + p04*y^4 + p50*x^5 + p41*x^4*y\n+ p32*x^3*y^2 + p23*x^2*y^3 + p14*x*y^4 + p05*y^5\n\n');
  fprintf(fid, '%f\n', fit2.p00, fit2.p10, fit2.p01, fit2.p20, fit2.p11, fit2.p02, fit2.p30, fit2.p21, fit2.p12, fit2.p03, fit2.p40, fit2.p31, fit2.p22, fit2.p13, fit2.p04, fit2.p50, fit2.p41, fit2.p32, fit2.p23, fit2.p14, fit2.p05);
  fclose(fid);
  
  fid = fopen('final_split_indeces.txt', 'w');
  fprintf(fid, repmat('%g', 1, size(indeces)), indeces);
  fclose(fid);
  
  fid = fopen('final_residuals.txt', 'w');
  n = size(Y);
  n = n(1);
  x = 0;
  for i=1:n;
    if indeces(i) == 1
      x = fit1(Y(i), Z(i));
    else 
      x = fit2(Y(i), Z(i));
    end
    residual = X(i) - x;
    fprintf(fid, '%.3f\n', residual);
  end;  
  fclose(fid);
end;


