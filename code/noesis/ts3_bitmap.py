from inc_noesis import *
import noesis
import rapi
import os
def registerNoesisTypes():
    handle = noesis.register("Toy Story 3 Bitmap_Z",".Bitmap_Z")
    noesis.setHandlerTypeCheck(handle,noepyCheckType)
    noesis.setHandlerLoadRGBA(handle,getTex)
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(4)
    check = bs.readInt()
    if check == 1056 or check == 96:
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
    check = bs.readInt()
    bs.seek(0x1e)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    bs.readUInt()
    flags = bs.readUInt()
    bs.seek(6,1)
    type = list(bs.readBytes(4))
    print(hex(bs.tell()))
    texName = os.path.splitext(rapi.getInputName())[0]
    bs.seek(0x38)
    print(texHeight,texWidth)
    if check == 1056:
        palData = bs.readBytes(0x400)
        texData = bs.readBytes(texWidth*texHeight)
        untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 8)
    elif check == 96:
        palData = bs.readBytes(0x40)
        texData = bs.readBytes(texWidth*texHeight//2)
        untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 4)
    if flags & 0x450:
        texData = untwiddle
        
    
    if check == 1056:
        Data = rapi.imageDecodeRawPal(texData,palData,texWidth,texHeight,8,"R8G8B8A8",noesis.DECODEFLAG_PS2SHIFT)
    elif check == 96:
        Data = rapi.imageDecodeRawPal(texData,palData,texWidth,texHeight,4,"R8G8B8A8")
    texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
