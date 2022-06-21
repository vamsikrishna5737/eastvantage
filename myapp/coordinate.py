import requests

# using mapquest api for getting the coordinate of perticuller address 

# api Secret Key 
Key = "pvOpcxxAePN4A3ijS0ThQ4cCnAnYd6Ce"

# api end point with query ?location=
coordinateApi = f"http://www.mapquestapi.com/geocoding/v1/address?key={Key}&location="


# it's return the address information along with coordinate of and address 
# It's take 3 parameter and use them as location query for api 

def coordinate(userAddress, city, state):
    mainCoordinateApi = f"{coordinateApi}{userAddress},{city},{state}"
    r = requests.get(mainCoordinateApi)
    locationData = r.json()["results"][0]["locations"][0]
    return locationData