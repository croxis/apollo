# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto.proto',
  package='apollo',
  serialized_pb='\n\x0bproto.proto\x12\x06\x61pollo\"g\n\tShipClass\x12\x11\n\tclassName\x18\x01 \x02(\t\x12\x0c\n\x04mass\x18\x02 \x02(\x03\x12\x12\n\nfolderName\x18\x03 \x01(\t\x12\x10\n\x08meshName\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\"3\n\x0bShipClasses\x12$\n\tshipClass\x18\x01 \x03(\x0b\x32\x11.apollo.ShipClass\"\xa6\x01\n\x0cShipStations\x12\x19\n\nmainScreen\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x19\n\nnavigation\x18\x02 \x01(\x08:\x05\x66\x61lse\x12\x16\n\x07weapons\x18\x03 \x01(\x08:\x05\x66\x61lse\x12\x1a\n\x0b\x65ngineering\x18\x04 \x01(\x08:\x05\x66\x61lse\x12\x16\n\x07science\x18\x05 \x01(\x08:\x05\x66\x61lse\x12\x14\n\x05\x63omms\x18\x06 \x01(\x08:\x05\x66\x61lse\"\xa6\x02\n\x04Ship\x12\n\n\x02id\x18\x01 \x02(\x05\x12\t\n\x01x\x18\x02 \x01(\x01\x12\t\n\x01y\x18\x03 \x01(\x01\x12\t\n\x01z\x18\x04 \x01(\x01\x12\t\n\x01h\x18\x05 \x01(\x02\x12\t\n\x01p\x18\x06 \x01(\x02\x12\t\n\x01r\x18\x07 \x01(\x02\x12\n\n\x02\x64x\x18\x08 \x01(\x01\x12\n\n\x02\x64y\x18\t \x01(\x01\x12\n\n\x02\x64z\x18\n \x01(\x01\x12\n\n\x02\x64h\x18\x0b \x01(\x02\x12\n\n\x02\x64p\x18\x0c \x01(\x02\x12\n\n\x02\x64r\x18\r \x01(\x02\x12\x0e\n\x06thrust\x18\x0e \x01(\x02\x12\x0e\n\x06torque\x18\x0f \x01(\x02\x12\x1f\n\x07turrets\x18\x10 \x03(\x0b\x32\x0e.apollo.Turret\x12&\n\x08stations\x18! \x01(\x0b\x32\x14.apollo.ShipStations\x12\x0c\n\x04name\x18\" \x01(\t\x12\x11\n\tclassName\x18# \x01(\t\"#\n\x05Ships\x12\x1a\n\x04ship\x18\x01 \x03(\x0b\x32\x0c.apollo.Ship\"}\n\x08Throttle\x12\x0e\n\x06normal\x18\x01 \x01(\x02\x12\x0c\n\x04warp\x18\x02 \x01(\x02\x12\x0c\n\x04jump\x18\x03 \x01(\x08\x12\x10\n\x08\x62sgjumpx\x18\x04 \x01(\x01\x12\x10\n\x08\x62sgjumpy\x18\x05 \x01(\x01\x12\x10\n\x08\x62sgjumpz\x18\x06 \x01(\x01\x12\x0f\n\x07heading\x18\x07 \x01(\x02\"0\n\x06Target\x12\x10\n\x08targetId\x18\x01 \x02(\x05\x12\x14\n\x08turretId\x18\x02 \x01(\x05:\x02-1\"M\n\x06Turret\x12\x10\n\x08turretid\x18\x01 \x02(\x05\x12\x12\n\nturretName\x18\x02 \x01(\t\x12\x1d\n\x06joints\x18\x03 \x03(\x0b\x32\r.apollo.Joint\"\x91\x01\n\x05Joint\x12\x11\n\tjointName\x18\x01 \x02(\t\x12\x0f\n\x07targetH\x18\x02 \x02(\x02\x12\x0f\n\x07targetP\x18\x03 \x02(\x02\x12\x0f\n\x07targetR\x18\x04 \x02(\x02\x12\x0c\n\x04time\x18\x05 \x02(\x02\x12\x10\n\x08\x63urrentH\x18\x06 \x01(\x02\x12\x10\n\x08\x63urrentP\x18\x07 \x01(\x02\x12\x10\n\x08\x63urrentR\x18\x08 \x01(\x02')




_SHIPCLASS = _descriptor.Descriptor(
  name='ShipClass',
  full_name='apollo.ShipClass',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='className', full_name='apollo.ShipClass.className', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mass', full_name='apollo.ShipClass.mass', index=1,
      number=2, type=3, cpp_type=2, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='folderName', full_name='apollo.ShipClass.folderName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='meshName', full_name='apollo.ShipClass.meshName', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
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


_SHIPCLASSES = _descriptor.Descriptor(
  name='ShipClasses',
  full_name='apollo.ShipClasses',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
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


_SHIPSTATIONS = _descriptor.Descriptor(
  name='ShipStations',
  full_name='apollo.ShipStations',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='mainScreen', full_name='apollo.ShipStations.mainScreen', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='navigation', full_name='apollo.ShipStations.navigation', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='weapons', full_name='apollo.ShipStations.weapons', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='engineering', full_name='apollo.ShipStations.engineering', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='science', full_name='apollo.ShipStations.science', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='comms', full_name='apollo.ShipStations.comms', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
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
  serialized_start=182,
  serialized_end=348,
)


_SHIP = _descriptor.Descriptor(
  name='Ship',
  full_name='apollo.Ship',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='apollo.Ship.id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='x', full_name='apollo.Ship.x', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='y', full_name='apollo.Ship.y', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='z', full_name='apollo.Ship.z', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='h', full_name='apollo.Ship.h', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='p', full_name='apollo.Ship.p', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='r', full_name='apollo.Ship.r', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dx', full_name='apollo.Ship.dx', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dy', full_name='apollo.Ship.dy', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dz', full_name='apollo.Ship.dz', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dh', full_name='apollo.Ship.dh', index=10,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dp', full_name='apollo.Ship.dp', index=11,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dr', full_name='apollo.Ship.dr', index=12,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='thrust', full_name='apollo.Ship.thrust', index=13,
      number=14, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='torque', full_name='apollo.Ship.torque', index=14,
      number=15, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turrets', full_name='apollo.Ship.turrets', index=15,
      number=16, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stations', full_name='apollo.Ship.stations', index=16,
      number=33, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='apollo.Ship.name', index=17,
      number=34, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='className', full_name='apollo.Ship.className', index=18,
      number=35, type=9, cpp_type=9, label=1,
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
  serialized_start=351,
  serialized_end=645,
)


_SHIPS = _descriptor.Descriptor(
  name='Ships',
  full_name='apollo.Ships',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
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
  serialized_start=647,
  serialized_end=682,
)


_THROTTLE = _descriptor.Descriptor(
  name='Throttle',
  full_name='apollo.Throttle',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='normal', full_name='apollo.Throttle.normal', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='warp', full_name='apollo.Throttle.warp', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='jump', full_name='apollo.Throttle.jump', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bsgjumpx', full_name='apollo.Throttle.bsgjumpx', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bsgjumpy', full_name='apollo.Throttle.bsgjumpy', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bsgjumpz', full_name='apollo.Throttle.bsgjumpz', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='heading', full_name='apollo.Throttle.heading', index=6,
      number=7, type=2, cpp_type=6, label=1,
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
  serialized_start=684,
  serialized_end=809,
)


_TARGET = _descriptor.Descriptor(
  name='Target',
  full_name='apollo.Target',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='targetId', full_name='apollo.Target.targetId', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turretId', full_name='apollo.Target.turretId', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=True, default_value=-1,
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
  serialized_start=811,
  serialized_end=859,
)


_TURRET = _descriptor.Descriptor(
  name='Turret',
  full_name='apollo.Turret',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='turretid', full_name='apollo.Turret.turretid', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='turretName', full_name='apollo.Turret.turretName', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='joints', full_name='apollo.Turret.joints', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  serialized_start=861,
  serialized_end=938,
)


_JOINT = _descriptor.Descriptor(
  name='Joint',
  full_name='apollo.Joint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='jointName', full_name='apollo.Joint.jointName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='targetH', full_name='apollo.Joint.targetH', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='targetP', full_name='apollo.Joint.targetP', index=2,
      number=3, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='targetR', full_name='apollo.Joint.targetR', index=3,
      number=4, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time', full_name='apollo.Joint.time', index=4,
      number=5, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currentH', full_name='apollo.Joint.currentH', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currentP', full_name='apollo.Joint.currentP', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='currentR', full_name='apollo.Joint.currentR', index=7,
      number=8, type=2, cpp_type=6, label=1,
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
  serialized_start=941,
  serialized_end=1086,
)

_SHIPCLASSES.fields_by_name['shipClass'].message_type = _SHIPCLASS
_SHIP.fields_by_name['turrets'].message_type = _TURRET
_SHIP.fields_by_name['stations'].message_type = _SHIPSTATIONS
_SHIPS.fields_by_name['ship'].message_type = _SHIP
_TURRET.fields_by_name['joints'].message_type = _JOINT
DESCRIPTOR.message_types_by_name['ShipClass'] = _SHIPCLASS
DESCRIPTOR.message_types_by_name['ShipClasses'] = _SHIPCLASSES
DESCRIPTOR.message_types_by_name['ShipStations'] = _SHIPSTATIONS
DESCRIPTOR.message_types_by_name['Ship'] = _SHIP
DESCRIPTOR.message_types_by_name['Ships'] = _SHIPS
DESCRIPTOR.message_types_by_name['Throttle'] = _THROTTLE
DESCRIPTOR.message_types_by_name['Target'] = _TARGET
DESCRIPTOR.message_types_by_name['Turret'] = _TURRET
DESCRIPTOR.message_types_by_name['Joint'] = _JOINT

class ShipClass(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPCLASS

  # @@protoc_insertion_point(class_scope:apollo.ShipClass)

class ShipClasses(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPCLASSES

  # @@protoc_insertion_point(class_scope:apollo.ShipClasses)

class ShipStations(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPSTATIONS

  # @@protoc_insertion_point(class_scope:apollo.ShipStations)

class Ship(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIP

  # @@protoc_insertion_point(class_scope:apollo.Ship)

class Ships(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SHIPS

  # @@protoc_insertion_point(class_scope:apollo.Ships)

class Throttle(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _THROTTLE

  # @@protoc_insertion_point(class_scope:apollo.Throttle)

class Target(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TARGET

  # @@protoc_insertion_point(class_scope:apollo.Target)

class Turret(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TURRET

  # @@protoc_insertion_point(class_scope:apollo.Turret)

class Joint(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _JOINT

  # @@protoc_insertion_point(class_scope:apollo.Joint)


# @@protoc_insertion_point(module_scope)
