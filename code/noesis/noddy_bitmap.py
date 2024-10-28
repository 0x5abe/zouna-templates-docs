# Author: Violet
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Black Sheep Bitmap",".BITMAP")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1
def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    if bs.readInt() == 412457258:
        return 1
    else:
        return 0
def getTex(data,texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0x8)
    texName = bs.readInt()
    bs.seek(0x10)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    ddsCheck = bs.readUInt()
    version = list(bs.readBytes(4))
    if not ddsCheck:
        print(version[0])
        if version[0] == 12:
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 4)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8A8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 13:
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 3)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 7:
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 2)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "b5g5r5a1")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 8:
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 2)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B5G6R5")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 10:
            texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 2)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B4G4R4A4")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))


