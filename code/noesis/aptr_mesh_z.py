from inc_noesis import *

import noesis

import rapi

import os

import struct

import sys

def registerNoesisTypes():
    handle = noesis.register("A Plague Tale Mesh_Z", ".Mesh_Z")
    noesis.setHandlerTypeCheck(handle, noepyCheckType)
    noesis.setHandlerLoadModel(handle, noepyLoadModel)
    noesis.logPopup()
    #print("The log can be useful for catching debug prints from preview loads.\nBut don't leave it on when you release your script, or it will probably annoy people.")
    return 1

def noepyCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0,0)
    classcrc64 = bs.readInt64()
    #print(classcrc64)
    if classcrc64 != 8575883205890504413:
        return 0
    return 1

# this stuff is important to get the mesh but its not for the actual mesh

def load_model(data, mdlList):
    normalPrintCount = 0
    vertexBuffers = []
    indexBuffers = []
    materials = []
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0,0)
    className = bs.readInt64()
    fileName = bs.readInt64()
    name = bs.readInt64()
    size = bs.readUInt()
    linkSize = bs.readUInt()
    bodySize = bs.readUInt()
    bs.seek(135,NOESEEK_REL)
    linkCount = bs.readUInt()
    #print(linkCount)
    if (linkCount != 0):
        for i in range(linkCount):
            bs.seek(8,NOESEEK_REL)
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
            bs.seek(12,NOESEEK_REL)
            bs.readInt64()
    cylindercolcount = bs.readUInt()
    if (cylindercolcount != 0):
        for i in range(cylindercolcount):
            bs.seek(36,NOESEEK_REL)
            bs.readUInt()
            bs.seek(12,NOESEEK_REL)
            bs.readInt64()
    AABBColTreeNodeCount = bs.readUInt()
    if (AABBColTreeNodeCount != 0):
        for i in range(AABBColTreeNodeCount):
            bs.seek(64,NOESEEK_REL)
    AABBColTriCount = bs.readUInt()
    if (AABBColTriCount != 0):
        for i in range(AABBColTriCount):
            bs.seek(10,NOESEEK_REL)
    unkCount1 = bs.readUInt()
    if (unkCount1 != 0):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA unkCount1 != 0")
    AABBColVertexCount = bs.readUInt()
    for i in range(AABBColVertexCount):
        bs.seek(12,NOESEEK_REL)
    materialCount = bs.readUInt()
    #print("matcount " + str(materialCount))
    if (materialCount != 0):
        for i in range(materialCount):
            materialCrc64 = bs.readInt64()
            materialname = str(materialCrc64)
            materials.append(materialname)
    unkCount2 = bs.readUInt()
    if (unkCount2 != 0):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA unkCount2 != 0")
    unkCount3 = bs.readUInt()
    if (unkCount3 != 0):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA unkCount3 != 0")
    unkCount4 = bs.readUInt()
    if (unkCount4 != 0):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA unkCount4 != 0")
    unkCount5 = bs.readUInt()
    if (unkCount5 != 0):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA unkCount5 != 0")
    unkCount6 = bs.readUInt()
    if (unkCount6 != 0):
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA unkCount6 != 0")
    vertexBufferCount = bs.readUInt()
    print("VBUF" + str(vertexBufferCount))
    for i in range(vertexBufferCount):
        vertBuff = []
        normBuff = []
        uvBuff = []
        vertexcount = bs.readUInt()
        vertexsize = bs.readUInt()
        flags = bs.readUInt()
        #print(vertexcount)
        for j in range(vertexcount):
            if vertexsize == 48:
                vert = NoeVec3.fromBytes(bs.readBytes(0x0c))
                vertBuff.append(vert)
                tgt = bs.readFloat()
                bnx = bs.readByte()
                bny = bs.readByte()
                bnz = bs.readByte()
                nx=(bnx/127)
                ny=(bny/127)
                nz=(bnz/127)
                normBuff.append(nx)
                normBuff.append(ny)
                normBuff.append(nz)
                if normalPrintCount < 24:
                    normalPrintCount += 1
                    print("normals vtx{" + str(j) + "}: " + str(nx) + " " + str(ny) + " " + str(nz) + " \n")
                padding = bs.readByte()
                uvX = bs.readUShort()
                uvY = bs.readUShort()
                uvBuff.append(uvX)
                uvBuff.append(uvY)
                bs.seek(vertexsize - 0x18,NOESEEK_REL)
            elif vertexsize == 36:
                vert = NoeVec3.fromBytes(bs.readBytes(0x0c))
                vertBuff.append(vert)
                tgt = bs.readFloat()
                bnx = bs.readByte()
                bny = bs.readByte()
                bnz = bs.readByte()
                nx=(bnx/127)
                ny=(bny/127)
                nz=(bnz/127)
                normBuff.append(nx)
                normBuff.append(ny)
                normBuff.append(nz)
                if normalPrintCount < 24:
                    normalPrintCount += 1
                    print("normals vtx{" + str(j) + "}: " + str(nx) + " " + str(ny) + " " + str(nz) + " \n")
                padding = bs.readByte()
                bs.seek(vertexsize - 0x14,NOESEEK_REL)
            else:
                vert = NoeVec3.fromBytes(bs.readBytes(0x0c))
                vertBuff.append(vert)
                bs.seek(vertexsize - 0xc,NOESEEK_REL)
        vertexBuffers.append(vertBuff)
        vertexBuffers.append(normBuff)
        vertexBuffers.append(uvBuff)
        vertexBuffers.append(vertexsize)

    indexBufferCount = bs.readUInt()
    for i in range(indexBufferCount):
        idxBuff = []
        indexCount = bs.readUInt()
        #print("offs " + str(bs.tell()))
        #print("idxCnt " + str(indexCount))
        flags = bs.readUInt()
        faceCount = indexCount / 3
        #print(faceCount)
        for j in range(indexCount):
            idx = bs.readUShort()
            idxBuff.append(idx)
        indexBuffers.append(idxBuff)
    vertexGroupCount = bs.readUInt()
    #print("vertexGroupCount: " + str(vertexGroupCount))
    for i in range(vertexGroupCount):
        vertexsize = vertexBuffers[3]
        bs.seek(8,NOESEEK_REL)
        vertexCount = bs.readUInt()
        idxOffset = bs.readUInt()
        faceCount = bs.readUInt()
        vertOffset = bs.readUInt()
        unkZero = bs.readUInt()
        vertSize = bs.readUShort()
        materialId = bs.readUShort()
        vBuff = bytes()
        nBuff = bytes()
        uBuff = bytes()
        iBuff = bytes()
        #print("vGroup " + str(i) + " vertOffset " + str(vertOffset))
        #print("vGroup " + str(i) + " vertOffset+vertexCount " + str(vertOffset+vertexCount))
        #print("sizeOf VBuff before" + str(sys.getsizeof(vBuff)))
        #print("sizeOf iBuff before" + str(sys.getsizeof(vBuff)))
        #print("len vertexBuffers[0]: " + str(len(vertexBuffers[0])))
        for j in range(vertOffset, vertOffset+vertexCount):
            vBuff += vertexBuffers[0][j].toBytes()
        rapi.rpgBindPositionBuffer(vBuff, noesis.RPGEODATA_FLOAT, 12)
        if vertexsize == 48:
            for j in range(vertOffset*3, vertOffset*3+vertexCount*3):
                nBuff += struct.pack("<f", vertexBuffers[1][j])
            rapi.rpgBindNormalBuffer(nBuff, noesis.RPGEODATA_FLOAT, 12)
            for j in range(vertOffset*2, vertOffset*2+vertexCount*2):
                uBuff += struct.pack("<H", vertexBuffers[2][j])
            rapi.rpgBindUV1Buffer(uBuff, noesis.RPGEODATA_HALFFLOAT, 4)
        elif vertexsize == 36:
            for j in range(vertOffset*3, vertOffset*3+vertexCount*3):
                nBuff += struct.pack("<f", vertexBuffers[1][j])
            rapi.rpgBindNormalBuffer(nBuff, noesis.RPGEODATA_FLOAT, 12)
        #print("sizeOf VBuff " + str(sys.getsizeof(vBuff)))
        
        for j in range(idxOffset, idxOffset+faceCount*3):
            iBuff += struct.pack("<H", indexBuffers[0][j])
        rapi.rpgCommitTriangles(iBuff, noesis.RPGEODATA_USHORT, faceCount*3, noesis.RPGEO_TRIANGLE,3)
        mdl = rapi.rpgConstructModel()
        mdlList.append(mdl)
    unkCount6 = bs.readUInt()
    for i in range(vertexGroupCount):
        unkCount7 = bs.readUInt()
        boneCount = bs.readUInt()
        for j in range(boneCount):
            boneCrc64 = bs.readInt64()
            boneNameSize = bs.readUInt()
            bs.seek(boneNameSize,NOESEEK_REL)
            bs.seek(20,NOESEEK_REL)
            vtxOffset = bs.readUInt()
    faceTotal = bs.readUInt()

def noepyLoadModel(data, mdlList):
    rapi.rpgCreateContext()
    load_model(data, mdlList)
    return 1