from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
from typing import List


class Characteristics(BaseModel):
    max_speed: int
    max_fuel_capacity: int


class CarModel(BaseModel):
    id: str
    brand: str
    model: str
    characteristics: Characteristics


app = FastAPI()
car_list: List[CarModel] = []


@app.get("/ping")
def ping():
    return Response(
        content="pong",
        status_code=200,
        media_type="text/plain"
    )


@app.post("/cars")
def create_car(new_cars_list: List[CarModel]):
    if len(new_cars_list) == 0:
        return Response(
            content="No cars to add",
            status_code=400,
            media_type="text/plain"
        )

    car_list.extend(new_cars_list)

    return Response(
        content=f"{len(new_cars_list)} cars added successfully",
        status_code=201,
        media_type="text/plain"
    )


@app.get("/cars")
def get_cars():
    return car_list


@app.get("/cars/{id}")
def get_car_by_id(given_id: str):
    for car in car_list:
        if car.id == given_id:
            return Response(
                content=car,
                status_code=200,
                media_type="application/json"
            )
    return Response(
        content=f"Car with ID {id} doesn't exist or not found",
        status_code=404,
        media_type="text/plain"
    )


@app.put("/cars/{id}/characteristics")
def update_car_characteristics(given_id: str, new_characteristics: Characteristics):
    for car in car_list:
        if car.id == given_id:
            car.characteristics = new_characteristics
            return Response(
                content=f"Car's characteristics with ID {given_id} updated successfully",
                status_code=200,
                media_type="text/plain"
            )
    return Response(
        content=f"Car with ID {given_id} doesn't exist or not found",
        status_code=404,
        media_type="text/plain"
    )
