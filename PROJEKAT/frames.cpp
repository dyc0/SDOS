#include "base/application.hpp"
#include <GLFW/glfw3.h>
#include <SOIL/SOIL.h>
#include <bits/chrono.h>
#include <glm/ext/matrix_clip_space.hpp>
#include <glm/ext/matrix_transform.hpp>
#include <glm/ext/vector_float3.hpp>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <chrono>
#include <cmath>
#include <cstddef>
#include <glm/trigonometric.hpp>
#include <string>
#include <fstream>

#define APP_VERT_ARRAY_SIZE 42*8

class AppVertices: public Application
{
	public:
	AppVertices()
	{
		GLfloat tmpVert[] = {
		//   Position            Color             Texture
			-0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,
			 0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			 0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			 0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			-0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			-0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,

			-0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,
			 0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			 0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			 0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			-0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			-0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,

			-0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			-0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			-0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			-0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			-0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,
			-0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,

			 0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			 0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			 0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			 0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			 0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,
			 0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,

			-0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			 0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			 0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			 0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			-0.5f, -0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,
			-0.5f, -0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,

			-0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,
			 0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 1.0f,
			 0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			 0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 1.0f, 0.0f,
			-0.5f,  0.5f,  0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 0.0f,
			-0.5f,  0.5f, -0.5f, 1.0f, 1.0f, 1.0f, 0.0f, 1.0f,

			-1.0f, -1.0f, -0.5f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f,
			 1.0f, -1.0f, -0.5f, 0.0f, 0.0f, 0.0f, 1.0f, 0.0f,
			 1.0f,  1.0f, -0.5f, 0.0f, 0.0f, 0.0f, 1.0f, 1.0f,
			 1.0f,  1.0f, -0.5f, 0.0f, 0.0f, 0.0f, 1.0f, 1.0f,
			-1.0f,  1.0f, -0.5f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f,
			-1.0f, -1.0f, -0.5f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f
		};	 
		
		float tmpQuad[] = {
			-1.0f,  1.0f,  0.0f, 1.0f,
			 1.0f,  1.0f,  1.0f, 1.0f,
			 1.0f, -1.0f,  1.0f, 0.0f,

			 1.0f, -1.0f,  1.0f, 0.0f,
			-1.0f, -1.0f,  0.0f, 0.0f,
			-1.0f,  1.0f,  0.0f, 1.0f
		};

		for (size_t i=0; i < APP_VERT_ARRAY_SIZE; i++)
		{
			vertices[i] = tmpVert[i];
			if (i < 24) quadVertices[i] = tmpQuad[i];
		}
	}

	float vertices[APP_VERT_ARRAY_SIZE];
	float quadVertices[24];
	GLuint vaoCube, vaoQuad;
	GLuint vboCube, vboQuad;
	GLuint tex;
	GLuint sceneVertexShader, sceneFragmentShader, shaderProgram;
	GLuint screenVertexShader, screenFragmentShader, screenProgram;
	GLint uniColor;
	GLint uniMod, uniView, uniProj;
	GLuint texColorBuffer, rboDepthStencil, frameBuffer;
	glm::mat4 model, view, proj;
	GLuint texKitten, texPuppy;

	std::chrono::time_point<std::chrono::high_resolution_clock> tStart, tNow;
	float time;

	GLuint loadTexture(std::string path)
	{
		GLuint texture;
		glGenTextures(1, &texture);
		
		int width, height;
		unsigned char* image;

		glBindTexture(GL_TEXTURE_2D, texture);		
		image =	SOIL_load_image(path.c_str(), &width, &height, 0, SOIL_LOAD_RGB);
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image);
		SOIL_free_image_data(image);
		
		glGenerateMipmap(GL_TEXTURE_2D);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR_MIPMAP_NEAREST);

		return texture;
	}

	void createShaderProgram(const std::string& vertSrc, const std::string& fragSrc,
				GLuint& vertexShader, GLuint& fragmentShader, GLuint& shaderProgram)
	{
		vertexShader = glCreateShader(GL_VERTEX_SHADER);
		std::string vShaderStr = load_shader(vertSrc);
		const char* vShaderChar = vShaderStr.c_str();
		glShaderSource(vertexShader, 1, &vShaderChar, NULL);
		glCompileShader(vertexShader);
		if (!checkShaderError(vertexShader)) return;

		fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
		std::string fShaderStr = load_shader(fragSrc);
		const char* fShaderChar = fShaderStr.c_str();
		glShaderSource(fragmentShader, 1, &fShaderChar, NULL);
		glCompileShader(fragmentShader);
		if (!checkShaderError(fragmentShader)) return;
		
		shaderProgram = glCreateProgram();
		glAttachShader(shaderProgram, vertexShader);
		glAttachShader(shaderProgram, fragmentShader);	
		glBindFragDataLocation(shaderProgram, 0, "outColor");
		glLinkProgram(shaderProgram);
	}

	virtual void startup() override
	{
		tStart = std::chrono::high_resolution_clock::now();

		model = glm::mat4(1.0f);
		model = glm::rotate(model, glm::radians(180.0f), glm::vec3(0.0f, 0.0f, 1.0f));

		view = glm::lookAt(glm::vec3(2.5f, 2.5f, 2.5f),
			   			   glm::vec3(0.0f, 0.0f, 0.0f),
			               glm::vec3(0.0f, 0.0f, 1.0f));

		proj = glm::perspective(glm::radians(45.0f),
			   				   (float)info.WindowWidth / (float)info.WindowHeight,
							   1.0f, 10.0f);

		glGenVertexArrays(1, &vaoCube);
		glGenVertexArrays(1, &vaoQuad);

		glGenBuffers(1, &vboCube);		
		glGenBuffers(1, &vboQuad);

		glBindBuffer(GL_ARRAY_BUFFER, vboCube);
		glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

		glBindBuffer(GL_ARRAY_BUFFER, vboQuad);
		glBufferData(GL_ARRAY_BUFFER, sizeof(quadVertices), quadVertices, GL_STATIC_DRAW);
		
		// SCENE SHADER PROGRAMS

		createShaderProgram("fram.vert", "fram.frag", sceneVertexShader, sceneFragmentShader, shaderProgram);
		glUseProgram(shaderProgram);

			glBindVertexArray(vaoCube);
			glBindBuffer(GL_ARRAY_BUFFER, vboCube);

			GLint posAttrib = glGetAttribLocation(shaderProgram, "position");
			glEnableVertexAttribArray(posAttrib);
			glVertexAttribPointer(posAttrib, 3, GL_FLOAT, GL_FALSE,
								  8*sizeof(float), 0);

			GLint colAttrib = glGetAttribLocation(shaderProgram, "color");
			glEnableVertexAttribArray(colAttrib);
			glVertexAttribPointer(colAttrib, 3, GL_FLOAT, GL_FALSE,
								  8*sizeof(float), (void*)(3*sizeof(float)));
			
			GLint texAttrib = glGetAttribLocation(shaderProgram, "texcoord");
			glEnableVertexAttribArray(texAttrib);
			glVertexAttribPointer(texAttrib, 2, GL_FLOAT, GL_FALSE,
								  8*sizeof(float), (void*)(6*sizeof(float)));


		createShaderProgram("framScreen.vert", "framScreen.frag", 
				screenVertexShader, screenFragmentShader, screenProgram);
		glUseProgram(screenProgram);

			glBindVertexArray(vaoQuad);
			glBindBuffer(GL_ARRAY_BUFFER, vboQuad);
			
			GLint posScreenAttrib = glGetAttribLocation(screenProgram, "position");
			glEnableVertexAttribArray(posScreenAttrib);
			glVertexAttribPointer(posScreenAttrib, 2, GL_FLOAT, GL_FALSE,
								  4*sizeof(float), 0);

			GLint texScreenAttrib = glGetAttribLocation(screenProgram, "texcoord");
			glEnableVertexAttribArray(texScreenAttrib);
			glVertexAttribPointer(texScreenAttrib, 2, GL_FLOAT, GL_FALSE,
								  4*sizeof(float), (void*)(2*sizeof(float)));


		glUseProgram(shaderProgram);

			texKitten = loadTexture("sample.png");
			texPuppy = loadTexture("sample2.png");
			glUniform1i(glGetUniformLocation(shaderProgram, "texKitten"), 0);
			glUniform1i(glGetUniformLocation(shaderProgram, "texPuppy"), 1);

			uniMod = glGetUniformLocation(shaderProgram, "model");
			glUniformMatrix4fv(uniMod, 1, GL_FALSE, glm::value_ptr(model));

			uniView = glGetUniformLocation(shaderProgram, "view");
			glUniformMatrix4fv(uniView, 1, GL_FALSE, glm::value_ptr(view));

			uniProj = glGetUniformLocation(shaderProgram, "proj");
			glUniformMatrix4fv(uniProj, 1, GL_FALSE, glm::value_ptr(proj));

			uniColor = glGetUniformLocation(shaderProgram, "ColorFactor"); 


		glUseProgram(screenProgram);

			glUniform1i(glGetUniformLocation(screenProgram, "texFrameBuffer"), 0);

			glGenFramebuffers(1, &frameBuffer);
			glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer);

			glGenTextures(1, &texColorBuffer);
			glBindTexture(GL_TEXTURE_2D, texColorBuffer);
			glTexImage2D(
				GL_TEXTURE_2D, 0, GL_RGB, info.WindowWidth, info.WindowHeight,
				0, GL_RGB, GL_UNSIGNED_BYTE, NULL
				);
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
			glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
			glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texColorBuffer, 0);

			glGenRenderbuffers(1, &rboDepthStencil);
			glBindRenderbuffer(GL_RENDERBUFFER, rboDepthStencil);
			glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, info.WindowWidth, info.WindowHeight);
			glFramebufferRenderbuffer(
				GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rboDepthStencil
				);
	}

	
	void render(double currentTime) override
	{
		// Draw cube to framebuffer
		//glBindFramebuffer(GL_FRAMEBUFFER, 0);
		glBindFramebuffer(GL_FRAMEBUFFER, frameBuffer);
		glBindVertexArray(vaoCube);
		glEnable(GL_DEPTH_TEST);
		glUseProgram(shaderProgram);
		
		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, texKitten);
		glActiveTexture(GL_TEXTURE1);
		glBindTexture(GL_TEXTURE_2D, texPuppy);

		glClearColor(0.0f, 1.0f, 1.0f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		tNow = std::chrono::high_resolution_clock::now();
		time = std::chrono::duration_cast<std::chrono::duration<float>>(tNow - tStart).count();

		model = glm::mat4(1.0f);
		model = glm::rotate(model, time*glm::radians(180.0f), glm::vec3(0.0f, 0.0f, 1.0f));
		glUniformMatrix4fv(uniMod, 1, GL_FALSE, glm::value_ptr(model));
		glUniform3f(uniColor, 1.0f, 1.0f, 1.0f);

		glDrawArrays(GL_TRIANGLES, 0, 36);

		glEnable(GL_STENCIL_TEST);
			glStencilFunc(GL_ALWAYS, 1, 0xFF);
			glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);
			glStencilMask(0xFF);
			glDepthMask(GL_FALSE);
			glClear(GL_STENCIL_BUFFER_BIT);

			glDrawArrays(GL_TRIANGLES, 36, 6);
			
			glStencilFunc(GL_EQUAL, 1, 0xFF);
			glStencilMask(0x00);
			glDepthMask(GL_TRUE);

			model = glm::scale(glm::translate(model, glm::vec3(0, 0, -1)), glm::vec3(1, 1, -1));
			glUniformMatrix4fv(uniMod, 1, GL_FALSE, glm::value_ptr(model));
			glUniform3f(uniColor, 0.3f, 0.3f, 0.3f);
			glDrawArrays(GL_TRIANGLES, 0, 36);
		glDisable(GL_STENCIL_TEST);

		glBindFramebuffer(GL_FRAMEBUFFER, 0);
		glClearColor(1.0f, 0.0f, 1.0f, 1.0f);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

		glBindVertexArray(vaoQuad);
		glDisable(GL_DEPTH_TEST);
		glUseProgram(screenProgram);

		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, texColorBuffer);

		glDrawArrays(GL_TRIANGLES, 0, 6);
	}

	bool checkShaderError(GLuint shader)
	{
		GLint status;
		glGetShaderiv(shader, GL_COMPILE_STATUS, &status);
		if (!status)
		{
			char buffer[512];
			glGetShaderInfoLog(sceneVertexShader, 512, NULL, buffer);
			for(size_t i = 0; buffer[i] != '\0'; i++)
			{
				if (i >= 512) break;
				std::cout << buffer[i];
    		}
			std::cerr << std::endl;
		}
		return status;
	}

	std::string load_shader(const std::string& fileName) const
	{
		std::ifstream file;
		file.open(fileName);

		std::string output, line;

		if (file.is_open())
			while (file.good())
			{
				getline(file, line);
				output.append(line + "\n");
			}
		else
			std::cerr << "Unable to load shader from file " << fileName << std::endl;

		return output;
	}
};

int main()
{
	AppVertices* app = new AppVertices();
	app->run();
	return 0;
}
