from inc_noesis import *

import noesis

import rapi

import os

def registerNoesisTypes():
    handle = noesis.register("Toy Story 3 Ps2 Test Converted Mesh", ".COCK")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    noesis.logPopup()
    #print("The log can be useful for catching debug prints from preview loads.\nBut don't leave it on when you release your script, or it will probably annoy people.")
    return 1

def noepyCheckType(data):
    return 1

def getTex(texName,data,texList):
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

# def getTex(name,data,texList):
#     bs = NoeBitStream(data,NOE_LITTLEENDIAN)
#     bs.seek(4)
#     linksize = bs.readUInt()
#     texSize = bs.readUInt()
#     bs.seek(0x04)
#     version = bs.readUInt()
#     print(version)
#     if version == 13:
#         for i in range(1):
#             bs.seek(0x25)
#             texWidth = bs.readUInt()
#             texHeight = bs.readUInt()
#             texFmt = bs.readUInt()
#             ignore1 = bs.readUInt()
#             ignore3 = bs.readUInt()
#             texType(bs,data,texSize,texWidth,texHeight,texList,name)
#             print(texWidth, texHeight)
#     if version == 8:
#         for i in range(1):
#             bs.seek(0x20)
#             texWidth = bs.readUInt()
#             texHeight = bs.readUInt()
#             texFmt = bs.readUInt()
#             ignore1 = bs.readUInt()
#             ignore3 = bs.readUInt()
#             texType(bs,data,texSize,texWidth,texHeight,texList,name)
#             print(texWidth, texHeight)
#     if version == 1056:
#         for i in range(1):
#             bs.seek(0x1e)
#             texWidth = bs.readUInt()
#             texHeight = bs.readUInt()
#             texFmt = bs.readUInt()
#             ignore1 = bs.readUInt()
#             ignore3 = bs.readUInt()
#             texType(bs,data,texSize,texWidth,texHeight,texList,name)
#             print(texWidth, texHeight)
#     if version == 96:
#         for i in range(1):
#             bs.seek(0x1e)
#             texWidth = bs.readUInt()
#             texHeight = bs.readUInt()
#             texFmt = bs.readUInt()
#             ignore1 = bs.readUInt()
#             ignore3 = bs.readUInt()
#             texType(bs,data,texSize,texWidth,texHeight,texList,name)
#             print(texWidth, texHeight)
#     if version == 32:
#         for i in range(1):
#             bs.seek(0x1e)
#             texWidth = bs.readUInt()
#             texHeight = bs.readUInt()
#             texFmt = bs.readUInt()
#             ignore1 = bs.readUInt()
#             ignore3 = bs.readUInt()
#             texType(bs,data,texSize,texWidth,texHeight,texList,name)
#             print(texWidth, texHeight)
#     bs.seek(0x8)
#     version = bs.readUInt()
#     if version == 2667163991:
#         for i in range(1):
#             bs.seek(0x14)
#             texWidth = bs.readUInt()
#             texHeight = bs.readUInt()
#             texFmt = bs.readUInt()
#             ignore1 = bs.readUInt()
#             ignore3 = bs.readUInt()
#             texType(bs,data,texSize,texWidth,texHeight,texList,name)
#             print(texWidth, texHeight)
        
#     return 1
    
# def texType(bs,texSize,bruh,texWidth,texHeight,texList,name):
#     bs.seek(0x4)
#     version = bs.readUInt()
#     texName = "tex"+name
#     if version == 13:
#         bs.seek(0x2d)
#         ddscheck = bs.readUInt()
#         print(ddscheck)
#         if ddscheck != 0:
#             ddssize = (ddscheck - 0x80)
#             bs.seek(0x8a)
#             ddstype = bs.readString()
#             print(ddstype)
#             bs.seek(0xb6)
#             texData = bs.readBytes(ddssize)
#             if ddstype == "DXT1":
#                 texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
#             if ddstype == "DXT5":
#                 texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
#         if ddscheck == 0:
#             bs.seek(0x36)
#             texData = bs.readBytes(texWidth * texHeight * 2)
#             data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8")
#             texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
#     if version == 8:
#         bs.seek(0x28)
#         ddscheckrat = bs.readUInt()
#         if ddscheckrat != 0:
#             ddssize = (ddscheckrat - 0x80)
#             bs.seek(0x88)
#             ddstyperat = bs.readString()
#             print(ddstyperat)
#             bs.seek(0xb4)
#             texData = bs.readBytes(ddssize)
#             if ddstyperat == "DXT1":
#                 texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT1))
#             if ddstyperat == "DXT5":
#                 texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
#         if ddscheckrat == 0:
#             bs.seek(0x2c)
#             versionnum = bs.readBytes(0x01)
#             print(versionnum)
#             if versionnum == b'\x0c':
#                 bs.seek(0x34)
#                 texData = bs.readBytes(texWidth * texHeight * 4)
#                 data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8A8")
#                 texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
#             if versionnum == b'\x0d':
#                 bs.seek(0x34)
#                 texData = bs.readBytes(texWidth * texHeight * 3)
#                 data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8")
#                 texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
#             if versionnum == b'\x07':
#                 bs.seek(0x34)
#                 texData = bs.readBytes(texWidth * texHeight)
#                 data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R2G2B2A2")
#                 texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
#     if version == 1056:
#         bs.seek(0x38)
#         palData = bs.readBytes(0x400)
#         texData = bs.readBytes(texWidth*texHeight)
#         untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 8)
#         Data = rapi.imageDecodeRawPal(untwiddle,palData,texWidth,texHeight,8,"R8G8B8A8",noesis.DECODEFLAG_PS2SHIFT)
#         texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
#     if version == 96:
#         bs.seek(0x38)
#         palData = bs.readBytes(0x40)
#         texData = bs.readBytes(texWidth*(texHeight//2))
#         untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 4)
#         Data = rapi.imageDecodeRawPal(untwiddle,palData,texWidth,texHeight,4,"R8G8B8A8")
#         texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
#     if version == 96:
#         bs.seek(0x38)
#         texData = bs.readBytes(texWidth*texHeight*2)
#         untwiddle = rapi.imageUntwiddlePS2(texData, texWidth, texHeight, 4)
#         Data = rapi.imageDecodeRaw(texData,texWidth,texHeight,"R16G16B16A16")
#         texList.append(NoeTexture(texName,texWidth,texHeight,Data,noesis.NOESISTEX_RGBA32))
#     bs.seek(0x8)
#     version = bs.readUInt()
#     if version == 2667163991:
#         bs.seek(0x1c)
#         ddscheckrat = bs.readUInt()
#         if ddscheckrat != 0:    
#             ddssize = (ddscheckrat - 0x80)
#             bs.seek(0xA8)
#             texData = bs.readBytes(ddssize)
#             texList.append(NoeTexture(texName,texWidth,texHeight,texData,noesis.NOESISTEX_DXT5))
#         else:
#             bs.seek(0x20)
#             versionnum = bs.readBytes(0x01)
#             if versionnum == b'\x0d':
#                 bs.seek(0x28)
#                 texData = bs.readBytes(texWidth * texHeight * 3)
#                 data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "R8G8B8")
#                 texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
#             if versionnum == b'\x0c':
#                 bs.seek(0x28)
#                 texData = bs.readBytes(texWidth * texHeight * 4)
#                 data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "r8g8b8a8")
#                 texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))

def findMulRelativeToFile(fileName, mulName):
    localPath = rapi.getDirForFilePath(fileName)
    testPath = localPath
    print(testPath)
    if os.path.exists(testPath):
        print(testPath + mulName)
        return testPath + mulName
    return None

def getMaterialAndTextureLists(name, matList, texList):
    print(rapi.getLastCheckedName())
    path = findMulRelativeToFile(rapi.getLastCheckedName(),name+".Bitmap_Z")
    print(path)
    getTex(path, rapi.loadIntoByteArray(path), texList)

    material = NoeMaterial(path,"")
    material.setTexture(path)
    rapi.rpgSetMaterial(material.name)
    print(str(material))
    matList.append(material)

def load_submesh(bs, bitmapname, matList, texList, iter):
    getMaterialAndTextureLists(bitmapname, matList, texList)
    vertexcount = bs.readUInt()
    print(vertexcount)
    vertBuff = bytes()
    normalBuff = bytes()
    uvBuff = bytes()
    colorBuff = bytes()
    for i in range(vertexcount):
        vert = NoeVec3.fromBytes(bs.readBytes(0x0c))
        normal = NoeVec3.fromBytes(bs.readBytes(0x0c))
        uvBuff += bs.readBytes(8)
        color = NoeVec4.fromBytes(bs.readBytes(16))
        vertBuff += vert.toBytes()
        normalBuff += normal.toBytes()
        colorBuff += color.toBytes()
        rapi.rpgBindNormalBuffer(normalBuff, noesis.RPGEODATA_FLOAT, 12)
        rapi.rpgBindPositionBuffer(vertBuff, noesis.RPGEODATA_FLOAT, 12)
        rapi.rpgBindUV1Buffer(uvBuff, noesis.RPGEODATA_FLOAT, 8)
        rapi.rpgBindColorBuffer(colorBuff, noesis.RPGEODATA_FLOAT, 16, 4)
    triangleShortCount = bs.readUInt()
    faceCount = triangleShortCount / 3
    FaceBuff = bs.readBytes(triangleShortCount*2)
    print("ASASASDAS I: " + str(iter))
    rapi.rpgCommitTriangles(FaceBuff, noesis.RPGEODATA_USHORT, triangleShortCount, noesis.RPGEO_TRIANGLE,3)
    rapi.rpgClearBufferBinds()
    return rapi.rpgConstructModelSlim()

def noepyLoadModel(data, mdlList):
    rapi.rpgCreateContext()
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0,0)
    bitmapcount = bs.readUInt()
    bitmaps = []
    for i in range(bitmapcount):
       bitmaps.append(bs.readUInt())
    submeshcount = bs.readUInt()
    print("sdsads" + str(submeshcount))
    for i in range(submeshcount):
        print(str(i))
        print("not continued")
        matList = []
        texList = []
        str(bitmaps[i])
        mdl = load_submesh(bs, str(bitmaps[i]), matList, texList, i)
        print(texList,matList)
        mdlList.append(mdl)
        rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)
        mdl.setModelMaterials(NoeModelMaterials(texList, matList))
    return 1