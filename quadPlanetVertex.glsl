//Cg
//Cg profile glslv glslf  

struct OUTPUT {
    vector pos : POSITION;
    float2 uv : TEXCOORD0; // coordinates for normal-map lookup
    float z : TEXCOORD1; // coordinates for elevation-map lookup
    float alpha : TEXCOORD2; // transition blend on normal map
};

uniform float4 ScaleFactor, FineBlockOrig;
uniform float2 ViewerPos, AlphaOffset, OneOverWidth;
uniform float ZScaleFactor, ZTexScaleFactor;
uniform matrix WorldViewProjMatrix;

// Vertex shader for rendering the geometry clipmap
//OUTPUT RenderVS(float2 gridPos: TEXCOORD0)
OUTPUT vshader(float2 gridPos: TEXCOORD0)
{
    OUTPUT output;
    // convert from grid xy to world xy coordinates
    // ScaleFactor.xy: grid spacing of current level
    // ScaleFactor.zw: origin of current block within world
    float2 worldPos = gridPos * ScaleFactor.xy + ScaleFactor.zw;

    // compute coordinates for vertex texture
    // FineBlockOrig.xy: 1/(w, h) of texture
    // FineBlockOrig.zw: origin of block in texture
    float2 uv = gridPos * FineBlockOrig.xy + FineBlockOrig.zw;

    // sample the vertex texture
    float zf_zd = tex2Dlod(ElevationSampler, float4(uv, 0, 1));

    // unpack to obtain zf and zd = (zc - zf)
    // zf is elevation value in current (fine) level
    // zc is elevation value in coarser level
    float zf = floor(zf_zd);
    float zd = frac(zf_zd) * 512 - 256; // (zd = zc - zf)

    // compute alpha (transition parameter) and blend elevation
    float2 alpha = float2(0, 0);
    //float2 alpha = clamp((abs(worldPos - ViewerPos) –
    //                    AlphaOffset) * OneOverWidth, 0, 1);
    alpha.x = max(alpha.x, alpha.y);
    float z = zf + alpha.x * zd;
    z = z * ZScaleFactor;
    output.pos =
    mul
    (
    float4
    (worldPos.x, worldPos.y, z, 1),
    WorldViewProjMatrix);
    output.uv = uv;
    output.z = z * ZTexScaleFactor;
    output.alpha = alpha.x;
    return
    output;
}