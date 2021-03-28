using Tokenize

function uncomment(x)
    join(map(y -> split(y, "//")[1], split(x, "\n")), "\n")
end

function parse_identifier(x, i)
    if Tokens.kind(x[i]) == Tokens.IDENTIFIER
        return untokenize(x[i]), i+1
    end
    if Tokens.kind(x[i]) == Tokens.KEYWORD
        return untokenize(x[i]), i+1
    end
    return nothing, 0
end

function parse_number(x, i)
    if Tokens.kind(x[i]) == Tokens.INTEGER
        return parse(Int64, untokenize(x[i])), i+1
    end
    if Tokens.kind(x[i]) == Tokens.FLOAT
        return parse(Float64, untokenize(x[i])), i+1
    end
    if Tokens.exactkind(x[i]) == Tokens.MINUS
        r, j = parse_item(x, i+1)
        if r isa Number
            return -r, j
        end
        return Expr(:call, :(-), r), j
    end
    return nothing, 0
end

function parse_dict(x, i)
    if Tokens.kind(x[i]) != Tokens.LBRACE
        return nothing, 0
    end
    args = []
    k = i + 1
    v, j = parse_dict_item(x, k)
    while j != 0
        push!(args, v)
        k = j
        v, j = parse_dict_item(x, k)
    end
    if Tokens.kind(x[k]) != Tokens.RBRACE
        println(x[k])
        return nothing, 0
    end
    Dict(args...), k+1
end

function parse_tuple(x, i)
    if Tokens.kind(x[i]) != Tokens.LPAREN
        return nothing, 0
    end
    args = []
    k = i + 1
    v, j = parse_item(x, k)
    while j != 0
        push!(args, v)
        k = j
        v, j = parse_item(x, k)
    end
    if Tokens.kind(x[k]) != Tokens.RPAREN
        return nothing, 0
    end
    (args...,), k+1
end

function parse_item(x, i)
    y, j = parse_identifier(x, i)
    if j != 0
        if Tokens.kind(x[j]) == Tokens.SEMICOLON
            return y, j+1
        end
        return y, j
    end
    y, j = parse_number(x, i)
    if j != 0
        if Tokens.kind(x[j]) == Tokens.SEMICOLON
            return y, j+1
        end
        return y, j
    end
    y, j = parse_dict(x, i)
    if j != 0
        if Tokens.kind(x[j]) == Tokens.SEMICOLON
            return y, j+1
        end
        return y, j
    end
    y, j = parse_tuple(x, i)
    if j != 0
        if Tokens.kind(x[j]) == Tokens.SEMICOLON
            return y, j+1
        end
        return y, j
    end
    return nothing, 0
end

function parse_dict_item(x, i)
    lhs, j = parse_identifier(x, i)
    if j == 0
        return nothing, 0
    end
    rhs, j = parse_item(x, j)
    if j == 0
        return nothing, 0
    end
    return Symbol(lhs) => rhs, j
end

function parsefile(filename)
    tks = filter(x -> Tokens.kind(x) != Tokens.WHITESPACE, collect(tokenize(uncomment(read(filename, String)))))

    args = []
    k = 1
    v, j = parse_dict_item(tks, k)
    while j != 0
        push!(args, v)
        k = j
        v, j = parse_dict_item(tks, k)
    end

    Dict(args...)
end

d = parsefile("blockMeshDict")

# Derived from diagram in https://cfd.direct/openfoam/user-guide/v6-blockmesh/
faceidxs = [
    [0, 1, 2, 3],
    [0, 4, 5, 1],
    [1, 5, 6, 2],
    [4, 7, 6, 5],
    [2, 6, 7, 3],
    [3, 7, 4, 0]
]

open("blockMesh.obj", "w") do io
    for vert ∈ d[:vertices]
        println(io, "v ", join(map(x -> string(x), vert), " "))
    end
    idx = 1
    for block ∈ 2:5:length(d[:blocks])
        println(io, "o Node.", idx)
        idx += 1
        blockdata = d[:blocks][block] .+ 1
        for idx ∈ faceidxs
            r = map(x -> blockdata[x], idx .+ 1)
            println(io, "f ", join(map(string, r), " "))
        end
        if idx == 15
            v = map(x -> d[:vertices][x], blockdata)
            for vk ∈ blockdata
                vkn = (vk > 32 ? vk - 32 : vk) - 1
                println(vkn => d[:vertices][vk])
            end
        end
    end
end