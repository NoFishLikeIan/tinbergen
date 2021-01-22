include("games.jl")
include("shapley.jl")
include("utils.jl")
include("graphgames.jl")
include("cyclefree.jl")
include("linkgames.jl")
include("rivergame.jl")

week = 3

if week == 1
    include("one/one.jl")
    include("one/three.jl")
elseif week == 2
    include("two/supply.jl")
    include("two/soc.jl")
elseif week == 3
    include("three/river.jl")
end