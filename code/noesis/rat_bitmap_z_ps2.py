
from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Ratatouille Bitmap_Z",".Bitmap_Z")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    if bs.readInt() == 8:
        bs.seek(0x10)
        if bs.readUInt() == 1471281566:
            return 1
        else: 
            return 0
    else:
        return 0

def getTex(data,texList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    linksize = bs.readUInt()
    texSize = bs.readUInt()
    bs.seek(0x20)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    ddscheckrat = bs.readUInt()
    bs.seek(0x32)
    flag = bs.readUShort()
    swizzled = flag & 0x40 != 0
    print("Swizzled: ",swizzled)
    if ddscheckrat != 0:
        ddssize = (ddscheckrat - 0x80)
        bs.seek(0x88)
        ddstyperat = bs.readString()
        print(ddstyperat)
        bs.seek(0xb4)
        texName = os.path.splitext(rapi.getInputName())[0]
        texData = bs.readBytes(ddssize)
        if ddstyperat == "DXT1":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
        elif ddstyperat == "DXT5":
            texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
    elif ddscheckrat == 0:
        bs.seek(0x2c)
        versionnum = bs.readByte()
        print(versionnum)
        texName = os.path.splitext(rapi.getInputName())[0]
        bs.seek(0x34)
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
