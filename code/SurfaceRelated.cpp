#include <vector>

struct Vec4f
{
    float x;
    float y;
    float z;
    float w;

    Vec4f();

    Vec4f(float x, float y, float z, float w)
    {
        this->x = x;
        this->y = y;
        this->z = z;
        this->w = w;
    }

    Vec4f(Vec3f vec3f, float w)
    {
        this->x = vec3f.x;
        this->y = vec3f.y;
        this->z = vec3f.z;
        this->w = w;
    }

    Vec4f &operator+(const Vec4f &other)
    {
        return Vec4f(this->z + other.z, this->y + other.y, this->z + other.z, this->w + other.w);
    }

    Vec4f &operator-(const Vec4f &other)
    {
        return Vec4f(this->z - other.z, this->y - other.y, this->z - other.z, this->w - other.w);
    }
};

struct Vec3f
{
    float x;
    float y;
    float z;
};

enum PatchFlag
{
    EDGE1 = 2,
    EDGE2 = 4,
    EDGE3 = 8,
    EDGE4 = 16,
};

struct QuadCtrlPoint_Z
{
    Vec4f ControlPoints[4][4];
};

struct Patch
{
    uint16_t Flag;
    uint16_t EdgeIndices[4];
};

struct Edge
{
    uint16_t P[2];
    uint16_t T[2];
};

class Surface_Z
{
    void Surface_Z::GetQuadPatchCtrlPoint(Patch& i_Patch, QuadCtrlPoint_Z& o_QuadCtrlPoint);

    struct
    {
        std::vector<Vec3f> Vertices;
    } Points;
    Edge EdgeDA[];
};

void Surface_Z::GetQuadPatchCtrlPoint(Patch& i_Patch, QuadCtrlPoint_Z& o_QuadCtrlPoint)
{
    // Points on the extremities
    o_QuadCtrlPoint.ControlPoints[0][0] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[0]].P[i_Patch.Flag & EDGE1 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[0][3] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[1]].P[i_Patch.Flag & EDGE2 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[3][3] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[2]].P[i_Patch.Flag & EDGE3 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[3][0] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[3]].P[i_Patch.Flag & EDGE4 ? 1 : 0]], 1.0);

    // First side
    o_QuadCtrlPoint.ControlPoints[0][1] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[0]].T[i_Patch.Flag & EDGE1 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[0][2] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[0]].T[i_Patch.Flag & EDGE1 ? 0 : 1]], 1.0);

    // Second side
    o_QuadCtrlPoint.ControlPoints[1][3] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[1]].T[i_Patch.Flag & EDGE2 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[2][3] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[1]].T[i_Patch.Flag & EDGE2 ? 0 : 1]], 1.0);

    // Third side
    o_QuadCtrlPoint.ControlPoints[3][2] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[2]].T[i_Patch.Flag & EDGE3 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[3][1] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[2]].T[i_Patch.Flag & EDGE3 ? 0 : 1]], 1.0);

    // Fourth side
    o_QuadCtrlPoint.ControlPoints[2][0] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[3]].T[i_Patch.Flag & EDGE4 ? 1 : 0]], 1.0);
    o_QuadCtrlPoint.ControlPoints[1][0] = Vec4f(Points.Vertices[EdgeDA[i_Patch.EdgeIndices[3]].T[i_Patch.Flag & EDGE4 ? 0 : 1]], 1.0);

    // Calculate central points from adjacent extremity and side points
    o_QuadCtrlPoint.ControlPoints[1][1] = (o_QuadCtrlPoint.ControlPoints[1][0] + o_QuadCtrlPoint.ControlPoints[0][1]) - o_QuadCtrlPoint.ControlPoints[0][0];
    o_QuadCtrlPoint.ControlPoints[1][2] = (o_QuadCtrlPoint.ControlPoints[0][2] + o_QuadCtrlPoint.ControlPoints[1][3]) - o_QuadCtrlPoint.ControlPoints[0][3];
    o_QuadCtrlPoint.ControlPoints[2][1] = (o_QuadCtrlPoint.ControlPoints[3][1] + o_QuadCtrlPoint.ControlPoints[2][0]) - o_QuadCtrlPoint.ControlPoints[3][0];
    o_QuadCtrlPoint.ControlPoints[2][2] = (o_QuadCtrlPoint.ControlPoints[2][3] + o_QuadCtrlPoint.ControlPoints[3][2]) - o_QuadCtrlPoint.ControlPoints[3][3];
}