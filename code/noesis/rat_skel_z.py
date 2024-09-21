from inc_noesis import *
#literally just stole basically all of this from emily
def registerNoesisTypes():
	handle = noesis.register('Ratatouille Skeleton','.Skel_Z')
	noesis.setHandlerTypeCheck(handle, CheckType)
	noesis.setHandlerLoadModel(handle, LoadModel)	
	return 1
	
def CheckType(data):
	return 1

def LoadModel(data, mdlList):
	ctx = rapi.rpgCreateContext()
	
	bs = NoeBitStream(data,NOE_LITTLEENDIAN)
	bs.seek(4)
	linkSize = bs.readUInt()
	bs.seek(60 + linkSize)
	jointCount = bs.readUInt()
	jointList = []	
	for i in range(jointCount):
		start = bs.tell()
		bs.seek(164,1)
		mat = NoeMat44.fromBytes(bs.readBytes(64)).toMat43()		
		unk = bs.readInt()
		parent = bs.readInt()		
		joint = NoeBone(i, str(i), mat, None, parent)
		jointList.append(joint)
		bs.seek(start + 248)
	
	mdl = NoeModel()
		
	mdl.setBones(jointList)
	mdlList.append(mdl)
	
	return 1
