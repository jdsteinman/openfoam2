module OpenFOAM
# Adapted from https://github.com/xu-xianghua/ofpp/blob/master/Ofpp/field_parser.py

using TikzPictures

"""
Input: list of lines, first line index to parse, last
       line index
Output: Either vector of vectors of floats or vector of floats
"""
function parse_data_nonuniform(content, n, n2)
    num = parse(Int, content[n+1])
    if occursin("scalar", content[n])
        return map(x -> parse(Float64, x), content[n + 3: n + 3 + num])
    else
        return filter(y -> length(y) > 0, map(x -> map(z -> parse(Float64, z), split(strip(x)[2:end-1])), content[n + 3: n + 3 + num]))
    end
end

"""
Input: line string
Output: Either float or vector of floats
"""
function parse_data_uniform(line)
    if occursin("(", line)
        return map(x -> parse(Float64, x), split(split(split(line, "(")[2], ")")[1]))
    else
        return parse(Float64, strip(split(split(line, "uniform")[2], ";")[1]))
    end
end

"""
Input: file
Output: unstructured parsed internal field
"""
function parse_internal_field(x)
    content = readlines(x)
    for (ln, lc) ∈ enumerate(content)
        if startswith(lc, "internalField")
            if occursin("nonuniform", lc)
                return parse_data_nonuniform(content, ln, length(content))
            else
                return parse_data_uniform(content[ln])
            end
        end
    end
end

function parse_poly_mesh(x)
    content1 = readlines(joinpath(x, "points"))
    parsing = false
    verts = Tuple[]
    for (ln, lc) ∈ enumerate(content1)
        if strip(lc) == "("
            parsing = true
            continue
        end
        if strip(lc) == ")"
            break
        end
        if parsing
            data = eval(Meta.parse(join(split(lc), ",")))
            push!(verts, data)
        end
    end
    parsing = false
    content2 = readlines(joinpath(x, "faces"))
    faces = Tuple[]
    for (ln, lc) ∈ enumerate(content2)
        if strip(lc) == "("
            parsing = true
            continue
        end
        if strip(lc) == ")"
            break
        end
        if parsing
            data = map(x -> verts[x+1], eval(Meta.parse(join(split(lc), ",")).args[3]))
            push!(faces, data)
        end
    end
    parsing = false
    content3 = readlines(joinpath(x, "owner"))
    cells = Dict{Int, Vector{Tuple}}()
    i = 1
    for (ln, lc) ∈ enumerate(content3)
        if strip(lc) == "("
            parsing = true
            continue
        end
        if strip(lc) == ")"
            break
        end
        if parsing
            idx = eval(Meta.parse(lc))
            if !haskey(cells, idx)
                push!(cells, idx => Tuple[])
            end
            push!(cells[idx], faces[i])
            i += 1
        end
    end
    parsing = false
    return cells
end

function tikzZ(polymesh, z = 0.5)
    
end

end
