from pydantic import BaseModel
#Pydantic allows custom data types to be defined or you can extend validation with methods on a model decorated with the validator decorator.

# using pydanttic BaseModel creating an request model 
class Address(BaseModel):
    userAddress: str 
    userName: str
    city: str 
    state: str
    postalCode: int