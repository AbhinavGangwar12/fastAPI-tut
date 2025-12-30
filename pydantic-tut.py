from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):

    house : Optional[int] = None
    city : str 
    state : str 
    pincode : int 


class Person(BaseModel):

    name : Annotated[str, Field(max_length=50, title="Name of the person", description='this is a description')]
    # email : Optional[EmailStr] = None
    email : EmailStr
    age : int = Field(gt=0, le=110)
    weight : float
    height : Annotated[float, Field(title="Height", description='Enter the height of the person in meters.')]
    address : Address
    hobbies : List[str] = Field(max_length=5)
    family_info : Optional[Dict[str, str]] = 'Not Available'
    @field_validator('email') #used to perform the field validation on a single field, it cannot perform field validation on multiple fields
    @classmethod 
    def validate(cls, value):
        valid_domains = ['gmail.com', 'hdfc.com', 'icici.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('not a valid email domain')
        else:
            return value 
    
    @model_validator(mode='after')
    def validator(cls, model):
        if model.age > 60 and 'son' not in model.family_info.keys:
            raise ValueError('Patients older than 60 should have their children in the family info.')
        return model 
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / self.height ** 2,2)
    

def print_person(person : Person):
    print(person.name)
    print(person.age)
    print(person.bmi)
    return 

address = {
    'city' : 'Bareilly',
    'state' : 'Uttar Pradesh',
    'pincode' : 243122
}

add_ress = Address(**address)


person_info = {
    'name' : 'Abhinav',
    'email' : 'abs@gmail.com',
    'age' : 22,
    'weight' : 82.5,
    'height' : 1.88,
    'address' : add_ress,
    'hobbies' : ['cricket', 'gym']
}
# person_info1 = {
#     'name' : 'Abhinav',
#     'email' : 'abs@gmil.com',
#     'age' : 22,
#     'hobbies' : ['cricket', 'gym']
# }

person1 = Person(**person_info)
# person2 = Person(**person_info1)

print_person(person1)
# print_person(person2)
