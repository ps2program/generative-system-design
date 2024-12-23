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

# Define the Requirement model with JSON data
class Requirement(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=False)
    data = Column(JSON, nullable=False)  # Store Requirement as JSON

    component = relationship("Component", back_populates="requirements")
    functions = relationship("Function", secondary=requirement_function_association, back_populates="requirements")

    def __repr__(self):
        return f"<Requirement(id={self.id}, data={self.data})>"

# Define the Function model with JSON data
class Function(Base):
    __tablename__ = 'functions'

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)  # Store Function as JSON

    requirements = relationship("Requirement", secondary=requirement_function_association, back_populates="functions")
    physicals = relationship("Physical", secondary=function_physical_association, back_populates="functions")

    def __repr__(self):
        return f"<Function(id={self.id}, data={self.data})>"

# Define the Physical model with JSON data
class Physical(Base):
    __tablename__ = 'physicals'

    id = Column(Integer, primary_key=True)
    data = Column(JSON, nullable=False)  # Store Physical as JSON

    functions = relationship("Function", secondary=function_physical_association, back_populates="physicals")

    def __repr__(self):
        return f"<Physical(id={self.id}, data={self.data})>"

# Database setup
engine = create_engine('sqlite:///rflp_component_json_relations.db')
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Example data
component = Component(name="Electric Scooter", description="Personal electric scooter system")

requirement1 = Requirement(data={"description": "Charge time to 80%", "spec": "2 hours"}, component=component)
requirement2 = Requirement(data={"description": "Power for 40 miles", "spec": "10Ah battery"}, component=component)

function1 = Function(data={"description": "Turn on/off", "operation": "switch control"})
function2 = Function(data={"description": "Charging", "operation": "plug-in charging"})
function3 = Function(data={"description": "Acceleration control", "operation": "handle control"})

# Establish relationships between requirements and functions
requirement1.functions.extend([function1, function2])
requirement2.functions.append(function3)

physical1 = Physical(data={"component": "Battery", "type": "Lithium-ion, 48V"})
physical2 = Physical(data={"component": "Motor", "type": "Hub motor"})

# Establish relationships between functions and physical elements
function2.physicals.append(physical1)  # Charging function related to Battery
function3.physicals.append(physical2)  # Acceleration control function related to Motor

# Add and commit all entities
session.add_all([component, requirement1, requirement2, function1, function2, function3, physical1, physical2])
session.commit()

# Query example: Print component, requirements, functions, and physicals with JSON data
for comp in session.query(Component).all():
    print(comp)
    for req in comp.requirements:
        print(f"  Requirement: {req.data}")
        for func in req.functions:
            print(f"    Function: {func.data}")
            for phys in func.physicals:
                print(f"      Physical: {phys.data}")

# Close session
session.close()
