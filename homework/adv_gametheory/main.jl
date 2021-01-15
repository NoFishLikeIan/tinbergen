include("games.jl")
include("shapley.jl")
include("utils.jl")
include("graphgames.jl")
include("cyclefree.jl")

week = 2

if week == 1
    include("one/one.jl")
    include("one/three.jl")
else week == 2
    include("two/supply.jl")
end
