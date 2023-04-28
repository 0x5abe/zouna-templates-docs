from binary_reader import *
import bpy
import os
import bmesh

rootpath = ""
excludedMeshes = []

def readMesh_Z(f,subsectionMatIndices):
    reader = BinaryReader(f.read())
    datasize = reader.read_uint32()
    linksize = reader.read_uint32()
    decompressedsize = reader.read_uint32()
    compressedsize = reader.read_uint32()
    classcrc32 = reader.read_uint32()
    namecrc32 = reader.read_uint32()
    name = str(namecrc32)
    reader.seek(linksize + 32, whence=1)
    matCrc32Count = reader.read_uint32()
    matCrc32List = []
    matList = []
    addMatIndices = False
    
    if not subsectionMatIndices:
        addMatIndices = True
        
    for i in range(matCrc32Count):
        matCrc32List.append(str(reader.read_uint32()))
        if addMatIndices: subsectionMatIndices.append(i)

    for h in matCrc32List:
        mat = bpy.data.materials.new(name=str(h))
        mat.use_nodes = True
        material_z = (rootpath + str(h) + ".Material_Z")
        fe = open(material_z, "rb")
        reader2 = BinaryReader(fe.read())
        reader2.seek(0x20)
        texturename = reader2.read_uint32()
        strtexturename = str(texturename)
            
         #open bitmap_z's and get dds from those automatically

        bitmap_z = (rootpath + strtexturename + ".Bitmap_Z")
        dds = (rootpath + strtexturename + ".dds")
        bm = open(bitmap_z, "rb")
        tex = open(dds, "wb")
        reader3 = BinaryReader(bm.read())
        reader3.set_endian(False)
        reader3.seek(0x28)
        size3 = reader3.read_uint32()
        reader3.seek(0x34)
        tex.write(reader3.read_bytes(size3))
        bm.close()
        tex.close()
        fe.close()
        
        nodes = mat.node_tree.nodes
        bdsf = nodes['Principled BSDF']
        imagetexture = nodes.new('ShaderNodeTexImage')
        imagetexture.location = (-300, 250)
        imagetexture.image = bpy.data.images.load(rootpath + strtexturename + ".dds")
        link = mat.node_tree.links.new
        link(imagetexture.outputs[0], bdsf.inputs[0])
        link(imagetexture.outputs[1], bdsf.inputs[21])
        bdsf.inputs['Specular'].default_value = 0

    stuffRelatedToCounts = reader.read_bytes(24)
    spherecolcount = reader.read_uint32()
    if (spherecolcount != 0):
        for i in range(spherecolcount):
            reader.read_bytes(20)
            reader.read_uint32()
    boxcolcount = reader.read_uint32()
    if (boxcolcount != 0):
        for i in range(boxcolcount):
            reader.read_float(16)
            reader.read_uint32()
            reader.read_uint32()
    cylindercolcount = reader.read_uint32()
    if (cylindercolcount != 0):
        for i in range(cylindercolcount):
            reader.read_bytes(40)
            reader.read_uint32()
    AABBColRelatedCount = reader.read_uint32()
    if (AABBColRelatedCount != 0):
        for i in range(AABBColRelatedCount):
            reader.read_uint32(2)
    AABBColCount = reader.read_uint32()
    if (AABBColCount != 0):
        for i in range(AABBColCount):
            reader.read_uint32(8)
    shortvertexcount = reader.read_uint32()
    #setup mesh for creation


    vertices_list = []
    uv_list = []
    normals2 = list()
    faces_list = []
    test = []

    #read short vertices and basically ignore them

    for i in range(shortvertexcount * 3):
        reader.read_uint16()
    zero = reader.read_uint32()
    unkUintCount = reader.read_uint32()
    if (unkUintCount != 0):
        for i in range(unkUintCount):
            reader.read_uint32()
    one = reader.read_uint32()
    #vertices

    vertexcount = reader.read_uint16()
    vertexSize = reader.read_uint16()
    if (vertexSize == 24):
        print("!!!!!! SKIPPED (24B vertices): " + name + ".Mesh_Z")
        return
    vertexStart = reader.pos()
    reader.seek(vertexcount*vertexSize,1)
    reader.read_uint32()
    faceShortCount = reader.read_uint16()
    faceStart = reader.pos()
    reader.seek(faceShortCount * 2,1)
    vertexGroupCount = reader.read_uint32()
    reader.seek(18,1)
    for i in range(vertexGroupCount):
        bm = bmesh.new()
        uv_layer = bm.loops.layers.uv.new()
        vertexBufferOffset = reader.read_uint16()
        vertexCountInBuffer = reader.read_uint16()
        faceBufferOffset = reader.read_uint16()
        faceCountInBuffer = reader.read_uint32()
        reader.read_uint8()
        material = reader.read_uint8()
        stay = reader.pos()
        reader.seek(vertexStart + vertexBufferOffset*vertexSize)
        for j in range(vertexCountInBuffer):
            x = reader.read_float()
            z = reader.read_float()
            y = reader.read_float()
            unk1 = reader.read_float()
            bnx = reader.read_uint8()
            bny = reader.read_uint8()
            bnz = reader.read_uint8()
            pad = reader.read_int8()
            uvx = reader.read_float()
            uvy = reader.read_float()
            reader.read_bytes(vertexSize - 28)
            vertices_list.append(bm.verts.new((x,y,z)))
            uv_list.append((uvx,uvy))
            byteToNormalX = (bnx / 255.0)
            byteToNormalY = (bny / 255.0)
            byteToNormalZ = (bnz / 255.0)
            nx = (((byteToNormalX*2)-1))
            ny = (((byteToNormalY*2)-1))
            nz = (((byteToNormalZ*2)-1))
            normals2.append([nx,nz,ny])
        
        reader.seek(faceStart + faceBufferOffset*2)
        
        for k in range(faceCountInBuffer):
            try:
                face = bm.faces.new([vertices_list[reader.read_uint16()] for x in range(3)])
                face.material_index = subsectionMatIndices[i]
            except:
                continue
        
        bm.verts.ensure_lookup_table()
        bm.verts.index_update()
        def uv_to_blender(uv):
            return (uv[0], 1.0 - uv[1])
        for face in bm.faces:
            for loop in face.loops:
                loop[uv_layer].uv = uv_to_blender(uv_list[loop.vert.index])
            
        newmesh = bpy.data.meshes.new('newmesh')
        bm.to_mesh(newmesh)
        newmesh.create_normals_split()
        newmesh.normals_split_custom_set_from_vertices(normals2)
        newmesh.auto_smooth_angle = 0
        newmesh.use_auto_smooth = True
        newobject = bpy.data.objects.new((name + "_" + str(i)), newmesh)
        bpy.context.collection.objects.link(newobject)
        normals2.clear()
        uv_list.clear()
        
        obj = bpy.context.collection.objects[(name + "_" + str(i))]
        obj.data.materials.append(bpy.data.materials.get(matCrc32List[subsectionMatIndices[i]]))
        
        try:
            reader.seek(stay + 24)
        except:
            continue

def readSkin(f):
    subSectionMaterialIndices = []
    reader = BinaryReader(f.read())
    reader.set_endian(False)
    datasize = reader.read_uint32()
    linksize = reader.read_uint32()
    decompressedsize = reader.read_uint32()
    compressedsize = reader.read_uint32()
    classcrc32 = reader.read_uint32()
    namecrc32 = reader.read_uint32()
    linkCrc32 = reader.read_uint32()
    linkCount = reader.read_uint32()
    reader.seek(4*linkCount,1)
    skelCrc32 = reader.read_uint32()
    reader.seek(16,1)
    reader.seek(74,1)
    meshCrc32Count = reader.read_uint32()
    meshCrc32 = []
    for i in range(meshCrc32Count):
        curMesh = reader.read_uint32();
        meshCrc32.append(curMesh)
        excludedMeshes.append(rootpath + str(curMesh) + ".Mesh_Z")
    for i in range(reader.read_uint32()):
        reader.seek(8,1)
    for i in range(reader.read_uint32()):
        reader.read_uint32()
        for i in range(reader.read_uint32()):
            reader.read_uint16()
            for i in range(reader.read_uint32()):
                reader.seek(8,1)
            for i in range(reader.read_uint32()):
                reader.seek(8,1)
    isClassId = reader.read_uint8()
    if (isClassId != 0):
        for i in range(reader.read_uint32()):
            reader.seek(8,1)
        for i in range(reader.read_uint32()):
            reader.seek(8,1)
    matrixCacheCheck = reader.read_uint32()
    skinSectionCount = reader.read_uint32()
    for i in range(skinSectionCount):
        subSectionMaterialIndices = []
        oldMaterial = -1
        curIndex = -1
        skinSubSectionCount = reader.read_uint32()
        for j in range(skinSubSectionCount):
            curMaterial = reader.read_uint32()
            if (curMaterial != oldMaterial):
                curIndex += 1
            reader.seek(36,1)
            morphPacketCount = reader.read_uint32()
            reader.seek(8*morphPacketCount,1)
            subSectionMaterialIndices.append(curIndex)
            oldMaterial = curMaterial;
        meshName = ((rootpath + "\\" + str(meshCrc32[i])) + ".Mesh_Z")
        mf = open(meshName, "rb")
        readMesh_Z(mf,subSectionMaterialIndices)

def loadAll(path):
    
    for file in os.listdir(rootpath):
        
        if file.endswith(".Skin_Z"):
            f = open(os.path.join(rootpath, file), "rb")
            print("loading: " + os.path.join(path, file))
            
            readSkin(f)
            
    for file in os.listdir(rootpath):
        
        if file.endswith(".Mesh_Z"):
            if (os.path.join(path, file)) in excludedMeshes:
                continue
            f = open(os.path.join(path, file), "rb")
            print("loading: " + os.path.join(path, file))
            
            readMesh_Z(f,[])
            
def loadOne(path):
    
    if path.endswith(".Skin_Z"):
        f = open(path, "rb")
        print("loading: " + path)
            
        readSkin(f)
    elif path.endswith(".Mesh_Z"):
        f = open(path, "rb")
        print("loading: " + path)
            
        readMesh_Z(f,[])

# Load specific skin/mesh

pathOne = 'D:\\Program Files (x86)\\THQ\\Disney-Pixar\\Ratatouille\\RatDebug\\WORLD\\CT.DPC.out\\objects\\3321233114.Skin_Z'
rootpath = os.path.dirname(pathOne) + "\\"
loadOne(pathOne)

# Load all skin/mesh files in directory

#pathAll = 'D:\\Program Files (x86)\\THQ\\Disney-Pixar\\Ratatouille\\RatDebug\\WORLD\\MB.DPC.out\\objects'
#rootpath = pathAll + "\\"
#loadAll(pathAll)