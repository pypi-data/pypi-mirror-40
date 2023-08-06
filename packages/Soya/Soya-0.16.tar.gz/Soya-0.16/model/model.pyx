# -*- indent-tabs-mode: t -*-

# Soya 3D
# Copyright (C) 2003-2004 Jean-Baptiste LAMY -- jiba@tuxfamily.org
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


# cdef class _VertexBuffer(_CObj):
# 	cdef int _buf_data
# 	cdef int _buf_data2
# 	cdef int _buf_index
	
# 	cdef int _option
# 	cdef int _nb_vertex, _nb_face
# 	cdef int _sizeof_vertex
	
# 	cdef int _normal_offset, _color_offset, _tex_coords_offset
	
# 	cdef float* _pos_pointer, _normal_pointer, _color_pointer, _tex_coords_pointer, _tex_coords2_pointer
# 	cdef int*   _face_pointer
#   cdef int*   _faces_id
#   cdef int*   _vertices_id
	
# 	cdef uintptr_t _material_id
#   cdef Chunk*    _face_chunk   # Only used for initialization
#   cdef Chunk*    _vertex_chunk # Only used for initialization
#   cdef           _vertex_set   # Only used for initialization
	
# 	def __init__(self, option):
# 		self._option = option
		
# 		self._sizeof_vertex = 6
# 		if self._option & VERTEX_BUFFER_HAS_VERTEX_COLOR:  self._sizeof_vertex = self._sizeof_vertex + 4
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS:    self._sizeof_vertex = self._sizeof_vertex + 2
# 		self._sizeof_vertex = self._sizeof_vertex * sizeof(float)
		
#     glGenBuffers(1, &self._buf_index)
# 		glGenBuffers(1, &self._buf_data)
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS2: glGenBuffers(1, &self._buf_data2)
		
# 	cdef void _set_size(self, int nb_face, int nb_vertex):
# 		cdef int offset
		
# 		self._nb_vertex     = _nb_vertex
# 		self._nb_face       = _nb_face
		
# 		self._normal_offset = 3 * self._nb_vertex
# 		offset = self._normal_offset
# 		if self._option & VERTEX_BUFFER_HAS_VERTEX_COLOR:
# 			self._color_offset = offset
# 			offset = offset + 4 * self._nb_vertex
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS:
# 			self._tex_coords_offset = offset
# 			offset = offset + 2 * self._nb_vertex
			
# 		glBindBuffer(GL_ARRAY_BUFFER, self._buf_data)		
# 		if self._option & VERTEX_BUFFER_STATIC_VERTEX: glBufferData(GL_ARRAY_BUFFER, self._nb_vertex * self._sizeof_vertex, NULL, GL_STATIC_DRAW)
# 		else:                                          glBufferData(GL_ARRAY_BUFFER, self._nb_vertex * self._sizeof_vertex, NULL, GL_DYNAMIC_DRAW)
		
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS2:
# 			glBindBuffer(GL_ARRAY_BUFFER, self._buf_data2)		
# 			glBufferData(GL_ARRAY_BUFFER, 2 * sizeof(float), NULL, GL_DYNAMIC_DRAW)
			
# 		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._buf_index)
# 		if self._option & VERTEX_BUFFER_STATIC_FACE: glBufferData(GL_ELEMENT_ARRAY_BUFFER, 3 * self._nb_face * sizeof(int), NULL, GL_STATIC_DRAW)
# 		else:                                        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 3 * self._nb_face * sizeof(int), NULL, GL_DYNAMIC_DRAW)
		
# 		glBindBuffer(GL_ARRAY_BUFFER        , 0)		
# 		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		
# 	cdef void _enable(self):
# 		glBindBuffer(GL_ARRAY_BUFFER        , self._buf_data)
# 		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._buf_index)
# 		glEnableClientState(GL_VERTEX_ARRAY)
# 		glVertexPointer(3, GL_FLOAT, 0, BUFFER_OFFSET(0))
# 		glEnableClientState(GL_NORMAL_ARRAY)
# 		glNormalPointer(GL_FLOAT, 0, BUFFER_OFFSET(self._normal_offset * sizeof(float)))
# 		if self._option & VERTEX_BUFFER_HAS_VERTEX_COLOR:
# 			glEnableClientState(GL_COLOR_ARRAY)
# 			glColorPointer(4, GL_FLOAT, 0, BUFFER_OFFSET(self._color_offset * sizeof(float)))
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS:
# 			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
# 			glTexCoordPointer(2, GL_FLOAT, 0, BUFFER_OFFSET(self._tex_coords_offset * sizeof(float)))
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS2:
# 			glClientActiveTexture(GL_TEXTURE1)
# 			glBindBuffer(GL_ARRAY_BUFFER, self._buf_data2)
# 			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
# 			glTexCoordPointer(2, GL_FLOAT, 0, BUFFER_OFFSET(0))
# 			glClientActiveTexture(GL_TEXTURE0)
			
# 	cdef void _disable(self):
# 		glDisableClientState(GL_VERTEX_ARRAY)
# 		glDisableClientState(GL_NORMAL_ARRAY)
# 		if self._option & VERTEX_BUFFER_HAS_VERTEX_COLOR: glDisableClientState(GL_COLOR_ARRAY)
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS:   glDisableClientState(GL_TEXTURE_COORD_ARRAY)
# 		if self._option & VERTEX_BUFFER_HAS_TEX_COORDS2:
# 			glClientActiveTexture(GL_TEXTURE1)
# 			glDisableClientState(GL_TEXTURE_COORD_ARRAY)
# 			glClientActiveTexture(GL_TEXTURE0)
# 		glBindBuffer(GL_ARRAY_BUFFER        , 0)		
# 		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		
# 	cdef void _map_pointers(self):
# 		cdef int offset
# 		glBindBuffer(GL_ARRAY_BUFFER        , self._buf_data)
# 		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._buf_index)
# 		self._pos_pointer    = <float*> glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY)
# 		self._face_pointer   = <int*>   glMapBuffer(GL_ELEMENT_ARRAY_BUFFER, GL_WRITE_ONLY)
# 		self._normal_pointer = self._pos_pointer + self._normal_offset
# 		if self._color_offset       > 0: self._color_pointer       = self._pos_pointer + self._color_offset
# 		if self._tex_coords_offset  > 0: self._tex_coords_pointer  = self._pos_pointer + self._tex_coords_offset
		
# 	cdef void _unmap_pointers(self):
# 		glUnmapBuffer(GL_ARRAY_BUFFER)
# 		glUnmapBuffer(GL_ELEMENT_ARRAY_BUFFER)
# 		glBindBuffer (GL_ARRAY_BUFFER        , 0)		
# 		glBindBuffer (GL_ELEMENT_ARRAY_BUFFER, 0)
		
# 	cdef void _map_tex_coords2_pointer(self):
# 		glBindBuffer(GL_ARRAY_BUFFER, self._buf_data2)
# 		self._tex_coords2_pointer = <float*> glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY)
		
# 	cdef void _unmap_tex_coords2_pointer(self):
# 		glUnmapBuffer(GL_ARRAY_BUFFER)
# 		glBindBuffer (GL_ARRAY_BUFFER, 0)		
		
		
cdef class _Model(_CObj):
	#cdef public _filename
	
	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self._filename)
	
	cdef void _batch               (self, _Body body): pass
	cdef void _render              (self, _Body body): pass
	cdef int  _shadow              (self, CoordSyst coord_syst, _Light light): return 0
	cdef void _get_box             (self, float* box, float* matrix): pass
	cdef void _raypick             (self, RaypickData raypick_data, CoordSyst raypickable): pass
	cdef int  _raypick_b           (self, RaypickData raypick_data, CoordSyst raypickable): return 0
	cdef void _raypick_part(self, RaypickData raypick_data, float* raydata, int part, CoordSyst parent):
		raise TypeError("This type of model doesn't support part raypicking !")
	cdef int _raypick_part_b(self, RaypickData raypick_data, float* raydata, int part):
		raise TypeError("This type of model doesn't support part raypicking !")
	cdef void _collect_raypickables(self, Chunk* items, float* rsphere, float* sphere, CoordSyst parent): pass
	
	cdef void _attach(self, mesh_names): raise TypeError("This type of model doesn't support attach!")
	cdef void _detach(self, mesh_names): raise TypeError("This type of model doesn't support detach!")
	cdef int  _is_attached(self, mesh_name): return 0
	cdef void _attach_to_bone(self, CoordSyst coordsyst, bone_name): raise TypeError("This type of model doesn't support attach_to_bone!")
	cdef void _detach_from_bone(self, CoordSyst coordsyst): raise TypeError("This type of model doesn't support detach_from_bone!")
	cdef      _get_attached_meshes    (self): return []
	cdef      _get_attached_coordsysts(self): return []
	cdef void _animate_blend_cycle   (self, animation_name, float weight, float fade_in):   raise TypeError("This type of model doesn't support animation!")
	cdef void _animate_clear_cycle   (self, animation_name, float fade_out):                raise TypeError("This type of model doesn't support animation!")
	cdef void _animate_execute_action(self, animation_name, float fade_in, float fade_out): raise TypeError("This type of model doesn't support animation!")
	cdef void _animate_reset(self): pass
	cdef void _set_lod_level(self, float lod_level): raise TypeError("This type of model doesn't support LOD!")
	cdef void _begin_round  (self): pass
	cdef void _advance_time (self, float proportion): pass
	
	cdef void _instanced(self, _Body body, opt):
		body._data = self
		
	cdef _Model _create_deformed_data(self): return None
	#cdef void _apply_deform(self, _Deform deform): pass
	
	cdef void _batch_part(self, _Body body, int index): raise TypeError("This type of model doesn't support part batching !")
	cdef void _batch_end(self, _Body body): raise TypeError("This type of model doesn't support part batching !")
	
	def __deepcopy__(self, memo):
		"""Models are immutable."""
		return self
	

#ctypedef struct DisplayList:
#  int    option
#  int    id
#  uintptr_t    material_id #Material* material
#  int*   faces_id
#  Chunk* chunk # Only used for initialization of the DisplayList
#  
#ctypedef struct DisplayLists:
#  int nb_opaque_list
#  int nb_alpha_list
#  DisplayList* display_lists
#  
#ctypedef struct ModelFace:
#  int      option
#  Pack*    pack
#  int      normal
#  int      v[4] # v[3] is optional (only for quad, unused for triangle)
	
#U#cdef int face_vertices_number(ModelFace* self):
#U#	if   self.option & FACE_TRIANGLE: return 3
#U#	elif self.option & FACE_QUAD:     return 4
#U#	return 0


cdef class _SimpleModel(_Model):
	#cdef int           _option
	#cdef               _materials
	#cdef int           _nb_faces, _nb_vertices, _nb_coords, _nb_vnormals, _nb_colors, _nb_values
	#cdef float*        _coords, *_vnormals, *_colors, *_values
	#cdef int*          _vertex_coords, *_vertex_texcoords, *_vertex_diffuses, *_vertex_emissives
	#cdef char*         _vertex_options
	#cdef ModelFace*    _faces
	#cdef int*          _neighbors, *_simple_neighbors
	#cdef signed char*  _neighbors_side, *_simple_neighbors_side
	#cdef DisplayLists* _display_lists
	#cdef float*        _sphere
	
	cdef _Model _create_deformed_data(self):
		cdef _SimpleModel data
		data = self.__class__.__new__(self.__class__)
		data.base_model = self # Needed, to keep in memory the base model
		
		data._materials     = self._materials
		data._option        = self._option
		data._nb_vertices   = self._nb_vertices
		data._nb_coords     = self._nb_coords
		data._nb_vnormals   = self._nb_vnormals
		data._nb_colors     = self._nb_colors
		data._nb_values     = self._nb_values
		data._nb_faces      = self._nb_faces
		
		data._faces         = self._faces
		data._coords        = <float*> malloc(3 * data._nb_coords * sizeof(float))
		data._vnormals      = self._vnormals
		data._colors        = self._colors
		data._values        = self._values
		data._vertex_coords = self._vertex_coords
		
		if self._option & MODEL_VERTEX_OPTIONS: data._vertex_options   = self._vertex_options
		if self._option & MODEL_TEXCOORDS:      data._vertex_texcoords = self._vertex_texcoords
		if self._option & MODEL_DIFFUSES:       data._vertex_diffuses  = self._vertex_diffuses
		if self._option & MODEL_EMISSIVES:      data._vertex_emissives = self._vertex_emissives
		if self._option & MODEL_HAS_SPHERE:     data._sphere           = self._sphere
		
		if self._option & MODEL_NEIGHBORS:
			data._neighbors      = self._neighbors
			data._neighbors_side = self._neighbors_side
			
		if self._option & MODEL_SIMPLE_NEIGHBORS:
			data._simple_neighbors      = self._simple_neighbors
			data._simple_neighbors_side = self._simple_neighbors_side
			
		data._build_display_list()
		
		data._option = data._option & ~MODEL_DISPLAY_LISTS # Deformed models change => don't render them with display lists
		data._option = data._option & ~MODEL_INITED
		data._option = data._option |  MODEL_SHARED_DATA
		return data
	
	cdef void _get_box(self, float* box, float* matrix):
		cdef float* coord
		cdef float  coord2[3]
		
		coord = self._coords
		for i from 0 <= i < self._nb_coords:
			point_by_matrix_copy(coord2, coord, matrix)
			
			if coord2[0] < box[0]: box[0] = coord2[0]
			if coord2[1] < box[1]: box[1] = coord2[1]
			if coord2[2] < box[2]: box[2] = coord2[2]
			if coord2[0] > box[3]: box[3] = coord2[0]
			if coord2[1] > box[4]: box[4] = coord2[1]
			if coord2[2] > box[5]: box[5] = coord2[2]
			
			coord = coord + 3
			
	cdef __getcstate__(self):
		cdef Chunk*     chunk
		cdef int        i
		cdef ModelFace* face
		cdef            material_id2index
		cdef uintptr_t   ptr
		material_id2index = {}
		for i from 0 <= i < len(self._materials):
			ptr = id(self._materials[i]) # Required for Python 2.4
			material_id2index[ptr] = i
			
		chunk = get_chunk()
		chunk_add_int_endian_safe   (chunk, self._option)
		chunk_add_int_endian_safe   (chunk, self._nb_vertices)
		chunk_add_int_endian_safe   (chunk, self._nb_coords)
		chunk_add_int_endian_safe   (chunk, self._nb_vnormals)
		chunk_add_int_endian_safe   (chunk, self._nb_colors)
		chunk_add_int_endian_safe   (chunk, self._nb_values)
		chunk_add_int_endian_safe   (chunk, self._nb_faces)
		
		chunk_add_floats_endian_safe(chunk, self._coords   , 3 * self._nb_coords)
		chunk_add_floats_endian_safe(chunk, self._vnormals , 3 * self._nb_vnormals)
		chunk_add_floats_endian_safe(chunk, self._colors   , 4 * self._nb_colors)
		chunk_add_floats_endian_safe(chunk, self._values   ,     self._nb_values)
		
		chunk_add_ints_endian_safe(chunk, self._vertex_coords, self._nb_vertices)
		if self._option & MODEL_VERTEX_OPTIONS:
			chunk_add_chars_endian_safe (chunk, self._vertex_options  , self._nb_vertices)
		if self._option & MODEL_TEXCOORDS:
			chunk_add_ints_endian_safe  (chunk, self._vertex_texcoords, self._nb_vertices)
		if self._option & MODEL_DIFFUSES:       chunk_add_ints_endian_safe  (chunk, self._vertex_diffuses , self._nb_vertices)
		if self._option & MODEL_EMISSIVES:      chunk_add_ints_endian_safe  (chunk, self._vertex_emissives, self._nb_vertices)
		if self._option & MODEL_HAS_SPHERE:     chunk_add_floats_endian_safe(chunk, self._sphere          , 4)
		
		for i from 0 <= i < self._nb_faces:
			face = self._faces + i
			chunk_add_int_endian_safe (chunk, face.option)
			chunk_add_int_endian_safe (chunk, material_id2index[face.pack.material_id])
			chunk_add_int_endian_safe (chunk, face.normal)
			chunk_add_ints_endian_safe(chunk, face.v, 4)
			
		if self._option & MODEL_NEIGHBORS:
			chunk_add_ints_endian_safe (chunk, self._neighbors     , self._nb_faces * 4)
			chunk_add_chars_endian_safe(chunk, self._neighbors_side, self._nb_faces * 4)
			
		if self._option & MODEL_SIMPLE_NEIGHBORS:
			chunk_add_ints_endian_safe (chunk, self._simple_neighbors     , self._nb_faces * 4)
			chunk_add_chars_endian_safe(chunk, self._simple_neighbors_side, self._nb_faces * 4)
			
		return drop_chunk_to_string(chunk), self._filename, self._materials
	
	cdef void __setcstate_data__(self, cstate):
		cdef int        i
		cdef int        temp
		cdef Chunk*     chunk
		cdef ModelFace* face
		cstate2, self._filename, self._materials = cstate
		chunk = string_to_chunk(cstate2)
		
		chunk_get_int_endian_safe(chunk, &self._option)
		chunk_get_int_endian_safe(chunk, &self._nb_vertices)
		chunk_get_int_endian_safe(chunk, &self._nb_coords)
		chunk_get_int_endian_safe(chunk, &self._nb_vnormals)
		chunk_get_int_endian_safe(chunk, &self._nb_colors)
		chunk_get_int_endian_safe(chunk, &self._nb_values)
		chunk_get_int_endian_safe(chunk, &self._nb_faces)
		
		self._faces         = <ModelFace*> malloc(    self._nb_faces    * sizeof(ModelFace))
		self._coords        = <float*>     malloc(3 * self._nb_coords   * sizeof(float))
		self._vnormals      = <float*>     malloc(3 * self._nb_vnormals * sizeof(float))
		self._colors        = <float*>     malloc(4 * self._nb_colors   * sizeof(float))
		self._values        = <float*>     malloc(    self._nb_values   * sizeof(float))
		
		chunk_get_floats_endian_safe(chunk, self._coords   , 3 * self._nb_coords)
		chunk_get_floats_endian_safe(chunk, self._vnormals , 3 * self._nb_vnormals)
		chunk_get_floats_endian_safe(chunk, self._colors   , 4 * self._nb_colors)
		chunk_get_floats_endian_safe(chunk, self._values   ,     self._nb_values)
			
		self._vertex_coords = <int*> malloc(self._nb_vertices * sizeof(int))
		chunk_get_ints_endian_safe(chunk, self._vertex_coords, self._nb_vertices)
		if self._option & MODEL_VERTEX_OPTIONS: self._vertex_options   = <char* > malloc(self._nb_vertices * sizeof(char )); chunk_get_chars_endian_safe (chunk, self._vertex_options  , self._nb_vertices)
		if self._option & MODEL_TEXCOORDS:      self._vertex_texcoords = <int*  > malloc(self._nb_vertices * sizeof(int  )); chunk_get_ints_endian_safe  (chunk, self._vertex_texcoords, self._nb_vertices)
		if self._option & MODEL_DIFFUSES:       self._vertex_diffuses  = <int*  > malloc(self._nb_vertices * sizeof(int  )); chunk_get_ints_endian_safe  (chunk, self._vertex_diffuses , self._nb_vertices)
		if self._option & MODEL_EMISSIVES:      self._vertex_emissives = <int*  > malloc(self._nb_vertices * sizeof(int  )); chunk_get_ints_endian_safe  (chunk, self._vertex_emissives, self._nb_vertices)
		if self._option & MODEL_HAS_SPHERE:     self._sphere           = <float*> malloc(4                 * sizeof(float)); chunk_get_floats_endian_safe(chunk, self._sphere          , 4)
		
		for i from 0 <= i < self._nb_faces:
			face        = self._faces + i
			chunk_get_int_endian_safe (chunk, &face.option)
			chunk_get_int_endian_safe (chunk, &temp)
			face.pack   = (<_Material> (<void*> (self._materials[temp])))._pack(face.option)
			chunk_get_int_endian_safe (chunk, &face.normal)
			chunk_get_int_endian_safe(chunk, &face.v[0])
			chunk_get_int_endian_safe(chunk, &face.v[1])
			chunk_get_int_endian_safe(chunk, &face.v[2])
			chunk_get_int_endian_safe(chunk, &face.v[3])
			
		if self._option & MODEL_NEIGHBORS:
			self._neighbors      = <int        *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(signed char))
			chunk_get_ints_endian_safe (chunk, self._neighbors     , self._nb_faces * 4)
			chunk_get_chars_endian_safe(chunk, self._neighbors_side, self._nb_faces * 4)
			
		if self._option & MODEL_SIMPLE_NEIGHBORS:
			self._simple_neighbors      = <int        *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._simple_neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(signed char))
			chunk_get_ints_endian_safe (chunk, self._simple_neighbors     , self._nb_faces * 4)
			chunk_get_chars_endian_safe(chunk, self._simple_neighbors_side, self._nb_faces * 4)
			
		drop_chunk(chunk)
		
		self._option = self._option & ~MODEL_INITED
		
	cdef void __setcstate__(self, cstate):
		self.__setcstate_data__(cstate)
		self._build_display_list()
		
	property option:
		def __get__(self):
			return self._option
		
	property materials:
		def __get__(self):
			return self._materials
		
	property nb_coords:
		def __get__(self):
			return self._nb_coords
		
	property nb_vertices:
		def __get__(self):
			return self._nb_vertices
		
	property nb_faces:
		def __get__(self):
			return self._nb_faces

	def get_face(self, int index):
		"""Debugging functions"""
		cdef ModelFace* face
		face = self._faces + index
		if face.option & FACE_QUAD: return face.v[0], face.v[1], face.v[2], face.v[3]
		else:                       return face.v[0], face.v[1], face.v[2]
		
	def get_vertex_index(self, int index):
		"""Debugging functions"""
		l = [self._vertex_coords[index]]
		if self._option & MODEL_VERTEX_OPTIONS: l.append(self._vertex_options[index])
		else:                                   l.append(-1)
		if self._option & MODEL_TEXCOORDS:      l.append(self._vertex_texcoords[index])
		else:                                   l.append(-1)
		if self._option & MODEL_DIFFUSES:       l.append(self._vertex_diffuses[index])
		else:                                   l.append(-1)
		if self._option & MODEL_EMISSIVES:      l.append(self._vertex_emissives[index])
		else:                                   l.append(-1)
		return tuple(l)
	
	def get_vertex(self, int index):
		"""Debugging functions"""
		l = [(self._coords[self._vertex_coords[index]], self._coords[self._vertex_coords[index] + 1], self._coords[self._vertex_coords[index] + 2])]
		if self._option & MODEL_VERTEX_OPTIONS: l.append(self._vertex_options[index])
		else:                                   l.append(-1)
		if self._option & MODEL_TEXCOORDS:      l.append((self._values[self._vertex_texcoords[index]], self._values[self._vertex_texcoords[index] + 1]))
		else:                                   l.append(-1)
		if self._option & MODEL_DIFFUSES:       l.append((self._colors[self._vertex_diffuses [index]], self._colors[self._vertex_diffuses [index] + 1], self._colors[self._vertex_diffuses [index] + 2], self._colors[self._vertex_diffuses [index] + 3]))
		else:                                   l.append(-1)
		if self._option & MODEL_EMISSIVES:      l.append((self._colors[self._vertex_emissives[index]], self._colors[self._vertex_emissives[index] + 1], self._colors[self._vertex_emissives[index] + 2], self._colors[self._vertex_emissives[index] + 3]))
		else:                                   l.append(-1)
		return tuple(l)
	
	def get_neighbor(self, int index):
		if not (self._option & MODEL_NEIGHBORS): return None
		cdef int* neighbor
		neighbor = self._neighbors + (4 * index)
		return neighbor[0], neighbor[1], neighbor[2], neighbor[3]
		
	def get_neighbor_side(self, int index):
		if not (self._option & MODEL_NEIGHBORS): return None
		cdef signed char* neighbor_side
		neighbor_side = self._neighbors_side + (4 * index)
		return neighbor_side[0], neighbor_side[1], neighbor_side[2], neighbor_side[3]
		
	def get_simple_neighbor(self, int index):
		if not (self._option & MODEL_SIMPLE_NEIGHBORS): return None
		cdef int* neighbor
		neighbor = self._simple_neighbors + (4 * index)
		return neighbor[0], neighbor[1], neighbor[2], neighbor[3]
	
	def get_simple_neighbor_side(self, int index):
		if not (self._option & MODEL_SIMPLE_NEIGHBORS): return None
		cdef signed char* neighbor_side
		neighbor_side = self._simple_neighbors_side + (4 * index)
		return neighbor_side[0], neighbor_side[1], neighbor_side[2], neighbor_side[3]
	
	property sphere:
		def __get__(self):
			return (self._sphere[0], self._sphere[1], self._sphere[2], self._sphere[3])
		
	cdef void _register_material(self, _Material material):
		if material in self._materials: return
		self._materials.append(material)
		
	cdef void _add_coord(self, _Vertex vertex):
		vertex._out(self._coords + 3 * self._nb_coords)
		self._nb_coords = self._nb_coords + 1
		if not vertex._normal is None:
			vertex._normal._out(self._vnormals + 3 * self._nb_vnormals)
			vector_normalize(self._vnormals + 3 * self._nb_vnormals)
			self._nb_vnormals = self._nb_vnormals + 1
			
	cdef int _register_value(self, float* value, int nb):
		cdef int r, i
		for r from 0 <= r <= self._nb_values - nb:
			if float_array_compare(value, self._values + r, nb) == 1: return r
		r = self._nb_values
		self._nb_values = self._nb_values + nb
		self._values = <float*> realloc(self._values, self._nb_values * sizeof(float))
		memcpy(self._values + r, value, nb * sizeof(float))
		return r
	
	cdef int _register_color(self, float color[4]):
		cdef float* ptr
		cdef int    i
		ptr = self._colors
		for i from 0 <= i < self._nb_colors:
			if ((fabs(color[0] - ptr[0]) < EPSILON) and
					(fabs(color[1] - ptr[1]) < EPSILON) and
					(fabs(color[2] - ptr[2]) < EPSILON) and
					(fabs(color[3] - ptr[3]) < EPSILON)): return 4 * i
			ptr = ptr + 4
			
		i = self._nb_colors * 4
		self._nb_colors = self._nb_colors + 1
		self._colors = <float*> realloc(self._colors, self._nb_colors * 4 * sizeof(float))
		memcpy(self._colors + i, color, 4 * sizeof(float))
		return i
	
	cdef void _add_face(self, _Face face, vertex2ivertex, ivertex2index, lights, int static_shadow):
		cdef ModelFace* sf
		cdef int        nb_vertices
		cdef float      n[4]
		cdef float*     p
		sf = self._faces + self._nb_faces
		
		sf.option = 0
		n[0] = n[1] = n[2] = n[3] = 0.0
		nb_vertices = len(face._vertices)
		if   nb_vertices == 3: sf.option = sf.option | FACE_TRIANGLE
		elif nb_vertices == 4: sf.option = sf.option | FACE_QUAD
		else:
			print "Face with %s vertices are not supported in model." % nb_vertices
			raise ValueError("Face with %s vertices are not supported in model." % nb_vertices)
		if face.is_alpha():                   sf.option = sf.option | FACE_ALPHA
		if face._option & FACE2_DOUBLE_SIDED: sf.option = sf.option | FACE_DOUBLE_SIDED
		if face._option & FACE2_SMOOTH_LIT:   sf.option = sf.option | FACE_SMOOTH_LIT
		if not(face._option & FACE2_LIT):     sf.option = sf.option | FACE_NON_LIT
		if face._option & NON_SOLID:          sf.option = sf.option | FACE_NON_SOLID
		
		# compute data and then register all in 1 pass because registering data
		# can have side effect on the faces chunk
		sf.v[0] = self._add_vertex(face._vertices[0], vertex2ivertex, ivertex2index, lights, static_shadow)
		sf.v[1] = self._add_vertex(face._vertices[1], vertex2ivertex, ivertex2index, lights, static_shadow)
		sf.v[2] = self._add_vertex(face._vertices[2], vertex2ivertex, ivertex2index, lights, static_shadow)
		if nb_vertices == 4: sf.v[3] = self._add_vertex(face._vertices[3], vertex2ivertex, ivertex2index, lights, static_shadow)
		
		face._normal._out(n)
		if self._option & MODEL_PLANE_EQUATION:
			p = self._coords + self._vertex_coords[sf.v[0]]
			n[3] = -(p[0] * n[0] + p[1] * n[1] + p[2] * n[2])
			plane_vector_normalize(n)
			sf.normal = self._register_value(n, 4)
		else:
			vector_normalize(n)
			sf.normal = self._register_value(n, 3)
		
		
		if not face._material in self._materials: self._materials.append(face._material)
		sf.pack = face._material._pack(sf.option)
		
		self._nb_faces = self._nb_faces + 1
		
	cdef int _add_vertex(self, _Vertex vertex, vertex2ivertex, ivertex2index, lights, int static_shadow):
		cdef float   value[4], p[3], v[3]
		cdef int     coord, texcoord, diffuse, emissive
		cdef _Light  light
		cdef _Vertex ivertex
		cdef int     i
		ivertex = vertex2ivertex[vertex]
		
		coord = 3 * ivertex2index[vertex2ivertex[vertex]]


		if self._option & MODEL_TEXCOORDS:
			value[0] = vertex._tex_x
			value[1] = vertex._tex_y
			texcoord = self._register_value(value, 2)
		else: texcoord = -1

		if self._option & MODEL_DIFFUSES:
			if not vertex._diffuse is None:
				value[0] = vertex._diffuse[0]
				value[1] = vertex._diffuse[1]
				value[2] = vertex._diffuse[2]
				value[3] = vertex._diffuse[3]
			else: # the face use diffuse color, but not for this vertex. but we need ALL the face's vertices to have a color => we take the material diffuse color as default.
				memcpy(&value[0], &vertex._face._material._diffuse[0], 4 * sizeof(float))
			diffuse = self._register_color(value)
		else: diffuse = -1

		if self._option & MODEL_EMISSIVES:
			if not vertex._emissive is None:
				value[0] = vertex._emissive[0]
				value[1] = vertex._emissive[1]
				value[2] = vertex._emissive[2]
				value[3] = vertex._emissive[3]
			else: # the face use emissive color, but not for this vertex. the default emissive is BLACK, i.e. no emission.
				value[0] = value[1] = value[2] = 0.0
				value[3] = 1.0

		elif lights:
			value[0] = value[1] = value[2] = 0.0
			value[3] = 1.0

		if lights: # Apply static lighting
			for light in lights:
				vertex._into(light, p)
				if vertex._face._option & FACE2_SMOOTH_LIT: ivertex     ._normal._into(light, v)
				else:                                       vertex._face._normal._into(light, v)
				light._static_light_at(p, v, static_shadow, value)
		if self._option & MODEL_EMISSIVES: emissive = self._register_color(value)
		else: emissive = -1

		for i from 0 <= i < self._nb_vertices:
			if                  ((self._vertex_coords   [i] == coord   )  and
			((texcoord == -1) or (self._vertex_texcoords[i] == texcoord)) and
			((diffuse  == -1) or (self._vertex_diffuses [i] == diffuse )) and
			((emissive == -1) or (self._vertex_emissives[i] == emissive))): return i

		i = self._nb_vertices
		self._nb_vertices = self._nb_vertices + 1
		self._vertex_coords = <int*> realloc(self._vertex_coords, self._nb_vertices * sizeof(int))
		self._vertex_coords[i] = coord

		if self._option & MODEL_TEXCOORDS: self._vertex_texcoords = <int*> realloc(self._vertex_texcoords, self._nb_vertices * sizeof(int)); self._vertex_texcoords[i] = texcoord
		if self._option & MODEL_DIFFUSES : self._vertex_diffuses  = <int*> realloc(self._vertex_diffuses , self._nb_vertices * sizeof(int)); self._vertex_diffuses [i] = diffuse
		if self._option & MODEL_EMISSIVES: self._vertex_emissives = <int*> realloc(self._vertex_emissives, self._nb_vertices * sizeof(int)); self._vertex_emissives[i] = emissive

		return i
			
	cdef object _identify_vertices(self, faces, float angle):
		"""Finds which vertices are at the same position, for vertex sharing capabilities.
2 vertices are considered at the same position if the distance between them is > EPSILON,
and if the angle between their 2 faces is < ANGLE."""
		# "ivertex" means "identified vertex"
		cdef _Face   face
		cdef _Vertex vertex, ivertex, vertex2
		cdef int     i, j
		cdef float   p[3], amin, a
		cdef         ivertices
		
		vertex2ivertex   = {}
		ivertex2vertices = {}
		hashcube         = {}
		for face in faces:
			for vertex in face._vertices:
				vertex._out(p)
				p[0] = (<float> (<int> (p[0] / EPSILON))) * EPSILON
				p[1] = (<float> (<int> (p[1] / EPSILON))) * EPSILON
				p[2] = (<float> (<int> (p[2] / EPSILON))) * EPSILON
				
				hash = (p[0], p[1], p[2])
				ivertex = hashcube.get(hash)
				if ivertex is None:
					vertex2ivertex[vertex] = hashcube[hash] = ivertex = vertex
					ivertex2vertices[ivertex] = [vertex]
				else:
					vertex2ivertex[vertex] = ivertex
					ivertex2vertices[ivertex].append(vertex)
					
		if angle > 180.0: return vertex2ivertex, ivertex2vertices
		
		# Take face angle into account for vertex identification.
		vertex2ivertex2   = {}
		ivertex2vertices2 = {}
		from sets import Set
		for vertices in ivertex2vertices.values():
			couples = []
			for i from 0 <= i < len(vertices):
				for j from i + 1 <= j < len(vertices):
					couples.append((vertices[i].face.normal.angle_to(vertices[j].face.normal), vertices[i], vertices[j]))
					
			couples.sort()
			
			shared_vertices = {}
			for vertex in vertices: shared_vertices[vertex] = Set([vertex])
			
			for a, vertex1, vertex2 in couples:
				if a > angle: break
				shared_vertex1 = shared_vertices.get(vertex1)
				shared_vertex2 = shared_vertices.get(vertex2)
				shared_vertex  = shared_vertex1 | shared_vertex2
				for vertex in shared_vertex: shared_vertices[vertex] = shared_vertex

			for shared_vertex in Set(shared_vertices.values()):
				shared_vertex = list(shared_vertex)
				ivertex = shared_vertex[0]
				ivertex2vertices2[ivertex] = shared_vertex
				for vertex in shared_vertex:
					vertex2ivertex2[vertex] = ivertex
					
		return vertex2ivertex2, ivertex2vertices2
	
	cdef void _compute_face_normals(self, faces):
		cdef _Face face
		for face in faces: face._compute_normal()
		
	cdef void _compute_vertex_normals(self, faces, vertex2ivertex, ivertex2vertices):
		cdef _Vertex vertex, ivertex
		for ivertex in ivertex2vertices.keys():
			for vertex in ivertex2vertices[ivertex]:
				if vertex._face._option & FACE2_SMOOTH_LIT:
					if ivertex._normal is None: ivertex._normal = Vector(vertex._face.get_root())
					vertex._face._compute_normal() # Needed ? Or already done ?
					ivertex._normal.add_mul_vector(vertex._angle_at(), vertex._face._normal)
					
	cdef void _compute_face_neighbors(self, faces, vertex2ivertex, ivertex2vertices, int* neighbor, signed char* neighbor_side):
		# 2 faces are neighbors <=> they share 2 vertices.
		cdef int          i, j, v1_neighbor_index, v2_neighbor_index
		cdef _Vertex      v1, v2, v1_neighbor, v2_neighbor
		cdef _Face        face
		
		i = 0
		face2index = {}
		for face in faces:
			face2index[face] = i
			i = i + 1
			
		for face in faces:
			for i from 0 <= i < len(face.vertices):
				neighbor[i] = -1 # default value meaning 'no neighbor'
				
				v1 = vertex2ivertex[face.vertices[i]]
				v2 = vertex2ivertex[((i + 1 < len(face.vertices)) and face.vertices[i + 1]) or face.vertices[0]]
				
				for v1_neighbor in ivertex2vertices[v1]:
					#if (not v1_neighbor._face is face) and (face.normal.angle_to(v1_neighbor._face.normal) < angle):
					
					# A double sided face cannot be the neighbor of a non-double sided face
					if (face._option & FACE2_DOUBLE_SIDED) != (v1_neighbor._face._option & FACE2_DOUBLE_SIDED): continue
					
					if not v1_neighbor._face is face:
						for v2_neighbor in v1_neighbor._face.vertices:
							if vertex2ivertex[v2_neighbor] is v2:
								# one neighbor found
								neighbor[i] = face2index[v1_neighbor._face]
								
								if face._option & FACE2_DOUBLE_SIDED: # Check for "backside-neighbor"
									v1_neighbor_index = v1_neighbor._face.vertices.index(v1_neighbor)
									v2_neighbor_index = v1_neighbor._face.vertices.index(v2_neighbor)
									if (v1_neighbor_index == v2_neighbor_index - 1) or ((v1_neighbor_index > 1) and (v2_neighbor_index == 0)): # Same rotation sens
										neighbor_side[i] = 1
									else: neighbor_side[i] = -1
									
								else: neighbor_side[i] = 1
								break
						else: continue
						break
					
			if len(face.vertices) < 4: neighbor[3] = -1 # triangle can have only 3 neighbors
			neighbor      = neighbor      + 4
			neighbor_side = neighbor_side + 4
			
	def __init__(self, _World world, float angle, int option, lights):
		cdef CoordSyst coordsyst
		cdef object    faces
		cdef _Face     face
		cdef _Vertex   vertex, ivertex
		cdef Chunk*    chunk
		cdef int       i
		chunk = chunk_new() # Do NOT use get_chunk() since we will keep the content of the chunk and drop the structure !!!
		
		self._materials = []
		
		# Collect faces
		# XXX collect models too (by loading the corresponding world)
		faces = []
		for coordsyst in world.recursive():
			if isinstance(coordsyst, _Face) and not(coordsyst._option & HIDDEN): faces.append(coordsyst)
			
		# check for additional options
		self._option = self._option | option
		if lights: self._option = self._option | (MODEL_STATIC_LIT + MODEL_EMISSIVES)
		
		for face in faces:
			for vertex in face._vertices:
				if (not face._material._texture is None) and ((vertex._tex_x != 0.0) or (vertex._tex_y != 0.0)): self._option = self._option | MODEL_TEXCOORDS
				if not vertex._diffuse  is None: self._option = self._option | MODEL_DIFFUSES
				if not vertex._emissive is None: self._option = self._option | MODEL_EMISSIVES
				
		self._compute_face_normals(faces)
		vertex2ivertex, ivertex2vertices = self._identify_vertices(faces, angle)
		self._compute_vertex_normals(faces, vertex2ivertex, ivertex2vertices)
		
		# creates vertex coords and normals -- process ivertex with normal first (memory optimization)
		i = 0
		ivertices = []
		ivertex2index = {}
		for ivertex in ivertex2vertices.keys():
			if not ivertex._normal is None:
				ivertices.append(ivertex)
				ivertex2index[ivertex] = i
				i = i + 1
		self._vnormals = <float*> malloc(len(ivertices) * 3 * sizeof(float))
		for ivertex in ivertex2vertices.keys():
			if ivertex._normal is None:
				ivertices.append(ivertex)
				ivertex2index[ivertex] = i
				i = i + 1
		self._coords = <float*> malloc(len(ivertices) * 3 * sizeof(float))
		for ivertex in ivertices: self._add_coord(ivertex)
		
		# creates the faces
		self._faces = <ModelFace*> malloc(len(faces) * sizeof(ModelFace))
		for face in faces: self._add_face(face, vertex2ivertex, ivertex2index, lights, self._option & MODEL_STATIC_SHADOW)
		
		# avoid SimpleModel.material.append(...)
		self._materials = tuple(self._materials)
		
		# find face neighbors
		if self._option & MODEL_NEIGHBORS:
			self._neighbors      = <int *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(char))
			self._compute_face_neighbors(faces, vertex2ivertex, ivertex2vertices, self._neighbors, self._neighbors_side)
			
		# find face simple neighbors (doesn't take angle into account)
		if self._option & MODEL_SIMPLE_NEIGHBORS:
			# Re-identify vertices, because for simple neighbors we don't take angle into account
			vertex2ivertex, ivertex2vertices = self._identify_vertices(faces, 360.0)
			self._simple_neighbors      = <int *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._simple_neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(char))
			self._compute_face_neighbors(faces, vertex2ivertex, ivertex2vertices, self._simple_neighbors, self._simple_neighbors_side)
			
		# TO DO ?
		#self._compute_dimension()
		
	cdef void _build_sphere(self):
		if self._nb_coords > 0:
			self._sphere = <float*> malloc(4 * sizeof(float))
			sphere_from_points(self._sphere, self._coords, self._nb_coords)
			self._option = self._option | MODEL_HAS_SPHERE
			
			
	cdef void _build_display_list(self):
		cdef DisplayLists* display_lists
		cdef DisplayList*  display_list
		cdef ModelFace*    face
		cdef int           nb, i, j, k
		cdef Chunk*        chunk
		
		display_lists = <DisplayLists*> malloc(sizeof(DisplayLists))
		display_lists.nb_opaque_list = display_lists.nb_alpha_list = 0
		nb = 0
		display_lists.display_lists = NULL
		for k from 0 <= k < 2:
			for j from 0 <= j < self._nb_faces:
				face = self._faces + j
				if ((face.option & FACE_ALPHA) and (k == 1)) or ((not(face.option & FACE_ALPHA)) and (k == 0)):
					for i from 0 <= i < nb:
						display_list = display_lists.display_lists + i
						if (display_list.material_id == face.pack.material_id) and (display_list.option == (face.option & DISPLAY_LIST_OPTIONS)):
							chunk_add_int(display_list.chunk, j)
							break
					else:
						display_lists.display_lists = <DisplayList*> realloc(display_lists.display_lists, (nb + 1) * sizeof(DisplayList))
						display_list = display_lists.display_lists + nb
						display_list.material_id = face.pack.material_id
						display_list.option      = face.option & DISPLAY_LIST_OPTIONS
						display_list.chunk       = chunk_new()
						chunk_add_int(display_list.chunk, j)
						if display_list.option & FACE_ALPHA: display_lists.nb_alpha_list  = display_lists.nb_alpha_list  + 1
						else:                                display_lists.nb_opaque_list = display_lists.nb_opaque_list + 1
						nb = nb + 1
						
		for i from 0 <= i < nb:
			display_list = display_lists.display_lists + i
			chunk_add_int(display_list.chunk, -1) # -1 means end
			display_list.faces_id = <int*> (display_list.chunk.content)
			free(display_list.chunk)
			
		# XXX sort display list by material ?
			
		self._display_lists = display_lists
		self._option = self._option | MODEL_DISPLAY_LISTS
		
	cdef void _init_display_list(self):
		cdef DisplayList*  display_list
		cdef ModelFace*    face
		cdef int i, nb, j
		#model_option_activate(self._option) # XXX usefull ? not put in the display list, but may modify the data stored in it ???
		nb = self._display_lists.nb_opaque_list + self._display_lists.nb_alpha_list
		display_list = self._display_lists.display_lists
		
		for i from 0 <= i < nb:
			display_list = self._display_lists.display_lists + i
			display_list.id = glGenLists(1)
			(<_Material> (<void*> (display_list.material_id)))._activate()
			face_option_activate(display_list.option)
			glNewList(display_list.id, GL_COMPILE)
			
			if   display_list.option & FACE_TRIANGLE: glBegin(GL_TRIANGLES)
			elif display_list.option & FACE_QUAD:     glBegin(GL_QUADS)
			else:
				print "Model supports only triangle or quad faces !"
				raise ValueError("Model supports only triangle or quad faces !")
			
			for j from 0 <= j < self._nb_faces:
				face = self._faces + j
				if ((face.option & DISPLAY_LIST_OPTIONS) == display_list.option) and (face.pack.material_id == display_list.material_id):
					if face.option & FACE_QUAD: self._render_quad    (face)
					else:                       self._render_triangle(face)
					
			glEnd()
			glEndList()
			face_option_inactivate(display_list.option)
		#model_option_inactivate(self._option)
		self._option = self._option | MODEL_INITED
		
	def __dealloc__(self):
		cdef DisplayList*  display_list
		cdef int i, nb
		
		if (self._option & MODEL_DISPLAY_LISTS) and (self._option & MODEL_INITED):
			nb = self._display_lists.nb_opaque_list + self._display_lists.nb_alpha_list
			display_list = self._display_lists.display_lists
			for i from 0 <= i < nb:
				display_list = self._display_lists.display_lists + i
				glDeleteLists(display_list.id, 1)
				
		free(self._coords)
		
		if not self.option & MODEL_SHARED_DATA:
			free(self._faces)
			free(self._vnormals)
			free(self._colors)
			free(self._values)
			free(self._vertex_coords)
			if self._option & MODEL_VERTEX_OPTIONS: free(self._vertex_options)
			if self._option & MODEL_TEXCOORDS:      free(self._vertex_texcoords)
			if self._option & MODEL_DIFFUSES:       free(self._vertex_diffuses)
			if self._option & MODEL_EMISSIVES:      free(self._vertex_emissives)
			if self._option & MODEL_HAS_SPHERE:     free(self._sphere)
			
	cdef void _batch(self, _Body body):
		if body._option & HIDDEN: return
		
		#cdef Frustum* frustum
		#frustum = renderer._frustum(body)
		#if (self._option & MODEL_HAS_SPHERE) and (sphere_in_frustum(frustum, self._sphere) == 0): return
		cdef float sphere[4]
		if self._option & MODEL_HAS_SPHERE:
			sphere_by_matrix_copy(sphere, self._sphere, body._root_matrix())
			if sphere_in_frustum(renderer.root_frustum, sphere) == 0: return
		
		if self._display_lists.nb_opaque_list != 0: renderer._batch(renderer.opaque, self, body, NULL)
		if self._display_lists.nb_alpha_list  != 0: renderer._batch(renderer.alpha , self, body, NULL)
		
	# Not used by _SimpleModel, but by subclasses (like _TreeModel or _CellShadingModel)
	cdef void _batch_face(self, ModelFace* face):
		# XXX inline this func
		# XXX add a face option in order to know if the face has only invisible vertices
		# XXX add a face option in order to know if the face has at least one alpha vertices
		if self._option & MODEL_VERTEX_OPTIONS:
			if ((self._vertex_options[face.v[0]] & VERTEX_INVISIBLE) and
					(self._vertex_options[face.v[1]] & VERTEX_INVISIBLE) and
					(self._vertex_options[face.v[2]] & VERTEX_INVISIBLE) and
					((face.option & FACE_TRIANGLE) or (self._vertex_options[face.v[3]] & VERTEX_INVISIBLE))):
				return
				 
			if ((self._vertex_options[face.v[0]] & VERTEX_ALPHA) or
					(self._vertex_options[face.v[1]] & VERTEX_ALPHA) or
					(self._vertex_options[face.v[2]] & VERTEX_ALPHA) or
					((face.option & FACE_QUAD) and (self._vertex_options[face.v[3]] & VERTEX_ALPHA))):
				
				pack_batch_face(pack_get_alpha(face.pack), face, 0)
				return
			
		pack_batch_face(face.pack, face, 0)
		
	cdef void _render(self, _Body body):
		cdef DisplayList*  display_list
		cdef ModelFace*    face
		cdef int i, j, start, end
		
		model_option_activate(self._option) # XXX put this in the display list ?
		if body._option & LEFTHANDED: glFrontFace(GL_CW)
		
		if self._option & MODEL_DISPLAY_LISTS:
			if not(self._option & MODEL_INITED): self._init_display_list()
			if renderer.state == RENDERER_STATE_OPAQUE:
				start = 0
				end   = self._display_lists.nb_opaque_list
			else:
				start = self._display_lists.nb_opaque_list
				end   = start + self._display_lists.nb_alpha_list
			for i from start <= i < end:
				display_list = self._display_lists.display_lists + i
				face_option_activate(display_list.option)
				(<_Material> (<void*> (display_list.material_id)))._activate()        
				glCallList(display_list.id)
				face_option_inactivate(display_list.option)
				
		else:
			if renderer.state == RENDERER_STATE_OPAQUE:
				start = 0
				end   = self._display_lists.nb_opaque_list
			else:
				start = self._display_lists.nb_opaque_list
				end   = start + self._display_lists.nb_alpha_list
			for i from start <= i < end:
				display_list = self._display_lists.display_lists + i
				face_option_activate(display_list.option)
				(<_Material> (<void*> (display_list.material_id)))._activate()        
				
				if   display_list.option & FACE_TRIANGLE: glBegin(GL_TRIANGLES)
				elif display_list.option & FACE_QUAD:     glBegin(GL_QUADS)
				else:
					print "Model supports only triangle or quad faces !"
					raise ValueError("Model supports only triangle or quad faces !")
				
				for j from 0 <= j < self._nb_faces:
					face = self._faces + j
					if ((face.option & DISPLAY_LIST_OPTIONS) == display_list.option) and (face.pack.material_id == display_list.material_id):
						if face.option & FACE_QUAD: self._render_quad    (face)
						else:                       self._render_triangle(face)
						
				glEnd()
				
				face_option_inactivate(display_list.option)
				
		if body._option & LEFTHANDED:	glFrontFace(GL_CCW)
		model_option_inactivate(self._option)
		
	cdef void _raypick(self, RaypickData data, CoordSyst parent):
		cdef float* raydata
		cdef int    i
		raydata = parent._raypick_data(data)
		if (self._option & MODEL_HAS_SPHERE) and (sphere_raypick(raydata, self._sphere) == 0): return
		for i from 0 <= i < self._nb_faces:
			self._face_raypick(self._faces + i, raydata, data, parent)
			
	cdef int _raypick_b(self, RaypickData data, CoordSyst parent):
		cdef float* raydata
		cdef int    i
		raydata = parent._raypick_data(data)
		if (self._option & MODEL_HAS_SPHERE) and (sphere_raypick(raydata, self._sphere) == 0): return 0
		for i from 0 <= i < self._nb_faces:
			if self._face_raypick_b(self._faces + i, raydata, data): return 1
		return 0
	
	cdef void _face_raypick(self, ModelFace* face, float* raydata, RaypickData data, CoordSyst parent):
		# XXX inline this func ?
		cdef float z, root_z
		cdef int   r
		
		if  face.option & FACE_NON_SOLID: return
		if (face.option & FACE_DOUBLE_SIDED) and (data.option & RAYPICK_CULL_FACE): data.option = data.option - RAYPICK_CULL_FACE # XXX weird... where RAYPICK_CULL_FACE is added back ?
		if  face.option & FACE_QUAD:
			r = quad_raypick    (raydata, self._coords + self._vertex_coords[face.v[0]], self._coords + self._vertex_coords[face.v[1]], self._coords + self._vertex_coords[face.v[2]], self._coords + self._vertex_coords[face.v[3]], self._values + face.normal, data.option, &z)
		else:
			r = triangle_raypick(raydata, self._coords + self._vertex_coords[face.v[0]], self._coords + self._vertex_coords[face.v[1]], self._coords + self._vertex_coords[face.v[2]], self._values + face.normal, data.option, &z)
			
		if r != 0:
			root_z = parent._distance_out(z)
			if (data.result_coordsyst is None) or (fabs(root_z) < fabs(data.root_result)):
				data.result      = z
				data.root_result = root_z
				data.result_coordsyst = parent
				if   r == RAYPICK_DIRECT: memcpy(&data.normal[0], self._values + face.normal, 3 * sizeof(float))
				elif r == RAYPICK_INDIRECT:
					if face.option & FACE_DOUBLE_SIDED:
						data.normal[0] = -(self._values + face.normal)[0]
						data.normal[1] = -(self._values + face.normal)[1]
						data.normal[2] = -(self._values + face.normal)[2]
					else: memcpy(&data.normal[0], self._values + face.normal, 3 * sizeof(float))
				
	cdef int _face_raypick_b(self, ModelFace* face, float* raydata, RaypickData data):
		# XXX inline this func ?
		cdef float   z
		
		if  face.option & FACE_NON_SOLID: return 0
		if (face.option & FACE_DOUBLE_SIDED) and (data.option & RAYPICK_CULL_FACE): data.option = data.option - RAYPICK_CULL_FACE # XXX weird... where RAYPICK_CULL_FACE is added back ?
		if  face.option & FACE_QUAD:
			if quad_raypick    (raydata, self._coords + self._vertex_coords[face.v[0]], self._coords + self._vertex_coords[face.v[1]], self._coords + self._vertex_coords[face.v[2]], self._coords + self._vertex_coords[face.v[3]], self._values + face.normal, data.option, &z) != 0: return 1
		else:
			if triangle_raypick(raydata, self._coords + self._vertex_coords[face.v[0]], self._coords + self._vertex_coords[face.v[1]], self._coords + self._vertex_coords[face.v[2]], self._values + face.normal, data.option, &z) != 0: return 1
		return 0
	
	cdef void _collect_raypickables(self, Chunk* items, float* rsphere, float* sphere, CoordSyst parent):
		if not(self._option & MODEL_HAS_SPHERE) or (sphere_distance_sphere(sphere, self._sphere) < 0.0):
			chunk_add_ptr(items, <void*> parent)
			
	cdef void _render_triangle(self, ModelFace* face):
		if not(face.option & FACE_SMOOTH_LIT): glNormal3fv(self._values + face.normal) # face normal
		self._render_vertex(face.v[0], face.option) # render each vertex
		self._render_vertex(face.v[1], face.option)
		self._render_vertex(face.v[2], face.option)
		
	cdef void _render_quad(self, ModelFace* face):
		if not(face.option & FACE_SMOOTH_LIT): glNormal3fv(self._values + face.normal) # face normal
		self._render_vertex(face.v[0], face.option) # render each vertex
		self._render_vertex(face.v[1], face.option)
		self._render_vertex(face.v[2], face.option)
		self._render_vertex(face.v[3], face.option)
		
	cdef void _render_vertex(self, int index, int face_option):
		if self._option & MODEL_DIFFUSES : glColor4fv   (self._colors   + self._vertex_diffuses [index])
		if self._option & MODEL_EMISSIVES: glMaterialfv (GL_FRONT_AND_BACK, GL_EMISSION, self._colors + self._vertex_emissives[index]) # XXX use glColorMaterial when emissive color but no diffuse ?
		if self._option & MODEL_TEXCOORDS: glTexCoord2fv(self._values   + self._vertex_texcoords[index])
		if face_option & FACE_SMOOTH_LIT : glNormal3fv  (self._vnormals + self._vertex_coords   [index])
		glVertex3fv(self._coords + self._vertex_coords[index])
		






	cdef int _shadow(self, CoordSyst coord_syst, _Light light):
		if not(self._option & MODEL_SHADOW): return 0
		
		cdef int      displaylist
		cdef Frustum* frustum
		cdef float    coord[4]
		cdef float    cone[9]
		cdef float    b
		
		b = renderer.current_camera._back
		light._cast_into(coord_syst)
		if light._w == 0.0: # Directional light
			cone_from_sphere_and_vector(cone, self._sphere, light._data, b)
		else:
			if cone_from_sphere_and_origin(cone, self._sphere, light._data, b) == 0: return 0
			
		frustum = renderer._frustum(coord_syst)
		coord[0] = 0.5 * (frustum.points[0] + frustum.points[6])
		coord[1] = 0.5 * (frustum.points[1] + frustum.points[7])
		coord[2] = 0.5 * (frustum.points[2] + frustum.points[8])
		coord[3] = point_distance_to(coord, frustum.points)
		
		if (coord_syst._option & COORDSYS_STATIC) and (light._option & COORDSYS_STATIC):
			
			if sphere_is_in_cone(coord, cone): # The camera is inside the shadow, special case
				return self._build_shadow(coord_syst, light, 1, SHADOW_DISPLAY_LIST)
			
			else:
				displaylist = light._static_shadow_displaylists.get(coord_syst, -1)
				if displaylist == -1:
					displaylist = light._static_shadow_displaylists[coord_syst] = glGenLists(1)
					
					#glNewList(displaylist, GL_COMPILE_AND_EXECUTE)
					self._build_shadow(coord_syst, light, 0, displaylist)
					#glEndList()
					
				else:
					glStencilFunc(GL_ALWAYS, 1, 0xFFFFFFFF)
					glFrontFace  (GL_CW)
					glStencilOp  (GL_KEEP, GL_KEEP, GL_INCR)
					glLoadMatrixf(coord_syst._render_matrix)
					glCallList   (displaylist)
					
					glFrontFace  (GL_CCW)
					glStencilOp  (GL_KEEP, GL_KEEP, GL_DECR)
					glCallList   (displaylist)
					
			return 1
			
		else:
			displaylist = light._static_shadow_displaylists.get(coord_syst, -1)
			if displaylist != -1:
				del light._static_shadow_displaylists[coord_syst]
				
			return self._build_shadow(coord_syst, light, sphere_is_in_cone(coord, cone), SHADOW_DISPLAY_LIST)
		
			
	cdef int _build_shadow(self, CoordSyst coord_syst, _Light light, int camera_inside_shadow, int displaylist):
		if not(self._option & MODEL_SHADOW): return 0
		
		#cdef Frustum*     frustum
		cdef ModelFace*   face, *neighbor_face
		cdef float*       coord_ptr, *normal
		cdef double*      coord_ptrd
		cdef float        coord[4]
		#cdef float        cone[9]
		cdef float        b
		cdef int          nbv, i, j, k, p1, p2, nb_inter, nb_segment
		cdef int*         neighbors
		cdef signed char* neighbors_side
		
		cdef Chunk*       chunk, *chunk2
		cdef float        fp1[3], fp2[3], inter1[3], inter2[3], face_data[15]
		cdef float        plane[4]
		cdef float        v1[3], v2[3]
		cdef int          nb_points[3]
		
		b = renderer.current_camera._back
		
		# Tag all faces front or back, for the given light
		
		#light._cast_into(coord_syst)
		if light._w == 0.0: # Directional light
			#cone_from_sphere_and_vector(cone, self._sphere, light._data, b)
			for i from 0 <= i < self._nb_faces:
				face = self._faces + i
				if self._option & MODEL_VERTEX_OPTIONS:
					if ((self._vertex_options[face.v[0]] & VERTEX_INVISIBLE) and
							(self._vertex_options[face.v[1]] & VERTEX_INVISIBLE) and
							(self._vertex_options[face.v[2]] & VERTEX_INVISIBLE) and
							((face.option & FACE_TRIANGLE) or (self._vertex_options[face.v[3]] & VERTEX_INVISIBLE))):
						continue
					
				if vector_dot_product(light._data, self._values + face.normal) >= 0.0:
					face.option = (face.option & ~FACE_LIGHT_FRONT) | FACE_LIGHT_BACK
				else:
					face.option = (face.option & ~FACE_LIGHT_BACK ) | FACE_LIGHT_FRONT
					
		else:
			#if cone_from_sphere_and_origin(cone, self._sphere, light._data, b) == 0: return 0
			for i from 0 <= i < self._nb_faces:
				face = self._faces + i
				if self._option & MODEL_VERTEX_OPTIONS:
					if ((self._vertex_options[face.v[0]] & VERTEX_INVISIBLE) and
							(self._vertex_options[face.v[1]] & VERTEX_INVISIBLE) and
							(self._vertex_options[face.v[2]] & VERTEX_INVISIBLE) and
							((face.option & FACE_TRIANGLE) or (self._vertex_options[face.v[3]] & VERTEX_INVISIBLE))):
						continue
					
				normal = self._values + face.normal
				if light._data[0] * normal[0] + light._data[1] * normal[1] + light._data[2] * normal[2] + normal[3] > 0.0:
					face.option = (face.option & ~FACE_LIGHT_BACK ) | FACE_LIGHT_FRONT
				else:
					face.option = (face.option & ~FACE_LIGHT_FRONT) | FACE_LIGHT_BACK
					
		# draw shadow body 1rst step
		glStencilFunc(GL_ALWAYS, 1, 0xFFFFFFFF)
		glFrontFace  (GL_CW)
		glStencilOp  (GL_KEEP, GL_KEEP, GL_INCR)
		glLoadMatrixf(coord_syst._render_matrix)
		glNewList    (displaylist, GL_COMPILE_AND_EXECUTE)
		
		# test if camera is inside the shadow
		#frustum = renderer._frustum(coord_syst)
		#coord[0] = 0.5 * (frustum.points[0] + frustum.points[6])
		#coord[1] = 0.5 * (frustum.points[1] + frustum.points[7])
		#coord[2] = 0.5 * (frustum.points[2] + frustum.points[8])
		#coord[3] = point_distance_to(coord, frustum.points)
		#if sphere_is_in_cone(coord, cone):
		if camera_inside_shadow == 1:
			# camera is inside the shadow => special case 
			# we must draw the intersection of the shadow body with the camera front plane
			
			plane[0], plane[1], plane[2], plane[3] = 0.0, 0.0, -1.0, -0.1 - renderer.current_camera._front
			
			chunk    = get_chunk()
			chunk2   = get_chunk()
			nb_inter = nb_segment = 0
			
			# find edges and draw shadow body
			for i from 0 <= i < self._nb_faces:
				face = self._faces + i
				
				if (face.option & FACE_LIGHT_BACK) or (face.option & FACE_DOUBLE_SIDED):
					# test if neighbors are front
					neighbors      = self._simple_neighbors      + (4 * i)
					neighbors_side = self._simple_neighbors_side + (4 * i)
					if face.option & FACE_QUAD: nbv = 4
					else:                       nbv = 3
					
					for k from 0 <= k < nbv:
						neighbor_face = self._faces + neighbors[k]
						
						if (
							(not (face.option & FACE_DOUBLE_SIDED) and ((neighbors[k] == -1) or (neighbor_face.option & FACE_LIGHT_FRONT)))
							or
							(    (face.option & FACE_DOUBLE_SIDED) and ((neighbors[k] == -1) or (((
								(neighbors_side[k] == -1) and (((face.option & FACE_LIGHT_FRONT) and (neighbor_face.option & FACE_LIGHT_BACK )) or ((face.option & FACE_LIGHT_BACK) and (neighbor_face.option & FACE_LIGHT_FRONT)))
									) or (
								(neighbors_side[k] ==  1) and (((face.option & FACE_LIGHT_FRONT) and (neighbor_face.option & FACE_LIGHT_FRONT)) or ((face.option & FACE_LIGHT_BACK) and (neighbor_face.option & FACE_LIGHT_BACK)))
							)))))):
							
							if face.option & FACE_LIGHT_BACK:
								p1 = k 
								if k < nbv - 1: p2 = k + 1
								else:           p2 = 0
							else: # Trace in reverse order
								if k < nbv - 1: p1 = k + 1
								else:           p1 = 0
								p2 = k
								
							nb_segment = nb_segment + 1
							chunk_add(chunk, self._coords + self._vertex_coords[face.v[p1]], 3 * sizeof(float))
							chunk_add(chunk, self._coords + self._vertex_coords[face.v[p2]], 3 * sizeof(float))
							chunk_add_int(chunk, -1)
							
			# Joins the segments
			joined = {}
			for i from 0 <= i < nb_segment:
				for j from 0 <= j < nb_segment:
					if i == j: continue
					if joined.has_key(j): continue
					
					if memcmp(chunk.content + i * (6 * sizeof(float) + sizeof(int)) + 3 * sizeof(float), chunk.content + j * (6 * sizeof(float) + sizeof(int)), 3 * sizeof(float)) == 0:
						(<int*> (chunk.content + (i * (6 * sizeof(float) + sizeof(int)) + 6 * sizeof(float))))[0] = j
						
						joined[j] = 1
						
						break
				else:
					print "* Soya * warning : drawing shadow for non-closed model (can't join segments)!"
					
			glLoadIdentity()
			i = 0
			for k from 0 <= k < nb_segment:
				if i == -1: break # error, was not able to join segments
				coord_ptr = <float*> (chunk.content + i * (6 * sizeof(float) + sizeof(int)))
				
				i = (<int*> (chunk.content + (i * (6 * sizeof(float) + sizeof(int)) + 6 * sizeof(float))))[0]
				
				memcpy(&fp1[0], coord_ptr    , 3 * sizeof(float))
				memcpy(&fp2[0], coord_ptr + 3, 3 * sizeof(float))
				
				if light._w == 0.0: # Directional light
					memcpy(&v1[0], &light._data[0], 3 * sizeof(float))
					memcpy(&v2[0], &light._data[0], 3 * sizeof(float))
				else:
					v1[0] = fp1[0] - light._data[0]
					v1[1] = fp1[1] - light._data[1]
					v1[2] = fp1[2] - light._data[2]
					vector_normalize(v1)
					
					v2[0] = fp2[0] - light._data[0]
					v2[1] = fp2[1] - light._data[1]
					v2[2] = fp2[2] - light._data[2]
					vector_normalize(v2)
					
				
				point_by_matrix(fp1, coord_syst._root_matrix())
				point_by_matrix(fp1, renderer.current_camera._inverted_root_matrix())
				
				point_by_matrix(fp2, coord_syst._root_matrix())
				point_by_matrix(fp2, renderer.current_camera._inverted_root_matrix())
				
				vector_by_matrix(v1, coord_syst._root_matrix())
				vector_by_matrix(v1, renderer.current_camera._inverted_root_matrix())
				
				vector_by_matrix(v2, coord_syst._root_matrix())
				vector_by_matrix(v2, renderer.current_camera._inverted_root_matrix())
				
				segment_projection_intersect_plane(fp1, v1, fp2, v2, b, plane, inter1, inter2, face_data, nb_points)
				
				glBegin(GL_POLYGON)
				for j from 0 <= j < nb_points[0]:
					glVertex3fv(&face_data[0] + j * 3)
				glEnd()
				
				if nb_points[1]:
					chunk_add_double(chunk2, <double> (inter1[0]))
					chunk_add_double(chunk2, <double> (inter1[1]))
					chunk_add_double(chunk2, <double> (inter1[2]))
					nb_inter = nb_inter + 1
					
				if nb_points[2]:
					chunk_add_double(chunk2, <double> (inter2[0]))
					chunk_add_double(chunk2, <double> (inter2[1]))
					chunk_add_double(chunk2, <double> (inter2[2]))
					nb_inter = nb_inter + 1
				
				
				
			glLoadMatrixf(coord_syst._render_matrix)
					
			glEndList()
			
			
			# draw shadow body 3rd step
			glDisable(GL_CULL_FACE)
			glLoadIdentity()
			gluTessBeginPolygon(SHADOW_TESS, NULL)
			gluTessBeginContour(SHADOW_TESS)
			for i from 0 <= i < nb_inter:
				gluTessVertex(SHADOW_TESS, (<double*> chunk2.content) + i * 3, (<double*> chunk2.content) + i * 3)
			gluTessEndContour(SHADOW_TESS)
			gluTessEndPolygon(SHADOW_TESS)
			glLoadMatrixf(coord_syst._render_matrix)
			glEnable(GL_CULL_FACE)
			
			
			# draw shadow body 2nd step
			glFrontFace(GL_CCW)
			glStencilOp(GL_KEEP, GL_KEEP, GL_DECR)
			glCallList (displaylist)
			
			
			# Cleaning
			
			# Free the double[3] created by model_shadow_tess_combine
			i = SHADOW_TESS_CHUNK.nb
			SHADOW_TESS_CHUNK.nb = 0
			while SHADOW_TESS_CHUNK.nb < i: free(chunk_get_ptr(SHADOW_TESS_CHUNK))
			
			SHADOW_TESS_CHUNK.nb = 0 # reset the chunk
			
			drop_chunk(chunk)
			drop_chunk(chunk2)


			
		else:
			# find edges and draw shadow body
			glBegin(GL_QUADS)
			for i from 0 <= i < self._nb_faces:
				face = self._faces + i
				
				if (face.option & FACE_LIGHT_BACK) or (face.option & FACE_DOUBLE_SIDED):
					neighbors      = self._simple_neighbors      + (4 * i)
					neighbors_side = self._simple_neighbors_side + (4 * i)
					if face.option & FACE_QUAD: nbv = 4
					else:                       nbv = 3
					
					for k from 0 <= k < nbv:
						neighbor_face = self._faces + neighbors[k]
						
						if (
							(not (face.option & FACE_DOUBLE_SIDED) and ((neighbors[k] == -1) or (neighbor_face.option & FACE_LIGHT_FRONT)))
							or
							(    (face.option & FACE_DOUBLE_SIDED) and ((neighbors[k] == -1) or (((
								(neighbors_side[k] == -1) and (((face.option & FACE_LIGHT_FRONT) and (neighbor_face.option & FACE_LIGHT_BACK )) or ((face.option & FACE_LIGHT_BACK) and (neighbor_face.option & FACE_LIGHT_FRONT)))
									) or (
								(neighbors_side[k] ==  1) and (((face.option & FACE_LIGHT_FRONT) and (neighbor_face.option & FACE_LIGHT_FRONT)) or ((face.option & FACE_LIGHT_BACK) and (neighbor_face.option & FACE_LIGHT_BACK)))
							)))))):
								
							if face.option & FACE_LIGHT_BACK:
								p1 = k 
								if k < nbv - 1: p2 = k + 1
								else:           p2 = 0
							else: # Trace in reverse order
								if k < nbv - 1: p1 = k + 1
								else:           p1 = 0
								p2 = k
							
							coord_ptr = self._coords + self._vertex_coords[face.v[p1]]
							glVertex3fv(coord_ptr)
							
							# push coord far away
							if light._w == 0.0: # Directional light
								glVertex3f(coord_ptr[0] + b * light._data[0], coord_ptr[1] + b * light._data[1], coord_ptr[2] + b * light._data[2])
							else:
								coord[0] = coord_ptr[0] - light._data[0]
								coord[1] = coord_ptr[1] - light._data[1]
								coord[2] = coord_ptr[2] - light._data[2]
								vector_normalize(coord)
								glVertex3f(coord_ptr[0] + b * coord[0], coord_ptr[1] + b * coord[1], coord_ptr[2] + b * coord[2])
								
							coord_ptr = self._coords + self._vertex_coords[face.v[p2]]
							
							# push coord far away
							if light._w == 0.0: # Directional light
								glVertex3f(coord_ptr[0] + b * light._data[0], coord_ptr[1] + b * light._data[1], coord_ptr[2] + b * light._data[2])
							else:
								coord[0] = coord_ptr[0] - light._data[0]
								coord[1] = coord_ptr[1] - light._data[1]
								coord[2] = coord_ptr[2] - light._data[2]
								vector_normalize(coord)
								glVertex3f(coord_ptr[0] + b * coord[0], coord_ptr[1] + b * coord[1], coord_ptr[2] + b * coord[2])
								
							glVertex3fv(coord_ptr)
							
							
			glEnd    ()
			glEndList() # XXX This line bugs on blam's computer
			
			# draw shadow body 2nd step
			glFrontFace(GL_CCW)
			glStencilOp(GL_KEEP, GL_KEEP, GL_DECR)
			glCallList (displaylist)
			
			
			
			
		return 1
	





#ctypedef struct _VertexBufferModelFace:
#  int      option
#  Pack*    pack
#  float    normal[4] # normal[3] is optional (for shadows)
#  int      v[4]      # v[3]      is optional (only for quad, unused for triangle)

#ctypedef struct _VertexBufferModelFaceGroup:
#  int       option
#  int       start, nb_triangles
#  uintptr_t material_id

cdef class _VertexBufferedModel(_Model):
	#cdef int           _option
	#cdef               _materials
	#cdef float*        _sphere
	#cdef int           _nb_faces, _nb_quads, _nb_vertices
	#cdef float*        _coords, *_vnormals, *_diffuses, *_emissives, *_texcoords, *_texcoords2
	#cdef int*          _vertexids
	#cdef char*         _vertex_options
	
	#cdef VertexBufferModelFace* _faces
	#cdef int*                   _neighbors, *_simple_neighbors
	#cdef signed char*           _neighbors_side, *_simple_neighbors_side
	
	#cdef int                          _nb_opaque_face_groups
	#cdef int                          _nb_face_groups
	#cdef int*                         _face_group_vertices
	#cdef _VertexBufferModelFaceGroup* _face_groups
	
	#cdef GLuint        _vertex_buffer, _texcoords2_buffer, _face_buffer
	#cdef int           _buffer_sizeof_vertex
	#cdef int           _vnormal_offset, _diffuse_offset, _emissive_offset, _texcoord_offset
	
	def __dealloc__(self):
		free(self._faces)
		free(self._coords)
		free(self._vnormals)
		free(self._vertexids)
		free(self._face_group_vertices)
		free(self._face_groups)
		if self._option & MODEL_VERTEX_OPTIONS:   free(self._vertex_options)
		if self._option & MODEL_TEXCOORDS:        free(self._texcoords)
		if self._option & MODEL_TEXCOORDS2:       free(self._texcoords2)
		if self._option & MODEL_DIFFUSES:         free(self._diffuses)
		if self._option & MODEL_EMISSIVES:        free(self._emissives)
		if self._option & MODEL_HAS_SPHERE:       free(self._sphere)
		if self._option & MODEL_NEIGHBORS:        free(self._neighbors); free(self._neighbors_side)
		if self._option & MODEL_SIMPLE_NEIGHBORS: free(self._simple_neighbors); free(self._simple_neighbors_side)
		if self._option & MODEL_INITED:
			glDeleteBuffers(1, &self._face_buffer)
			glDeleteBuffers(1, &self._vertex_buffer)
			if self._option & MODEL_TEXCOORDS2: glDeleteBuffers(1, &self._texcoords2_buffer)
			
	cdef __getcstate__(self):
		cdef Chunk*                       chunk
		cdef int                          i
		cdef _VertexBufferModelFace*      face
		cdef _VertexBufferModelFaceGroup* face_group
		cdef                              material_id2index
		cdef uintptr_t                    ptr
		
		material_id2index = {}
		for i from 0 <= i < len(self._materials):
			ptr = id(self._materials[i]) # Required for Python 2.4
			material_id2index[ptr] = i
			
		chunk = get_chunk()
		chunk_add_int_endian_safe   (chunk, self._option)
		chunk_add_int_endian_safe   (chunk, self._nb_vertices)
		chunk_add_int_endian_safe   (chunk, self._nb_faces)
		chunk_add_int_endian_safe   (chunk, self._nb_quads)
		chunk_add_int_endian_safe   (chunk, self._nb_opaque_face_groups)
		chunk_add_int_endian_safe   (chunk, self._nb_face_groups)
		
		chunk_add_floats_endian_safe(chunk, self._coords   , 3 * self._nb_vertices)
		chunk_add_floats_endian_safe(chunk, self._vnormals , 3 * self._nb_vertices)
		chunk_add_ints_endian_safe  (chunk, self._vertexids,     self._nb_vertices)
		if self._option & MODEL_HAS_SPHERE:     chunk_add_floats_endian_safe(chunk, self._sphere        , 4)
		if self._option & MODEL_VERTEX_OPTIONS: chunk_add_chars_endian_safe (chunk, self._vertex_options,     self._nb_vertices)
		if self._option & MODEL_DIFFUSES:       chunk_add_floats_endian_safe(chunk, self._diffuses      , 4 * self._nb_vertices)
		if self._option & MODEL_EMISSIVES:      chunk_add_floats_endian_safe(chunk, self._emissives     , 4 * self._nb_vertices)
		if self._option & MODEL_TEXCOORDS:      chunk_add_floats_endian_safe(chunk, self._texcoords     , 2 * self._nb_vertices)
		# texcoords2 is for special effects like cell-shading, and do not need to be saved
		
		for i from 0 <= i < self._nb_faces:
			face = self._faces + i
			chunk_add_int_endian_safe   (chunk, face.option)
			chunk_add_floats_endian_safe(chunk, face.normal, 4)
			chunk_add_ints_endian_safe  (chunk, face.v     , 4)
			chunk_add_int_endian_safe   (chunk, material_id2index[face.pack.material_id])
			
		if self._option & MODEL_NEIGHBORS:
			chunk_add_ints_endian_safe (chunk, self._neighbors     , self._nb_faces * 4)
			chunk_add_chars_endian_safe(chunk, self._neighbors_side, self._nb_faces * 4)
			
		if self._option & MODEL_SIMPLE_NEIGHBORS:
			chunk_add_ints_endian_safe (chunk, self._simple_neighbors     , self._nb_faces * 4)
			chunk_add_chars_endian_safe(chunk, self._simple_neighbors_side, self._nb_faces * 4)
			
		for i from 0 <= i < self._nb_face_groups:
			face_group = self._face_groups + i
			chunk_add_int_endian_safe(chunk, face_group.option)
			chunk_add_int_endian_safe(chunk, face_group.start)
			chunk_add_int_endian_safe(chunk, face_group.nb_triangles)
			chunk_add_int_endian_safe(chunk, material_id2index[face_group.material_id])
			
		chunk_add_ints_endian_safe  (chunk, self._face_group_vertices, 3 * (self._nb_faces + self._nb_quads))
		
		return drop_chunk_to_string(chunk), self._filename, self._materials
	
	cdef void __setcstate_data__(self, cstate):
		cdef int                          i
		cdef int                          temp
		cdef Chunk*                       chunk
		cdef _VertexBufferModelFace*      face
		cdef _VertexBufferModelFaceGroup* face_group
		
		cstate2, self._filename, self._materials = cstate
		chunk = string_to_chunk(cstate2)
		
		chunk_get_int_endian_safe(chunk, &self._option)
		chunk_get_int_endian_safe(chunk, &self._nb_vertices)
		chunk_get_int_endian_safe(chunk, &self._nb_faces)
		chunk_get_int_endian_safe(chunk, &self._nb_quads)
		chunk_get_int_endian_safe(chunk, &self._nb_opaque_face_groups)
		chunk_get_int_endian_safe(chunk, &self._nb_face_groups)
		
		self._coords        = <float*>     malloc(3 * self._nb_vertices * sizeof(float))
		self._vnormals      = <float*>     malloc(3 * self._nb_vertices * sizeof(float))
		self._vertexids     = <int*>       malloc(    self._nb_vertices * sizeof(int  ))
		chunk_get_floats_endian_safe(chunk, self._coords   , 3 * self._nb_vertices)
		chunk_get_floats_endian_safe(chunk, self._vnormals , 3 * self._nb_vertices)
		chunk_get_ints_endian_safe  (chunk, self._vertexids,     self._nb_vertices)
		if self._option & MODEL_HAS_SPHERE:     self._sphere         = <float*> malloc(4                     * sizeof(float)); chunk_get_floats_endian_safe(chunk, self._sphere        , 4)
		if self._option & MODEL_VERTEX_OPTIONS: self._vertex_options = <char* > malloc(    self._nb_vertices * sizeof(char )); chunk_get_chars_endian_safe (chunk, self._vertex_options,     self._nb_vertices)
		if self._option & MODEL_DIFFUSES:       self._diffuses       = <float*> malloc(4 * self._nb_vertices * sizeof(float)); chunk_get_floats_endian_safe(chunk, self._diffuses      , 4 * self._nb_vertices)
		if self._option & MODEL_EMISSIVES:      self._emissives      = <float*> malloc(4 * self._nb_vertices * sizeof(float)); chunk_get_floats_endian_safe(chunk, self._emissives     , 4 * self._nb_vertices)
		if self._option & MODEL_TEXCOORDS:      self._texcoords      = <float*> malloc(2 * self._nb_vertices * sizeof(float)); chunk_get_floats_endian_safe(chunk, self._texcoords     , 2 * self._nb_vertices)
		if self._option & MODEL_TEXCOORDS2:     self._texcoords2     = <float*> malloc(2 * self._nb_vertices * sizeof(float)) # texcoords2 is for special effects like cell-shading, and do not need to be saved
		
		
		self._faces = <_VertexBufferModelFace*> malloc(self._nb_faces * sizeof(_VertexBufferModelFace))
		for i from 0 <= i < self._nb_faces:
			face = self._faces + i
			chunk_get_int_endian_safe    (chunk, &face.option)
			chunk_get_float_endian_safe  (chunk, &face.normal[0])
			chunk_get_float_endian_safe  (chunk, &face.normal[1])
			chunk_get_float_endian_safe  (chunk, &face.normal[2])
			chunk_get_float_endian_safe  (chunk, &face.normal[3])
			chunk_get_int_endian_safe    (chunk, &face.v     [0])
			chunk_get_int_endian_safe    (chunk, &face.v     [1])
			chunk_get_int_endian_safe    (chunk, &face.v     [2])
			chunk_get_int_endian_safe    (chunk, &face.v     [3])
			chunk_get_int_endian_safe    (chunk, &temp)
			face.pack = (<_Material> (<void*> (self._materials[temp])))._pack(face.option)
			
		if self._option & MODEL_NEIGHBORS:
			self._neighbors      = <int        *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(signed char))
			chunk_get_ints_endian_safe (chunk, self._neighbors     , self._nb_faces * 4)
			chunk_get_chars_endian_safe(chunk, self._neighbors_side, self._nb_faces * 4)
			
		if self._option & MODEL_SIMPLE_NEIGHBORS:
			self._simple_neighbors      = <int        *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._simple_neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(signed char))
			chunk_get_ints_endian_safe (chunk, self._simple_neighbors     , self._nb_faces * 4)
			chunk_get_chars_endian_safe(chunk, self._simple_neighbors_side, self._nb_faces * 4)
			
		self._face_groups = <_VertexBufferModelFaceGroup*> malloc(self._nb_face_groups * sizeof(_VertexBufferModelFaceGroup))
		for i from 0 <= i < self._nb_face_groups:
			face_group = self._face_groups + i
			chunk_get_int_endian_safe(chunk, &face_group.option)
			chunk_get_int_endian_safe(chunk, &face_group.start)
			chunk_get_int_endian_safe(chunk, &face_group.nb_triangles)
			chunk_get_int_endian_safe(chunk, &temp)
			face_group.material_id = id(<_Material> (<void*> (self._materials[temp])))
			
		self._face_group_vertices = <int*> malloc(3 * (self._nb_faces + self._nb_quads) * sizeof(int))
		chunk_get_ints_endian_safe  (chunk, self._face_group_vertices, 3 * (self._nb_faces + self._nb_quads))
		
		drop_chunk(chunk)
		
		self._option = self._option & ~MODEL_INITED
		
	cdef void __setcstate__(self, cstate):
		self.__setcstate_data__(cstate)
		
	property option:
		def __get__(self):
			return self._option
		
	property materials:
		def __get__(self):
			return self._materials
		
	property nb_vertices:
		def __get__(self):
			return self._nb_vertices
		
	property nb_faces:
		def __get__(self):
			return self._nb_faces

	def get_face(self, int index):
		"""Debugging functions"""
		cdef _VertexBufferModelFace* face
		face = self._faces + index
		if face.option & FACE_QUAD: return face.v[0], face.v[1], face.v[2], face.v[3]
		else:                       return face.v[0], face.v[1], face.v[2]
		
	def get_vertex(self, int index):
		"""Debugging functions"""
		l = [self._coords[3 * index], self._coords[3 * index + 1], self._coords[3 * index + 2]]
		if self._option & MODEL_VERTEX_OPTIONS: l.append(self._vertex_options[index])
		else:                                   l.append(-1)
		if self._option & MODEL_TEXCOORDS:      l.append(self._texcoords[index])
		else:                                   l.append(-1)
		if self._option & MODEL_DIFFUSES:       l.append(self._colors[index])
		else:                                   l.append(-1)
		if self._option & MODEL_EMISSIVES:      l.append(self._emissives[index])
		else:                                   l.append(-1)
		return tuple(l)
	
	def get_neighbor(self, int index):
		if not (self._option & MODEL_NEIGHBORS): return None
		cdef int* neighbor
		neighbor = self._neighbors + (4 * index)
		return neighbor[0], neighbor[1], neighbor[2], neighbor[3]
		
	def get_neighbor_side(self, int index):
		if not (self._option & MODEL_NEIGHBORS): return None
		cdef signed char* neighbor_side
		neighbor_side = self._neighbors_side + (4 * index)
		return neighbor_side[0], neighbor_side[1], neighbor_side[2], neighbor_side[3]
		
	def get_simple_neighbor(self, int index):
		if not (self._option & MODEL_SIMPLE_NEIGHBORS): return None
		cdef int* neighbor
		neighbor = self._simple_neighbors + (4 * index)
		return neighbor[0], neighbor[1], neighbor[2], neighbor[3]
	
	def get_simple_neighbor_side(self, int index):
		if not (self._option & MODEL_SIMPLE_NEIGHBORS): return None
		cdef signed char* neighbor_side
		neighbor_side = self._simple_neighbors_side + (4 * index)
		return neighbor_side[0], neighbor_side[1], neighbor_side[2], neighbor_side[3]
	
	property sphere:
		def __get__(self):
			return (self._sphere[0], self._sphere[1], self._sphere[2], self._sphere[3])
		
	cdef object _identify_vertices(self, faces, float angle):
		"""Finds which vertices are at the same position, for vertex sharing capabilities.
2 vertices are considered at the same position if the distance between them is > EPSILON,
and if the angle between their 2 faces is < ANGLE."""
		# "ivertex" means "identified vertex"
		cdef _Face   face
		cdef _Vertex vertex, ivertex, vertex2
		cdef int     i, j
		cdef float   p[3], amin, a
		cdef         ivertices
		
		vertex2ivertex   = {}
		ivertex2vertices = {}
		hashcube         = {}
		for face in faces:
			for vertex in face._vertices:
				vertex._out(p)
				p[0] = (<float> (<int> (p[0] / EPSILON))) * EPSILON
				p[1] = (<float> (<int> (p[1] / EPSILON))) * EPSILON
				p[2] = (<float> (<int> (p[2] / EPSILON))) * EPSILON
				
				hash = (p[0], p[1], p[2])
				ivertex = hashcube.get(hash)
				if ivertex is None:
					vertex2ivertex[vertex] = hashcube[hash] = ivertex = vertex
					ivertex2vertices[ivertex] = [vertex]
				else:
					vertex2ivertex[vertex] = ivertex
					ivertex2vertices[ivertex].append(vertex)
					
		if angle > 180.0: return vertex2ivertex, ivertex2vertices
		
		# Take face angle into account for vertex identification.
		vertex2ivertex2   = {}
		ivertex2vertices2 = {}
		from sets import Set
		for vertices in ivertex2vertices.values():
			couples = []
			for i from 0 <= i < len(vertices):
				for j from i + 1 <= j < len(vertices):
					couples.append((vertices[i].face.normal.angle_to(vertices[j].face.normal), vertices[i], vertices[j]))
					
			couples.sort()
			
			shared_vertices = {}
			for vertex in vertices: shared_vertices[vertex] = Set([vertex])
			
			for a, vertex1, vertex2 in couples:
				if a > angle: break
				shared_vertex1 = shared_vertices.get(vertex1)
				shared_vertex2 = shared_vertices.get(vertex2)
				shared_vertex  = shared_vertex1 | shared_vertex2
				for vertex in shared_vertex: shared_vertices[vertex] = shared_vertex

			for shared_vertex in Set(shared_vertices.values()):
				shared_vertex = list(shared_vertex)
				ivertex = shared_vertex[0]
				ivertex2vertices2[ivertex] = shared_vertex
				for vertex in shared_vertex:
					vertex2ivertex2[vertex] = ivertex
					
		return vertex2ivertex2, ivertex2vertices2
	
	cdef void _compute_face_normals(self, faces):
		cdef _Face face
		for face in faces: face._compute_normal()
		
	cdef void _compute_vertex_normals(self, faces, vertex2ivertex, ivertex2vertices):
		cdef _Vertex vertex, ivertex
		for ivertex in ivertex2vertices.keys():
			for vertex in ivertex2vertices[ivertex]:
				if vertex._face._option & FACE2_SMOOTH_LIT:
					if ivertex._normal is None: ivertex._normal = Vector(vertex._face.get_root())
					#vertex._face._compute_normal() # Needed ? Or already done ?
					ivertex._normal.add_mul_vector(vertex._angle_at(), vertex._face._normal)
					
	cdef void _compute_face_neighbors(self, faces, vertex2ivertex, ivertex2vertices, int* neighbor, signed char* neighbor_side):
		# 2 faces are neighbors <=> they share 2 vertices.
		cdef int          i, j, v1_neighbor_index, v2_neighbor_index
		cdef _Vertex      v1, v2, v1_neighbor, v2_neighbor
		cdef _Face        face
		
		i = 0
		face2index = {}
		for face in faces:
			face2index[face] = i
			i = i + 1
			
		for face in faces:
			for i from 0 <= i < len(face.vertices):
				neighbor[i] = -1 # default value meaning 'no neighbor'
				
				v1 = vertex2ivertex[face.vertices[i]]
				v2 = vertex2ivertex[((i + 1 < len(face.vertices)) and face.vertices[i + 1]) or face.vertices[0]]
				
				for v1_neighbor in ivertex2vertices[v1]:
					# A double sided face cannot be the neighbor of a non-double sided face
					if (face._option & FACE2_DOUBLE_SIDED) != (v1_neighbor._face._option & FACE2_DOUBLE_SIDED): continue
					
					if not v1_neighbor._face is face:
						for v2_neighbor in v1_neighbor._face.vertices:
							if vertex2ivertex[v2_neighbor] is v2:
								# one neighbor found
								neighbor[i] = face2index[v1_neighbor._face]
								
								if face._option & FACE2_DOUBLE_SIDED: # Check for "backside-neighbor"
									v1_neighbor_index = v1_neighbor._face.vertices.index(v1_neighbor)
									v2_neighbor_index = v1_neighbor._face.vertices.index(v2_neighbor)
									if (v1_neighbor_index == v2_neighbor_index - 1) or ((v1_neighbor_index > 1) and (v2_neighbor_index == 0)): # Same rotation sens
										neighbor_side[i] = 1
									else: neighbor_side[i] = -1
									
								else: neighbor_side[i] = 1
								break
						else: continue
						break
					
			if len(face.vertices) < 4: neighbor[3] = -1 # triangle can have only 3 neighbors
			neighbor      = neighbor      + 4
			neighbor_side = neighbor_side + 4
			
	def __init__(self, _World world, float angle, int option, lights):
		cdef CoordSyst coordsyst
		cdef _Face                   face
		cdef _VertexBufferModelFace* model_face
		cdef _Vertex                 vertex, ivertex
		cdef int                     i, j, k, face_nb_vertices
		cdef int*                    face_group_vertices
		cdef float*                  p
		cdef float                   pos[3], vec[3]
		cdef _Material               material
		cdef _Light                  light
		
		self._materials = []
		
		# Collect faces  XXX collect models too (by loading the corresponding world)
		faces = []
		for coordsyst in world.recursive():
			if isinstance(coordsyst, _Face) and not(coordsyst._option & HIDDEN): faces.append(coordsyst)
			
		# check for additional options
		self._option = option
		if lights: self._option = self._option | (MODEL_STATIC_LIT + MODEL_EMISSIVES)
		
		for face in faces:
			for vertex in face._vertices:
				if (not face._material._texture is None) and ((vertex._tex_x != 0.0) or (vertex._tex_y != 0.0)): self._option = self._option | MODEL_TEXCOORDS
				if (not vertex._diffuse  is None) and ((vertex._diffuse [0] != 1.0) or (vertex._diffuse [1] != 1.0) or (vertex._diffuse [2] != 1.0) or (vertex._diffuse [3] != 1.0)): self._option = self._option | MODEL_DIFFUSES
				if (not vertex._emissive is None) and ((vertex._emissive[0] != 1.0) or (vertex._emissive[1] != 1.0) or (vertex._emissive[2] != 1.0) or (vertex._emissive[3] != 1.0)): self._option = self._option | MODEL_EMISSIVES
				
		self._compute_face_normals(faces)
		vertex2ivertex, ivertex2vertices = self._identify_vertices(faces, angle)
		self._compute_vertex_normals(faces, vertex2ivertex, ivertex2vertices)
		
		self._nb_vertices = len(vertex2ivertex)
		self._nb_faces    = len(faces)
		self._nb_quads    = 0
		self._coords      = <float*> malloc(3 * self._nb_vertices * sizeof(float))
		self._vnormals    = <float*> malloc(3 * self._nb_vertices * sizeof(float))
		self._vertexids   = <int*  > malloc(    self._nb_vertices * sizeof(int  ))
		if self._option & MODEL_DIFFUSES:	  self._diffuses   = <float*> malloc(4 * self._nb_vertices * sizeof(float))
		if self._option & MODEL_EMISSIVES:  self._diffuses   = <float*> malloc(4 * self._nb_vertices * sizeof(float))
		if self._option & MODEL_TEXCOORDS:  self._texcoords  = <float*> malloc(2 * self._nb_vertices * sizeof(float))
		if self._option & MODEL_TEXCOORDS2: self._texcoords2 = <float*> malloc(2 * self._nb_vertices * sizeof(float))
		
		vertex2index = {}
		vertices = vertex2ivertex.keys()
		i = 0
		for vertex in vertices:
			vertex2index[vertex] = i
			ivertex = vertex2ivertex[vertex]
			vertex._out(self._coords + 3 * i)
			if vertex._face._option & FACE2_SMOOTH_LIT:
				ivertex._normal._out(self._vnormals + 3 * i)
				vector_normalize    (self._vnormals + 3 * i)
			else:
				vertex._face._normal._out(self._vnormals + 3 * i)
				vector_normalize         (self._vnormals + 3 * i)
				
			if self._option & MODEL_TEXCOORDS:
				p = self._texcoords + 2 * i
				p[0] = vertex._tex_x
				p[1] = vertex._tex_y
				
			if self._option & MODEL_DIFFUSES:
				p = self._diffuses + 2 * i
				if not vertex._diffuse is None:
					p[0] = vertex._diffuse[0]
					p[1] = vertex._diffuse[1]
					p[2] = vertex._diffuse[2]
					p[3] = vertex._diffuse[3]
				else: # the face use diffuse color, but not for this vertex. but we need ALL the face's vertices to have a color => we take the material diffuse color as default.
					memcpy(&p[0], &vertex._face._material._diffuse[0], 4 * sizeof(float))
					
			if self._option & MODEL_EMISSIVES:
				p = self._emissives + 2 * i
				if not vertex._emissive is None:
					p[0] = vertex._emissive[0]
					p[1] = vertex._emissive[1]
					p[2] = vertex._emissive[2]
					p[3] = vertex._emissive[3]
				else: # the face use diffuse color, but not for this vertex. but we need ALL the face's vertices to have a color => we take the material diffuse color as default.
					p[0] = p[1] = p[2] = 0.0
					p[3] = 1.0
					
				if lights: # Apply static lighting as emissive colors
					for light in lights:
						vertex._into(light, pos)
						if vertex._face._option & FACE2_SMOOTH_LIT: ivertex     ._normal._into(light, vec)
						else:                                       vertex._face._normal._into(light, vec)
						light._static_light_at(pos, vec, self._option & MODEL_STATIC_SHADOW, p)
						
			i = i + 1

		i = 0
		for vertex in vertices:
			ivertex = vertex2ivertex[vertex]
			self._vertexids[i] = vertex2index[ivertex]
			i = i + 1
			
			
		self._faces = <_VertexBufferModelFace*> malloc(self._nb_faces * sizeof(_VertexBufferModelFace))
		i = 0
		for face in faces:
			model_face = self._faces + i
			model_face.option = 0
			face_nb_vertices = len(face._vertices)
			if   face_nb_vertices == 3: model_face.option = model_face.option | FACE_TRIANGLE
			elif face_nb_vertices == 4: model_face.option = model_face.option | FACE_QUAD; self._nb_quads = self._nb_quads + 1
			else:
				print "Face with %s vertices are not supported in model." % face_nb_vertices
				raise ValueError("Face with %s vertices are not supported in model." % face_nb_vertices)
			if face.is_alpha():                   model_face.option = model_face.option | FACE_ALPHA
			if face._option & FACE2_DOUBLE_SIDED: model_face.option = model_face.option | FACE_DOUBLE_SIDED
			if face._option & FACE2_SMOOTH_LIT:   model_face.option = model_face.option | FACE_SMOOTH_LIT
			if not(face._option & FACE2_LIT):     model_face.option = model_face.option | FACE_NON_LIT
			if face._option & NON_SOLID:          model_face.option = model_face.option | FACE_NON_SOLID

			model_face.v[0] = vertex2index[face._vertices[0]]
			model_face.v[1] = vertex2index[face._vertices[1]]
			model_face.v[2] = vertex2index[face._vertices[2]]
			if model_face.option & FACE_QUAD: model_face.v[3] = vertex2index[face._vertices[3]]
			
			if self._option & MODEL_PLANE_EQUATION:
				face._normal._out(model_face.normal)
				p = self._coords + 3 * model_face.v[0]
				model_face.normal[3] = -(p[0] * model_face.normal[0] + p[1] * model_face.normal[1] + p[2] * model_face.normal[2])
				plane_vector_normalize(model_face.normal)
			else:
				face._normal._out(model_face.normal)
				vector_normalize (model_face.normal)
				
			if not face._material in self._materials: self._materials.append(face._material)
			model_face.pack = face._material._pack(model_face.option)
			
			i = i + 1
			
			
		self._materials = tuple(self._materials)
		for material in self._materials:
			if material._option & MATERIAL_ALPHA: self._option = self._option | MODEL_HAS_ALPHA
			else:                                 self._option = self._option | MODEL_HAS_OPAQUE
		if (self._option & MODEL_DIFFUSES) and not(self._option == self._option & MODEL_HAS_ALPHA):
			p = self._diffuses
			for i from 0 <= i < self._nb_vertices:
				if p[3] != 1.0:
					self._option = self._option | MODEL_HAS_ALPHA
					break
				p = p + 4
				
				
		cdef _VertexBufferModelFaceGroup* face_group
		self._nb_face_groups        = 0
		self._nb_opaque_face_groups = 0
		self._face_groups           = <_VertexBufferModelFaceGroup*> malloc(sizeof(_VertexBufferModelFaceGroup))
		for k from 0 <= k < 2:
			for j from 0 <= j < self._nb_faces:
				model_face = self._faces + j
				if ((model_face.option & FACE_ALPHA) and (k == 1)) or ((not(model_face.option & FACE_ALPHA)) and (k == 0)):
					for i from 0 <= i < self._nb_face_groups:
						face_group = self._face_groups + i
						if (face_group.material_id == model_face.pack.material_id) and (face_group.option == (model_face.option & VERTEX_BUFFER_OPTIONS)):
							break
					else:
						self._face_groups = <_VertexBufferModelFaceGroup*> realloc(self._face_groups, (self._nb_face_groups + 1) * sizeof(_VertexBufferModelFaceGroup))
						face_group = self._face_groups + self._nb_face_groups
						face_group.material_id = model_face.pack.material_id
						face_group.option      = model_face.option & VERTEX_BUFFER_OPTIONS
						if k == 0: self._nb_opaque_face_groups = self._nb_opaque_face_groups + 1
						self._nb_face_groups = self._nb_face_groups + 1
						
						
		self._face_group_vertices = <int*> malloc(3 * (self._nb_faces + self._nb_quads) * sizeof(int))
		face_group_vertices = self._face_group_vertices
		for i from 0 <= i < self._nb_face_groups:
			face_group = self._face_groups + i
			for j from 0 <= j < self._nb_faces:
				model_face = self._faces + j
				if (face_group.material_id == model_face.pack.material_id) and (face_group.option == (model_face.option & VERTEX_BUFFER_OPTIONS)):
					memcpy(face_group_vertices, model_face.v, 3 * sizeof(int))
					face_group_vertices = face_group_vertices + 3
					if model_face.option & FACE_QUAD:
						face_group_vertices[0] = model_face.v[2]
						face_group_vertices[1] = model_face.v[3]
						face_group_vertices[2] = model_face.v[0]
						face_group_vertices = face_group_vertices + 3
						
		# find face neighbors
		if self._option & MODEL_NEIGHBORS:
			self._neighbors      = <       int *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(char))
			self._compute_face_neighbors(faces, vertex2ivertex, ivertex2vertices, self._neighbors, self._neighbors_side)
			
		if self._option & MODEL_SIMPLE_NEIGHBORS: # find face simple neighbors (doesn't take angle into account)
			vertex2ivertex, ivertex2vertices = self._identify_vertices(faces, 360.0) # Re-identify vertices, because for simple neighbors we don't take angle into account
			self._simple_neighbors      = <       int *> malloc(self._nb_faces * 4 * sizeof(int ))
			self._simple_neighbors_side = <signed char*> malloc(self._nb_faces * 4 * sizeof(char))
			self._compute_face_neighbors(faces, vertex2ivertex, ivertex2vertices, self._simple_neighbors, self._simple_neighbors_side)
			
			
	cdef void _build_sphere(self):
		if self._nb_vertices > 0:
			self._sphere = <float*> malloc(4 * sizeof(float))
			sphere_from_points(self._sphere, self._coords, self._nb_vertices)
			self._option = self._option | MODEL_HAS_SPHERE
			
	cdef void _get_box(self, float* box, float* matrix):
		cdef float* coord
		cdef float  coord2[3]
		
		coord = self._coords
		for i from 0 <= i < self._nb_vertices:
			point_by_matrix_copy(coord2, coord, matrix)
			
			if coord2[0] < box[0]: box[0] = coord2[0]
			if coord2[1] < box[1]: box[1] = coord2[1]
			if coord2[2] < box[2]: box[2] = coord2[2]
			if coord2[0] > box[3]: box[3] = coord2[0]
			if coord2[1] > box[4]: box[4] = coord2[1]
			if coord2[2] > box[5]: box[5] = coord2[2]
			
			coord = coord + 3
			
			
	cdef void _init_vertex_buffers(self):
		cdef int*                    faces
		cdef _VertexBufferModelFace* face
		cdef int                     i, alpha, offset
		
		glGenBuffers(1, &self._face_buffer)
		glGenBuffers(1, &self._vertex_buffer)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._face_buffer)
		glBindBuffer(GL_ARRAY_BUFFER        , self._vertex_buffer)
		
		self._buffer_sizeof_vertex = 6 * sizeof(float)
		if self._option & MODEL_DIFFUSES:   self._buffer_sizeof_vertex = self._buffer_sizeof_vertex + 4 * sizeof(float)
		if self._option & MODEL_EMISSIVES:  self._buffer_sizeof_vertex = self._buffer_sizeof_vertex + 4 * sizeof(float)
		if self._option & MODEL_TEXCOORDS:  self._buffer_sizeof_vertex = self._buffer_sizeof_vertex + 2 * sizeof(float)
		
		if self._option & MODEL_STATIC_FACE:   glBufferData(GL_ELEMENT_ARRAY_BUFFER, 3 * (self._nb_faces + self._nb_quads) * sizeof(int), self._face_group_vertices, GL_STATIC_DRAW)
		else:                                  glBufferData(GL_ELEMENT_ARRAY_BUFFER, 3 * (self._nb_faces + self._nb_quads) * sizeof(int), self._face_group_vertices, GL_DYNAMIC_DRAW)
		if self._option & MODEL_STATIC_VERTEX: glBufferData(GL_ARRAY_BUFFER, self._nb_vertices * self._buffer_sizeof_vertex, NULL, GL_STATIC_DRAW)
		else:                                  glBufferData(GL_ARRAY_BUFFER, self._nb_vertices * self._buffer_sizeof_vertex, NULL, GL_DYNAMIC_DRAW)
		
		self._vnormal_offset = 3 * self._nb_vertices * sizeof(float)
		offset = self._vnormal_offset + 3 * self._nb_vertices * sizeof(float)
		glBufferSubData(GL_ARRAY_BUFFER, 0                   , 3 * self._nb_vertices * sizeof(float), self._coords  )
		glBufferSubData(GL_ARRAY_BUFFER, self._vnormal_offset, 3 * self._nb_vertices * sizeof(float), self._vnormals)
		
		if self._option & MODEL_DIFFUSES:
			self._diffuse_offset = offset
			glBufferSubData(GL_ARRAY_BUFFER, self._diffuse_offset, 4 * self._nb_vertices * sizeof(float), self._diffuses)
			offset = offset + 4 * self._nb_vertices * sizeof(float)
			
		if self._option & MODEL_EMISSIVES:
			self._emissive_offset = offset
			glBufferSubData(GL_ARRAY_BUFFER, self._emissive_offset, 4 * self._nb_vertices * sizeof(float), self._emissives)
			offset = offset + 4 * self._nb_vertices * sizeof(float)
			
		if self._option & MODEL_TEXCOORDS:
			self._texcoord_offset = offset
			glBufferSubData(GL_ARRAY_BUFFER, self._texcoord_offset, 2 * self._nb_vertices * sizeof(float), self._texcoords)
			offset = offset + 2 * self._nb_vertices * sizeof(float)
			
		if self._option & MODEL_TEXCOORDS2:
			glGenBuffers(1, &self._texcoords2_buffer)
			glBindBuffer(GL_ARRAY_BUFFER, self._texcoords2_buffer)
			glBufferData(GL_ARRAY_BUFFER, 2 * self._nb_vertices * sizeof(float), NULL, GL_DYNAMIC_DRAW)
			
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		glBindBuffer(GL_ARRAY_BUFFER        , 0)		
		
		self._option = self._option | MODEL_INITED
		
	cdef void _batch(self, _Body body):
		if body._option & HIDDEN: return
		
		cdef float sphere[4]
		if self._option & MODEL_HAS_SPHERE:
			sphere_by_matrix_copy(sphere, self._sphere, body._root_matrix())
			if sphere_in_frustum(renderer.root_frustum, sphere) == 0: return
			
		if self._option & MODEL_HAS_OPAQUE: renderer._batch(renderer.opaque, self, body, NULL)
		if self._option & MODEL_HAS_ALPHA : renderer._batch(renderer.alpha , self, body, NULL)
		
#	cdef void _batch_face(self, VertexBufferModelFace* face): # Not used by _SimpleModel, but by subclasses (like _TreeModel or _CellShadingModel)
		
	cdef void _render(self, _Body body):
		cdef _VertexBufferModelFaceGroup* face_group
		cdef int i, start, end
		
		model_option_activate(self._option)
		if body._option & LEFTHANDED: glFrontFace(GL_CW)
		
		if not(self._option & MODEL_INITED): self._init_vertex_buffers()
		
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._face_buffer)
		glBindBuffer(GL_ARRAY_BUFFER        , self._vertex_buffer)
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_NORMAL_ARRAY)
		glVertexPointer(3, GL_FLOAT, 0, BUFFER_OFFSET(0))
		glNormalPointer(   GL_FLOAT, 0, BUFFER_OFFSET(self._vnormal_offset))
		
		if self._option & MODEL_DIFFUSES:
			glEnableClientState(GL_COLOR_ARRAY)
			glColorPointer(4, GL_FLOAT, 0, BUFFER_OFFSET(self._diffuse_offset))
			
		if self._option & MODEL_EMISSIVES:
			glColorMaterial(GL_FRONT_AND_BACK, GL_EMISSION)
			glEnableClientState(GL_COLOR_ARRAY)
			glColorPointer(4, GL_FLOAT, 0, BUFFER_OFFSET(self._emissives_offset))
			glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
			
		if self._option & MODEL_TEXCOORDS:
			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
			glTexCoordPointer(2, GL_FLOAT, 0, BUFFER_OFFSET(self._texcoord_offset))
			
		if self._option & MODEL_TEXCOORDS2:
			glClientActiveTexture(GL_TEXTURE1)
			glBindBuffer(GL_ARRAY_BUFFER, self._texcoords2_buffer)
			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
			glTexCoordPointer(2, GL_FLOAT, 0, BUFFER_OFFSET(0))
			glClientActiveTexture(GL_TEXTURE0)
			glBindBuffer(GL_ARRAY_BUFFER, self._vertex_buffer)
			
		if renderer.state == RENDERER_STATE_OPAQUE:
			start = 0
			end   = self._nb_opaque_face_groups
		else:
			start = self._nb_opaque_face_groups
			end   = self._nb_face_groups
			
		for i from start <= i < end:
			face_group = self._face_groups + i
			face_option_activate(face_group.option)
			(<_Material> (<void*> (face_group.material_id)))._activate()        
			glDrawRangeElements(GL_TRIANGLES, face_group.start, face_group.start + 3 * face_group.nb_triangles, 3 * (self._nb_faces + self._nb_quads), GL_UNSIGNED_INT, BUFFER_OFFSET(0))
			face_option_inactivate(face_group.option)
			
		glDisableClientState(GL_VERTEX_ARRAY)
		glDisableClientState(GL_NORMAL_ARRAY)
		
		if self._option & MODEL_DIFFUSES: glDisableClientState(GL_COLOR_ARRAY)
		if self._option & MODEL_EMISSIVES:
			glColorMaterial(GL_FRONT_AND_BACK, GL_EMISSION)
			glDisableClientState(GL_COLOR_ARRAY)
			glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
			
		if self._option & MODEL_TEXCOORDS: glDisableClientState(GL_TEXTURE_COORD_ARRAY)
		
		if self._option & MODEL_TEXCOORDS2:
			glClientActiveTexture(GL_TEXTURE1)
			glDisableClientState(GL_TEXTURE_COORD_ARRAY)
			glClientActiveTexture(GL_TEXTURE0)
			
		glBindBuffer(GL_ARRAY_BUFFER        , 0)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		
		if body._option & LEFTHANDED:	glFrontFace(GL_CCW)
		model_option_inactivate(self._option)
		
		
	cdef void _raypick(self, RaypickData data, CoordSyst parent):
		cdef float* raydata
		cdef int    i
		raydata = parent._raypick_data(data)
		if (self._option & MODEL_HAS_SPHERE) and (sphere_raypick(raydata, self._sphere) == 0): return
		for i from 0 <= i < self._nb_faces:
			self._face_raypick(self._faces + i, raydata, data, parent)
			
	cdef int _raypick_b(self, RaypickData data, CoordSyst parent):
		cdef float* raydata
		cdef int    i
		raydata = parent._raypick_data(data)
		if (self._option & MODEL_HAS_SPHERE) and (sphere_raypick(raydata, self._sphere) == 0): return 0
		for i from 0 <= i < self._nb_faces:
			if self._face_raypick_b(self._faces + i, raydata, data): return 1
		return 0
	
	cdef void _face_raypick(self, _VertexBufferModelFace* face, float* raydata, RaypickData data, CoordSyst parent):
		cdef float z, root_z
		cdef int   r, option
		
		option = data.option
		if  face.option & FACE_NON_SOLID: return
		if (face.option & FACE_DOUBLE_SIDED) and (option & RAYPICK_CULL_FACE): option = option - RAYPICK_CULL_FACE
		if  face.option & FACE_QUAD:
			r = quad_raypick    (raydata, self._coords + 3 * face.v[0], self._coords + 3 * face.v[1], self._coords + 3 * face.v[2], self._coords + 3 * face.v[3], face.normal, option, &z)
		else:
			r = triangle_raypick(raydata, self._coords + 3 * face.v[0], self._coords + 3 * face.v[1], self._coords + 3 * face.v[2], face.normal, option, &z)
			
		if r != 0:
			root_z = parent._distance_out(z)
			if (data.result_coordsyst is None) or (fabs(root_z) < fabs(data.root_result)):
				data.result           = z
				data.root_result      = root_z
				data.result_coordsyst = parent
				if   r == RAYPICK_DIRECT: memcpy(&data.normal[0], face.normal, 3 * sizeof(float))
				elif r == RAYPICK_INDIRECT:
					if face.option & FACE_DOUBLE_SIDED:
						data.normal[0] = -face.normal[0]
						data.normal[1] = -face.normal[1]
						data.normal[2] = -face.normal[2]
					else: memcpy(&data.normal[0], face.normal, 3 * sizeof(float))
					
	cdef int _face_raypick_b(self, _VertexBufferModelFace* face, float* raydata, RaypickData data):
		cdef float z
		cdef int   option
		
		option = data.option
		if  face.option & FACE_NON_SOLID: return 0
		if (face.option & FACE_DOUBLE_SIDED) and (option & RAYPICK_CULL_FACE): option = option - RAYPICK_CULL_FACE
		if  face.option & FACE_QUAD:
			if quad_raypick    (raydata, self._coords + 3 * face.v[0], self._coords + 3 * face.v[1], self._coords + 3 * face.v[2], self._coords + 3 * face.v[3], face.normal, option, &z) != 0: return 1
		else:
			if triangle_raypick(raydata, self._coords + 3 * face.v[0], self._coords + 3 * face.v[1], self._coords + 3 * face.v[2], face.normal, option, &z) != 0: return 1
		return 0
	
	cdef void _collect_raypickables(self, Chunk* items, float* rsphere, float* sphere, CoordSyst parent):
		if not(self._option & MODEL_HAS_SPHERE) or (sphere_distance_sphere(sphere, self._sphere) < 0.0):
			chunk_add_ptr(items, <void*> parent)
			















cdef void model_option_activate(int option):
	if option & MODEL_STATIC_LIT: disable_static_lights()
	
cdef void model_option_inactivate(int option):
	if option & MODEL_STATIC_LIT: enable_static_lights()
	
cdef void face_option_activate(int option):
	if option & FACE_DOUBLE_SIDED:
		glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
		glDisable(GL_CULL_FACE)
	if option & FACE_NON_LIT: glDisable(GL_LIGHTING)
	
cdef void face_option_inactivate(int option):
	if option & FACE_DOUBLE_SIDED:
		glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_FALSE)
		glEnable(GL_CULL_FACE)
	if option & FACE_NON_LIT: glEnable(GL_LIGHTING)
		
		
cdef void model_shadow_tess_combine(double coords[3], void* vertex_data[4], float weight[4], void** out_data):
	cdef double* d
	d = out_data[0] = <double*> malloc(3 * sizeof(double))
	memcpy(d, coords, 3 * sizeof(double))
	
	chunk_add_ptr(SHADOW_TESS_CHUNK, d)




cdef void segment_projection_intersect_plane(float* p1, float* v1, float* p2, float* v2, float infinity, float plane[4], float* inter1, float* inter2, float* face, int* nb):
	cdef int   nb_face, has_i1, has_i2, has_i3, has_i4
	cdef float p1d, p2d, pv1d, pv2d
	cdef float f, fdiv
	cdef float v[3], pv1[3], pv2[3], i1[3], i2[3], i3[3], i4[3]
	
	nb_face = 0
	has_i1 = has_i2 = has_i3 = has_i4 = 0
	
	pv1[0] = p1[0] + infinity * v1[0]
	pv1[1] = p1[1] + infinity * v1[1]
	pv1[2] = p1[2] + infinity * v1[2]
	
	pv2[0] = p2[0] + infinity * v2[0]
	pv2[1] = p2[1] + infinity * v2[1]
	pv2[2] = p2[2] + infinity * v2[2]
	
	# compute the distances from points to plane
	p1d  = plane[0] * p1 [0] + plane[1] * p1 [1] + plane[2] * p1 [2] + plane[3]
	p2d  = plane[0] * p2 [0] + plane[1] * p2 [1] + plane[2] * p2 [2] + plane[3]
	pv1d = plane[0] * pv1[0] + plane[1] * pv1[1] + plane[2] * pv1[2] + plane[3]
	pv2d = plane[0] * pv2[0] + plane[1] * pv2[1] + plane[2] * pv2[2] + plane[3]
	
	fdiv = plane[0] * v1[0] + plane[1] * v1[1] + plane[2] * v1[2]
	if fdiv != 0.0:
		f = - (plane[0] * p1[0] + plane[1] * p1[1] + plane[2] * p1[2] + plane[3]) / fdiv
		if f > 0.0:
			has_i1 = 1
			i1[0] = p1[0] + f * v1[0]
			i1[1] = p1[1] + f * v1[1]
			i1[2] = p1[2] + f * v1[2]
			
	fdiv = plane[0] * v2[0] + plane[1] * v2[1] + plane[2] * v2[2]
	if fdiv != 0.0:
		f = - (plane[0] * p2[0] + plane[1] * p2[1] + plane[2] * p2[2] + plane[3]) / fdiv
		if f > 0.0:
			has_i2 = 1
			i2[0] = p2[0] + f * v2[0]
			i2[1] = p2[1] + f * v2[1]
			i2[2] = p2[2] + f * v2[2]
			
	if p1d * p2d < 0.0:
		v[0] = p1[0] - p2[0]
		v[1] = p1[1] - p2[1]
		v[2] = p1[2] - p2[2]
		fdiv = plane[0] * v[0] + plane[1] * v[1] + plane[2] * v[2]
		f = - (plane[0] * p1[0] + plane[1] * p1[1] + plane[2] * p1[2] + plane[3]) / fdiv
		has_i3 = 1
		i3[0] = p1[0] + f * v[0]
		i3[1] = p1[1] + f * v[1]
		i3[2] = p1[2] + f * v[2]
		
	if pv1d * pv2d < 0.0:
		v[0] = pv1[0] - pv2[0]
		v[1] = pv1[1] - pv2[1]
		v[2] = pv1[2] - pv2[2]
		fdiv = plane[0] * v[0] + plane[1] * v[1] + plane[2] * v[2]
		f = - (plane[0] * pv1[0] + plane[1] * pv1[1] + plane[2] * pv1[2] + plane[3]) / fdiv
		has_i4 = 1
		i4[0] = pv1[0] + f * v[0]
		i4[1] = pv1[1] + f * v[1]
		i4[2] = pv1[2] + f * v[2]
		
	if has_i1 or has_i2: has_i4 = 0
	
	
	if p1d > 0.0: # p1 is on the right side of the plane => keep it in face
		memcpy(face + nb_face, p1, 3 * sizeof(float))
		nb_face = nb_face + 3
		
	if has_i1:
		memcpy(face + nb_face, &i1[0], 3 * sizeof(float))
		nb_face = nb_face + 3
		
	if (pv1d > 0.0) and not(has_i1 and (p1d > 0.0)):
		memcpy(face + nb_face, &pv1[0], 3 * sizeof(float))
		nb_face = nb_face + 3
		
		
	if has_i4:
		memcpy(face + nb_face, &i4[0], 3 * sizeof(float))
		nb_face = nb_face + 3
		
		
	if (pv2d > 0.0) and not(has_i2 and (p2d > 0.0)):
		memcpy(face + nb_face, &pv2[0], 3 * sizeof(float))
		nb_face = nb_face + 3
		
	if has_i2:
		memcpy(face + nb_face, &i2[0], 3 * sizeof(float))
		nb_face = nb_face + 3
		
	if p2d > 0.0:
		memcpy(face + nb_face, p2, 3 * sizeof(float))
		nb_face = nb_face + 3
		
		
	if has_i3:
		memcpy(face + nb_face, &i3[0], 3 * sizeof(float))
		nb_face = nb_face + 3
		
		
	if   has_i1: memcpy(inter1, &i1[0], 3 * sizeof(float)); nb[1] = 1
	elif has_i3: memcpy(inter1, &i3[0], 3 * sizeof(float)); nb[1] = 1
	elif has_i4: memcpy(inter1, &i4[0], 3 * sizeof(float)); nb[1] = 1
	else: nb[1] = 0
	
	if   has_i2: memcpy(inter2, &i2[0], 3 * sizeof(float)); nb[2] = 1
	elif has_i4: memcpy(inter2, &i4[0], 3 * sizeof(float)); nb[2] = 1
	elif has_i3: memcpy(inter2, &i3[0], 3 * sizeof(float)); nb[2] = 1
	else: nb[2] = 0
	
	nb[0] = nb_face / 3

cdef class _ModelData(_Model):
	def __init__(self, _Body body, _Model model): pass
	
