class Car:  
  def drive(self):
     print("Starting the Car engine!")
  
class Bus:  
  def drive(self):
    print("Starting the Bus engine!")

class CarFactory:    
    def get_vehicle(self):
      ''' Return Car object'''
      return Car()
    

class VehicleStore:
    '''  VehicleStore houses Abstract Factory'''    
    def __init__(self, vehicle_factory=None):
        self._vehicle_factory = vehicle_factory        
    
    def buy_vehicle(self):
        vehicle = self._vehicle_factory.get_vehicle()
        vehicle.drive()
        

factory = CarFactory()
store = VehicleStore(factory)
store.buy_vehicle()