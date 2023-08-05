#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline uint8_t __deref_value_ptr_uint8_t(node_ptr node):

    return deref( <uint8_t*>deref(node).value )


cdef inline void __insert_node_uint8_t(rb_tree_ptr& index, key, uint8_t value) except*:

    cdef void* address = malloc( sizeof(uint8_t) )
    # assign new value and insert node with address
    (<uint8_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_uint8_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, uint8_t value ) except*:

    cdef void* address = malloc( sizeof(uint8_t) )
    # assign new value and insert node with address
    (<uint8_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_uint8_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_uint8_t(node_ptr node, uint8_t value) nogil except*:

    if deref(node).value != NULL:
        (<uint8_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(uint8_t) )
        (<uint8_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_uint8_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline uint16_t __deref_value_ptr_uint16_t(node_ptr node):

    return deref( <uint16_t*>deref(node).value )


cdef inline void __insert_node_uint16_t(rb_tree_ptr& index, key, uint16_t value) except*:

    cdef void* address = malloc( sizeof(uint16_t) )
    # assign new value and insert node with address
    (<uint16_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_uint16_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, uint16_t value ) except*:

    cdef void* address = malloc( sizeof(uint16_t) )
    # assign new value and insert node with address
    (<uint16_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_uint16_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_uint16_t(node_ptr node, uint16_t value) nogil except*:

    if deref(node).value != NULL:
        (<uint16_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(uint16_t) )
        (<uint16_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_uint16_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline uint32_t __deref_value_ptr_uint32_t(node_ptr node):

    return deref( <uint32_t*>deref(node).value )


cdef inline void __insert_node_uint32_t(rb_tree_ptr& index, key, uint32_t value) except*:

    cdef void* address = malloc( sizeof(uint32_t) )
    # assign new value and insert node with address
    (<uint32_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_uint32_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, uint32_t value ) except*:

    cdef void* address = malloc( sizeof(uint32_t) )
    # assign new value and insert node with address
    (<uint32_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_uint32_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_uint32_t(node_ptr node, uint32_t value) nogil except*:

    if deref(node).value != NULL:
        (<uint32_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(uint32_t) )
        (<uint32_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_uint32_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline uint64_t __deref_value_ptr_uint64_t(node_ptr node):

    return deref( <uint64_t*>deref(node).value )


cdef inline void __insert_node_uint64_t(rb_tree_ptr& index, key, uint64_t value) except*:

    cdef void* address = malloc( sizeof(uint64_t) )
    # assign new value and insert node with address
    (<uint64_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_uint64_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, uint64_t value ) except*:

    cdef void* address = malloc( sizeof(uint64_t) )
    # assign new value and insert node with address
    (<uint64_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_uint64_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_uint64_t(node_ptr node, uint64_t value) nogil except*:

    if deref(node).value != NULL:
        (<uint64_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(uint64_t) )
        (<uint64_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_uint64_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline uint96_t __deref_value_ptr_uint96_t(node_ptr node):

    return deref( <uint96_t*>deref(node).value )


cdef inline void __insert_node_uint96_t(rb_tree_ptr& index, key, uint96_t value) except*:

    cdef void* address = malloc( sizeof(uint96_t) )
    # assign new value and insert node with address
    (<uint96_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_uint96_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, uint96_t value ) except*:

    cdef void* address = malloc( sizeof(uint96_t) )
    # assign new value and insert node with address
    (<uint96_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_uint96_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_uint96_t(node_ptr node, uint96_t value) nogil except*:

    if deref(node).value != NULL:
        (<uint96_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(uint96_t) )
        (<uint96_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_uint96_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline uint128_t __deref_value_ptr_uint128_t(node_ptr node):

    return deref( <uint128_t*>deref(node).value )


cdef inline void __insert_node_uint128_t(rb_tree_ptr& index, key, uint128_t value) except*:

    cdef void* address = malloc( sizeof(uint128_t) )
    # assign new value and insert node with address
    (<uint128_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_uint128_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, uint128_t value ) except*:

    cdef void* address = malloc( sizeof(uint128_t) )
    # assign new value and insert node with address
    (<uint128_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_uint128_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_uint128_t(node_ptr node, uint128_t value) nogil except*:

    if deref(node).value != NULL:
        (<uint128_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(uint128_t) )
        (<uint128_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_uint128_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline int8_t __deref_value_ptr_int8_t(node_ptr node):

    return deref( <int8_t*>deref(node).value )


cdef inline void __insert_node_int8_t(rb_tree_ptr& index, key, int8_t value) except*:

    cdef void* address = malloc( sizeof(int8_t) )
    # assign new value and insert node with address
    (<int8_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_int8_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, int8_t value ) except*:

    cdef void* address = malloc( sizeof(int8_t) )
    # assign new value and insert node with address
    (<int8_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_int8_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_int8_t(node_ptr node, int8_t value) nogil except*:

    if deref(node).value != NULL:
        (<int8_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(int8_t) )
        (<int8_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_int8_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline int16_t __deref_value_ptr_int16_t(node_ptr node):

    return deref( <int16_t*>deref(node).value )


cdef inline void __insert_node_int16_t(rb_tree_ptr& index, key, int16_t value) except*:

    cdef void* address = malloc( sizeof(int16_t) )
    # assign new value and insert node with address
    (<int16_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_int16_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, int16_t value ) except*:

    cdef void* address = malloc( sizeof(int16_t) )
    # assign new value and insert node with address
    (<int16_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_int16_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_int16_t(node_ptr node, int16_t value) nogil except*:

    if deref(node).value != NULL:
        (<int16_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(int16_t) )
        (<int16_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_int16_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline int32_t __deref_value_ptr_int32_t(node_ptr node):

    return deref( <int32_t*>deref(node).value )


cdef inline void __insert_node_int32_t(rb_tree_ptr& index, key, int32_t value) except*:

    cdef void* address = malloc( sizeof(int32_t) )
    # assign new value and insert node with address
    (<int32_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_int32_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, int32_t value ) except*:

    cdef void* address = malloc( sizeof(int32_t) )
    # assign new value and insert node with address
    (<int32_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_int32_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_int32_t(node_ptr node, int32_t value) nogil except*:

    if deref(node).value != NULL:
        (<int32_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(int32_t) )
        (<int32_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_int32_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline int64_t __deref_value_ptr_int64_t(node_ptr node):

    return deref( <int64_t*>deref(node).value )


cdef inline void __insert_node_int64_t(rb_tree_ptr& index, key, int64_t value) except*:

    cdef void* address = malloc( sizeof(int64_t) )
    # assign new value and insert node with address
    (<int64_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_int64_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, int64_t value ) except*:

    cdef void* address = malloc( sizeof(int64_t) )
    # assign new value and insert node with address
    (<int64_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_int64_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_int64_t(node_ptr node, int64_t value) nogil except*:

    if deref(node).value != NULL:
        (<int64_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(int64_t) )
        (<int64_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_int64_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline int96_t __deref_value_ptr_int96_t(node_ptr node):

    return deref( <int96_t*>deref(node).value )


cdef inline void __insert_node_int96_t(rb_tree_ptr& index, key, int96_t value) except*:

    cdef void* address = malloc( sizeof(int96_t) )
    # assign new value and insert node with address
    (<int96_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_int96_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, int96_t value ) except*:

    cdef void* address = malloc( sizeof(int96_t) )
    # assign new value and insert node with address
    (<int96_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_int96_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_int96_t(node_ptr node, int96_t value) nogil except*:

    if deref(node).value != NULL:
        (<int96_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(int96_t) )
        (<int96_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_int96_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline int128_t __deref_value_ptr_int128_t(node_ptr node):

    return deref( <int128_t*>deref(node).value )


cdef inline void __insert_node_int128_t(rb_tree_ptr& index, key, int128_t value) except*:

    cdef void* address = malloc( sizeof(int128_t) )
    # assign new value and insert node with address
    (<int128_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_int128_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, int128_t value ) except*:

    cdef void* address = malloc( sizeof(int128_t) )
    # assign new value and insert node with address
    (<int128_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_int128_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_int128_t(node_ptr node, int128_t value) nogil except*:

    if deref(node).value != NULL:
        (<int128_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(int128_t) )
        (<int128_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_int128_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline float32_t __deref_value_ptr_float32_t(node_ptr node):

    return deref( <float32_t*>deref(node).value )


cdef inline void __insert_node_float32_t(rb_tree_ptr& index, key, float32_t value) except*:

    cdef void* address = malloc( sizeof(float32_t) )
    # assign new value and insert node with address
    (<float32_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_float32_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, float32_t value ) except*:

    cdef void* address = malloc( sizeof(float32_t) )
    # assign new value and insert node with address
    (<float32_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_float32_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_float32_t(node_ptr node, float32_t value) nogil except*:

    if deref(node).value != NULL:
        (<float32_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(float32_t) )
        (<float32_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_float32_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline float64_t __deref_value_ptr_float64_t(node_ptr node):

    return deref( <float64_t*>deref(node).value )


cdef inline void __insert_node_float64_t(rb_tree_ptr& index, key, float64_t value) except*:

    cdef void* address = malloc( sizeof(float64_t) )
    # assign new value and insert node with address
    (<float64_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_float64_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, float64_t value ) except*:

    cdef void* address = malloc( sizeof(float64_t) )
    # assign new value and insert node with address
    (<float64_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_float64_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_float64_t(node_ptr node, float64_t value) nogil except*:

    if deref(node).value != NULL:
        (<float64_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(float64_t) )
        (<float64_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_float64_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline float80_t __deref_value_ptr_float80_t(node_ptr node):

    return deref( <float80_t*>deref(node).value )


cdef inline void __insert_node_float80_t(rb_tree_ptr& index, key, float80_t value) except*:

    cdef void* address = malloc( sizeof(float80_t) )
    # assign new value and insert node with address
    (<float80_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_float80_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, float80_t value ) except*:

    cdef void* address = malloc( sizeof(float80_t) )
    # assign new value and insert node with address
    (<float80_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_float80_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_float80_t(node_ptr node, float80_t value) nogil except*:

    if deref(node).value != NULL:
        (<float80_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(float80_t) )
        (<float80_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_float80_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline float96_t __deref_value_ptr_float96_t(node_ptr node):

    return deref( <float96_t*>deref(node).value )


cdef inline void __insert_node_float96_t(rb_tree_ptr& index, key, float96_t value) except*:

    cdef void* address = malloc( sizeof(float96_t) )
    # assign new value and insert node with address
    (<float96_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_float96_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, float96_t value ) except*:

    cdef void* address = malloc( sizeof(float96_t) )
    # assign new value and insert node with address
    (<float96_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_float96_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_float96_t(node_ptr node, float96_t value) nogil except*:

    if deref(node).value != NULL:
        (<float96_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(float96_t) )
        (<float96_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_float96_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#


cdef inline float128_t __deref_value_ptr_float128_t(node_ptr node):

    return deref( <float128_t*>deref(node).value )


cdef inline void __insert_node_float128_t(rb_tree_ptr& index, key, float128_t value) except*:

    cdef void* address = malloc( sizeof(float128_t) )
    # assign new value and insert node with address
    (<float128_t*>address)[0] = value
    index.insert( rb_node_valued(to_c_pyobject(key), address) )


cdef inline  void __insert_node_by_ptr_float128_t( rb_tree_ptr& index, node_ptr& position, 
                                        		key, float128_t value ) except*:

    cdef void* address = malloc( sizeof(float128_t) )
    # assign new value and insert node with address
    (<float128_t*>address)[0] = value
    index.insert( position, rb_node_valued(to_c_pyobject(key), address) )


cdef void __erase_node_float128_t(rb_tree_ptr& index, key) except*:
    
    cdef c_pyobject c_key = c_pyobject(<PyObject*>key) 
    cdef node_ptr node = index.search(c_key)

    if ( node != index.link() ):
        # free memomry that has been used to keeping value
        if deref(node).value != NULL:
            free(deref(node).value)
        # Decrement reference counter to destroy key
        Py_XDECREF(deref(node).key.data)
        index.erase(node)


cdef inline void __set_value_float128_t(node_ptr node, float128_t value) nogil except*:

    if deref(node).value != NULL:
        (<float128_t*>deref(node).value)[0] = value

    else:
        deref(node).value = malloc( sizeof(float128_t) )
        (<float128_t*>deref(node).value)[0] = value


cdef inline void __dealloc_value_float128_t(node_ptr node) nogil except*:

    if deref(node).value != NULL:
        free(deref(node).value)


