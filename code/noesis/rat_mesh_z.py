from inc_noesis import *

import noesis

import rapi

import os

def registerNoesisTypes():
    handle = noesis.register("Ratatouille Mesh_Z", ".rMesh_Z")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    # noesis.logPopup()
    #print("The log can be useful for catching debug prints from preview loads.\nBut don't leave it on when you release your script, or it will probably annoy people.")
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0x10)
    classcrc32 = bs.readUInt()
    print(classcrc32)
    if classcrc32 != 1387343541:
        return 0
    return 1

# this stuff is important to get the mesh but its not for the actual mesh
materials = []

def load_model(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0,0)
    datasize = bs.readUInt()
    linksize = bs.readUInt()
    decompressedsize = bs.readUInt()
    compressedsize = bs.readUInt()
    classcrc32 = bs.readUInt()
    namecrc32 = bs.readUInt()
    namestr = str(namecrc32)
    bs.seek(linksize,NOESEEK_REL)
    pointrelated0 = bs.readUInt()
    if (pointrelated0 != 0):
        for i in range(pointrelated0):
            bs.seek(12,NOESEEK_REL)
    pointrelated1 = bs.readUInt()
    if (pointrelated1 != 0):
        for i in range(pointrelated1):
            bs.seek(16,NOESEEK_REL)
    MorpherRelatedCount = bs.readUInt()
    if (MorpherRelatedCount != 0):
        for i in range(MorpherRelatedCount):
            bs.seek(16,NOESEEK_REL)
    morphTargetDescCount = bs.readUInt()
    if (morphTargetDescCount != 0):
        for i in range(morphTargetDescCount):
            bs.readUInt()
            MorphTargetDescRelatedCount = bs.readUInt32()
            if (MorphTargetDescRelatedCount != 0):
                for i in range(MorphTargetDescRelatedCount):
                    bs.seek(16,NOESEEK_REL)
    bs.seek(16,NOESEEK_REL)
    materialCrc32Count = bs.readUInt()
    if (materialCrc32Count != 0):
        for i in range(materialCrc32Count):
            materialCrc32 = bs.readUInt()
            materialname = str(materialCrc32)
            materials.append(materialname)
    bs.seek(24,NOESEEK_REL)
    spherecolcount = bs.readUInt()
    if (spherecolcount != 0):
        for i in range(spherecolcount):
            bs.seek(20,NOESEEK_REL)
            bs.readUInt()
    boxcolcount = bs.readUInt()
    if (boxcolcount != 0):
        for i in range(boxcolcount):
            bs.seek(64,NOESEEK_REL)
            bs.readUInt()
            bs.readUInt()
    cylindercolcount = bs.readUInt()
    if (cylindercolcount != 0):
        for i in range(cylindercolcount):
            bs.seek(40,NOESEEK_REL)
            bs.readUInt()
    AABBColRelatedCount = bs.readUInt()
    if (AABBColRelatedCount != 0):
        for i in range(AABBColRelatedCount):
            bs.seek(8,NOESEEK_REL)
    AABBColCount = bs.readUInt()
    if (AABBColCount != 0):
        for i in range(AABBColCount):
            bs.seek(32,NOESEEK_REL)
    shortvertexcount = bs.readUInt()
    for i in range(shortvertexcount):
        bs.seek(6,NOESEEK_REL)
    bs.seek(4,NOESEEK_REL)
    unkUintCount = bs.readUInt()
    if (unkUintCount != 0):
        for i in range(unkUintCount):
            bs.readUInt()
    one = bs.readUInt()
    vertBuff = bytes()
    normalBuff = bytes()
    uvBuff = bytes()
    vertexcount = bs.readShort()
    vertexsize = bs.readShort()
    print(vertexcount)
    for i in range(vertexcount):
        vert = NoeVec3.fromBytes(bs.readBytes(0x0c))
        vertBuff += vert.toBytes()
        unk = bs.readFloat()
        bnx = bs.readByte()
        nny = bs.readByte()
        bnz = bs.readByte()
        padding = bs.readByte()
        uvBuff += bs.readBytes(8)
        bs.seek(vertexsize - 0x1c,NOESEEK_REL)
    rapi.rpgBindPositionBuffer(vertBuff, noesis.RPGEODATA_FLOAT, 12)
    rapi.rpgBindUV1Buffer(uvBuff, noesis.RPGEODATA_FLOAT, 8)
    one = bs.readUInt()
    triangleShortCount = bs.readShort()
    faceCount = triangleShortCount / 3
    FaceBuff = bs.readBytes(triangleShortCount*2)
    rapi.rpgCommitTriangles(FaceBuff, noesis.RPGEODATA_USHORT, triangleShortCount, noesis.RPGEO_TRIANGLE,3)

def noepyLoadModel(data, mdlList):

    rapi.rpgCreateContext()
    load_model(data)
    rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)
    mdl = rapi.rpgConstructModel()
    mdlList.append(mdl)
    return 1