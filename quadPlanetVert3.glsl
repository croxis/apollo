uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 trans_model_to_cube;
uniform mat4 trans_cube_to_apiclip;

varying vec4 texCoords;

<rdb> croxis, something along those lines.  the idea is that you first transform it from model to cube space, *then* normalize the vector using whatever way actually works, then transform it to apiclip space
//out varying vec4 Position;

void main(void) {
    //gl_Position = p3d_ModelViewProjectionMatrix * gl_Vertex;
    //gl_Position = vec4(normalize(gl_Vertex.xyz), gl_Vertex.w);

    //gl_Position = p3d_ModelViewProjectionMatrix * vec4(normalize(gl_Vertex.xyz), gl_Vertex.w);
    
    //vec4 test = p3d_ModelViewProjectionMatrix * gl_Vertex;    
    //gl_Position = vec4(normalize(test.xyz), gl_Vertex.w);
    gl_Position = mul(trans_model_to_cube, gl_Position);
    gl_Position = vec4(normalize(gl_Position.xyz / gl_Position.w), 1);
    gl_Position = mul(trans_cube_to_apiclip, gl_Vertex);
    //vec4 test = gl_Vertex;
    //test.z = test.z + 1.0;
    //gl_Position = p3d_ModelViewProjectionMatrix * vec4(normalize(test.xyz), test.w);
    //gl_Position.w = gl_Position.w -1.0;
    
    //float x = gl_Position.x;
    //float y = gl_Position.y;
    //float z = gl_Position.z;
    //float x = gl_Vertex.x;
    //float y = gl_Vertex.y;
    //float z = gl_Vertex.z;
    //gl_Position.x *= sqrt(1.0 - y * y * 0.5 - z * z * 0.5 + y * y * z * z / 3.0);
    //gl_Position.y = gl_Position.y * sqrt(1.0 - z * z * 0.5 - x * x * 0.5 + z * z * x * x / 3.0);
    //gl_Position.z = gl_Position.z * sqrt(1.0 - x * x * 0.5 - y * y * 0.5 + x * x * y * y / 3.0);
    gl_FrontColor = gl_Color;
    texCoords = gl_MultiTexCoord0;          
}