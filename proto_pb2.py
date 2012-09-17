# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='proto.proto',
  package='apollo',
  serialized_pb='\n\x0bproto.proto\x12\x06\x61pollo\"g\n\tShipClass\x12\x11\n\tclassName\x18\x01 \x02(\t\x12\x0c\n\x04mass\x18\x02 \x02(\x03\x12\x12\n\nfolderName\x18\x03 \x01(\t\x12\x10\n\x08meshName\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"3\n\x0bShipClasses\x12$\n\tshipClass\x18\x01 \x03(\x0b\x32\x11.apollo.ShipClass\"|\n\x0cShipStations\x12\x12\n\nmainScreen\x18\x01 \x01(\x08\x12\x12\n\nnavigation\x18\x02 \x01(\x08\x12\x0f\n\x07weapons\x18\x03 \x01(\x08\x12\x13\n\x0b\x65ngineering\x18\x04 \x01(\x08\x12\x0f\n\x07science\x18\x05 \x01(\x08\x12\r\n\x05\x63omms\x18\x06 \x01(\x08\"\xa0\x01\n\x04Ship\x12\n\n\x02id\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x01(\x01\x12\t\n\x01z\x18\x03 \x01(\x01\x12\t\n\x01h\x18\x04 \x01(\x02\x12\n\n\x02\x64x\x18\x05 \x01(\x01\x12\n\n\x02\x64z\x18\x06 \x01(\x01\x12\n\n\x02\x64h\x18\x07 \x01(\x02\x12&\n\x08stations\x18\x10 \x01(\x0b\x32\x14.apollo.ShipStations\x12\x0c\n\x04name\x18\x11 \x01(\t\x12\x11\n\tclassName\x18\x12 \x01(\t\"#\n\x05Ships\x12\x1a\n\x04ship\x18\x01 \x03(\x0b\x32\x0c.apollo.Ship\"Z\n\x08Throttle\x12\x0e\n\x06normal\x18\x01 \x01(\x02\x12\x0c\n\x04warp\x18\x02 \x01(\x02\x12\x0c\n\x04jump\x18\x03 \x01(\x08\x12\x10\n\x08\x62sgjumpx\x18\x04 \x01(\x01\x12\x10\n\x08\x62sgjumpz\x18\x05 \x01(\x01')




_SHIPCLASS = descriptor.Descriptor(
  name='ShipClass',
  full_name='apollo.ShipClass',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='className', full_name='apollo.ShipClass.className', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mass', full_name='apollo.ShipClass.mass', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='folderName', full_name='apollo.ShipClass.folderName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='meshName', full_name='apollo.ShipClass.meshName', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='description', full_name='apollo.ShipClass.description', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=23,
  serialized_end=126,
)


_SHIPCLASSES = descriptor.Descriptor(
  name='ShipClasses',
  full_name='apollo.ShipClasses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='shipClass', full_name='apollo.ShipClasses.shipClass', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=128,
  serialized_end=179,
)


_SHIPSTATIONS = descriptor.Descriptor(
  name='ShipStations',
  full_name='apollo.ShipStations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='mainScreen', full_name='apollo.ShipStations.mainScreen', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='navigation', full_name='apollo.ShipStations.navigation', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='weapons', full_name='apollo.ShipStations.weapons', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='engineering', full_name='apollo.ShipStations.engineering', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='science', full_name='apollo.ShipStations.science', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='comms', full_name='apollo.ShipStations.comms', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=181,
  serialized_end=305,
)


_SHIP = descriptor.Descriptor(
  name='Ship',
  full_name='apollo.Ship',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='id', full_name='apollo.Ship.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='x', full_name='apollo.Ship.x', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='z', full_name='apollo.Ship.z', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='h', full_name='apollo.Ship.h', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dx', full_name='apollo.Ship.dx', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dz', full_name='apollo.Ship.dz', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='dh', full_name='apollo.Ship.dh', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='stations', full_name='apollo.Ship.stations', index=7,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='name', full_name='apollo.Ship.name', index=8,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='className', full_name='apollo.Ship.className', index=9,
      number=18, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=308,
  serialized_end=468,
)


_SHIPS = descriptor.Descriptor(
  name='Ships',
  full_name='apollo.Ships',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='ship', full_name='apollo.Ships.ship', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=470,
  serialized_end=505,
)


_THROTTLE = descriptor.Descriptor(
  name='Throttle',
  full_name='apollo.Throttle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='normal', full_name='apollo.Throttle.normal', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='warp', full_name='apollo.Throttle.warp', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='jump', full_name='apollo.Throttle.jump', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bsgjumpx', full_name='apollo.Throttle.bsgjumpx', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='bsgjumpz', full_name='apollo.Throttle.bsgjumpz', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=507,
  serialized_end=597,
)

_SHIPCLASSES.fields_by_name['shipClass'].message_type = _SHIPCLASS
_SHIP.fields_by_name['stations'].message_type = _SHIPSTATIONS
_SHIPS.fields_by_name['ship'].message_type = _SHIP
DESCRIPTOR.message_types_by_name['ShipClass'] = _SHIPCLASS
DESCRIPTOR.message_types_by_name['ShipClasses'] = _SHIPCLASSES
DESCRIPTOR.message_types_by_name['ShipStations'] = _SHIPSTATIONS
DESCRIPTOR.message_types_by_name['Ship'] = _SHIP
DESCRIPTOR.message_types_by_name['Ships'] = _SHIPS
DESCRIPTOR.message_types_by_name['Throttle'] = _THROTTLE

class ShipClass(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPCLASS
  
  # @@protoc_insertion_point(class_scope:apollo.ShipClass)

class ShipClasses(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPCLASSES
  
  # @@protoc_insertion_point(class_scope:apollo.ShipClasses)

class ShipStations(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPSTATIONS
  
  # @@protoc_insertion_point(class_scope:apollo.ShipStations)

class Ship(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIP
  
  # @@protoc_insertion_point(class_scope:apollo.Ship)

class Ships(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPS
  
  # @@protoc_insertion_point(class_scope:apollo.Ships)

class Throttle(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _THROTTLE
  
  # @@protoc_insertion_point(class_scope:apollo.Throttle)

# @@protoc_insertion_point(module_scope)
