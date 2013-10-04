// based on https://www.shadertoy.com/view/4dXGR4 by flight404
// CC-NC-SA

uniform float time;
uniform sampler2D p3d_Texture0;
varying vec2 texture_coordinate;
varying vec4 texCoords;

varying vec3 varyingNormalDirection; 
            // normalized surface normal vector
varying vec3 varyingViewDirection; 
            // normalized view direction 

float snoise(vec3 uv, float res)    // by trisomie21
{
    const vec3 s = vec3(1e0, 1e2, 1e4);
    
    uv *= res;
    
    vec3 uv0 = floor(mod(uv, res))*s;
    vec3 uv1 = floor(mod(uv+vec3(1.), res))*s;
    
    vec3 f = fract(uv); f = f*f*(3.0-2.0*f);
    
    vec4 v = vec4(uv0.x+uv0.y+uv0.z, uv1.x+uv0.y+uv0.z,
                  uv0.x+uv1.y+uv0.z, uv1.x+uv1.y+uv0.z);
    
    vec4 r = fract(sin(v*1e-3)*1e5);
    float r0 = mix(mix(r.x, r.y, f.x), mix(r.z, r.w, f.x), f.y);
    
    r = fract(sin((v + uv1.z - uv0.z)*1e-3)*1e5);
    float r1 = mix(mix(r.x, r.y, f.x), mix(r.z, r.w, f.x), f.y);
    
    return mix(r0, r1, f.z)*2.-1.;
}

float freqs[4];

void main(void)
{
    float brightness    = 0.25;
    vec3 orange         = vec3( 0.8, 0.65, 0.3 );
    vec3 orangeRed      = vec3( 0.8, 0.35, 0.1 );

    vec3 starSphere     = vec3( 0.0 );

    //float f = (1.0-sqrt(abs(1.0-r)))/(r) + brightness * 0.5;
    //if (dist < radius){
        vec2 newUV      = vec2(0.0, 0.0);

        vec3 texSample  = texture(p3d_Texture0, newUV);
        //float uOff      = ( texSample.g * brightness * 4.5 + time);
        float uOff  = texSample.g;
        vec2 starUV = texCoords.xy + vec2(uOff, 0.0);
        starSphere = texture(p3d_Texture0, starUV);
        //}


    vec3 normalDirection = normalize(varyingNormalDirection);
    vec3 viewDirection = normalize(varyingViewDirection);
    gl_FragColor.rgb = vec3(( 0.75 + min(1.0, 0.1/abs(dot(viewDirection, normalDirection))) ) * orange) + starSphere;
    //gl_FragColor.rgb    = vec3( f * ( 0.75 + brightness * 0.3 ) * orange ) + starSphere  + starGlow * orangeRed;
    gl_FragColor.a      = 1.0;
}
