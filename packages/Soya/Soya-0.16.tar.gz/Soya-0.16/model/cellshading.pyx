# -*- indent-tabs-mode: t -*-

# Soya 3D
# Copyright (C) 2004 Jean-Baptiste LAMY -- jiba@tuxfamily.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


cdef class _CellShadingModel(_SimpleModel):
	#cdef _Material _shader
	#cdef float     _outline_color[4]
	#cdef float     _outline_width, _outline_attenuation
	
	cdef _Model _create_deformed_data(self):
		cdef _CellShadingModel data
		data = _SimpleModel._create_deformed_data(self)
		data._shader              = self._shader
		data._outline_width       = self._outline_width
		data._outline_attenuation = self._outline_attenuation
		memcpy(&data._outline_color[0], &self._outline_color[0], 4 * sizeof(float))
		return data
		
	property shader:
		def __get__(self):
			return self._shader
		
	cdef __getcstate__(self):
		cdef Chunk* chunk
		chunk = get_chunk()
		chunk_add_float_endian_safe (chunk, self._outline_width)
		chunk_add_float_endian_safe (chunk, self._outline_attenuation)
		chunk_add_floats_endian_safe(chunk, self._outline_color, 4)
		return _SimpleModel.__getcstate__(self), drop_chunk_to_string(chunk), self._shader
		
	cdef void __setcstate__(self, cstate):
		_SimpleModel.__setcstate_data__(self, cstate[0])
		
		cdef Chunk* chunk
		chunk = string_to_chunk(cstate[1])
		chunk_get_float_endian_safe (chunk, &self._outline_width)
		chunk_get_float_endian_safe (chunk, &self._outline_attenuation)
		chunk_get_floats_endian_safe(chunk,  self._outline_color, 4)
		drop_chunk(chunk)
		
		self._shader = cstate[2]
		
		# Build the display list data, but don't create the corresponding OpenGL display list
		self._build_display_list()
		
	cdef void _build_cellshading(self, _Material shader, outline_color, float outline_width, float outline_attenuation):
		cdef int i
		
		self._shader              = shader
		self._outline_width       = outline_width
		self._outline_attenuation = outline_attenuation
		for i from 0 <= i < 4: self._outline_color[i] = outline_color[i]
		
	cdef void _batch(self, _Body body):
		if body._option & HIDDEN: return
		
		if quality == QUALITY_LOW:
			_SimpleModel._batch(self, body)
			return
		
		#cdef Frustum* frustum
		#frustum = renderer._frustum(body)
		#if (self._option & MODEL_HAS_SPHERE) and (sphere_in_frustum(frustum, self._sphere) == 0): return
		cdef float sphere[4]
		if self._option & MODEL_HAS_SPHERE:
			sphere_by_matrix_copy(sphere, self._sphere, body._root_matrix())
			if sphere_in_frustum(renderer.root_frustum, sphere) == 0: return
		
		if self._display_lists.nb_opaque_list != 0: renderer._batch(renderer.opaque, body._data, body, NULL)
		if self._display_lists.nb_alpha_list  != 0: renderer._batch(renderer.alpha , body._data, body, NULL)
		
		# For outline
		#if self._outline_width > 0.0: renderer._batch(renderer.secondpass, body._data, body, 0) ???? why 0 and not -1 here ???
		if self._outline_width > 0.0: renderer._batch(renderer.secondpass, body._data, body, NULL)

				
		
	cdef void _render(self, _Body body):
		if quality == QUALITY_LOW:
			_SimpleModel._render(self, body)
			return
		
		cdef int          i, start, end
		cdef int*         face_id
		cdef Frustum*     frustum
		cdef Chunk*       chunk
		cdef float*       shades
		cdef _Material    material
		cdef DisplayList* display_list
		
		if renderer.state == RENDERER_STATE_SECONDPASS:
			frustum = renderer._frustum(body)
			self._render_outline(frustum)
		else:
			if body._option & LEFTHANDED: glFrontFace(GL_CW)
			model_option_activate(self._option)
			
			chunk = get_chunk()
			chunk_register(chunk, self._nb_vnormals * sizeof(float))
			shades = <float*> chunk.content
			self._prepare_cellshading(body, shades)
			
			if renderer.state == RENDERER_STATE_OPAQUE:
				start = 0
				end   = self._display_lists.nb_opaque_list
			else: # Alpha
				start = self._display_lists.nb_opaque_list
				end   = start + self._display_lists.nb_alpha_list
				
			# Activate shader texture
			glActiveTextureARB(GL_TEXTURE1)
			
			if self._shader._id == 0:	self._shader._init_texture()
			
			glEnable          (GL_TEXTURE_2D)
			glTexEnvi         (GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
			glBindTexture     (GL_TEXTURE_2D, self._shader._id)
			glActiveTextureARB(GL_TEXTURE0)
			glDisable         (GL_LIGHTING)
			
			for i from start <= i < end:
				display_list = self._display_lists.display_lists + i
				
				material = <_Material> (<void*> (display_list.material_id))
				material._activate()
				
				face_option_activate(display_list.option)
				
				face_id = display_list.faces_id
				if   display_list.option & FACE_TRIANGLE:
					glBegin(GL_TRIANGLES)
					while face_id[0] != -1:
						self._render_triangle_cellshading(self._faces + face_id[0], shades)
						face_id = face_id + 1
						
				elif display_list.option & FACE_QUAD:
					glBegin(GL_QUADS)
					while face_id[0] != -1:
						self._render_quad_cellshading(self._faces + face_id[0], shades)
						face_id = face_id + 1
						
				glEnd()
				
				face_option_inactivate(display_list.option)
			
			# Unactivate shader texture
			glActiveTextureARB(GL_TEXTURE1)
			glDisable         (GL_TEXTURE_2D)
			glActiveTextureARB(GL_TEXTURE0)
			glEnable          (GL_LIGHTING)
			
			
			drop_chunk(chunk)
			model_option_inactivate(self._option)
			if body._option & LEFTHANDED: glFrontFace(GL_CCW)
			
			
	cdef void _render_outline(self, Frustum* frustum):
		cdef int        i, j, k, ns, nb
		cdef float      d
		cdef float*     plane
		cdef ModelFace* face, neighbor_face
		
		# Compute outline width, which depends on distance to camera
		d = sphere_distance_point(self._sphere, frustum.position) * self._outline_attenuation
		if d < 1.0: d = self._outline_width
		else:
			d = self._outline_width / d
			if d < 2.0: d = 2.0
			
		_DEFAULT_MATERIAL._activate()
		glLineWidth(d)
		glColor4fv (self._outline_color)
		glEnable   (GL_BLEND)
		glEnable   (GL_LINE_SMOOTH)
		glDisable  (GL_LIGHTING)
		glDepthFunc(GL_LEQUAL)
		
		# mark faces as either front or back
		for i from 0 <= i < self._nb_faces:
			face = self._faces + i
			plane = self._values + face.normal
			if plane[0] * frustum.position[0] + plane[1] * frustum.position[1] + plane[2] * frustum.position[2] + plane[3] > 0.0:
				face.option = (face.option & ~FACE_BACK ) | FACE_FRONT
			else:
				face.option = (face.option & ~FACE_FRONT) | FACE_BACK
				
				



		cdef Chunk* chunk
		chunk = get_chunk()
		chunk_register(chunk, self._nb_coords * sizeof(int))
		cdef int* vertex_used
		vertex_used = <int*> (chunk.content)
		for i from 0 <= i < self._nb_coords: vertex_used[i] = -1
		
		
		# find and draw edges   
		glBegin(GL_LINES)
		for i from 0 <= i < self._nb_faces:
			face = self._faces + i
			if face.option & FACE_ALPHA: continue
			
			if face.option & FACE_QUAD: nb = 4
			else:                       nb = 3
			
			if face.option & FACE_SMOOTH_LIT:
				if face.option & FACE_DOUBLE_SIDED:
					for j from 0 <= j < nb:
						k = self._neighbors[4 * i + j]
						if k == -1: # No neighbor, but double-sided face => the face is its own neighbor
							vertex_used[self._vertex_coords[face.v[j]] / 3] = 1

							# draw edge between vertices j and j + 1
							glVertex3fv(self._coords + self._vertex_coords[face.v[j]])
							if j < nb - 1: glVertex3fv(self._coords + self._vertex_coords[face.v[j + 1]])
							else:          glVertex3fv(self._coords + self._vertex_coords[face.v[    0]])
								
						else:
							ns = self._neighbors_side[4 * i + j]
							neighbor_face = self._faces[k]
							if (
								(ns == -1) and (((face.option & FACE_FRONT) and (neighbor_face.option & FACE_BACK )) or ((face.option & FACE_BACK) and (neighbor_face.option & FACE_FRONT)))
									) or (
								(ns ==  1) and (((face.option & FACE_FRONT) and (neighbor_face.option & FACE_FRONT)) or ((face.option & FACE_BACK) and (neighbor_face.option & FACE_BACK)))
								):
								vertex_used[self._vertex_coords[face.v[j]] / 3] = 1
								
								# draw edge between vertices j and j + 1
								glVertex3fv(self._coords + self._vertex_coords[face.v[j]])
								if j < nb - 1: glVertex3fv(self._coords + self._vertex_coords[face.v[j + 1]])
								else:          glVertex3fv(self._coords + self._vertex_coords[face.v[    0]])
								
				else:
					if face.option & FACE_FRONT:
						# test if neighbors are back
						for j from 0 <= j < nb:
							k = self._neighbors[4 * i + j]
							if (k == -1) or (self._faces[k].option & FACE_BACK):
								vertex_used[self._vertex_coords[face.v[j]] / 3] = 1
								
								# draw edge between vertices j and j + 1
								glVertex3fv(self._coords + self._vertex_coords[face.v[j]])
								if j < nb - 1: glVertex3fv(self._coords + self._vertex_coords[face.v[j + 1]])
								else:          glVertex3fv(self._coords + self._vertex_coords[face.v[    0]])
								
			else: # Not smoothlit
				if (face.option & FACE_FRONT) or (face.option & FACE_DOUBLE_SIDED):
					for j from 0 <= j < nb:
						# draw edge between vertices j and j + 1
						glVertex3fv(self._coords + self._vertex_coords[face.v[j]])
						if j < nb - 1: glVertex3fv(self._coords + self._vertex_coords[face.v[j + 1]])
						else:          glVertex3fv(self._coords + self._vertex_coords[face.v[    0]])
						
		glEnd()
		
		glPointSize(d / 2)
				
		glBegin(GL_POINTS)
		for i from 0 <= i < self._nb_coords:
			if vertex_used[i] == 1: glVertex3fv(self._coords + i * 3)
		glEnd()
		
		
		drop_chunk(chunk)
		
		glLineWidth(1.0) # Reset to default
		glPointSize(1.0) # Reset to default
		glEnable   (GL_LIGHTING)
		glDepthFunc(GL_LESS)
		glColor4fv (white)


	cdef float _vertex_compute_cellshading(self, float* coord, float* normal, lights, float shade):
		cdef _Light light
		cdef float  ptr[3]
		cdef float  tmp
		cdef int    i
		
		for light in lights:
			if light._w == 0.0: # directional light
				tmp = -vector_dot_product(normal, light._data)
			else: # positional light
				ptr[0] = light._data[0] - coord[0]
				ptr[1] = light._data[1] - coord[1]
				ptr[2] = light._data[2] - coord[2]
				vector_normalize(ptr)
				tmp = vector_dot_product(normal, ptr)
				
			shade = shade + tmp
			
		return shade

	cdef void _prepare_cellshading_shades(self, float* shades, lights):
		cdef _Light light
		cdef float* ptr1, *ptr2
		cdef float  v[3]
		cdef float  tmp
		cdef int    i, j, k
		
		for light in lights:
			ptr1 = self._vnormals
			if light._w == 0.0: # directional light
				for j from 0 <= j < self._nb_vnormals:
					tmp = -vector_dot_product(ptr1, light._data)
					shades[j] = shades[j] + tmp
					ptr1 = ptr1 + 3
					
			else: # positional light
				ptr2 = self._coords
				for j from 0 <= j < self._nb_vnormals:
					v[0] = light._data[0] - ptr2[0]
					v[1] = light._data[1] - ptr2[1]
					v[2] = light._data[2] - ptr2[2]
					vector_normalize(v)
					tmp = vector_dot_product(ptr1, v)
					shades[j] = shades[j] + tmp
					ptr1 = ptr1 + 3
					ptr2 = ptr2 + 3
					
	cdef void _prepare_cellshading(self, CoordSyst coordsyst, float* shades):
		cdef int    n
		cdef _Light light
		for light in renderer.top_lights:             light._cast_into(coordsyst)
		for light in renderer.current_context.lights: light._cast_into(coordsyst)
		
		if self._nb_vnormals > 0: # Else the shades are computed at the vertex rendering time, since the shades are not shared (all (coord,normal) couples are different)
			for n from 0 <= n < self._nb_vnormals: shades[n] = 0.5
			self._prepare_cellshading_shades(shades, renderer.top_lights)
			self._prepare_cellshading_shades(shades, renderer.current_context.lights)
			
			# clip shade texcoord values
			for n from 0 <= n < self._nb_vnormals:
				# do not clip with interval [0, 1] because smooth magnification of texture
				# causes visual bugs
				if   shades[n] > 0.95: shades[n] = 0.95
				elif shades[n] < 0.05: shades[n] = 0.05


	cdef void _render_triangle_cellshading(self, ModelFace* face, float* shades):
		if face.option & FACE_SMOOTH_LIT:
			self._render_vertex_cellshading_smoothlit(face.v[0], face.option, shades)
			self._render_vertex_cellshading_smoothlit(face.v[1], face.option, shades)
			self._render_vertex_cellshading_smoothlit(face.v[2], face.option, shades)
		else:
			glNormal3fv(self._values + face.normal)
			self._render_vertex_cellshading(face.v[0], face.option, self._values + face.normal)
			self._render_vertex_cellshading(face.v[1], face.option, self._values + face.normal)
			self._render_vertex_cellshading(face.v[2], face.option, self._values + face.normal)

	cdef void _render_quad_cellshading(self, ModelFace* face, float* shades):
		if face.option & FACE_SMOOTH_LIT:
			self._render_vertex_cellshading_smoothlit(face.v[0], face.option, shades)
			self._render_vertex_cellshading_smoothlit(face.v[1], face.option, shades)
			self._render_vertex_cellshading_smoothlit(face.v[2], face.option, shades)
			self._render_vertex_cellshading_smoothlit(face.v[3], face.option, shades)
		else:
			glNormal3fv(self._values + face.normal)
			self._render_vertex_cellshading(face.v[0], face.option, self._values + face.normal)
			self._render_vertex_cellshading(face.v[1], face.option, self._values + face.normal)
			self._render_vertex_cellshading(face.v[2], face.option, self._values + face.normal)
			self._render_vertex_cellshading(face.v[3], face.option, self._values + face.normal)


	# XXX face_option arg is useless
	cdef void _render_vertex_cellshading_smoothlit (self, int index, int face_option, float* shades):
		cdef int    n
		cdef float* coord
		cdef float  shade
		n     = self._vertex_coords[index]
		coord = self._coords + n
		
		if face_option & FACE_NON_LIT:
			shade = 0.5 # Medium shade
		else:
			shade = shades[n / 3]
		
		if self._option & MODEL_DIFFUSES : glColor4fv   (self._colors   + self._vertex_diffuses [index])
		if self._option & MODEL_EMISSIVES: glMaterialfv (GL_FRONT_AND_BACK, GL_EMISSION, self._colors + self._vertex_emissives[index]) # XXX use glColorMaterial when emissive color but no diffuse ?
		if self._option & MODEL_TEXCOORDS:
			glMultiTexCoord2fvARB(GL_TEXTURE0, self._values + self._vertex_texcoords[index])
			glMultiTexCoord2fARB (GL_TEXTURE1, shade, shade)
		else: glTexCoord2f(shade, shade)
		
		glNormal3fv(self._vnormals + n)
		glVertex3fv(coord)
		
	# XXX face_option arg is useless
	cdef void _render_vertex_cellshading(self, int index, int face_option, float* fnormal):
		cdef float* coord
		cdef float  shade
		coord = self._coords + self._vertex_coords[index]
		
		if face_option & FACE_NON_LIT:
			shade = 0.5 # Medium value
		else:
			shade = self._vertex_compute_cellshading(coord, fnormal, renderer.top_lights, 0.5)
			shade = self._vertex_compute_cellshading(coord, fnormal, renderer.current_context.lights, shade)
			if   shade < 0.05: shade = 0.05
			elif shade > 0.95: shade = 0.95
			
		if self._option & MODEL_DIFFUSES : glColor4fv  (self._colors   + self._vertex_diffuses [index])
		if self._option & MODEL_EMISSIVES: glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, self._colors + self._vertex_emissives[index]) # XXX use glColorMaterial when emissive color but no diffuse ?
		if self._option & MODEL_TEXCOORDS:
			glMultiTexCoord2fvARB(GL_TEXTURE0, self._values + self._vertex_texcoords[index])
			glMultiTexCoord2fARB (GL_TEXTURE1, shade, shade)
		else: glTexCoord2f(shade, shade)
		
		glVertex3fv(coord)
		
	







cdef GLuint _outline_buffer
_outline_buffer = 0

cdef void _init_outline_buffer():
	glGenBuffers(1, &_outline_buffer)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _outline_buffer)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, 64 * sizeof(int), NULL, GL_DYNAMIC_DRAW)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)




cdef class _CellShadingVertexBufferedModel(_VertexBufferedModel):
	#cdef _Material _shader
	#cdef float     _outline_color[4]
	#cdef float     _outline_width, _outline_attenuation
	
#	#cdef GLuint    _outline_buffer
	
	def __init__(self, _World world, float angle, int option, lights):
		_VertexBufferedModel.__init__(self, world, angle, option | MODEL_TEXCOORDS2, lights)
		
#	def __dealloc__(self):
#		_VertexBufferedModel.__dealloc__(self)
#		if self._option & MODEL_INITED:
#			if self._outline_width > 0.0: glDeleteBuffers(1, &self._outline_buffer)
			
	property shader:
		def __get__(self):
			return self._shader
		
	cdef __getcstate__(self):
		cdef Chunk* chunk
		chunk = get_chunk()
		chunk_add_float_endian_safe (chunk, self._outline_width)
		chunk_add_float_endian_safe (chunk, self._outline_attenuation)
		chunk_add_floats_endian_safe(chunk, self._outline_color, 4)
		return _VertexBufferedModel.__getcstate__(self), drop_chunk_to_string(chunk), self._shader
		
	cdef void __setcstate__(self, cstate):
		_VertexBufferedModel.__setcstate_data__(self, cstate[0])
		
		cdef Chunk* chunk
		chunk = string_to_chunk(cstate[1])
		chunk_get_float_endian_safe (chunk, &self._outline_width)
		chunk_get_float_endian_safe (chunk, &self._outline_attenuation)
		chunk_get_floats_endian_safe(chunk,  self._outline_color, 4)
		drop_chunk(chunk)
		self._shader = cstate[2]
		
	cdef void _build_cellshading(self, _Material shader, outline_color, float outline_width, float outline_attenuation):
		cdef int i
		self._shader              = shader
		self._outline_width       = outline_width
		self._outline_attenuation = outline_attenuation
		for i from 0 <= i < 4: self._outline_color[i] = outline_color[i]
		
		
	cdef void _init_vertex_buffers(self):
		_VertexBufferedModel._init_vertex_buffers(self)
		
		if self._outline_width > 0.0:
			if _outline_buffer == 0: _init_outline_buffer()
#			glGenBuffers(1, &self._outline_buffer)
#			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._outline_buffer)
#			glBufferData(GL_ELEMENT_ARRAY_BUFFER, 10, NULL, GL_DYNAMIC_DRAW)
#			glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		
		check_gl_error()
		
	cdef void _batch(self, _Body body):
		if body._option & HIDDEN: return
		
		if quality == QUALITY_LOW:
			_VertexBufferedModel._batch(self, body)
			return
		
		cdef float sphere[4]
		if self._option & MODEL_HAS_SPHERE:
			sphere_by_matrix_copy(sphere, self._sphere, body._root_matrix())
			if sphere_in_frustum(renderer.root_frustum, sphere) == 0: return
			
		if self._option & MODEL_HAS_OPAQUE: renderer._batch(renderer.opaque, self, body, NULL)
		if self._option & MODEL_HAS_ALPHA : renderer._batch(renderer.alpha , self, body, NULL)
		
		# For outline
		if self._outline_width > 0.0: renderer._batch(renderer.secondpass, body._data, body, NULL)
				
		
	cdef void _render(self, _Body body):
		#if quality == QUALITY_LOW:
		#	_VertexBufferedModel._render(self, body)
		#	return
		cdef Frustum *frustum
                
		if renderer.state == RENDERER_STATE_SECONDPASS:
			frustum = renderer._frustum(body)
			self._render_outline(frustum)
			
		else:
			if not(self._option & MODEL_INITED): self._init_vertex_buffers()
			
			# Set texture coordinates 2
			self._compute_texcoords2(body)
			glBindBuffer(GL_ARRAY_BUFFER, self._texcoords2_buffer)
			glBufferSubData(GL_ARRAY_BUFFER, 0, 2 * self._nb_vertices * sizeof(float), self._texcoords2)
			glBindBuffer(GL_ARRAY_BUFFER, 0)
			
			# Activate shader texture
			glActiveTextureARB(GL_TEXTURE1)
			
			if self._shader._id == 0:	self._shader._init_texture()
			
			glEnable          (GL_TEXTURE_2D)
			glTexEnvi         (GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
			glBindTexture     (GL_TEXTURE_2D, self._shader._id)
			glActiveTextureARB(GL_TEXTURE0)
			glDisable         (GL_LIGHTING)
			
			_VertexBufferedModel._render(self, body)
			
			# Unactivate shader texture
			glActiveTextureARB(GL_TEXTURE1)
			glDisable         (GL_TEXTURE_2D)
			glActiveTextureARB(GL_TEXTURE0)
			glEnable          (GL_LIGHTING)
			
			
	cdef void _compute_texcoords2(self, CoordSyst coordsyst):
		cdef float* texcoords2
		cdef int    i
		cdef _Light light
		
		texcoords2 = self._texcoords2
		for i from 0 <= i < self._nb_vertices: texcoords2[2 * i] = 0.5
		
		for light in renderer.top_lights:             self._compute_texcoords2_for_light(coordsyst, light)
		for light in renderer.current_context.lights: self._compute_texcoords2_for_light(coordsyst, light)
		
		# clip shade texcoord values
		for i from 0 <= i < self._nb_vertices:
			texcoords2 = self._texcoords2 + 2 * i
			if   texcoords2[0] > 0.95: texcoords2[0] = 0.95 # do not clip with interval [0, 1] because smooth magnification of texture
			elif texcoords2[0] < 0.05: texcoords2[0] = 0.05 # causes visual bugs
			texcoords2[1] = texcoords2[0]
			
			
	cdef void _compute_texcoords2_for_light(self, CoordSyst coordsyst, _Light light):
		cdef float* vnormals, *coords, *texcoords2
		cdef float  v[3]
		cdef int    j
		
		light._cast_into(coordsyst)
		
		vnormals   = self._vnormals
		texcoords2 = self._texcoords2
		if light._w == 0.0: # directional light
			for j from 0 <= j < self._nb_vertices:
				texcoords2[0] = texcoords2[0] - vector_dot_product(vnormals, light._data)
				vnormals   = vnormals   + 3
				texcoords2 = texcoords2 + 2
				
		else: # positional light
			coords = self._coords
			for j from 0 <= j < self._nb_vertices:
				v[0] = light._data[0] - coords[0]
				v[1] = light._data[1] - coords[1]
				v[2] = light._data[2] - coords[2]
				vector_normalize(v)
				texcoords2[0] = texcoords2[0] + vector_dot_product(vnormals, v)
				coords     = coords     + 3
				vnormals   = vnormals   + 3
				texcoords2 = texcoords2 + 2


			
	cdef void _render_outline(self, Frustum* frustum):
		cdef int                     i, j, k, ns, nb, buf
		#cdef int*                    edges
		cdef float                   d
		cdef _VertexBufferModelFace* face, neighbor_face
		cdef int                    edges[64]
		
		# Compute outline width, which depends on distance to camera
		d = sphere_distance_point(self._sphere, frustum.position) * self._outline_attenuation
		if d < 1.0: d = self._outline_width
		else:
			d = self._outline_width / d
			if d < 2.0: d = 2.0
			
		# mark faces as either front or back
		for i from 0 <= i < self._nb_faces:
			face  = self._faces + i
			if face.normal[0] * frustum.position[0] + face.normal[1] * frustum.position[1] + face.normal[2] * frustum.position[2] + face.normal[3] > 0.0: face.option = (face.option & ~FACE_BACK ) | FACE_FRONT
			else:                                                                                                                                         face.option = (face.option & ~FACE_FRONT) | FACE_BACK


		_DEFAULT_MATERIAL._activate()
		glLineWidth(d)
		glColor4fv (self._outline_color)
		glEnable   (GL_BLEND)
		glEnable   (GL_LINE_SMOOTH)
		glDisable  (GL_LIGHTING)
		glDepthFunc(GL_LEQUAL)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _outline_buffer)
		glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
		glEnableClientState(GL_VERTEX_ARRAY)
		#edges = <int*> glMapBuffer(GL_ELEMENT_ARRAY_BUFFER, GL_WRITE_ONLY)
		
		cdef Chunk* chunk
		chunk = get_chunk()
		chunk_register(chunk, self._nb_vertices * sizeof(int))
		cdef int* vertex_used
		vertex_used = <int*> (chunk.content)
		for i from 0 <= i < self._nb_vertices: vertex_used[i] = -1
		
		
		# find and draw edges
		buf = 0
		for i from 0 <= i < self._nb_faces:
			face = self._faces + i
			if face.option & FACE_ALPHA: continue
			
			if face.option & FACE_QUAD: nb = 4
			else:                       nb = 3
			
			if face.option & FACE_SMOOTH_LIT:
				if face.option & FACE_DOUBLE_SIDED:
					for j from 0 <= j < nb:
						k = self._neighbors[4 * i + j]
						if k == -1: # No neighbor, but double-sided face => the face is its own neighbor
							vertex_used[face.v[j]] = 1
							
							edges[buf] = face.v[j] # draw edge between vertices j and j + 1
							if j < nb - 1: edges[buf + 1] = face.v[j + 1]
							else:          edges[buf + 1] = face.v[0]
							buf = buf + 2
							
						else:
							ns = self._neighbors_side[4 * i + j]
							neighbor_face = self._faces[k]
							if (
								(ns == -1) and (((face.option & FACE_FRONT) and (neighbor_face.option & FACE_BACK )) or ((face.option & FACE_BACK) and (neighbor_face.option & FACE_FRONT)))
									) or (
								(ns ==  1) and (((face.option & FACE_FRONT) and (neighbor_face.option & FACE_FRONT)) or ((face.option & FACE_BACK) and (neighbor_face.option & FACE_BACK)))
								):
								vertex_used[face.v[j]] = 1
								
								edges[buf] = face.v[j] # draw edge between vertices j and j + 1
								if j < nb - 1: edges[buf + 1] = face.v[j + 1]
								else:          edges[buf + 1] = face.v[0]
								buf = buf + 2
								
				else:
					if face.option & FACE_FRONT:
						# test if neighbors are back
						for j from 0 <= j < nb:
							k = self._neighbors[4 * i + j]
							if (k == -1) or (self._faces[k].option & FACE_BACK):
								vertex_used[face.v[j]] = 1
								
								edges[buf] = face.v[j] # draw edge between vertices j and j + 1
								if j < nb - 1: edges[buf + 1] = face.v[j + 1]
								else:          edges[buf + 1] = face.v[0]
								buf = buf + 2
								
			else: # Not smoothlit
				if (face.option & FACE_FRONT) or (face.option & FACE_DOUBLE_SIDED):
					for j from 0 <= j < nb:
						edges[buf] = face.v[j] # draw edge between vertices j and j + 1
						if j < nb - 1: edges[buf + 1] = face.v[j + 1]
						else:          edges[buf + 1] = face.v[0]
						buf = buf + 2
						
			if buf >= 60: # A face has at maximum 4 edges => render now !
				#glUnmapBuffer(GL_ELEMENT_ARRAY_BUFFER)
				
				print 4.0
				check_gl_error()
				
				glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, buf * sizeof(int), edges)
				
				print 5
				check_gl_error()
				
				glDrawElements(GL_LINES, buf, GL_UNSIGNED_INT, BUFFER_OFFSET(0))
				
				print 6
				check_gl_error()
				
				#edges = <int*> glMapBuffer(GL_ELEMENT_ARRAY_BUFFER, GL_WRITE_ONLY)
				buf = 0
				
		if buf > 0: # Some lines are pending, draw them !
			#glUnmapBuffer(GL_ELEMENT_ARRAY_BUFFER)
			
			print 7
			check_gl_error()

			for k from 0 <= k < buf:
				print edges[k], self._nb_vertices
			glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, 0, buf * sizeof(int), edges)
			
			print 8
			check_gl_error()
			
			glDrawElements(GL_LINES, buf, GL_UNSIGNED_INT, BUFFER_OFFSET(0))
			
			print 9, buf
			check_gl_error()
				
			#edges = <int*> glMapBuffer(GL_ELEMENT_ARRAY_BUFFER, GL_WRITE_ONLY)
			buf = 0
			
		#glPointSize(d / 2)
		#for i from 0 <= i < self._nb_vertices:
		#	if vertex_used[i] == 1:
		#		edges[buf] = i
		#		buf = buf + 1
		#		if buf > 64:
		#			glDrawElements(GL_POINTS, buf, GL_UNSIGNED_INT, BUFFER_OFFSET(0))
		#			buf = 0
		#if buf > 0:
		#	glDrawElements(GL_POINTS, buf, GL_UNSIGNED_INT, BUFFER_OFFSET(0))
			
		drop_chunk(chunk)
		
		#glUnmapBuffer(GL_ELEMENT_ARRAY_BUFFER)
		glDisableClientState(GL_VERTEX_ARRAY)
		glBindBuffer (GL_ARRAY_BUFFER        , 0)		
		glBindBuffer (GL_ELEMENT_ARRAY_BUFFER, 0)
		glLineWidth(1.0) # Reset to
		glPointSize(1.0) # default
		glEnable   (GL_LIGHTING)
		glDepthFunc(GL_LESS)
		glColor4fv (white)
