### A Pluto.jl notebook ###
# v0.12.21

using Markdown
using InteractiveUtils

# This Pluto notebook uses @bind for interactivity. When running this notebook outside of Pluto, the following 'mock version' of @bind gives bound variables a default value (instead of an error).
macro bind(def, element)
    quote
        local el = $(esc(element))
        global $(esc(def)) = Core.applicable(Base.get, el) ? Base.get(el) : missing
        el
    end
end

# ╔═╡ bac24656-923e-11eb-054d-55424acf2614
using Pkg

# ╔═╡ 860c8f7c-9243-11eb-31ce-050fe89e3b18
using PlutoUI

# ╔═╡ 2bb0493a-923f-11eb-2dc1-c752ae64cb48
using Plots, Luxor

# ╔═╡ 0b474090-9244-11eb-1ca9-b5af0254590c
begin
	struct MySlider 
		range::AbstractRange
		default::Number
	end
	function Base.show(io::IO, ::MIME"text/html", slider::MySlider)
		print(io, """
			<input type="range" 
			min="$(first(slider.range))" 
			step="$(step(slider.range))"
			max="$(last(slider.range))" 
			value="$(slider.default)"
			oninput="this.nextElementSibling.value=this.value">
			<output>$(slider.default)</output>""")
	end
end

# ╔═╡ aebe45b4-9241-11eb-3ab4-a3cc5a6da2e1
md"""

# Utils

"""

# ╔═╡ 1fbc28d6-9241-11eb-1a15-4b942c72996b
function pconstraint(n::Int)
	round(Int, inv(1/2 - 1/n))
end

# ╔═╡ 607e0694-9245-11eb-2779-0faea629e012
function radius(n::Int, p::Int)
	"""
	Find the radius of the outer circle
	"""
		
	γ = π / n # Center angle
	β = (π / p) + (π / 2) # Inner angle
	
	siner = sin(β) / sin(γ)
	
	r = sqrt(inv(siner^2 - 1))
	
	return r
		
end

# ╔═╡ e139a024-9246-11eb-15d1-1f871b20a933
distance(r) = sqrt(1 + r^2)

# ╔═╡ bfcb77fa-9241-11eb-1148-612a1efebc6c
md"""
# Drawing
"""

# ╔═╡ dd6019bc-9247-11eb-3bcf-e3f769a0e367
n = 6; lower = pconstraint(n)

# ╔═╡ e32b45da-9247-11eb-32dd-4fb653b2e09b
md"Adjacent, p: $(@bind p MySlider(7:100, 4))"

# ╔═╡ 441f58aa-9242-11eb-0575-4564ab7cefd7
begin
	w = 500
	h = w
	diskr = 200
end

# ╔═╡ c690e656-9241-11eb-1022-b3355267eed9
begin
	
	Drawing(w, h)
	origin(w / 2, h / 2)
	
	# --- Poincaré disk
	sethue("gray")
	disk = Point(0, 0)
	circle(disk, diskr, :fill)
	
	# --- Outer circle
	r = radius(n, p)
	len = distance(r)
	
	scaledr = r * diskr
	scaledlen = len * diskr
	Luxor.rotate(π * .12)

	for _ in 0:(n-1)
		sethue("white")
		angle = 2π / n
		Luxor.rotate(angle) # Rotate coordinate system
		center = disk + (scaledlen, 0.) # Center of the outer circle
		
		α = π * (1/2 + 1/n + 1/p)
		compα = 2π - α
		if false
			from = Point(scaledr * cos(α) + center.x, scaledr * sin(α) + center.y)
			to = Point(scaledr * cos(compα) + center.x, scaledr * sin(compα) + center.y)

			arc2r(center, from, to, :stroke)
		end
		
		circle(center, scaledr, :stroke)

		
	end
	
	
	finish(); preview() # Finish
end

# ╔═╡ Cell order:
# ╠═bac24656-923e-11eb-054d-55424acf2614
# ╠═860c8f7c-9243-11eb-31ce-050fe89e3b18
# ╠═2bb0493a-923f-11eb-2dc1-c752ae64cb48
# ╟─0b474090-9244-11eb-1ca9-b5af0254590c
# ╟─aebe45b4-9241-11eb-3ab4-a3cc5a6da2e1
# ╠═1fbc28d6-9241-11eb-1a15-4b942c72996b
# ╠═607e0694-9245-11eb-2779-0faea629e012
# ╠═e139a024-9246-11eb-15d1-1f871b20a933
# ╟─bfcb77fa-9241-11eb-1148-612a1efebc6c
# ╠═dd6019bc-9247-11eb-3bcf-e3f769a0e367
# ╠═e32b45da-9247-11eb-32dd-4fb653b2e09b
# ╟─441f58aa-9242-11eb-0575-4564ab7cefd7
# ╠═c690e656-9241-11eb-1022-b3355267eed9
