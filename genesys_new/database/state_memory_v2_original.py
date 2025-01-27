import uuid

class Component:
    def __init__(self, name, description=None):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.requirements = []  # List of requirements associated with this component

    def __repr__(self):
        return f"<Component(id={self.id}, name='{self.name}', description='{self.description}')>"

class Requirement:
    def __init__(self, component, data):
        self.id = uuid.uuid4()
        self.component = component  # Link to the parent component
        self.data = data
        self.functions = []  # List of functions related to this requirement
        self.physicals = []  # List of physicals related to this requirement
        self._sub_requirements = []  # Internal list of sub-requirements
        self._parent_requirements = []  # Internal list of parent requirements
        
        if component:
            component.requirements.append(self)  # Adding this requirement to the component

    def __repr__(self):
        return f"<Requirement(id={self.id}, data={self.data})>"

    # Property for sub_requirements with automatic syncing
    @property
    def sub_requirements(self):
        return self._sub_requirements

    @sub_requirements.setter
    def sub_requirements(self, sub_requirements):
        for sub_req in sub_requirements:
            self.add_sub_requirement(sub_req)

    # Property for parent_requirements with automatic syncing
    @property
    def parent_requirements(self):
        return self._parent_requirements

    @parent_requirements.setter
    def parent_requirements(self, parent_requirements):
        for parent_req in parent_requirements:
            self.add_parent_requirement(parent_req)

    # Method to automatically add sub-requirement with bidirectional syncing
    def add_sub_requirement(self, sub_requirement):
        if sub_requirement not in self._sub_requirements:
            self._sub_requirements.append(sub_requirement)
            if self not in sub_requirement._parent_requirements:
                sub_requirement._parent_requirements.append(self)

    # Method to automatically add parent-requirement with bidirectional syncing
    def add_parent_requirement(self, parent_requirement):
        if parent_requirement not in self._parent_requirements:
            self._parent_requirements.append(parent_requirement)
            if self not in parent_requirement._sub_requirements:
                parent_requirement._sub_requirements.append(self)

    # Removing sub-requirements automatically syncs the parent list
    def remove_sub_requirement(self, sub_requirement):
        if sub_requirement in self._sub_requirements:
            self._sub_requirements.remove(sub_requirement)
            if self in sub_requirement._parent_requirements:
                sub_requirement._parent_requirements.remove(self)

    # Remove parent requirement automatically syncs sub-requirements
    def remove_parent_requirement(self, parent_requirement):
        if parent_requirement in self._parent_requirements:
            self._parent_requirements.remove(parent_requirement)
            if self in parent_requirement._sub_requirements:
                parent_requirement._sub_requirements.remove(self)

    # Updating a sub-requirement automatically syncs back to the parent (optional)
    def update_sub_requirement(self, sub_requirement, new_data):
        if sub_requirement in self._sub_requirements:
            sub_requirement.data = new_data
            # Optionally propagate this update to parent if needed
            self.data = "Updated parent due to sub-requirement change"  # Example of syncing back
            
    def to_dict(self, visited=None):
        if visited is None:
            visited = set()
        
        if self.id in visited:
            return {
                "id": str(self.id),
                "component": self.component.to_dict() if hasattr(self.component, "to_dict") else str(self.component),
                "data": self.data,
            }

        visited.add(self.id)

        return {
            "id": str(self.id),
            "component": self.component.to_dict() if hasattr(self.component, "to_dict") else str(self.component),
            "data": self.data,
            "sub_requirements": [str(sr.id) for sr in self.sub_requirements],  # Include only IDs
            "parent_requirements": [str(pr.id) for pr in self.parent_requirements],  # Include only IDs
        }
class Function:
    def __init__(self, data):
        self.id = uuid.uuid4()
        self.data = data
        self.requirements = []  # List of requirements related to this function
        self.physicals = []  # List of physicals related to this function
        self._sub_functions = []  # Internal list of sub-functions
        self._parent_functions = []  # Internal list of parent functions

    def __repr__(self):
        return f"<Function(id={self.id}, data={self.data})>"

    # Property for sub_functions with automatic syncing
    @property
    def sub_functions(self):
        return self._sub_functions

    @sub_functions.setter
    def sub_functions(self, sub_functions):
        for sub_func in sub_functions:
            self.add_sub_function(sub_func)

    # Property for parent_functions with automatic syncing
    @property
    def parent_functions(self):
        return self._parent_functions

    @parent_functions.setter
    def parent_functions(self, parent_functions):
        for parent_func in parent_functions:
            self.add_parent_function(parent_func)

    # Method to automatically add sub-function with bidirectional syncing
    def add_sub_function(self, sub_function):
        if sub_function not in self._sub_functions:
            self._sub_functions.append(sub_function)
            if self not in sub_function._parent_functions:
                sub_function._parent_functions.append(self)

    # Method to automatically add parent-function with bidirectional syncing
    def add_parent_function(self, parent_function):
        if parent_function not in self._parent_functions:
            self._parent_functions.append(parent_function)
            if self not in parent_function._sub_functions:
                parent_function._sub_functions.append(self)

    # Removing sub-functions automatically syncs the parent list
    def remove_sub_function(self, sub_function):
        if sub_function in self._sub_functions:
            self._sub_functions.remove(sub_function)
            if self in sub_function._parent_functions:
                sub_function._parent_functions.remove(self)

    # Remove parent function automatically syncs sub-functions
    def remove_parent_function(self, parent_function):
        if parent_function in self._parent_functions:
            self._parent_functions.remove(parent_function)
            if self in parent_function._sub_functions:
                parent_function._sub_functions.remove(self)

    # Updating a sub-function automatically syncs back to the parent (optional)
    def update_sub_function(self, sub_function, new_data):
        if sub_function in self._sub_functions:
            sub_function.data = new_data
            # Optionally propagate this update to parent if needed
            self.data = "Updated parent due to sub-function change"  # Example of syncing back
    def to_dict(self, visited=None):
        if visited is None:
            visited = set()
        
        if self.id in visited:
            return {
                "id": str(self.id),
                "data": self.data,
            }

        visited.add(self.id)

        return {
            "id": str(self.id),
            "data": self.data,
            "requirements": [str(req.id) for req in self.requirements],  # Include only IDs
            "physicals": [str(phys.id) for phys in self.physicals],  # Include only IDs
            "sub_functions": [str(sf.id) for sf in self.sub_functions],  # Include only IDs
            "parent_functions": [str(pf.id) for pf in self.parent_functions],  # Include only IDs
        }

class Physical:
    def __init__(self, data):
        self.id = uuid.uuid4()
        self.data = data
        self.requirements = []  # List of requirements related to this physical
        self.functions = []  # List of functions related to this physical
        self._sub_physicals = []  # Internal list of sub-physicals
        self._parent_physicals = []  # Internal list of parent physicals

    def __repr__(self):
        return f"<Physical(id={self.id}, data={self.data})>"

    # Property for sub_physicals with automatic syncing
    @property
    def sub_physicals(self):
        return self._sub_physicals

    @sub_physicals.setter
    def sub_physicals(self, sub_physicals):
        for sub_phys in sub_physicals:
            self.add_sub_physical(sub_phys)

    # Property for parent_physicals with automatic syncing
    @property
    def parent_physicals(self):
        return self._parent_physicals

    @parent_physicals.setter
    def parent_physicals(self, parent_physicals):
        for parent_phys in parent_physicals:
            self.add_parent_physical(parent_phys)

    # Method to automatically add sub-physical with bidirectional syncing
    def add_sub_physical(self, sub_physical):
        if sub_physical not in self._sub_physicals:
            self._sub_physicals.append(sub_physical)
            if self not in sub_physical._parent_physicals:
                sub_physical._parent_physicals.append(self)

    # Method to automatically add parent-physical with bidirectional syncing
    def add_parent_physical(self, parent_physical):
        if parent_physical not in self._parent_physicals:
            self._parent_physicals.append(parent_physical)
            if self not in parent_physical._sub_physicals:
                parent_physical._sub_physicals.append(self)

    # Removing sub-physicals automatically syncs the parent list
    def remove_sub_physical(self, sub_physical):
        if sub_physical in self._sub_physicals:
            self._sub_physicals.remove(sub_physical)
            if self in sub_physical._parent_physicals:
                sub_physical._parent_physicals.remove(self)

    # Remove parent physical automatically syncs sub-physicals
    def remove_parent_physical(self, parent_physical):
        if parent_physical in self._parent_physicals:
            self._parent_physicals.remove(parent_physical)
            if self in parent_physical._sub_physicals:
                parent_physical._sub_physicals.remove(self)

    # Updating a sub-physical automatically syncs back to the parent (optional)
    def update_sub_physical(self, sub_physical, new_data):
        if sub_physical in self._sub_physicals:
            sub_physical.data = new_data
            # Optionally propagate this update to parent if needed
            self.data = "Updated parent due to sub-physical change"  # Example of syncing back
    def to_dict(self, visited=None):
        if visited is None:
            visited = set()
        
        if self.id in visited:
            return {
                "id": str(self.id),
                "data": self.data,
            }

        visited.add(self.id)

        return {
            "id": str(self.id),
            "data": self.data,
            "requirements": [str(req.id) for req in self.requirements],  # Include only IDs
            "functions": [str(func.id) for func in self.functions],  # Include only IDs
            "sub_physicals": [str(sp.id) for sp in self.sub_physicals],  # Include only IDs
            "parent_physicals": [str(pp.id) for pp in self.parent_physicals],  # Include only IDs
        }

class StateMemory:
    def __init__(self):
        self.system=None
        self.components = {}
        self.requirements = {}
        self.functions = {}
        self.physicals = {}

    # Add a new component
    def add_component(self, name, description=None):
        component = Component(name, description)
        self.components[component.id] = component
        self.system = component
        return component

    # Add a new requirement
    def add_requirement(self, component_id, data):
        component = self.components.get(component_id)
        if not component:
            raise ValueError(f"Component with ID {component_id} not found.")
        requirement = Requirement(component, data)
        self.requirements[requirement.id] = requirement
        return requirement

    # Add a new function
    def add_function(self, data):
        function = Function(data)
        self.functions[function.id] = function
        return function

    # Add a new physical
    def add_physical(self, data):
        physical = Physical(data)
        self.physicals[physical.id] = physical
        return physical

    # Associate a function with a requirement
    def add_function_to_requirement(self, function_id, requirement_id):
        function = self.functions.get(function_id)
        requirement = self.requirements.get(requirement_id)
        if not function or not requirement:
            raise ValueError(f"Function or Requirement not found.")
        
        # Add the relationship from both sides (Requirement ↔ Function)
        requirement.functions.append(function)
        function.requirements.append(requirement)
        return function

    # Associate a physical with a requirement
    def add_physical_to_requirement(self, physical_id, requirement_id):
        physical = self.physicals.get(physical_id)
        requirement = self.requirements.get(requirement_id)
        if not physical or not requirement:
            raise ValueError(f"Physical or Requirement not found.")
        
        # Add the relationship from both sides (Requirement ↔ Physical)
        requirement.physicals.append(physical)
        physical.requirements.append(requirement)

    # Associate a physical with a function
    def add_physical_to_function(self, physical_id, function_id):
        physical = self.physicals.get(physical_id)
        function = self.functions.get(function_id)
        if not physical or not function:
            raise ValueError(f"Physical or Function not found.")
        
        # Add the relationship from both sides (Function ↔ Physical)
        function.physicals.append(physical)
        physical.functions.append(function)
        return physical


    # Get a component by ID
    def get_component(self, component_id):
        return self.components.get(component_id)

    # Get a requirement by ID
    def get_requirement(self, requirement_id):
        return self.requirements.get(requirement_id)

    # Get a function by ID
    def get_function(self, function_id):
        return self.functions.get(function_id)

    # Get a physical by ID
    def get_physical(self, physical_id):
        return self.physicals.get(physical_id)
    
    def get_entity_by_id(self, entity_type, entity_id):
        """Fetch an entity (Component, Requirement, Function, or Physical) by its ID."""
        entity_map = {
            'component': self.components,
            'requirement': self.requirements,
            'function': self.functions,
            'physical': self.physicals
        }

        # Get the entity map based on the entity type
        entity_dict = entity_map.get(entity_type.lower())
        
        if not entity_dict:
            raise ValueError(f"Invalid entity type '{entity_type}'. Valid types are: 'component', 'requirement', 'function', 'physical'.")
        
        # Fetch the entity by ID
        entity = entity_dict.get(entity_id)
        
        if not entity:
            raise ValueError(f"{entity_type.capitalize()} with ID {entity_id} not found.")
        
        return entity
    
    def get_all_entities(self):
        """Fetch all entities grouped by their type."""
        return {
            'components': list(self.components.values()),
            'requirements': list(self.requirements.values()),
            'functions': list(self.functions.values()),
            'physicals': list(self.physicals.values())
        }
    
    def get_all_entities_unrelated(self):
        """Fetch all entities with hierarchical data for components, requirements, functions, and physicals."""
        result = []

        for component in self.components.values():  # Iterate through all components
            component_data = {
                'id': component.id,
                'name': component.name,
                'description': component.description,
                'requirements': []
            }

            # Process requirements for the component
            for requirement in component.requirements:
                requirement_data = {
                    'id': requirement.id,
                    'data': requirement.data,
                    'functions': [],
                    'sub_requirements': [],
                    'physicals': []
                }

                # Process functions for the requirement
                for function in requirement.functions:
                    function_data = {
                        'id': function.id,
                        'data': function.data,
                        'physicals': [],
                        'sub_functions': []
                    }

                    # Process physicals for the function
                    for physical in function.physicals:
                        physical_data = {
                            'id': physical.id,
                            'data': physical.data,
                            'sub_physicals': []
                        }

                        # Add sub-physical elements
                        for sub_physical in physical.sub_physicals:
                            physical_data['sub_physicals'].append({
                                'id': sub_physical.id,
                                'data': sub_physical.data
                            })

                        function_data['physicals'].append(physical_data)

                    # Add sub-functions
                    for sub_function in function.sub_functions:
                        function_data['sub_functions'].append({
                            'id': sub_function.id,
                            'data': sub_function.data
                        })

                    requirement_data['functions'].append(function_data)

                # Add sub-requirements
                for sub_requirement in requirement.sub_requirements:
                    requirement_data['sub_requirements'].append({
                        'id': sub_requirement.id,
                        'data': sub_requirement.data
                    })

                # Process physicals for the requirement
                for physical in requirement.physicals:
                    physical_data = {
                        'id': physical.id,
                        'data': physical.data,
                        'sub_physicals': []
                    }

                    # Add sub-physical elements
                    for sub_physical in physical.sub_physicals:
                        physical_data['sub_physicals'].append({
                            'id': sub_physical.id,
                            'data': sub_physical.data
                        })

                    requirement_data['physicals'].append(physical_data)

                component_data['requirements'].append(requirement_data)

            result.append(component_data)

        return result

    # Update a component
    def update_component(self, component_id, new_name=None, new_description=None):
        component = self.get_component(component_id)
        if not component:
            raise ValueError(f"Component with ID {component_id} not found.")
        if new_name:
            component.name = new_name
        if new_description:
            component.description = new_description
        return component

    # Update a requirement
    def update_requirement(self, requirement_id, new_data=None):
        requirement = self.get_requirement(requirement_id)
        if not requirement:
            raise ValueError(f"Requirement with ID {requirement_id} not found.")
        if new_data:
            requirement.data = new_data
        return requirement

    # Update a function
    def update_function(self, function_id, new_data=None):
        function = self.get_function(function_id)
        if not function:
            raise ValueError(f"Function with ID {function_id} not found.")
        if new_data:
            function.data = new_data
        return function

    # Update a physical
    def update_physical(self, physical_id, new_data=None):
        physical = self.get_physical(physical_id)
        if not physical:
            raise ValueError(f"Physical with ID {physical_id} not found.")
        if new_data:
            physical.data = new_data
        return physical

    # Delete a component by ID
    def delete_component(self, component_id):
        if component_id in self.components:
            del self.components[component_id]

    # Delete a requirement by ID
    def delete_requirement(self, requirement_id):
        if requirement_id in self.requirements:
            del self.requirements[requirement_id]

    # Delete a function by ID
    def delete_function(self, function_id):
        if function_id in self.functions:
            del self.functions[function_id]

    # Delete a physical by ID
    def delete_physical(self, physical_id):
        if physical_id in self.physicals:
            del self.physicals[physical_id]

    # Miscellaneous getters
    def get_all_components(self):
        """Fetch all components with their details and associated requirements."""
        result = []
        for component in self.components.values():
            component_data = {
                'id': component.id,
                'name': component.name,
                'description': component.description,
                'requirements': [
                    {'id': req.id, 'data': req.data} for req in component.requirements
                ]
            }
            result.append(component_data)
        return result

    def get_all_requirements(self):
        """Fetch all requirements with their details and associated functions."""
        result = []
        for requirement in self.requirements.values():
            requirement_data = {
                'id': requirement.id,
                'data': requirement.data,
                'functions': [
                    {'id': func.id, 'data': func.data} for func in requirement.functions
                ],
                'sub_requirements': [
                    {'id': sub_req.id, 'data': sub_req.data} for sub_req in requirement.sub_requirements
                ],
                'physicals': [
                    {'id': phys.id, 'data': phys.data} for phys in requirement.physicals
                ]
            }
            result.append(requirement_data)
        return result

    def get_all_functions(self):
        """Fetch all functions with their details and associated physicals."""
        result = []
        for function in self.functions.values():
            function_data = {
                'id': function.id,
                'data': function.data,
                'physicals': [
                    {'id': phys.id, 'title': phys.data['title']} for phys in function.physicals
                ],
                'requirements': [
                    {'id': req.id, 'title': req.data['title']} for req in function.requirements
                ],
                'sub_functions': [
                    {'id': sub_func.id, 'data': sub_func.data} for sub_func in function.sub_functions
                ]
            }
            result.append(function_data)
        return result

    def get_all_physicals(self):
        """Fetch all physicals with their details and associated sub-physicals."""
        result = []
        for physical in self.physicals.values():
            physical_data = {
                'id': physical.id,
                'data': physical.data,
                'sub_physicals': [
                    {'id': sub_phys.id, 'data': sub_phys.data} for sub_phys in physical.sub_physicals
                ],
                'functions': [
                    {'id': func.id, 'title': func.data['title']} for func in physical.functions
                ],
            }
            result.append(physical_data)
        return result
    
    def clear_all(self):
        """Clears all components, requirements, functions, and physicals."""
        self.components.clear()
        self.requirements.clear()
        self.functions.clear()
        self.physicals.clear()
        
    # self-referencial Relations
    
    # 1. existing Node - self referential

    # 1. associate_sub_requirement_to_parent_requirement
    def associate_sub_requirement_to_parent_requirement(self, sub_requirement_id, parent_requirement_id):
        sub_requirement = self.requirements.get(sub_requirement_id)
        parent_requirement = self.requirements.get(parent_requirement_id)
        
        if not sub_requirement or not parent_requirement:
            raise ValueError(f"Sub-requirement or Parent requirement not found.")
        
        # Check if the sub-requirement is already associated with the parent requirement
        if sub_requirement in parent_requirement.sub_requirements:
            raise ValueError(f"Sub-requirement {sub_requirement_id} is already associated with Parent requirement {parent_requirement_id}.")
        
        # Add the relationship from both sides (Parent Requirement ↔ Sub-requirement)
        parent_requirement.sub_requirements.append(sub_requirement)
        sub_requirement.parent_requirements.append(parent_requirement)

    # 2. functions to subfunctions
    def associate_sub_function_to_function(self, sub_function_id, function_id):
        sub_function = self.functions.get(sub_function_id)
        function = self.functions.get(function_id)

        if not sub_function or not function:
            raise ValueError(f"Sub-function or Function not found.")

        # Check if the sub-function is already associated with the function
        if sub_function in function.sub_functions:
            raise ValueError(f"Sub-function {sub_function_id} is already associated with Function {function_id}.")

        # Add the relationship from both sides (Function ↔ Sub-function)
        function.sub_functions.append(sub_function)
        sub_function.parent_functions.append(function)
        
    # 3. physical to subp-physical
    def associate_sub_physical_to_physical(self, sub_physical_id, physical_id):
        sub_physical = self.physicals.get(sub_physical_id)
        physical = self.physicals.get(physical_id)
        
        if not sub_physical or not physical:
            raise ValueError(f"Sub-physical or Physical not found.")
        
        # Check if the sub-physical is already associated with the physical
        if sub_physical in physical.sub_physicals:
            raise ValueError(f"Sub-physical {sub_physical_id} is already associated with Physical {physical_id}.")
        
        # Add the relationship from both sides (Physical ↔ Sub-physical)
        physical.sub_physicals.append(sub_physical)
        sub_physical.parent_physicals.append(physical)

    # 2. New Node creation - Self Referential\
        
    # Add a sub-requirement to a requirement
    def add_sub_requirement_to_requirement(self, parent_requirement_id, sub_requirement_data):
        parent_requirement = self.get_requirement(parent_requirement_id)
        if not parent_requirement:
            raise ValueError(f"Parent Requirement with ID {parent_requirement_id} not found.")
        
        sub_requirement = Requirement(parent_requirement.component, sub_requirement_data)
        parent_requirement.add_sub_requirement(sub_requirement)
        self.requirements[sub_requirement.id] = sub_requirement
        return sub_requirement
        
        # Add a sub-function to a function
    def add_sub_function_to_function(self, parent_function_id, sub_function_data):
        parent_function = self.get_function(parent_function_id)
        if not parent_function:
            raise ValueError(f"Parent Function with ID {parent_function_id} not found.")
        
        sub_function = Function(sub_function_data)
        parent_function.add_sub_function(sub_function)
        self.functions[sub_function.id] = sub_function
        return sub_function

    # Add a sub-physical to a physical
    def add_sub_physical_to_physical(self, parent_physical_id, sub_physical_data):
        parent_physical = self.get_physical(parent_physical_id)
        if not parent_physical:
            raise ValueError(f"Parent Physical with ID {parent_physical_id} not found.")
        
        sub_physical = Physical(sub_physical_data)
        parent_physical.add_sub_physical(sub_physical)
        self.physicals[sub_physical.id] = sub_physical
        return sub_physical


state_memory = StateMemory()