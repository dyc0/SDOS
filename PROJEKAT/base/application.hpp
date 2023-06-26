#ifndef APPLICATION_HPP
#define APPLICATION_HPP

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <cmath>
#include <iostream>
#include <string.h>
#include <string>

class Application
{
	
	public:
	// Think of a way to make this a singleton
	//static Application* CreateApp()
	//{
	//	if (!Application::app)
	//		app = new Application();
	//	else std::cerr << "WARNING: Only one instance of application can be created within a project." << std::endl;
	//	return app;
	//}
	Application()
	{
		info.MajorVersion = 3;
		info.MinorVersion = 2;
		info.title = "OpenGL";
		info.WindowWidth = 1280;
		info.WindowHeight = 720;
		info.flags.all = false;
		info.flags.debug = true;
		app = this;
	}
	virtual ~Application() { };
	static Application* app;


	virtual void run()
	{ 
		if (!glfwInit())
		{
			std::cerr << "ERROR: Unable to initialize GLFW." << std::endl;
			return;
		}

		glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
		glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
		glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
		glfwWindowHint(GLFW_STENCIL_BITS, 8);

		glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

		if (info.flags.debug) glfwWindowHint(GLFW_OPENGL_DEBUG_CONTEXT, GL_TRUE);
		if (info.flags.robust) glfwWindowHint(GLFW_CONTEXT_ROBUSTNESS, GLFW_LOSE_CONTEXT_ON_RESET);
		
		glfwWindowHint(GLFW_SAMPLES, info.samples);
		glfwWindowHint(GLFW_STEREO, info.flags.stereo ? GL_TRUE : GL_FALSE);

		window = glfwCreateWindow(info.WindowWidth, info.WindowHeight, info.title.c_str(), nullptr, nullptr);
		if (!window)
		{
			std::cerr << "ERROR: Unable to create a window." << std::endl;
			return;
		}
		glfwMakeContextCurrent(window);

		glfwSetWindowSizeCallback(window, glfwWindowSizeCallback);
		glfwSetKeyCallback(window, glfwKeyCallback);
		glfwSetMouseButtonCallback(window, glfwMouseButtonCallback);
		glfwSetCursorPosCallback(window, glfwCursorPosCallback);
		glfwSetScrollCallback(window, glfwScrollCallback);

		glewInit();
		startup();
		while(!glfwWindowShouldClose(window))
		{
			render(glfwGetTime());

			glfwSwapBuffers(window);
			glfwPollEvents();
		}
		shutdown();
		glfwDestroyWindow(window);

		glfwTerminate();
	}
	


	public:
	struct APPINFO
	{
		std::string title;
		int WindowWidth;
		int WindowHeight;
		int MajorVersion;
		int MinorVersion;
		int samples;
		union
		{
			struct
			{
				unsigned int fullscreen	: 1;
				unsigned int vsync		: 1;
				unsigned int cursor		: 1;
				unsigned int stereo		: 1;
				unsigned int debug		: 1;
				unsigned int robust		: 1;
			};
			unsigned int 	 all;
		} flags;
	};

	protected:
	APPINFO info;
	GLFWwindow* window;


	public:
	virtual void init(int width, int height, std::string title)
	{
		info.WindowWidth = width;
		info.WindowHeight = height;
		info.title = title;
	}
	virtual void startup() { }
	virtual void render(double currentTime) { }
	virtual void shutdown() { }

	void setWindowTitle(const std::string& title)
	{
		info.title = title;
		glfwSetWindowTitle(window, title.c_str());
	}
	void getMousePosition(int&x, int& y)
	{
		double dx, dy;
		glfwGetCursorPos(window, &dx, &dy);
		
		x = std::floor(dx);
		y = std::floor(dy);
	}

	virtual void windowSizeCallback(GLFWwindow* window, int width, int height) { strTest("Size"); }
	virtual void keyCallback(int key, int scancode, int action, int mods) { strTest("Keypress"); }
	virtual void cursorPosCallback(GLFWwindow* window, double xpos, double ypos) { strTest("Cursor"); }
	virtual void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods) { strTest("Click"); }
	virtual void scrollCallback(GLFWwindow* window, double xoffset, double yoffset) { strTest("Scroll"); }

	protected:
	static void glfwWindowSizeCallback(GLFWwindow* window, int width, int height)
	{ app->windowSizeCallback(window, width, height); }

	static void glfwKeyCallback(GLFWwindow* window, int key, int scancode, int action, int mods)
	{ app->keyCallback(key, scancode, action, mods); }

	static void glfwCursorPosCallback(GLFWwindow* window, double xpos, double ypos)
	{ app->cursorPosCallback(window, xpos, ypos); }

	static void glfwMouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
	{ app->mouseButtonCallback(window, button, action, mods); }

	static void glfwScrollCallback(GLFWwindow* window, double xoffset, double yoffset)
	{ app->scrollCallback(window, xoffset, yoffset); }

	private:
	void strTest(std::string name)
	{ if(info.flags.debug) std::cout << name << std::endl; }

};

Application* Application::app = nullptr;

#endif
