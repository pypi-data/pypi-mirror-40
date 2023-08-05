from __future__ import print_function
import sys

from construct import this, Adapter, Byte, Bytes, Computed, Const, CString, If, IfThenElse, OneOf, Optional, Padding, PaddedString, PascalString, Peek, RepeatUntil, Struct, Switch, Int8ub, Int16ul
from enum import Enum


# ===============================================================================
# /*
#    * Rough structure of a .wsg file:
#    *
#    * === HEADER ===
#    * WoW File
#    *   [junk byte]
#    * Song words
#    *   [0x13 - 0x37 junk bytes]
#    *   [# of blocks in file]
#    *   [0x0 0x0 0x0]
#    *   [0xFF 0xFF]
#    *   [0x3E - 0x41 junk bytes]
#    * CSongDoc::CBlock
#    *   [BLOCKS - see below]
#    *   [Byte count of author]
#    * Author
#    *   [Byte count of copyright]
#    * Copyright
#    *   [LICENSEFLAG]
#    *   [0x0 0x0 0x0]
#    * [EOF]
#    *
#    * === LICENSEFLAG ===
#    * 0 - Covered by CCL
#    * 1 - Author's explicit permission
#    * 2 - Public Domain
#    * 3 - Copyright Expired
#    * 4 - Other
#    * === BLOCKS ===
#    *   [# of lines in block]
#    *   [0x0 0x0 0x0]
#    *   [LINES - see below]
#    *   [BLOCKTYPE]
#    *   [0x0 0x0 0x0]
#    *
#    * Two adjacent blocks will have two bytes of "junk" between them.
#    *
#    * === BLOCKTYPE ===
#    * 0 - verse
#    * 1 - chorus
#    * 2 - bridge
#    *
#    * === LINES ===
#    *   [# of bytes in line] - one byte, or if 0xFF, the following two bytes (little-endian)
#    *   Line text
#    *   [LINETYPE]
#    *
#    * === LINETYPE ===
#    * 0 - normal
#    * 1 - minor words
class LineType(Enum):
    NORMAL = 0
    MINOR = 1


class BlockType(Enum):
    VERSE = 0
    CHORUS = 1
    BRIDGE = 2


class LicenseType(Enum):
    CCL = 0
    AUTHOR_EXPLICIT_PERMISSION = 1
    PUBLIC_DOMAIN = 2
    COPYRIGHT_EXPIRED = 3
    OTHER = 4


class EnumAdapter(Adapter):
    def __init__(self, enumClass, subcon):
        super(Adapter, self).__init__(subcon)
        self.enumClass = enumClass

    def _encode(self, obj, context, path):
        return obj.value

    def _decode(self, obj, context, path):
        return self.enumClass(obj)


def valuesOf(enum):
    return list(map(lambda x: x.value, enum))


def findFormat(ctx):
    if 'format' in ctx:
        return ctx.format
    if '_' in ctx:
        return findFormat(ctx._)
    return 0


class WindowsStringAdapter(Adapter):
    def _encode(self, obj, context, path):
        return obj.encode('windows-1252')

    def _decode(self, obj, context, path):
        return bytearray(obj).decode('windows-1252').strip()


NullOrNewlineTerminatedBytes = RepeatUntil(
    lambda x, lst, ctx: x == 0 or x == 10,
    Byte
)


Line = Struct(
    "short_length" / Int8ub,
    "length" / IfThenElse(
        this.short_length == 0xFF,
        Int16ul,
        Computed(this.short_length)
    ),
    "text" / WindowsStringAdapter(Bytes(this.length)),
    "type" / IfThenElse(
        lambda ctx: findFormat(ctx) == 1,  # 0 = Really old WoW format without minor words
        EnumAdapter(LineType, OneOf(Int8ub, valuesOf(LineType))),
        Computed(LineType.NORMAL)
    )
)

Block = Struct(
    Padding(2),
    "linecount" / Int8ub,
    Padding(3),
    "line" / Line[this.linecount],
    "type" / EnumAdapter(BlockType, OneOf(Int8ub, valuesOf(BlockType))),
    Padding(3)
)

Song = Struct(
    "blockcount" / Int8ub,
    Padding(9),
    Const(b'CSongDoc::CBlo'),  # The 'ck' is considered padding at start of block
    "block" / Block[this.blockcount],
    "author" / PascalString(Int8ub, encoding="windows-1252"),
    "copyright" / PascalString(Int8ub, encoding="windows-1252"),
    "license" / Optional(
        Struct(
            "type" / EnumAdapter(LicenseType, OneOf(Int8ub, valuesOf(LicenseType))),
            Padding(3)
        )
    )
)

Liturgy = Struct(
    "linecount" / Int8ub,
    Padding(3),
    "line" / Line[this.linecount]
)

RESOURCE_MAPPING = {
    'Song Words': Song,
    'Liturgy': Liturgy
}

Resource = Struct(
    Const(b"WoW File\n"),
    "filetype" / OneOf(
        WindowsStringAdapter(NullOrNewlineTerminatedBytes),
        RESOURCE_MAPPING.keys()
    ),
    Padding(4),
    "format" / Int8ub,
    Padding(31),
    "content" / Switch(
        this.filetype,
        RESOURCE_MAPPING
    )
)


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "rb") as f:
        print(Resource.parse(f.read()))
