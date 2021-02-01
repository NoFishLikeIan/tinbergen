using Plots

N = 1_000
frequencies = [inv(10^n) for n in 0:5]
s = 0.75

f(k, s, N) = inv(k^s * sum(n^s for n in 1:N)) 

plot(frequencies, f.(1:length(frequencies), s, N))