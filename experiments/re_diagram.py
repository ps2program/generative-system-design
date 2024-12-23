from eralchemy import render_er

# Define the database schema in ERD format
schema = """
[components] {
    id Integer [PK]
    name String
    description String
}

[requirements] {
    id Integer [PK]
    component_id Integer [FK]
    data JSON
}

[functions] {
    id Integer [PK]
    data JSON
}

[physicals] {
    id Integer [PK]
    data JSON
}

[requirement_function] {
    requirement_id Integer [FK]
    function_id Integer [FK]
}

[function_physical] {
    function_id Integer [FK]
    physical_id Integer [FK]
}

[sub_requirement] {
    parent_id Integer [FK]
    child_id Integer [FK]
}

[sub_function] {
    parent_id Integer [FK]
    child_id Integer [FK]
}

[sub_physical] {
    parent_id Integer [FK]
    child_id Integer [FK]
}

components *--1 requirements: "has many"
requirements *--* functions: "maps to"
functions *--* physicals: "maps to"
requirements *--* requirements: "sub-requirements"
functions *--* functions: "sub-functions"
physicals *--* physicals: "sub-physicals"
"""

# Generate the ER diagram as a PNG image
output_path = '/mnt/data/rflp_er_diagram.png'
render_er(schema, output_path)

