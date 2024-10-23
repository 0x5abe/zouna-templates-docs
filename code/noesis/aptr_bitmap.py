from inc_noesis import *

import noesis

import rapi

import os

import struct

import sys

def registerNoesisTypes():
    handle = noesis.register("Bitmap_Z",".Bitmap_Z")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,loadTex)
    #noesis.logPopup()
    #print("The log can be useful for catching debug prints from preview loads.\nBut don't leave it on when you release your script, or it will probably annoy people.")
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0,0)
    classcrc64 = bs.readInt64()
    if classcrc64 != -1628723265474973075:
        return 0
    return 1

def loadTex(data, texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0,0)
    className = bs.readInt64()
    fileName = bs.readInt64()
    name = bs.readInt64()
    size = bs.readUInt()
    linkSize = bs.readUInt()
    bodySize = bs.readUInt()
    bs.seek(17,NOESEEK_REL)
    unk1 = bs.readShort()
    width = bs.readUInt()
    height = bs.readUInt()
    one1 = bs.readUInt()
    one2 = bs.readUInt()
    precalculatedSize = bs.readUInt()
    flag = bs.readShort()
    flag2 = bs.readUInt()
    bs.seek(6,NOESEEK_REL)
    mipCount = bs.readUInt()
    bs.seek(3,NOESEEK_REL)
    fmt = bs.readByte()
    modifier = bs.readByte()
    bs.seek(4,NOESEEK_REL)
    texData = bs.readBytes(precalculatedSize)
    texFormat = -1
    dxt = False
    snorm = False
    
    if fmt == 2 or fmt == 3 or fmt == 0x40 or fmt == 0x41:
        texFormat = "r8"
    elif fmt == 4 or fmt == 5 or fmt == 0x42 or fmt == 0x43:
        texFormat = "r8g8"
    elif fmt == 6 or fmt == 7 or fmt == 0x44 or fmt == 0x45:
        texFormat = "r8g8b8a8"
    elif fmt == 8:
        texFormat = "b8g8r8a8"
    elif fmt == 9 or fmt == 10:
        texFormat = "r10b10g10a2"
    elif fmt == 0xc or fmt == 0xd or fmt == 0x24 or fmt == 0x46 or fmt == 0x47:
        texFormat = "r16"
    elif fmt == 0xe or fmt == 0xf or fmt == 0x10:
        texFormat = "r16g16"
    elif fmt == 0x11 or fmt == 0x12 or fmt == 0x13 or fmt == 0x14:
        texFormat = "r16g16b16a16"
    elif fmt == 0x15 or fmt == 0x16 or fmt == 0x26:
        texFormat = "r32"
    elif fmt == 0x17 or fmt == 0x49:
        texFormat = "r32g32"
    elif fmt == 0x18:
        texFormat = "r32g32b32"
    elif fmt == 0x19 or fmt == 0x1a or fmt == 0x48:
        texFormat = "r32g32b32a32"
    elif fmt == 0x1b:
        texFormat = noesis.FOURCC_BC1
        dxt = True
    elif fmt == 0x1c:
        texFormat = noesis.FOURCC_BC2
        dxt = True
    elif fmt == 0x1d:
        texFormat = noesis.FOURCC_BC3
        dxt = True
    elif fmt == 0x1e:
        texFormat = noesis.FOURCC_BC4
        dxt = True
    elif fmt == 0x1f or fmt == 0x20:
        texFormat = noesis.FOURCC_BC5
        dxt = True
        snorm = True
    elif fmt == 0x21 or fmt == 0x22:
        texFormat = noesis.FOURCC_BC6H
        dxt = True
    elif fmt == 0x23:
        texFormat = noesis.FOURCC_BC7
        dxt = True
    elif fmt == 0x25:
        texFormat = "r24g8"
    elif fmt == 0x27:
        texFormat = "r32g8x24"

    if texFormat == -1:
        return 0

    if dxt:
        if snorm:
            texData = rapi.imageDecodeDXT(texData, width, height, texFormat, 0, 3) # not sure if 3 or 2 is right here
        else:
            texData = rapi.imageDecodeDXT(texData, width, height, texFormat)
        if texFormat == noesis.FOURCC_BC5:
            texData = rapi.imageEncodeRaw(texData, width, height, "r16g16")
            texData = rapi.imageDecodeRaw(texData, width, height, "r16g16")
    else:
        texData = rapi.imageDecodeRaw(texData, width, height, texFormat)

    texName = rapi.getInputName()
    texFormat = noesis.NOESISTEX_RGBA32
    tex = NoeTexture(texName, width, height, texData, texFormat)
    texList.append(tex)