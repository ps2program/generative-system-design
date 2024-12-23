from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Association tables for many-to-many relationships
requirement_function_association = Table(
    'requirement_function', Base.metadata,
    Column('requirement_id', Integer, ForeignKey('requirements.id')),
    Column('function_id', Integer, ForeignKey('functions.id'))
)

function_physical_association = Table(
    'function_physical', Base.metadata,
    Column('function_id', Integer, ForeignKey('functions.id')),
    Column('physical_id', Integer, ForeignKey('physicals.id'))
)

# Self-referential association tables for sub-requirements, sub-functions, and sub-physicals
sub_requirement_association = Table(
    'sub_requirement', Base.metadata,
    Column('parent_id', Integer, ForeignKey('requirements.id')),
    Column('child_id', Integer, ForeignKey('requirements.id'))
)

sub_function_association = Table(
    'sub_function', Base.metadata,
    Column('parent_id', Integer, ForeignKey('functions.id')),
    Column('child_id', Integer, ForeignKey('functions.id'))
)

sub_physical_association = Table(
    'sub_physical', Base.metadata,
    Column('parent_id', Integer, ForeignKey('physicals.id')),
    Column('child_id', Integer, ForeignKey('physicals.id'))
)

# Define the top-level Component model
class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # One-to-many relationship with requirements
    requirements = relationship("Requirement", back_populates="component")

    def __repr__(self):
        return f"<Component(id={self.id}, name='{self.name}')>"

# Define the Requirement model with JSON data and self-referential sub-requirements
class Requirement(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=True)  # Made nullable for sub-requirements
    data = Column(JSON, nullable=False)  # Store Requirement as JSON

    component = relationship("Component", back_populates="requirements")
    functions = relationship("Function", secondary=requirement_function_association, back_populates="requirements")
    
    # Self-referential relationship for sub-requirements
    sub_requirements = relationship(
        "Requirement", secondary=sub_requirement_association,
        primaryjoin=id == sub_requirement_association.c.parent_id,
        secondaryjoin=id == sub_requirement_association.c.child_id,
        backref="parent_requirements"
    )

    def __repr__(self):
        return f"<Requirement(id={self.id}, data={self.data})>"

# Define the Function model with JSON data and self-referential sub-functions
class Function(Base):
    __tablename__ = 'functions'

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)  # Store Function as JSON

    requirements = relationship("Requirement", secondary=requirement_function_association, back_populates="functions")
    physicals = relationship("Physical", secondary=function_physical_association, back_populates="functions")
    
    # Self-referential relationship for sub-functions
    sub_functions = relationship(
        "Function", secondary=sub_function_association,
        primaryjoin=id == sub_function_association.c.parent_id,
        secondaryjoin=id == sub_function_association.c.child_id,
        backref="parent_functions"
    )

    def __repr__(self):
        return f"<Function(id={self.id}, data={self.data})>"

# Define the Physical model with JSON data and self-referential sub-physicals
class Physical(Base):
    __tablename__ = 'physicals'

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)  # Store Physical as JSON

    functions = relationship("Function", secondary=function_physical_association, back_populates="physicals")
    
    # Self-referential relationship for sub-physical elements
    sub_physicals = relationship(
        "Physical", secondary=sub_physical_association,
        primaryjoin=id == sub_physical_association.c.parent_id,
        secondaryjoin=id == sub_physical_association.c.child_id,
        backref="parent_physicals"
    )

    def __repr__(self):
        return f"<Physical(id={self.id}, data={self.data})>"

# Database setup
engine = create_engine('sqlite:///rflp_component_json_relations.db')
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# # Example data with sub-requirements, sub-functions, and sub-physicals
# component = Component(name="Electric Scooter", description="Personal electric scooter system")

# requirement1 = Requirement(data={"description": "Charge time to 80%", "spec": "2 hours"}, component=component)
# requirement2 = Requirement(data={"description": "Power for 40 miles", "spec": "10Ah battery"}, component=component)
# sub_requirement = Requirement(data={"description": "Battery longevity", "spec": "500 cycles"})

# requirement1.sub_requirements.append(sub_requirement)

# function1 = Function(data={"description": "Turn on/off", "operation": "switch control"})
# function2 = Function(data={"description": "Charging", "operation": "plug-in charging"})
# sub_function = Function(data={"description": "Fast charge", "operation": "boost charge mode"})

# function2.sub_functions.append(sub_function)

# physical1 = Physical(data={"component": "Battery", "type": "Lithium-ion, 48V"})
# physical2 = Physical(data={"component": "Motor", "type": "Hub motor"})
# sub_physical = Physical(data={"component": "Battery cells", "type": "High-density cells"})

# physical1.sub_physicals.append(sub_physical)

# # Establish relationships between requirements, functions, and physicals
# requirement1.functions.extend([function1, function2])
# requirement2.functions.append(function1)

# function2.physicals.append(physical1)
# function1.physicals.append(physical2)

# # Add and commit all entities
# session.add_all([component, requirement1, requirement2, sub_requirement, function1, function2, sub_function, physical1, physical2, sub_physical])
# session.commit()

# # Query example: Print component, requirements, sub-requirements, functions, sub-functions, and physicals with sub-physicals
# for comp in session.query(Component).all():
#     print(comp)
#     for req in comp.requirements:
#         print(f"  Requirement: {req.data}")
#         for sub_req in req.sub_requirements:
#             print(f"    Sub-Requirement: {sub_req.data}")
#         for func in req.functions:
#             print(f"    Function: {func.data}")
#             for sub_func in func.sub_functions:
#                 print(f"      Sub-Function: {sub_func.data}")
#             for phys in func.physicals:
#                 print(f"      Physical: {phys.data}")
#                 for sub_phys in phys.sub_physicals:
#                     print(f"        Sub-Physical: {sub_phys.data}")

# # Close session
# session.close()



#  example use case


import json
from sqlalchemy.orm import sessionmaker

# Example of your large JSON data (replace with actual data)
large_json_data2= [
    {
        "component_name": "Electric Scooter",
        "component_description": "Personal electric scooter system",
        "requirements": [
            {
                "description": "Charge time to 80%",
                "spec": "2 hours",
                "sub_requirements": [
                    {"description": "Battery longevity", "spec": "500 cycles"}
                ],
                "functions": [
                    {"description": "Turn on/off", "operation": "switch control"},
                    {"description": "Charging", "operation": "plug-in charging"}
                ],
                "physicals": [
                    {"component": "Battery", "type": "Lithium-ion, 48V"},
                    {"component": "Motor", "type": "Hub motor"}
                ]
            },
            {
                "description": "Power for 40 miles",
                "spec": "10Ah battery",
                "functions": [
                    {"description": "Power output", "operation": "regulated output"}
                ],
                "physicals": [
                    {"component": "Motor controller", "type": "PWM"}
                ]
            }
        ]
    }
]

large_json_data= [
    {
        "component_name": "Electric Scooter",
        "component_description": "Personal electric scooter system",
        "requirements": [
            {
                "description": "Charge time to 80%",
                "spec": "2 hours",
                "sub_requirements": [
                    {"description": "Battery longevity", "spec": "500 cycles"}
                ]
            },
            {
                "description": "Power for 40 miles",
                "spec": "10Ah battery"
               
            }
        ]
    }
]

# Setup SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()

def add_json_data(data):
    for component_data in data:
        # Create component
        component = Component(name=component_data["component_name"], description=component_data["component_description"])
        session.add(component)

        for req_data in component_data["requirements"]:
            # Create requirement
            requirement = Requirement(data=req_data, component=component)
            session.add(requirement)

            # Handle sub-requirements
            if 'sub_requirements' in req_data:
                for sub_req_data in req_data['sub_requirements']:
                    sub_requirement = Requirement(data=sub_req_data, component=component)
                    session.add(sub_requirement)
                    requirement.sub_requirements.append(sub_requirement)

            # Create functions and associate them
            if 'functions' in req_data: 
                for func_data in req_data["functions"]:
                    function = Function(data=func_data)
                    session.add(function)
                    requirement.functions.append(function)

                    # Handle sub-functions
                    if 'sub_functions' in func_data:
                        for sub_func_data in func_data["sub_functions"]:
                            sub_function = Function(data=sub_func_data)
                            session.add(sub_function)
                            function.sub_functions.append(sub_function)

                    # Create physicals and associate them
                    for phys_data in req_data["physicals"]:
                        physical = Physical(data=phys_data)
                        session.add(physical)
                        function.physicals.append(physical)

                        # Handle sub-physicals
                        if 'sub_physicals' in phys_data:
                            for sub_phys_data in phys_data["sub_physicals"]:
                                sub_physical = Physical(data=sub_phys_data)
                                session.add(sub_physical)
                                physical.sub_physicals.append(sub_physical)

        session.commit()

# Adding the JSON data to the database
add_json_data(large_json_data)


# query all
# Query to retrieve all components, their requirements, functions, physicals, and sub-elements
for component in session.query(Component).all():
    print(f"Component: {component.name}, Description: {component.description}")

    # Query requirements related to this component
    for req in component.requirements:
        print(f"  Requirement: {req.data['description']}, Spec: {req.data['spec']}")

        # Query sub-requirements for this requirement
        for sub_req in req.sub_requirements:
            print(f"    Sub-Requirement: {sub_req.data['description']}, Spec: {sub_req.data['spec']}")

        # Query functions related to this requirement
        for func in req.functions:
            print(f"    Function: {func.data['description']}, Operation: {func.data['operation']}")

            # Query sub-functions for this function
            for sub_func in func.sub_functions:
                print(f"      Sub-Function: {sub_func.data['description']}, Operation: {sub_func.data['operation']}")

            # Query physicals related to this function
            for phys in func.physicals:
                print(f"      Physical: {phys.data['component']}, Type: {phys.data['type']}")

                # Query sub-physicals for this physical
                for sub_phys in phys.sub_physicals:
                    print(f"        Sub-Physical: {sub_phys.data['component']}, Type: {sub_phys.data['type']}")

# Close session
session.close()



# Close session
session.close()





# ?_____________________________



def add_requirement(session, component_id, data):
    """
    Adds a new requirement to the database.
    """
    requirement = Requirement(component_id=component_id, data=data)
    session.add(requirement)
    session.commit()
    return requirement

def add_sub_requirement(session, parent_requirement_id, data):
    """
    Adds a new sub-requirement to a parent requirement.
    """
    parent_requirement = session.query(Requirement).get(parent_requirement_id)
    if not parent_requirement:
        raise ValueError(f"No parent requirement found with ID {parent_requirement_id}")

    sub_requirement = Requirement(data=data)
    parent_requirement.sub_requirements.append(sub_requirement)
    session.add(sub_requirement)
    session.commit()
    return sub_requirement

def add_function(session, data):
    """
    Adds a new function to the database.
    """
    function = Function(data=data)
    session.add(function)
    session.commit()
    return function

def add_sub_function(session, parent_function_id, data):
    """
    Adds a new sub-function to a parent function.
    """
    parent_function = session.query(Function).get(parent_function_id)
    if not parent_function:
        raise ValueError(f"No parent function found with ID {parent_function_id}")

    sub_function = Function(data=data)
    parent_function.sub_functions.append(sub_function)
    session.add(sub_function)
    session.commit()
    return sub_function

def add_physical(session, data):
    """
    Adds a new physical entity to the database.
    """
    physical = Physical(data=data)
    session.add(physical)
    session.commit()
    return physical

def add_sub_physical(session, parent_physical_id, data):
    """
    Adds a new sub-physical entity to a parent physical entity.
    """
    parent_physical = session.query(Physical).get(parent_physical_id)
    if not parent_physical:
        raise ValueError(f"No parent physical found with ID {parent_physical_id}")

    sub_physical = Physical(data=data)
    parent_physical.sub_physicals.append(sub_physical)
    session.add(sub_physical)
    session.commit()
    return sub_physical
# --------

requirement = add_requirement(session, component_id=1, data={"title": "Requirement 1", "description": "Top-level requirement"})
print(requirement)


sub_requirement = add_sub_requirement(session, parent_requirement_id=requirement.id, data={"title": "Sub-Requirement 1", "description": "Child of Requirement 1"})
print(sub_requirement)


function = add_function(session, data={"name": "Function 1", "description": "Top-level function"})
print(function)


sub_function = add_sub_function(session, parent_function_id=function.id, data={"name": "Sub-Function 1", "description": "Child of Function 1"})
print(sub_function)


physical = add_physical(session, data={"name": "Physical 1", "description": "Top-level physical entity"})
print(physical)


sub_physical = add_sub_physical(session, parent_physical_id=physical.id, data={"name": "Sub-Physical 1", "description": "Child of Physical 1"})
print(sub_physical)


# --- complete query


from sqlalchemy.orm import joinedload

def get_component_hierarchy(component_id: int, session):
    """
    Retrieve the full hierarchy for a component from the database.
    
    Args:
        component_id (int): The ID of the component to retrieve.
        session: SQLAlchemy session object.
        
    Returns:
        list: Nested list of JSON-like structures representing the hierarchy.
    """
    
    def retrieve_sub_requirements(requirement):
        """ Recursively retrieve sub-requirements for a given requirement. """
        sub_requirements_data = []
        for sub_requirement in requirement.sub_requirements:
            sub_requirements_data.append({
                "id": sub_requirement.id,
                "data": sub_requirement.data,
                "sub_requirements": retrieve_sub_requirements(sub_requirement)
            })
        return sub_requirements_data

    def retrieve_sub_functions(function):
        """ Recursively retrieve sub-functions for a given function. """
        sub_functions_data = []
        for sub_function in function.sub_functions:
            sub_functions_data.append({
                "id": sub_function.id,
                "data": sub_function.data,
                "sub_functions": retrieve_sub_functions(sub_function)
            })
        return sub_functions_data
    
    def retrieve_sub_physicals(physical):
        """ Recursively retrieve sub-physicals for a given physical. """
        sub_physicals_data = []
        for sub_physical in physical.sub_physicals:
            sub_physicals_data.append({
                "id": sub_physical.id,
                "data": sub_physical.data,
                "sub_physicals": retrieve_sub_physicals(sub_physical)
            })
        return sub_physicals_data
    
    # Query the component by ID
    component = session.query(Component).filter(Component.id == component_id).first()
    
    if not component:
        raise ValueError(f"Component with id {component_id} not found.")

    # Build the JSON-like structure for the component
    component_data = {
        "id": component.id,
        "name": component.name,
        "description": component.description,
        "requirements": []
    }

    for requirement in component.requirements:
        requirement_data = {
            "id": requirement.id,
            "data": requirement.data,
            "sub_requirements": retrieve_sub_requirements(requirement),
            "functions": []
        }
        
        for function in requirement.functions:
            function_data = {
                "id": function.id,
                "data": function.data,
                "sub_functions": retrieve_sub_functions(function),
                "physicals": []
            }
            
            for physical in function.physicals:
                physical_data = {
                    "id": physical.id,
                    "data": physical.data,
                    "sub_physicals": retrieve_sub_physicals(physical)
                }
                function_data["physicals"].append(physical_data)
            
            requirement_data["functions"].append(function_data)
        
        component_data["requirements"].append(requirement_data)
    
    return [component_data]


