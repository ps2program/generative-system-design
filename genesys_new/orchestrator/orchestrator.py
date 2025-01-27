from database.state_memory import state_memory
class Orchestrator:
    def __init__(self, state_memory):
        """
        Initializes the Orchestrator with the provided state memory.

        Args:
            state_memory (object): The state memory instance that handles data operations.
        """
        self.state_memory = state_memory

#  1. Uploaders
    def batch_top_level_requirement_upload(self, requirement_data):
        """
        Adds multiple top-level requirements to a given component.

        Args:
            component_id (str): The ID of the component to which the requirements should be added.
            requirement_data (list): A list of data for each requirement.

        Returns:
            list: A list of added requirement objects.
        """
        
            # Check if system exists in state_memory, create one if not
        if not hasattr(state_memory, 'system') or not state_memory.system:
            # Assuming a system object needs to be created here
            state_memory.system = self.state_memory.add_component("xSystems")


        component_id = state_memory.system.id
        added_requirements = []
        for data in requirement_data:
            try:
                requirement = self.state_memory.add_requirement(component_id, data)
                added_requirements.append(requirement)
            except ValueError as e:
                print(f"Error adding requirement to component {component_id}: {e}")
        return added_requirements

    def batch_sub_requirement_upload(self, parent_requirement_id, requirement_data):
        """
        Adds multiple sub-requirements to a given parent requirement.

        Args:
            parent_requirement_id (str): The ID of the parent requirement.
            requirement_data (list): A list of data for each sub-requirement.

        Returns:
            list: A list of added sub-requirement objects.
        """
        added_sub_requirements = []
        for data in requirement_data:
            try:
                sub_requirement = self.state_memory.add_sub_requirement_to_requirement(parent_requirement_id, data)
                added_sub_requirements.append(sub_requirement)
            except ValueError as e:
                print(f"Error adding sub-requirement to parent requirement {parent_requirement_id}: {e}")
        return added_sub_requirements

    def batch_function_upload(self, requirement_id, function_data):
        """
        Adds multiple functions to a given requirement.

        Args:
            requirement_id (str): The ID of the requirement to which the functions should be added.
            function_data (list): A list of data for each function.

        Returns:
            list: A list of added function objects.
        """
        added_functions = []
        for data in function_data:
            try:
                function = self.state_memory.add_function(data)
                function = self.state_memory.add_function_to_requirement(function.id,requirement_id)
                added_functions.append(function)
            except ValueError as e:
                print(f"Error adding function to requirement {requirement_id}: {e}")
        return added_functions
    
    def batch_sub_function_upload(self, parent_function_id, sub_function_data):
        """
        Adds multiple sub-functions to a given parent function.

        Args:
            parent_function_id (str): The ID of the parent function.
            sub_function_data (list): A list of data for each sub-function.

        Returns:
            list: A list of added sub-function objects.
        """
        added_sub_functions = []
        for data in sub_function_data:
            try:
                # Add sub-function to the parent function in state memory
                sub_function = self.state_memory.add_sub_function_to_function(parent_function_id, data)
                added_sub_functions.append(sub_function)
            except ValueError as e:
                print(f"Error adding sub-function to parent function {parent_function_id}: {e}")
        return added_sub_functions

    def batch_physical_upload_to_function(self, function_id, physical_data):
        """
        Adds multiple physicals to a given function.

        Args:
            function_id (str): The ID of the function to which the physicals should be added.
            physical_data (list): A list of data for each physical.

        Returns:
            list: A list of added physical objects to the function.
        """
        added_physicals = []
        for data in physical_data:
            try:
                physical = self.state_memory.add_physical(data)
                physical = self.state_memory.add_physical_to_function(physical.id, function_id)
                added_physicals.append(physical)
            except ValueError as e:
                print(f"Error adding physical to function {function_id}: {e}")
        return added_physicals

    def batch_physical_upload_to_requirement(self, requirement_id, physical_data):
        """
        Adds multiple physicals to a given requirement.

        Args:
            requirement_id (str): The ID of the requirement to which the physicals should be added.
            physical_data (list): A list of data for each physical.

        Returns:
            list: A list of added physical objects to the requirement.
        """
        added_physicals = []
        for data in physical_data:
            try:
                # First, add the physical to the state memory
                physical = self.state_memory.add_physical(data)
                
                # Associate the physical with the requirement
                self.state_memory.add_physical_to_requirement(physical.id, requirement_id)
                
                added_physicals.append(physical)
            except ValueError as e:
                print(f"Error adding physical to requirement {requirement_id}: {e}")
        return added_physicals

    def batch_sub_physical_upload(self, parent_physical_id, sub_physical_data):
        """
        Adds multiple sub-physicals to a given parent physical entity.

        Args:
            parent_physical_id (str): The ID of the parent physical entity.
            sub_physical_data (list): A list of data for each sub-physical.

        Returns:
            list: A list of added sub-physical objects.
        """
        added_sub_physicals = []
        for data in sub_physical_data:
            try:
                # Add sub-physical to the parent physical in state memory
                sub_physical = self.state_memory.add_sub_physical_to_physical(parent_physical_id, data)
                added_sub_physicals.append(sub_physical)
            except ValueError as e:
                print(f"Error adding sub-physical to parent physical {parent_physical_id}: {e}")
        return added_sub_physicals

#  2. Retrievers

    def get_all_requirements(self):
        """
        Retrieves all requirements from the state memory.

        Returns:
            list: A list of all requirements.
        """
        try:
            all_requirements = self.state_memory.get_all_requirements()
            return all_requirements
        except ValueError as e:
            print(f"Error retrieving all requirements: {e}")
            return []

    def get_all_functions(self):
        """
        Retrieves all functions from the state memory.

        Returns:
            list: A list of all functions.
        """
        try:
            all_functions = self.state_memory.get_all_functions()
            return all_functions
        except ValueError as e:
            print(f"Error retrieving all functions: {e}")
            return []

    def get_all_physicals(self):
        """
        Retrieves all physicals from the state memory.

        Returns:
            list: A list of all physicals.
        """
        try:
            all_physicals = self.state_memory.get_all_physicals()
            return all_physicals
        except ValueError as e:
            print(f"Error retrieving all physicals: {e}")
            return []


orchestrator = Orchestrator(state_memory)