
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Revenge Of The Flying Dutchman Bitmap",".BITMAP")
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
    bs.seek(0x10)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    ddscheckrat = bs.readUInt()
    dataFormat = bs.readUByte()
    swizzled = dataFormat & 0x40 != 0
    print("Swizzled: ",swizzled)
    if ddscheckrat == 0:
        versionnum = bs.readByte()
        print(versionnum)
        texName = os.path.splitext(rapi.getInputName())[0]
        bs.seek(0x22)
        if versionnum == 1:
            texData = bs.readBytes(texWidth * texHeight // 2)
            palData = bs.readBytes(0x40)
            if (swizzled):
                texData = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 4)
            data = rapi.imageDecodeRawPal(texData, palData, texWidth, texHeight, 4, "r8g8b8a8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif versionnum == 2:
            texData = bs.readBytes(texWidth * texHeight)
            palData = bs.readBytes(0x400)
            if (swizzled):
                texData = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 8)
            Data = rapi.imageDecodeRawPal(texData,palData,texWidth,texHeight,8,"r8g8b8a8", noesis.DECODEFLAG_PS2SHIFT)
            texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
        elif versionnum == 7:
            texData = bs.readBytes(texWidth * texHeight)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R5G5B5A1")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif versionnum == 12:
            texData = bs.readBytes(texWidth * texHeight * 4)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8A8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif versionnum == 14:
            texData = bs.readBytes(texWidth * texHeight * 3)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))