# db_module.py

import uuid
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, JSON, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

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

# Define the models
class Component(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    requirements = relationship("Requirement", back_populates="component")

    def __repr__(self):
        return f"<Component(id={self.id}, uuid={self.uuid}, name='{self.name}')>"

class Requirement(Base):
    __tablename__ = 'requirements'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    component_id = Column(Integer, ForeignKey('components.id'), nullable=True)
    data = Column(JSON, nullable=False)

    component = relationship("Component", back_populates="requirements")
    functions = relationship("Function", secondary=requirement_function_association, back_populates="requirements")
    
    sub_requirements = relationship(
        "Requirement", secondary=sub_requirement_association,
        primaryjoin=id == sub_requirement_association.c.parent_id,
        secondaryjoin=id == sub_requirement_association.c.child_id,
        backref="parent_requirements"
    )

    def __repr__(self):
        return f"<Requirement(id={self.id}, uuid={self.uuid}, data={self.data})>"

class Function(Base):
    __tablename__ = 'functions'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    data = Column(JSON, nullable=False)

    requirements = relationship("Requirement", secondary=requirement_function_association, back_populates="functions")
    physicals = relationship("Physical", secondary=function_physical_association, back_populates="functions")
    
    sub_functions = relationship(
        "Function", secondary=sub_function_association,
        primaryjoin=id == sub_function_association.c.parent_id,
        secondaryjoin=id == sub_function_association.c.child_id,
        backref="parent_functions"
    )

    def __repr__(self):
        return f"<Function(id={self.id}, uuid={self.uuid}, data={self.data})>"

class Physical(Base):
    __tablename__ = 'physicals'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    data = Column(JSON, nullable=False)

    functions = relationship("Function", secondary=function_physical_association, back_populates="physicals")
    
    sub_physicals = relationship(
        "Physical", secondary=sub_physical_association,
        primaryjoin=id == sub_physical_association.c.parent_id,
        secondaryjoin=id == sub_physical_association.c.child_id,
        backref="parent_physicals"
    )

    def __repr__(self):
        return f"<Physical(id={self.id}, uuid={self.uuid}, data={self.data})>"

# Database setup
DATABASE_URL = 'sqlite:///state_memory_db.db'
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# CRUD Operations

def add_component(session, name, description=None):
    """
    Adds a new component to the database.
    """
    # Create a new component instance
    component = Component(name=name, description=description)
    
    # Add and commit the component to the session
    session.add(component)
    session.commit()
    
    return component


def add_requirement(session, component_id, data):
    # uuid.UUID("ffe6d0cd-aeab-4838-8918-0cf729ed5b3b"))
    component = session.query(Component).filter_by(uuid=uuid.UUID(component_id)).first()
    if not component:
        raise ValueError(f"No component found with ID {component_id}")

    requirement = Requirement(component_id=component.id, data=data)
    session.add(requirement)
    session.commit()
    return requirement

def add_sub_requirement(session, parent_requirement_id, data):
    try:
        parent_requirement_id = uuid.UUID(parent_requirement_id)  # Convert string to UUID
    except ValueError:
        raise ValueError(f"Invalid UUID format for parent_requirement_id: {parent_requirement_id}")

    parent_requirement = session.query(Requirement).filter_by(uuid=parent_requirement_id).first()
    if not parent_requirement:
        raise ValueError(f"No parent requirement found with ID {parent_requirement_id}")

    sub_requirement = Requirement(data=data)
    session.add(sub_requirement)
    session.commit()

    parent_requirement.sub_requirements.append(sub_requirement)
    session.commit()
    return sub_requirement

def add_function(session, data):
    function = Function(data=data)
    session.add(function)
    session.commit()
    return function

def add_sub_function(session, parent_function_id, data):
    parent_function = session.query(Function).filter_by(uuid=parent_function_id).first()
    if not parent_function:
        raise ValueError(f"No parent function found with ID {parent_function_id}")

    sub_function = Function(data=data)
    session.add(sub_function)
    session.commit()

    parent_function.sub_functions.append(sub_function)
    session.commit()
    return sub_function

def add_physical(session, data):
    physical = Physical(data=data)
    session.add(physical)
    session.commit()
    return physical

def add_sub_physical(session, parent_physical_id, data):
    parent_physical = session.query(Physical).filter_by(uuid=parent_physical_id).first()
    if not parent_physical:
        raise ValueError(f"No parent physical found with ID {parent_physical_id}")

    sub_physical = Physical(data=data)
    session.add(sub_physical)
    session.commit()

    parent_physical.sub_physicals.append(sub_physical)
    session.commit()
    return sub_physical


# partial search

def search_components_by_name(session: Session, partial_name: str):
    components = session.query(Component).filter(Component.name.ilike(f"%{partial_name}%")).all()
    if not components:
        raise ValueError(f"No components found containing '{partial_name}'")

    return components

#  to get associated data when a field is updated
def get_associated_data(session, updated_id, model_type):
    """
    Retrieve all associated data for a given updated entry.
    
    :param session: SQLAlchemy session
    :param updated_id: ID of the updated entry
    :param model_type: Model type ('Component', 'Requirement', 'Function', or 'Physical')
    :return: Associated data
    """
    if model_type == "Component":
        updated_entry = session.query(Component).filter_by(id=updated_id).first()
        if not updated_entry:
            raise ValueError(f"No Component found with ID {updated_id}")
        associated_requirements = updated_entry.requirements
        associated_functions = [func for req in associated_requirements for func in req.functions]
        associated_physicals = [phys for func in associated_functions for phys in func.physicals]
    elif model_type == "Requirement":
        updated_entry = session.query(Requirement).filter_by(id=updated_id).first()
        if not updated_entry:
            raise ValueError(f"No Requirement found with ID {updated_id}")
        associated_functions = updated_entry.functions
        associated_physicals = [phys for func in associated_functions for phys in func.physicals]
        associated_requirements = [updated_entry]
    elif model_type == "Function":
        updated_entry = session.query(Function).filter_by(id=updated_id).first()
        if not updated_entry:
            raise ValueError(f"No Function found with ID {updated_id}")
        associated_physicals = updated_entry.physicals
        associated_requirements = updated_entry.requirements
        associated_functions = [updated_entry]
    elif model_type == "Physical":
        updated_entry = session.query(Physical).filter_by(id=updated_id).first()
        if not updated_entry:
            raise ValueError(f"No Physical found with ID {updated_id}")
        associated_functions = updated_entry.functions
        associated_requirements = [req for func in associated_functions for req in func.requirements]
        associated_physicals = [updated_entry]
    else:
        raise ValueError("Invalid model type. Must be 'Component', 'Requirement', 'Function', or 'Physical'.")

    # Build the results dictionary
    results = {
        "component": {
            "id": updated_entry.id,
            "name": getattr(updated_entry, "name", None) if model_type == "Component" else None
        },
        "requirements": [{"id": req.id, "data": req.data} for req in associated_requirements],
        "functions": [{"id": func.id, "data": func.data} for func in associated_functions],
        "physicals": [{"id": phys.id, "data": phys.data} for phys in associated_physicals]
    }

    return results
