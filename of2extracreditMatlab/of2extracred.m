clc
clear
u=importdata('line0_U.xy');                  %the U data for the flow at the right of the cylinder
ux = u(:,4);                                    %extract only the U
h=(u(1,2)-u(end,2)+1)/length(ux);                                %the timestep that makes up the crosswise distance where we sampled from

U = ones(length(ux),1);                     %the freestream velocity

p=U-ux;                                     %setting up the discretized equation from the writeup
D = ux.*p*h;

df = sum(D);                                 %F/(density)
A = pi*(.5)^2;                               %area of the cylinder
Ufree = 1;                                   %velocity

Cd = df*2/(Ufree^2*A)                         %Coeffecient of friction = F/(0.5*density*area*velocity^2)