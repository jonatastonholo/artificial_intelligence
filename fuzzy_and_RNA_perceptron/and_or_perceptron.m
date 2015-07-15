%**************************************************************************
%-------- Centro Federal de Educação Tecnologica de Minas Gerais ----------
%--------------------------------------------------------------------------
%------------------------ Computer Engineering ----------------------------
%--------------------------------------------------------------------------
%------------------- Perceptron for AND & OR ports ------------------------
%--------------------------------------------------------------------------
%---------------------- Jônatas Ribeiro Ronholo ---------------------------
%**************************************************************************
% To execute, 
% Load and_or_perceptron.m in the path and run in Command Window:
% [X,AND,OR,W_AND,W_OR,Wi_AND,Wi_OR] = and_or_perceptron
%--------------------------------------------------------------------------
% Returns:
% X: Matrix Binary inputs
% AND: Result of perceptron for AND: Column Matrix Binary inputs
% OR: Result of perceptron for OR: Column Matrix Binary inputs
% W_AND: W Result of perceptron for AND: Column Matrix Binary inputs
% W_OR: W Result of perceptron for OR: Column Matrix Binary inputs
% Wi_AND: W initial of perceptron for AND: Column Matrix Binary inputs
% Wi_OR: W initial of perceptron for OR: Column Matrix Binary inputs
%**************************************************************************
function [X,AND,OR,W_AND,W_OR,Wi_AND,Wi_OR] = and_or_perceptron ()
    clc;close all; clear all;
    Error = 1;
    n = .25;    
    x0 = 1;
    
    % Entradas
    X = [0 0 0; 
         1 0 0;
         0 1 0; 
         0 0 1;
         1 0 1;
         1 1 0;
         0 1 1;
         1 1 1];
    
    %Yd para And
    Yd_and = [0; 0; 0; 0; 0; 0; 0; 1];
    AND = zeros(size(X,1),1);
        
    % Yd para Or
    Yd_or = [0; 1; 1; 1; 1; 1; 1; 1];    
    OR = zeros(size(X,1),1);
    
    W = createInitialW (size(X,2)+1);
    
    Wi_AND = W;
    
   %AND
    e=1;
    while e ~= 0        
        e=0;
        idx = randperm(size(X,1));
        for i=1:size(X,1)            
            xk=X(idx(i),1:end);
            yd=Yd_and(idx(i),1);
            trainning(xk,yd);
            if Error ~=0
                e=1;
            end
        end
    end
    
    
    for ii=1:size(X,1)
        xk = X(ii,1:end);
        net = sum_func(xk);
        y = activation(net);
        AND(ii) = y;
    end
    W_AND = W;
    
    %Gerando novos W para OR
    W = createInitialW (size(X,2)+1);
    Wi_OR = W;
    
    %OR
    Error = 1;
    e=1;
    while e ~= 0        
        e=0;
        idx = randperm(size(X,1));
        for j=1:size(X,1)            
            xk=X(idx(j),1:end);
            yd=Yd_or(idx(j),1);
            trainning(xk,yd);
            if Error ~=0
                e=1;
            end
        end
    end
    
    
    for k=1:size(X,1)
        xk = X(k,1:end);
        net = sum_func(xk);
        y = activation(net);
        OR(k) = y;
    end
    W_OR = W;
    clc
    
%--- End of program

% Perceptron Functions
    % Rand W function
    function W = createInitialW (size)
        W=zeros(1,size);        
        for l=1:size
            r= (rand -.5);
            W(l) = r;
        end
    end

    %Step function
    function y = activation(net)
        if net <= 0
            y=0;
        else
            y=1;
        end
    end

    function net = sum_func(xk)                
        net = 0;
        bias=W(1);
        net = net + (x0*bias);        
        for m=1:size(xk,2)
            xki = xk(m);
            wi = W(m+1);
            net = net + (wi*xki);
        end
    end

    function y = trainning(xk,yd)        
        net = sum_func(xk);
        y = activation(net);
        Error = (yd-y); %Delta Rule
               
        if Error ~= 0
            W(1) = W(1) + (n*Error*x0);            
            for o=2:size(W,2)
                dW = (n*Error*xk(o-1));
                W(o) = W(o) + dW;
            end
        end
    end
end