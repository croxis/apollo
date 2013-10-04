//Cg
//Cg profile glslv glslf 

// Parameters uv, alpha, and z are interpolated from vertex shader.
// Two texture samplers have min and mag filters set to linear:
// NormalMapSampler: 2D texture containing normal map,
// ZBasedColorSampler: 1D texture containing elevation-based color
uniform float3 LightDirection;
// Pixel shader for rendering the geometry clipmap
float4
fshader(
float2
uv :
TEXCOORD0
,
float
z :
TEXCOORD1
,
float
alpha :
TEXCOORD2
) :
COLOR
{
float4
normal_fc =
tex2D
(NormalMapSampler, uv);
// normal_fc.xy contains normal at current (fine) level
// normal_fc.zw contains normal at coarser level
// blend normals using alpha computed in vertex shader
float3
normal =
float3
((1 - alpha) * normal_fc.xy +
alpha * (normal_fc.zw), 1);
// unpack coordinates from [0, 1] to [-1, +1] range, and renormalize
normal =
normalize
(normal * 2 - 1);
// compute simple diffuse lighting
float
s =
clamp
(
dot
(normal, LightDirection), 0, 1);
// assign terrain color based on its elevation
return
s *
tex1D
(ZBasedColorSampler, z);
}