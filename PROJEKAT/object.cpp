#include "object.hpp"
#include "common.hpp"
#include <cstddef>
#include <cstdio>
#include <glm/fwd.hpp>
#include <sstream>
#include <string>
#include <vector>
#include <SOIL/SOIL.h>

void Object::generateBuffers()
{
	glGenVertexArrays(1, &vao);
	glBindVertexArray(vao);

	glGenBuffers(1, &vertexBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer);
	glBufferData(GL_ARRAY_BUFFER,
				 vertices.size()*sizeof(glm::vec3), 
				 &vertices[0], GL_STATIC_DRAW);

	glGenBuffers(1, &uvBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, uvBuffer);
	glBufferData(GL_ARRAY_BUFFER,
				 uvs.size()*sizeof(glm::vec2), 
				 &uvs[0], GL_STATIC_DRAW);

	glGenBuffers(1, &normalBuffer);
	glBindBuffer(GL_ARRAY_BUFFER, normalBuffer);
	glBufferData(GL_ARRAY_BUFFER,
				 normals.size()*sizeof(glm::vec2), 
				 &normals[0], GL_STATIC_DRAW);
}

void Object::loadTexture(const std::string path)
{
	glGenTextures(1, &texture);
	
	int width, height;
	unsigned char* image;

	glBindTexture(GL_TEXTURE_2D, texture);		
	image =	SOIL_load_image(path.c_str(), &width, &height, 0, SOIL_LOAD_RGB);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
				 width, height, 0, GL_RGB,
				 GL_UNSIGNED_BYTE, image);
	SOIL_free_image_data(image);
	
	glGenerateMipmap(GL_TEXTURE_2D);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_NEAREST);
}

void Object::setShaderProgram(GLuint shader)
{
	shaderProgram = shader;
}

void Object::bindShader()
{
	if (shaderProgram == -1) return;
	// TODO: Error.
	
	glUseProgram(shaderProgram);
	glBindVertexArray(vao);
	
	glBindBuffer(GL_ARRAY_BUFFER, vertexBuffer);
	GLint posAttrib = glGetAttribLocation(shaderProgram, "position");
	glEnableVertexAttribArray(posAttrib);	
	glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE, 0, 0);

	glBindBuffer(GL_ARRAY_BUFFER, uvBuffer);
	GLint uvAttrib = glGetAttribLocation(shaderProgram, "uv");
	glEnableVertexAttribArray(uvAttrib);	
	glVertexAttribPointer(uvAttrib, 2, GL_FLOAT, GL_FALSE, 0, 0);

	glBindBuffer(GL_ARRAY_BUFFER, normalBuffer);
	GLint normalAttrib = glGetAttribLocation(shaderProgram, "normal");
	glEnableVertexAttribArray(normalAttrib);	
	glVertexAttribPointer(normalAttrib, 3, GL_FLOAT, GL_FALSE, 0, 0);
}

void Object::render() const
{
	glBindVertexArray(vao);
	glUseProgram(shaderProgram);

	glActiveTexture(GL_TEXTURE0);
	glBindTexture(GL_TEXTURE_2D, texture);
	
	glDrawArrays(GL_TRIANGLES, 0, vertices.size());
}


Object* ObjectHandler::loadOBJ(const std::string& path)
{
	Object* object = new Object();

	std::vector<unsigned int> vertexIndices, uvIndices, normalIndices;
	std::vector<glm::vec3> tmpVertices, tmpNormals;
	std::vector<glm::vec2> tmpUvs;
	
	std::vector<std::string> lines = *parse_file(path);
	

	for (auto line: lines)
		parseLine(line, tmpVertices, tmpNormals, tmpUvs, vertexIndices, uvIndices, normalIndices);

	for (size_t i = 0; i<vertexIndices.size(); i++)
	{
		object->vertices.push_back(tmpVertices[vertexIndices[i] - 1]);
		object->uvs.push_back(tmpUvs[uvIndices[i] - 1]);
		object->normals.push_back(tmpNormals[normalIndices[i] - 1]);
	}

	return object;
}

void ObjectHandler::tokenize(const std::string& line,  std::vector<std::string>& tokens, char delimiter)const
{
	std::stringstream ss(line);	

	std::string token;
	while (getline(ss, token, delimiter))
		tokens.push_back(token);
}


void ObjectHandler::parseLine(
		const std::string& line,
		std::vector<glm::vec3>& vertices,
		std::vector<glm::vec3>& normals,
		std::vector<glm::vec2>& uvs,
		std::vector<unsigned int>& vIndices,
		std::vector<unsigned int>& uIndices,
		std::vector<unsigned int>& nIndices) const
{
   	std::vector<std::string> tokens, indices;	
	
	tokenize(line, tokens); 
	switch (line[0]) {
	case '#': break;
	case 'v':
		switch(line[1])
		{
		case ' ':
		vertices.push_back(
			glm::vec3(std::stof(tokens[1]), std::stof(tokens[2]), std::stof(tokens[3]))
			);
		break;
		case 't':
		uvs.push_back(
			glm::vec2(std::stof(tokens[1]), std::stof(tokens[2]))
			);
		break;
		case 'n':
		normals.push_back(
			glm::vec3(std::stof(tokens[1]), std::stof(tokens[2]), std::stof(tokens[3]))
			);
		break;
		}
		break;
	case 'f':
		for (int i=1; i<4; i++)
		{
			tokenize(tokens[i], indices, '/');
			vIndices.push_back(std::stoi(indices[0]));
			uIndices.push_back(std::stoi(indices[1]));
			nIndices.push_back(std::stoi(indices[2]));
			indices.clear();
		}
		break;
	}
	tokens.clear();
}
