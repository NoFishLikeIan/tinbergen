def compute_D(G, this_set, node):
    return sum(1 if j in this_set else -1 for j in G.neighbors(node))

def find_last(arr, condition):
    for i in reversed(range(len(arr))):
        if condition(arr[i]):
            return i
    
    return -1

def kl_partition(G, max_iter = 1_000):
    N = len(G)
    M = int(N / 2)

    A = set(random.sample(c.G.nodes, M))
    B = set(j for j in G.nodes if j not in A)

    iteration = 0

    while iteration <= max_iter:
        
        A_t = A.copy()
        B_t = B.copy()

        gv, av, bv = [], [], []

        for n in range(M):
            D = {**{ j: compute_D(G, A_t, j) for j in A_t}, **{ j: compute_D(G, B_t, j) for j in B_t}}
            cost = lambda a, b: 1 if (a in A and b in A_t) or (a in B and b in B_t) else -1

            max_g = -10e10
            max_a, max_b = None, None

            for (a, b) in itertools.product(A_t, B_t):
                g = D[a] + D[b] - 2*cost(a, b)
                if g > max_g:
                    max_g = g
                    max_a, max_b = a, b

            av.append(max_a)
            bv.append(max_b)
            gv.append(max_g)

            A_t.remove(max_a)
            B_t.remove(max_b)
                        
        k = find_last(gv, lambda x: x > 0)
        
        if k < 0: return A, B
        
        for i in range(k):
            
            a, b = av[i], bv[i]
            A.add(b), A.remove(a)
            B.add(a), B.remove(b)
                        
        iteration += 1
        
    return A, B
                