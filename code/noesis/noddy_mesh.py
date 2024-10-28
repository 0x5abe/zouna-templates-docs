
from inc_noesis import *
from collections import Counter

whiteTex = bytearray()
for _ in range(256):
    whiteTex.append(0xff)

def registerNoesisTypes():
    handle = noesis.register("Noddy Taxi/En Taxi Avec Oui-Oui Mesh",".MESH")
    noesis.setHandlerTypeCheck(handle, bcCheckType)
    noesis.setHandlerLoadModel(handle, bcLoadModel)
    return 1


# Check file type

def bcCheckType(data):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0x4)
    if bs.readUInt() == 3623540706:
        return 1
    return 0

def getTex(texName,data,texList):
    
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    bs.seek(0x8)
    #texName = bs.readInt()
    bs.seek(0x10)
    texWidth = bs.readUInt()
    texHeight = bs.readUInt()
    ddsCheck = bs.readUInt()
    version = list(bs.readBytes(4))
    if not ddsCheck:
        #print(version[0])
        if version[0] == 12:
            #texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 4)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8A8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 13:
            #texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 3)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B8G8R8")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 7:
            #texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 2)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "b5g5r5a1")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 8:
            #texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 2)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B5G6R5")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))
        elif version[0] == 10:
            #texName = os.path.splitext(rapi.getInputName())[0]+"_"+str(texName)
            texData = bs.readBytes(texWidth * texHeight * 2)
            data = rapi.imageDecodeRaw(texData, texWidth, texHeight, "B4G4R4A4")
            texList.append(NoeTexture(texName,texWidth,texHeight,data,noesis.NOESISTEX_RGBA32))

def getBitmapLinkAndColorFromMaterial(matName):
    path = findMulRelativeToFile(rapi.getLastCheckedName(),str(matName)+".MATERIAL")
    if path != None:
        try:
            matData = rapi.loadIntoByteArray(path)
            mbs = NoeBitStream(matData,NOE_LITTLEENDIAN)
            mbs.seek(0xc)
            matLinkName = mbs.readInt()
            diffuseColor = NoeVec4.fromBytes(mbs.readBytes(0x10))
            mbs.seek(0x75)
            bitmapName = mbs.readInt()
            return (bitmapName, matLinkName, diffuseColor)
        except Exception as error:
            noesis.messagePrompt("ERROR: " + str(error.message))
            noesis.messagePrompt("Failed to open material: " + path)
            colorM = bytearray()
            for _ in range(4):
                colorM.append(0x00)
                colorM.append(0x00)
                colorM.append(0x80)
                colorM.append(0x3f)
            return (0,0,NoeVec4.fromBytes(colorM))
    return None

def findMulRelativeToFile(fileName, mulName):
    localPath = rapi.getDirForFilePath(fileName)
    testPath = localPath
    if os.path.exists(testPath):
        return testPath + mulName
    return None

def getMaterialAndTextureLists(name, matList, texList, materialNameForBmap):
    path = None
    materName = "whiteMat"
    texName = "whiteTex"
    if name != 0:
        path = findMulRelativeToFile(rapi.getLastCheckedName(),str(name)+".BITMAP")
        try:
            texData = rapi.loadIntoByteArray(path)
            getTex(path, rapi.loadIntoByteArray(path), texList)
            materName = path
            texName = path
        except:
            noesis.messagePrompt("Failed to open bitmap: " + path + " of material: " + str(materialNameForBmap))
            texList.append(NoeTexture(texName,4,4,whiteTex,noesis.NOESISTEX_RGBA32))
    else:
        texList.append(NoeTexture(texName,4,4,whiteTex,noesis.NOESISTEX_RGBA32))
    material = NoeMaterial(materName,"")
    material.setTexture(texName)
    rapi.rpgSetMaterial(material.name)
    matList.append(material)

def bcLoadModel(data, mdlList):
    bs = NoeBitStream(data,NOE_LITTLEENDIAN)
    ctx = rapi.rpgCreateContext()
    bs.seek(0xC)
    name = bs.readUInt()
    bs.seek(0x62,NOESEEK_REL)
    objFlag = bs.readShort()

    vertexCount = bs.readUInt()
    #print("vertex count: " + str(vertexCount))
    verts = []
    for _ in range(vertexCount):
        verts.append(NoeVec3.fromBytes(bs.readBytes(0xc)))
    
    uvCount = bs.readUInt()
    #print("uv count: " + str(uvCount))
    uvBuff = []
    for _ in range(uvCount):
        uvBuff.append(bs.readBytes(0x8))
    
    normalCount = bs.readUInt()
    #print("normal count: " + str(normalCount))
    normalBuff = []
    for _ in range(normalCount):
        normalBuff.append(NoeVec3.fromBytes(bs.readBytes(0xc)))

    stripCount = bs.readUInt()
    #print("strip count: " + str(stripCount))
    strips = []
    for i in range(stripCount):
        strip = []
        vertexReferences = []
        vertexReferenceCount = bs.readUInt()
        
        #print("strip [" + str(i) + "] vertexRefCount: " + str(vertexReferenceCount))
        for _ in range(vertexReferenceCount):
            vertexReferences.append(bs.readShort())
        flag = bs.readUInt()
        triOrder = bs.readByte()
        strip.append(vertexReferences)
        strip.append(flag)
        strip.append(triOrder)
        strips.append(strip)

    #unks

    stripMaterials = []
    vertexGroups = []
    vertexGroupsStartIndices = []
    vertexGroupsEndIndices = []
    if objFlag & 4:
        #print("stripMaterial count: " + str(stripCount))
        for _ in range(stripCount):
            stripMaterials.append(bs.readInt())
        curMatLink = -1
        for i in range(len(stripMaterials)):
            if curMatLink != stripMaterials[i]:
                vertexGroups.append(stripMaterials[i])
                vertexGroupsStartIndices.append(i)
                if curMatLink != -1:
                    vertexGroupsEndIndices.append(i)
            curMatLink = stripMaterials[i]
        vertexGroupsEndIndices.append(len(stripMaterials)-1)

    #print("number of vertexGroups: " + str(len(vertexGroups)))
    #print("vertexGroupsStartIndices: " + str(vertexGroupsStartIndices))
    #print("vertexGroupsEndIndices: " + str(vertexGroupsEndIndices))

    stripDataCount = bs.readUInt()
    #print("stripData count: " + str(stripDataCount))
    stripDatas = []
    for i in range(stripDataCount):
        stripData = []
        elementDataCount = bs.readUInt()
        #print("stripData [" + str(i) + "] elementDataCount: " + str(elementDataCount))
        for _ in range(elementDataCount):
            elementData = []
            elementData.append(bs.readShort())
            elementData.append(bs.readShort())
            stripData.append(elementData)
        stripDatas.append(stripData)
    
    materialCrc32Count = bs.readUInt()
    #print("materialCrc32 count: " + str(materialCrc32Count))
    materialCRC32s = []
    bitmapCrc32s = []
    materialLinkCrc32s = []
    materialColors = []
    for _ in range(materialCrc32Count):
        matName = bs.readInt()
        materialCRC32s.append(matName)
        bitmapLinkAndColor = getBitmapLinkAndColorFromMaterial(matName)
        bitmapCrc32s.append(bitmapLinkAndColor[0])
        materialLinkCrc32s.append(bitmapLinkAndColor[1])
        materialColors.append(bitmapLinkAndColor[2])
    if not (objFlag & 4) and len(materialLinkCrc32s) > 0:
        curMatId = -1
        for i in range(len(strips)):
            curStrip = strips[i]
            if curMatId != curStrip[1]:
                vertexGroups.append(materialLinkCrc32s[curStrip[1]])
                vertexGroupsStartIndices.append(i)
                if curMatId != -1:
                    vertexGroupsEndIndices.append(i)
            curMatId = curStrip[1]
        vertexGroupsEndIndices.append(len(strips)-1)
    
    sphereColCount = bs.readUInt()
    #print("sphereCol count: " + str(sphereColCount))
    if sphereColCount > 0:
        for _ in range(sphereColCount):
            bs.seek(16,NOESEEK_REL)

    boxColCount = bs.readUInt()
    #print("boxCol count: " + str(boxColCount))
    if boxColCount > 0:
        for _ in range(boxColCount):
            bs.seek(80,NOESEEK_REL)

    cylinderColCount = bs.readUInt()
    #print("cylinderCol count: " + str(cylinderColCount))
    if cylinderColCount > 0:
        for _ in range(cylinderColCount):
            bs.seek(32,NOESEEK_REL)
    
    stripColorCount = bs.readUInt()
    #print("stripColor count: " + str(stripColorCount))
    stripColors = []
    for _ in range(stripColorCount):
        stripColors.append(NoeVec4.fromBytes(bs.readBytes(0x10)))
    
    stripIndiceCount = bs.readUInt()
    #print("stripIndice count: " + str(stripIndiceCount))
    stripIndices = []
    for _ in range(stripIndiceCount):
        stripIndices.append(bs.readUInt())

    face_vert_buffers = []
    face_uv_buffers = []
    face_normals_buffers = []
    face_color_buffers = []
    face_indices_buffers = []
    #print("number of vGroups: " + str(len(vertexGroups)))
    for vg in range(len(vertexGroups)):
        face_verts = bytes()
        face_uvs = bytes()
        face_normals = bytes()
        face_colors = bytes()
        faceIndices = bytes()
        faceIdx = 0

        vertGrpName = vertexGroups[vg]
        try:
            indexOfVertGrp = materialLinkCrc32s.index(vertGrpName)
            materialColorF = materialColors[indexOfVertGrp].toBytes()
        except:
            materialColorF = bytearray()
            for _ in range(4):
                materialColorF.append(0x00)
                materialColorF.append(0x00)
                materialColorF.append(0x80)
                materialColorF.append(0x3f)
        
        start = vertexGroupsStartIndices[vg]
        end = vertexGroupsEndIndices[vg]
        #print("vertexGroup [" + str(vg) + "] start: " + str(start) + ", end: " + str(end))
        for i in range(start,end+1):
            strip = strips[i]
            stripData = stripDatas[i]
            stripColorIndex = stripIndices[i]
            triorder = strip[2]
            for j in range(len(strip[0])-2):
                indices = []
                indices.append(j)
                if j % 2 == 0:
                    indices.append(3 - triorder + j)
                    indices.append(triorder + j)
                else:
                    indices.append(triorder + j)
                    indices.append(3 - triorder + j)
                face_verts += verts[strip[0][indices[0]]].toBytes()
                face_verts += verts[strip[0][indices[1]]].toBytes()
                face_verts += verts[strip[0][indices[2]]].toBytes()

                face_uvs += uvBuff[stripData[indices[0]][0]]
                face_uvs += uvBuff[stripData[indices[1]][0]]
                face_uvs += uvBuff[stripData[indices[2]][0]]

                face_normals += normalBuff[stripData[indices[0]][1]].toBytes()
                face_normals += normalBuff[stripData[indices[1]][1]].toBytes()
                face_normals += normalBuff[stripData[indices[2]][1]].toBytes()

                # face_colors += stripColors[stripColorIndex].toBytes()
                # face_colors += stripColors[stripColorIndex].toBytes()
                # face_colors += stripColors[stripColorIndex].toBytes()
                face_colors += materialColorF
                face_colors += materialColorF
                face_colors += materialColorF

                faceIndices += struct.pack("<H", faceIdx)
                faceIndices += struct.pack("<H", faceIdx+1)
                faceIndices += struct.pack("<H", faceIdx+2)
                faceIdx = faceIdx+3
        face_vert_buffers.append(face_verts)
        face_uv_buffers.append(face_uvs)
        face_normals_buffers.append(face_normals)
        face_color_buffers.append(face_colors)
        face_indices_buffers.append(faceIndices)

    #print("len face_verts: " + str(len(face_verts)))
    #print("len face_normals: " + str(len(face_normals)))
    #print("len face_uvs: " + str(len(face_uvs)))
    #print("len faceIndices: " + str(len(faceIndices)))
    for vg in range(len(vertexGroups)):
        vgName = vertexGroups[vg]
        try:
            indexOfVg = materialLinkCrc32s.index(vgName)
            bitmapName = bitmapCrc32s[indexOfVg]
            materialName = materialCRC32s[indexOfVg]
        except:
            indexOfVg = -1
            bitmapName = 0
            materialName = 0
        #print("indexOfVg: " + str(indexOfVg))
        #print("bitmapName: " + str(bitmapName))
        matList = []
        texList = []
        getMaterialAndTextureLists(bitmapName, matList, texList, materialName)
        rapi.rpgSetMaterial(matList[0].name)
        rapi.rpgBindPositionBuffer(face_vert_buffers[vg], noesis.RPGEODATA_FLOAT, 12)
        rapi.rpgBindNormalBuffer(face_normals_buffers[vg], noesis.RPGEODATA_FLOAT, 12)
        rapi.rpgBindUV1Buffer(face_uv_buffers[vg], noesis.RPGEODATA_FLOAT, 8)
        #dont think these are really colors
        rapi.rpgBindColorBuffer(face_color_buffers[vg], noesis.RPGEODATA_FLOAT, 16, 4)
        rapi.rpgCommitTriangles(face_indices_buffers[vg], noesis.RPGEODATA_USHORT, (len(face_indices_buffers[vg])//2), noesis.RPGEO_TRIANGLE, 3)

    try:
        mdl = rapi.rpgConstructModel()
    except:
        mdl = NoeModel()
    mdlList.append(mdl)
    return 1