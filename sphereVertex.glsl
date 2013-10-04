varying vec4 texCoords;
 
varying vec3 varyingNormalDirection; 
            // normalized surface normal vector
varying vec3 varyingViewDirection; 
            // normalized view direction 
void main(void) {
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    texCoords = gl_MultiTexCoord0;
    varyingNormalDirection = 
               normalize(gl_NormalMatrix * gl_Normal);
    varyingViewDirection = 
               -normalize(vec3(gl_ModelViewMatrix * gl_Vertex));           
}