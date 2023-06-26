#ifndef OBJLOADER_HPP
#define OBJLOADER_HPP

#include "common.hpp"
#include "errors.hpp"

#include <GL/glew.h>
#include <GL/gl.h>
#include <glm/glm.hpp>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include<vector>

class Object
{
	public:
	Object() = default;

	virtual void generateBuffers();
	virtual void loadTexture(const std::string path);
	
	void setShaderProgram(GLuint shader);
	virtual void bindShader();

	virtual void render() const;

	GLuint vao;
	GLuint vertexBuffer;
	GLuint uvBuffer;
	GLuint normalBuffer;

	GLuint texture;
	
	GLuint fragmentShader;
	GLuint vertexShader;
	glm::mat4 transform;

	GLuint shaderProgram;

	
	std::vector<glm::vec3> vertices, normals;
	std::vector<glm::vec2> uvs;

	enum attribute: GLuint {VERTEX, UV, NORMAL};

	private:
};

class ObjectHandler
{
	public:
		ObjectHandler() = default;
		Object* loadOBJ(const std::string& path);

	private:
	void tokenize(const std::string& line,  std::vector<std::string>& tokens, char delimiter = ' ') const;
	void parseLine(const std::string& line,
				   std::vector<glm::vec3>& vertices, 
				   std::vector<glm::vec3>& normals, 
				   std::vector<glm::vec2>& uvs, 
				   std::vector<unsigned int>& vIndices, 
				   std::vector<unsigned int>& uIndices, 
				   std::vector<unsigned int>& nIndices) const;

};

#endif
