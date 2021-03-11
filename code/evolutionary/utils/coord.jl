function coordloop(i, N)
    l = cld(i, N)
    r = i % N == 0 ? i : i % N

    return l, r
end