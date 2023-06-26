#version 150 core

in vec2 Texcoord;

out vec4 outColor;

uniform sampler2D texFrameBuffer;

const float blurSizeH = 1.0 / 1280.0;
const float blurSizeV = 1.0 / 720.0;

void main()
{
	vec4 sum = vec4(0.0);
	for (int x = -4; x <= 4; x++)
		for (int y = -4; y <= 4; y++)
			sum += texture(
				texFrameBuffer,
				vec2(Texcoord.x + x*blurSizeH, Texcoord.y + y*blurSizeV)
			) / 81.0;
	outColor = sum; 
}
