import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
from Object import *

pygame.init()

screen = pygame.display.set_mode(
    (1000, 800),
    pygame.OPENGL | pygame.DOUBLEBUF
)
# dT = pygame.time.Clock()


#Código para la creación del shader.
vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;

uniform mat4 amatrix;

out vec3 ourColor;


void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    ourColor = vertexColor;

}
"""
#Código para la creación del shader.
fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;


in vec3 ourColor;

void main()
{
    // fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""
#Código para la creación del shader.
compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
shader = compileProgram(
    compiled_vertex_shader,
    compiled_fragment_shader
) #Código para la creación del shader.

glUseProgram(shader) #Se usa el shader.

o = Object('bowOBJ.obj')

#Matriz de vértices para el triángulo.
vertex_data = numpy.array([
  o.vertices
], dtype=numpy.float32) #Matriz para dibujar el triángulo.


vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(
    GL_ARRAY_BUFFER,  # tipo de datos
    vertex_data.nbytes,  # tamaño de da data en bytes    
    vertex_data, # puntero a la data
    GL_STATIC_DRAW
)
vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * 4,
    ctypes.c_void_p(0)
) #Aquí se calculan los saltos que se darán en los índices de la matriz de vértices. (Esto es para los vérices del triángulo).
glEnableVertexAttribArray(0)


# glVertexAttribPointer(
#     1,
#     3,
#     GL_FLOAT,
#     GL_FALSE,
#     6 * 4,
#     ctypes.c_void_p(3 * 4)
# ) #Aquí se calculan los saltos que se darán en los índices de la matriz de vértices. (Esto es para los colores del triángulo).
# glEnableVertexAttribArray(1)


def calculateMatrix(angle): #Método para calcular la matriz del modelo.
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, 0, 0))
    rotate = glm.rotate(i, glm.radians(angle), glm.vec3(0, 1, 0))
    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate * rotate * scale

    view = glm.lookAt(
        glm.vec3(0, 0, 5),
        glm.vec3(0, 0, 0),
        glm.vec3(0, 1, 0)
    ) #Matriz de vista.

    projection = glm.perspective(
        glm.radians(45),
        1000/800,
        0.1,
        1000.0
    ) #Cálculo de la proyección de la cámara.

    amatrix = projection * view * model #Cálculo de la matriz de transformación.

    glUniformMatrix4fv(
        glGetUniformLocation(shader, 'amatrix'),
        1,
        GL_FALSE,
        glm.value_ptr(amatrix)
    ) #Envío de la matriz de transformación al shader.

glViewport(0, 0, 1000, 800) #Definición del viewport.

#Método para cargar un objeto.
def loadObject(path):
    o = Object(path)

    vertices = o.vertices

    vertex_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(
        GL_ARRAY_BUFFER,  # tipo de datos
        vertex_data.nbytes,  # tamaño de da data en bytes    
        vertex_data, # puntero a la data
        GL_STATIC_DRAW
    )
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    glVertexAttribPointer(
        0,
        3,
        GL_FLOAT,
        GL_FALSE,
        3 * 4,
        ctypes.c_void_p(0)
    ) #Aquí se calculan los saltos que se darán en los índices de la matriz de vértices. (Esto es para los vérices del triángulo).
    glEnableVertexAttribArray(0)

running = True

glClearColor(0.5, 1.0, 0.5, 1.0) #Color de fondo.

loadObject('bowOBJ.obj')

r = 0

while running:
    #r += 20 #Variable para el ángulo de rotación.

    glClear(GL_COLOR_BUFFER_BIT) #Limpieza del buffer de color.

    #Área del triángulo 1.
    color1 = random.random()
    color2 = random.random()
    color3 = random.random()

    color = glm.vec3(40, 25, 100) #Color del triángulo.

    glUniform3fv(
        glGetUniformLocation(shader,'color'),
        1,
        glm.value_ptr(color)
    ) #Envío del color al shader.

    calculateMatrix(r) #Calculo de la matriz de transformación.

    pygame.time.wait(1)


    glDrawArrays(GL_TRIANGLES, 0, 3) #Dibujo del triángulo.


    pygame.display.flip()

    for event in pygame.event.get(): #Cierre de la ventana.
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN: #Detectando la tecla presionada.
            if event.key == pygame.K_a: #Rotación hacia la izquierda.
                r += 20
            if event.key == pygame.K_d: #Rotación hacia la derecha.
                r -= 20
            if event.key == pygame.K_LEFT: #Rotación hacia la izquierda.
                r += 20
            if event.key == pygame.K_RIGHT: #Rotación hacia la derecha.
                r -= 20