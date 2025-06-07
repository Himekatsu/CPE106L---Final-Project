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
    def init(self, name): 
        self.name = name 
    def eat(self): 
        pass 
    def go_to_vet(self): 
        # pass
        print('go to vet') 
    return type('Animal', (object,), { 
        '__doc__': 'A class representing an arbitrary animal.',
        '__init__': init, 
        'eat': eat, 
        'go_to_vet': go_to_vet,
    })


animal = create_animal_class()
animal.go_to_vet
# print(type(animal))
