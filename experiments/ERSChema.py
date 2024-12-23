from graphviz import Digraph

# Initialize the graph
dot = Digraph('ER Schema', format='png')
dot.attr(rankdir='LR', size='8,5')

# Define nodes
dot.node('components', '[components]\n- id [PK]\n- name\n- description')
dot.node('requirements', '[requirements]\n- id [PK]\n- component_id [FK]\n- data [JSON]')
dot.node('functions', '[functions]\n- id [PK]\n- data [JSON]')
dot.node('physicals', '[physicals]\n- id [PK]\n- data [JSON]')
dot.node('requirement_function', '[requirement_function]\n- requirement_id [FK]\n- function_id [FK]')
dot.node('function_physical', '[function_physical]\n- function_id [FK]\n- physical_id [FK]')
dot.node('sub_requirement', '[sub_requirement]\n- parent_id [FK]\n- child_id [FK]')
dot.node('sub_function', '[sub_function]\n- parent_id [FK]\n- child_id [FK]')
dot.node('sub_physical', '[sub_physical]\n- parent_id [FK]\n- child_id [FK]')

# Define relationships
dot.edge('components', 'requirements', label='has many', arrowhead='crow', arrowsize='1.2')
dot.edge('requirements', 'functions', label='maps to', arrowhead='crow', dir='both', arrowsize='1.2')
dot.edge('functions', 'physicals', label='maps to', arrowhead='crow', dir='both', arrowsize='1.2')
dot.edge('requirements', 'requirements', label='sub-requirements', arrowhead='crow', dir='both', arrowsize='1.2')
dot.edge('functions', 'functions', label='sub-functions', arrowhead='crow', dir='both', arrowsize='1.2')
dot.edge('physicals', 'physicals', label='sub-physicals', arrowhead='crow', dir='both', arrowsize='1.2')

# Render the graph
dot.render('./er_schema_graph')
