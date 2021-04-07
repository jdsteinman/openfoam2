using TikzPictures

include("OpenFOAM.jl")

base_dir = "unsteady"

files = Dict(
  map(
    x -> x => OpenFOAM.parse_internal_field(joinpath(base_dir, "$x", "U")),
    sort(
      map(x -> parse(Int, x), filter(x -> try
          parse(Int, x)
          true
        catch e
          false
        end, readdir(base_dir))),
    ),
  )...,
)

polymesh = OpenFOAM.parse_poly_mesh(joinpath(base_dir, "constant", "polyMesh"))

function sign(p1, p2, p3)
  return (p1[1] - p3[1]) * (p2[2] - p3[2]) - (p2[1] - p3[1]) * (p1[2] - p3[2])
end

function in_tri(pt, v1, v2, v3)

  d1 = sign(pt, v1, v2)
  d2 = sign(pt, v2, v3)
  d3 = sign(pt, v3, v1)

  has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0)
  has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0)

  return !(has_neg && has_pos)
end

mul = 1
mend = mul .* (cos((90 - 64) / 180 * π), sin((90 - 64) / 180 * π))

z = 0.5
data = map(x -> x[1], files[745])

kn = filter(
  x -> begin
    l = polymesh[x-1]
    for v ∈ l
      if all(map(y -> v[y][3] ≈ z, 1:4))
        return in_tri(mend, v[1][1:2], v[2][1:2], v[3][1:2]) ||
               in_tri(mend, v[1][1:2], v[3][1:2], v[4][1:2])
      end
    end
    return false
  end,
  1:length(data),
)

function deriv(f)
  v = diff(f)
  [v..., v[end]]
end

dn = map(x -> x => begin
  if files[x] isa Vector{Float64}
    files[x][2]
  else
    files[x][kn[1]][2]
  end
end, sort(collect(keys(files))))

function find_root(f, a::Int, b::Int, ϵ = 1e-8)
  if (b - a) / 2 ≤ ϵ
    return (b + a) / 2
  end
  if b - a == 1
    return a
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

nt = map(x -> x[1], dn)
nx = map(x -> x[2], dn)
searchregion1 = [30, 60]
searchregion2 = [80, 100]
t0m = find_root(deriv(nx), searchregion1...)
t1m = find_root(deriv(nx), searchregion2...)
T = (nt[t1m] - nt[t0m]) * 0.005

m, b = ([maximum(data) 1; minimum(data) 1] \ [0, 1]...,)

tkz =
  join(
    map(
      x -> begin
        l = polymesh[x-1]
        k = []
        color = Int(round((m * data[x] + b) * 100))
        for v ∈ l
          if all(map(y -> v[y][3] ≈ z, 1:4))
            return "\\fill[red!$(color)!blue] ($(v[1][1]),$(v[1][2])) -- ($(v[2][1]),$(v[2][2])) -- ($(v[3][1]),$(v[3][2])) -- ($(v[4][1]),$(v[4][2])) -- cycle;"
          end
        end
        k
      end,
      1:length(data),
    ),
    "\n",
  ) * "\n"

function tikzopts(args...; kwargs...)
  "[" *
  join(
    [
      map(x -> string(x), args)...,
      map(x -> "$(x)=$(kwargs[x])", collect(keys(kwargs)))...,
    ],
    ",",
  ) *
  "]"
end

function tikzplot(xs, ys, args...; kwargs...)
  t = xs
  u0 = ys
  "\\draw$(tikzopts(args...; kwargs...)) " *
  join(map(x -> "($(t[x]),$(u0[x]))", 1:length(t)), " -- ") *
  ";"
end

width = 9
height = 4

nxpos = nx .- minimum(nx)
ntpos = nt .- minimum(nt)

nxnormalizer = height / maximum(nxpos)
ntnormalizer = width / maximum(ntpos)

tout1 = tikzplot(ntpos .* ntnormalizer, nxpos .* nxnormalizer)

n1 = (ntpos[t0m] .* ntnormalizer, nxpos[t0m] .* nxnormalizer)
n2 = (ntpos[t1m] .* ntnormalizer, nxpos[t1m] .* nxnormalizer)

tout2 = "\\draw[<->] $(n1) -- $(n2) node[midway,below]{\$T\$}; \\draw[very thick] (0,-0.2) -- (0,$(height+0.2)) node[left,midway]{\$U_x\$} -- ($(width),$(height+0.2)) -- ($(width),-0.2) -- cycle node[below,midway]{\$t\$};"

tp = TikzPicture(tout1 * tout2)

save(SVG("temp"), tp)

run(`convert temp.svg temp.png`)
