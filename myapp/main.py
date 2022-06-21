from fastapi import Depends, FastAPI, status, Response
from . import schema, models
from .db import SessionLocal, engine
from sqlalchemy.orm import Session
from .coordinate import coordinate
from geopy.distance import geodesic

app = FastAPI()  # creating an instance of fastapi

models.Base.metadata.create_all(engine)

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#operation= get or post or put or delete
#path = "/createAddress or "/readAllAddress".."
# @app is path operaation decorator
# def create_address is path operation function
# creating an address from request body 
@app.post("/createAddress", status_code=status.HTTP_201_CREATED)
def create_address(req: schema.Address, res:Response, db :Session = Depends(getDb)):
    try:
        # removing leading and ending extra space 
        userAddress = req.userAddress.strip()
        userName = req.userName
        city = req.city.strip()
        state = req.state.strip()
        postalCode = req.postalCode

        # getting the location & coordinate data from mapquest api 
        locationData = coordinate(userAddress, city, state)

        # creaing new row for address table 
        newAddress = models.Address(
            userAddress = userAddress,
            userName = userName,
            city = city,
            state = state,
            country = locationData["adminArea1"],
            postalCode = postalCode,
            longitude =  locationData["latLng"]["lng"],
            latitude =  locationData["latLng"]["lat"],
            mapUrl = locationData["mapUrl"]
        )

        # adding row to tabel
        db.add(newAddress)
        db.commit()
        db.refresh(newAddress)

        return {
            "status": "ok",
            "data": newAddress
        }

    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }

# get all the address 

@app.get("/getAllAddress", status_code=status.HTTP_200_OK)
def get_all_address(res: Response, db :Session = Depends(getDb)):
    try:
        # get all the address data from  database and send to user 
        allAddress = db.query(models.Address).all()
        return{
            "status" :"ok",
            "data" : allAddress
        }

    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }

# get those address that are nearest to the request body address {100 km}

@app.get("/findNearestAddress", status_code=status.HTTP_200_OK)
def get_nearest_address(res: Response, userAddress, city, state, db :Session = Depends(getDb)):
    try:
        # getting the location & coordinate data from mapquest api 
        locationData = coordinate(userAddress, city, state)
        queryCoordinate = locationData["latLng"]

        firstCoordinate = (queryCoordinate["lat"] , queryCoordinate["lng"])

        allAddress = db.query(models.Address).all()

        reqAddress = []

        for address in allAddress:
            secondCoordinate = (address.latitude, address.longitude)
            distanceBetween = geodesic(firstCoordinate, secondCoordinate).km
            if distanceBetween <= 100:
                reqAddress.append(address)
        

        # sending the nearest address data to user
        return {
            "status": "ok",
            "data" : reqAddress
        }

    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }



# update the address through id and request body 

@app.put("/updateAddress/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_address(id, req: schema.Address, res: Response, db: Session = Depends(getDb)):
    try:
        # removing leading and ending extra space 
        userAddress = req.userAddress.strip()
        userName  = req.userName
        city = req.city.strip()
        state = req.state.strip()
        postalCode = req.postalCode

        # getting the location & coordinate data from mapquest api 
        locationData = coordinate(userAddress, city, state)

        newAddress = {
            "userAddress" : userAddress,
            "userName": userName,
            "city" : city,
            "state" : state,
            "country" : locationData["adminArea1"],
            "postalCode" : postalCode,
            "longitude" :  locationData["latLng"]["lng"],
            "latitude" :  locationData["latLng"]["lat"],
            "mapUrl" : locationData["mapUrl"]
        }

        # updating address through id and query params 
        updatedAddress = db.query(models.Address).filter(models.Address.id == id).update(newAddress)

        # if data not found in database 
        if not updatedAddress:
            res.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status" : "failed",
                "msg" : f"Address id {id} not found"
            }

        db.commit()

        # if data got successfully updated 
        return {
            "status" : "ok",
            "data" : updatedAddress
        }
    
    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }



# delete the address through id 

@app.delete("/deleteAddress/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_address(id, res: Response, db: Session = Depends(getDb) ):
    try:
        # deleting address from databse through id
        deletedAddress = db.query(models.Address).filter(models.Address.id == id).delete(synchronize_session=False)

        # if data not found in database 
        if not deletedAddress:
            res.status_code = status.HTTP_404_NOT_FOUND
            return {
                "status" : "failed",
                "msg" : f"Address id {id} not found"
            }
        
        db.commit()

        # if data got sucessfully deleted 
        return {
            "status" : "ok",
            "data" : deletedAddress
        }

    except Exception as e:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "status" : "failed",
            "msg" : str(e)
        }
