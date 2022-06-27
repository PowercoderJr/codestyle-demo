import enum


class ClassId(enum.EnumType):
    """Перечисление классов детектора объектов."""

    person = 0
    face = 1
    wheelchair = 2
    bicycle = 3
    motorcycle = 4
    car = 5
    van = 6
    bus = 7
    truck = 8
    license_plate = 9
    bird = 10
    cat = 11
    dog = 12
    horse = 13
    sheep = 14
    bull = 15
    bear = 16
    luggage = 17


parking_vehicle_classes = [
    ClassId.motorcycle,
    ClassId.car,
    ClassId.van,
    ClassId.bus,
    ClassId.truck,
]
people_classes = [
    ClassId.person,
]
