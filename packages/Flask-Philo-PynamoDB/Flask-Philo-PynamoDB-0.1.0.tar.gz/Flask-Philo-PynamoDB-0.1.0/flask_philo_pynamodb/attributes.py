from pynamodb.attributes import UnicodeAttribute

import uuid


class UUIDAttribute(UnicodeAttribute):
    """
    Handles serialization of UUID objects
    """
    def serialize(self, value):
        # convert the value to sting and return it
        return str(value)

    def deserialize(self, value):
        # convert the value from srting back to uuid
        return uuid.UUID(value)
