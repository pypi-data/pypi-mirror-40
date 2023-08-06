#define BUFFER_OFFSET(i) ((char*)NULL + (i))

#ifdef HAS_FRAMEWORK_GLEW
#  include <GLEW/glew.h>
#else
#  include <GL/glew.h>
#endif
