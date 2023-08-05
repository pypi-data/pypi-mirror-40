# Package json_serializer

The library for serialize/deserialize into format JSON.

### How use it?

##### For example you have class that needed serialize or deserialize.

```python
class Car(object):
    mark = None
    model = None
    year = None
    color = None
```

##### Create object
```python
car = Car()
car.mark = 'Ford'
car.model = 'Mustang'
car.year = 2016
car.color = 'Black'
```

##### Import class JsonSerializer and create object of serializer

In the constructor pass list of classes that will be involved in serialization/deserialization.

```python
from json_serializer.Serializer import Serializer
...
serializer = Serializer([
    Car
])
```

##### Serialization 

```python
string = serializer.serialize(car)      # sting contains next json:
                                        # {
                                        #    "mark": "Ford",
                                        #    "model": "Mustang",
                                        #    "year": 2016,
                                        #    "color": "Black"
                                        # }
```

##### Deserialization
```python
car = serializer.deserialize(string)

```
Variable `car` type of `Car` and contains values of all fields.

Enjoy!