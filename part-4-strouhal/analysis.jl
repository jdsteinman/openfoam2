### A Pluto.jl notebook ###
# v0.12.21

using Markdown
using InteractiveUtils

# ╔═╡ 6a415cf2-94e7-11eb-1b8f-356774686ade
begin
	using Plots
	include("OpenFOAM.jl")
end

# ╔═╡ 4dab3b2e-94f5-11eb-135d-b3559eeea058
using TikzPictures, PlutoUI, FFTW

# ╔═╡ 78bfc5b8-94e7-11eb-3ddd-1bfcb1e13a3d
base_dir = "t10A"

# ╔═╡ ca529c78-94e7-11eb-3059-336c298dbe1a
files = Dict(map(x -> x => OpenFOAM.parse_internal_field(joinpath(base_dir, "$x", "U")), sort(map(x -> parse(Int, x), filter(x -> try parse(Int, x); true catch e false end, readdir(base_dir)))))...)

# ╔═╡ 70c93db4-94e8-11eb-1364-73a4d744f07b
polymesh = OpenFOAM.parse_poly_mesh(joinpath(base_dir, "constant", "polyMesh"))

# ╔═╡ 1cb77b98-94eb-11eb-1454-a9d5cefce52d
joinpath(base_dir, "constant", "polyMesh")

# ╔═╡ 447db3b4-94ef-11eb-0266-798efbc18934
begin
	z = 0.5
	data = map(x -> x[1], files[400])
	m, b = ([maximum(data)  1; minimum(data)  1] \ [0, 1]...,)
	tkz = join(map(x -> begin
			l = polymesh[x-1]
			k = []
			color = Int(round((m * data[x] + b) * 100))
			for v ∈ l
				if all(map(y -> v[y][3] ≈ z, 1:4))
					return "\\fill[red!$(color)!blue] ($(v[1][1]),$(v[1][2])) -- ($(v[2][1]),$(v[2][2])) -- ($(v[3][1]),$(v[3][2])) -- ($(v[4][1]),$(v[4][2])) -- cycle;"
				end
			end
			k
			end, 1:length(data)), "\n") * "\n"
	TikzPicture(tkz)
end

# ╔═╡ 3d2cda4a-9506-11eb-360d-83e053386fe3
begin
	r = 78
	angle = 116
	x = r * cos(angle * π / 180)
	y = r * sin(angle * π / 180)
	(x, y)
end

# ╔═╡ 4bc1e7d6-94f8-11eb-3122-03a964bafee7
begin
function sign(p1, p2, p3)
    return (p1[1] - p3[1]) * (p2[2] - p3[2]) - (p2[1] - p3[1]) * (p1[2] - p3[2]);
end

function in_tri(pt, v1, v2, v3)
    
	d1 = sign(pt, v1, v2);
    d2 = sign(pt, v2, v3);
    d3 = sign(pt, v3, v1);

    has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0)
    has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0)

    return !(has_neg && has_pos);
end
end

# ╔═╡ dfd52e8a-94f6-11eb-3676-11022c8ff070
begin
	mul = 1
	mend = mul .* (cos((90 - 64) / 180 * π), sin((90 - 64) / 180 * π))
end

# ╔═╡ 07e1883c-94f8-11eb-064c-17bc89e82e41
kn = filter(x -> begin
		l = polymesh[x-1]
		for v ∈ l
			if all(map(y -> v[y][3] ≈ z, 1:4))
				return in_tri(mend, v[1][1:2], v[2][1:2], v[3][1:2]) || in_tri(mend, v[1][1:2], v[3][1:2], v[4][1:2])
			end
		end
		return false
	end, 1:length(data))

# ╔═╡ f4dffc1c-94f4-11eb-0a49-6d4cd7748e7e
TikzPicture(tkz * "\\draw[green, ->] (0, 0) -- $mend;")

# ╔═╡ bbeee512-94f9-11eb-30e6-69271e0a9105
dn = map(x -> x => begin
		if files[x] isa Vector{Float64}
			files[x][2]
		else
			files[x][kn[1]][2]
		end
	end, sort(collect(keys(files))))

# ╔═╡ 74f2b646-94fb-11eb-0f4b-71d9f53a24cb
function deriv(f)
	v = diff(f)
	[v..., v[end]]
end

# ╔═╡ 985e69a4-94fb-11eb-0760-cf6aa3c70e84
function find_root(f, a::Int, b::Int, ϵ = 1e-8)
  if (b - a) / 2 ≤ ϵ
    return (b + a) / 2
  end
  if b - a == 1
    return b
  end
  if abs(f[a]) < ϵ
    return a
  end
  if abs(f[b]) < ϵ
    return b
  end
  c = Int(round((b + a) / 2))
  if f[a] * f[c] > 0
    return find_root(f, c, b, ϵ)
  else
    return find_root(f, a, c, ϵ)
  end
end

# ╔═╡ a1c25474-94fb-11eb-2118-35f88a6b8fe8
begin
	nt = map(x -> x[1], dn) ./ 2
	nx = map(x -> x[2], dn)
	searchregion1 = [30, 60]
	searchregion2 = [60, 80]
	t0m = find_root(deriv(nx), searchregion1...)
	t1m = find_root(deriv(nx), searchregion2...)
	
	F = fft(nx) |> fftshift
	T = fftfreq(length(nt), diff(nt)[1]) |> fftshift
	
	fm = sort(collect(enumerate(F)), lt=(a,b) -> abs(a[2]) < abs(b[2]))[end]
	
	psd = plot(T .+ diff(T)[1], abs.(F), xlims=(0,1), legend=nothing, xlabel=L"St", ylabel=L"P", title="Spectral Density of Probe Signal", minorticks=5)
end

# ╔═╡ fb623732-94f9-11eb-1ac9-5f2c060694d5
begin
	plot(nt, nx, legend=nothing)
	scatter!([nt[t0m], nt[t1m]], [nx[t0m], nx[t1m]])
end

# ╔═╡ 82efe4fe-971b-11eb-2920-c3678fb76365
diff(T)[1]

# ╔═╡ 23d8dd28-971f-11eb-0ccf-f7e4e30dd855
savefig(psd, "psd.png")

# ╔═╡ Cell order:
# ╠═6a415cf2-94e7-11eb-1b8f-356774686ade
# ╠═4dab3b2e-94f5-11eb-135d-b3559eeea058
# ╠═78bfc5b8-94e7-11eb-3ddd-1bfcb1e13a3d
# ╠═ca529c78-94e7-11eb-3059-336c298dbe1a
# ╠═70c93db4-94e8-11eb-1364-73a4d744f07b
# ╠═1cb77b98-94eb-11eb-1454-a9d5cefce52d
# ╠═447db3b4-94ef-11eb-0266-798efbc18934
# ╠═3d2cda4a-9506-11eb-360d-83e053386fe3
# ╠═4bc1e7d6-94f8-11eb-3122-03a964bafee7
# ╠═dfd52e8a-94f6-11eb-3676-11022c8ff070
# ╠═07e1883c-94f8-11eb-064c-17bc89e82e41
# ╠═fb623732-94f9-11eb-1ac9-5f2c060694d5
# ╠═f4dffc1c-94f4-11eb-0a49-6d4cd7748e7e
# ╠═bbeee512-94f9-11eb-30e6-69271e0a9105
# ╠═74f2b646-94fb-11eb-0f4b-71d9f53a24cb
# ╠═985e69a4-94fb-11eb-0760-cf6aa3c70e84
# ╠═a1c25474-94fb-11eb-2118-35f88a6b8fe8
# ╠═82efe4fe-971b-11eb-2920-c3678fb76365
# ╠═23d8dd28-971f-11eb-0ccf-f7e4e30dd855
