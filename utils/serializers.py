def serialize(obj, serializer_class, many=False):
    return [serializer_class(**item.dict()) for item in obj] if many else serializer_class(**obj.dict())
