def init(self, name):
    self.name = name 
def eat(self): 
    pass 
def go_to_vet(self): 
    pass 
Animal = type('Animal', (object,), { 
    '__doc__': 'A class representing an arbitrary animal.', 
    '__init__': init, 
    'eat': eat, 
    'go_to_vet': go_to_vet, 
    }
)
animal = Animal()
print(animal)