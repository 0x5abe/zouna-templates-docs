# Seads

In this page I'll try to explain what I understand Seads are, what they are used for and how they work. The main class of study for now is SeadHandle_Z, since World_Z files stores 2 of these (presumably for collision and display). Everything documented is based in the Opal version of Zouna used for Shaun White 1, it's known to be different for Asobo games, but the basic idea and usage is the same.

Here's what the members of SeadHandle_Z are:

- Vec2f PMin;
- Vec2f PMax;
- Vec2f InvDiag;
- S32 SizeX;
- S32 SizeY;
- U16 FirstFree;
- U16 NbFree;
- DynArray_Z<U16,32> GridDA;
- DynArray_Z<SeadEntry_Z,32> EntryPoolDA;
- Node_Z* ZoneNodes[SEAD_RECURSE_MAX_NODE];
- S32 ZoneNodeNb;

SeadHandle_Z uses a 2d grid (GridDA) made up of SizeX*SizeY squares to divide the world. 

Each square of the grid can have multiple SeadEntry_Z objects in the entry pool (EntryPoolDA) corresponding to it, each entry has references (the indices in the pool) to the previous and next entries of that grid position, as well as the next entry for that object and the index in the grid.

In the stored World_Z file, the entry pool already has some nodes referenced, but it also has free entries. Node_Z has 2 fields which store the indices of the first SeadEntry_Z's in the entry pools for the display and collision SeadHandle_Z's. These fields are loaded from the Node_Z files stored in the BF.

When a new Node_Z is created it has a flag set (FL_NODE_SEAD_ISINVALID) which is checked in Node_Z::Update and triggers a function to reference the node in the SeadHandle_Z's (recursively, as it will set FL_NODE_SEAD_ISINVALID for all children). In case the current node is already referenced and the rectangle it's using corresponds correctly to the one you get from the bounding box it won't try to reference it again, otherwise it will unreference it and reference it with the new rectangle. 

Methods that change the Node_Z's TRS will set FL_NODE_SEAD_ISINVALID, as well as some other more specific cases, for example, setting a new skybox sets that flag in the camera node.

SeadHandle_Z::SetZone is used to put the nodes that belong to the current zone in the ZoneNodes array, and those nodes can be then acquired to compute collision or visibility for example. Therefore not having to take every node into account, just the ones that matter (are in the view frustum for computing visibility, or are near for collision).










