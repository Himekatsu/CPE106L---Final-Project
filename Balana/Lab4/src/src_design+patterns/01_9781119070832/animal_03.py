# class Animal(object): 
#     """A class representing an arbitrary animal.""" 
#     def __init__(self, name): 
#         self.name = name 
#     def eat(self): 
#         pass 
#     def go_to_vet(self): 
#         pass


def create_animal_class(): 
    """Return an Animal class, built by invoking the type constructor. """ 
    class Animal(object): 
        """A class representing an arbitrary animal.""" 
        def __init__(self, name): 
            self.name = name 
        def eat(self): 
            pass 
        def go_to_vet(self): 
            pass
    return Animal 

animal = create_animal_class()
# print(type(animal))
