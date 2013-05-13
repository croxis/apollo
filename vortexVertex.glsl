varying vec4 position;

void main() {
    //position = 0.5 * (gl_Vertex + vec4(1.0, 1.0, 1.0, 0.0));
    position = gl_Vertex * 0.3;
  //gl_Position = ftransform();
  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}