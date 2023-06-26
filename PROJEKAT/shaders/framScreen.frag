#version 150 core

in vec2 Texcoord;

out vec4 outColor;

uniform sampler2D texFrameBuffer;


void main()
{
	vec4 top         = texture(texFrameBuffer, vec2(Texcoord.x, Texcoord.y + 1.0 / 720.0));
	vec4 bottom      = texture(texFrameBuffer, vec2(Texcoord.x, Texcoord.y - 1.0 / 720.0));
	vec4 left        = texture(texFrameBuffer, vec2(Texcoord.x - 1.0 / 1280.0, Texcoord.y));
	vec4 right       = texture(texFrameBuffer, vec2(Texcoord.x + 1.0 / 1280.0, Texcoord.y));
	vec4 topLeft     = texture(texFrameBuffer, vec2(Texcoord.x - 1.0 / 1280.0, Texcoord.y + 1.0 / 720.0));
	vec4 topRight    = texture(texFrameBuffer, vec2(Texcoord.x + 1.0 / 1280.0, Texcoord.y + 1.0 / 720.0));
	vec4 bottomLeft  = texture(texFrameBuffer, vec2(Texcoord.x - 1.0 / 1280.0, Texcoord.y - 1.0 / 720.0));
	vec4 bottomRight = texture(texFrameBuffer, vec2(Texcoord.x + 1.0 / 1280.0, Texcoord.y - 1.0 / 720.0));
	vec4 sx = -topLeft - 2 * left - bottomLeft + topRight   + 2 * right  + bottomRight;
	vec4 sy = -topLeft - 2 * top  - topRight   + bottomLeft + 2 * bottom + bottomRight;
	vec4 sobel = sqrt(sx * sx + sy * sy);
	outColor = sobel;
}
