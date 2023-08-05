#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef uint8_t ( *interpolate_uint8_t)(node_ptr, node_ptr, object, node_ptr, 
                   uint8_t, int32_t* )
ctypedef uint8_t (*itermode_search_uint8_t)(__TreeSeries_uint8_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef uint8_t __interpolate_floor_uint8_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, uint8_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_uint8_t(node_1)

    return extrapolate


cdef uint8_t __interpolate_ceil_uint8_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, uint8_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_uint8_t(node_2)

    return extrapolate


cdef uint8_t __interpolate_nn_uint8_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, uint8_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_uint8_t(node_2)

        return __deref_value_ptr_uint8_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_uint8_t(node_2)

    return __deref_value_ptr_uint8_t(node_1)


cdef uint8_t __interpolate_linear_uint8_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, uint8_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef uint8_t tan
    cdef uint8_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_uint8_t(node_1)

        return value + tan*(__deref_value_ptr_uint8_t(node_2) - value)

    return extrapolate


cdef uint8_t __interpolate_keys_only_uint8_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, uint8_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_uint8_t(node_1)

    error[0] = INT_KEY_ERROR

    return <uint8_t>0xdeadbeef 


cdef unordered_map[string, interpolate_uint8_t] __INTERPOLATE_uint8_t
__INTERPOLATE_uint8_t["floor"]  = &__interpolate_floor_uint8_t
__INTERPOLATE_uint8_t["ceil"]   = &__interpolate_ceil_uint8_t
__INTERPOLATE_uint8_t["nn"]     = &__interpolate_nn_uint8_t
__INTERPOLATE_uint8_t["linear"] = &__interpolate_linear_uint8_t
__INTERPOLATE_uint8_t["error"]  = &__interpolate_keys_only_uint8_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef uint16_t ( *interpolate_uint16_t)(node_ptr, node_ptr, object, node_ptr, 
                   uint16_t, int32_t* )
ctypedef uint16_t (*itermode_search_uint16_t)(__TreeSeries_uint16_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef uint16_t __interpolate_floor_uint16_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, uint16_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_uint16_t(node_1)

    return extrapolate


cdef uint16_t __interpolate_ceil_uint16_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, uint16_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_uint16_t(node_2)

    return extrapolate


cdef uint16_t __interpolate_nn_uint16_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, uint16_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_uint16_t(node_2)

        return __deref_value_ptr_uint16_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_uint16_t(node_2)

    return __deref_value_ptr_uint16_t(node_1)


cdef uint16_t __interpolate_linear_uint16_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, uint16_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef uint16_t tan
    cdef uint16_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_uint16_t(node_1)

        return value + tan*(__deref_value_ptr_uint16_t(node_2) - value)

    return extrapolate


cdef uint16_t __interpolate_keys_only_uint16_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, uint16_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_uint16_t(node_1)

    error[0] = INT_KEY_ERROR

    return <uint16_t>0xdeadbeef 


cdef unordered_map[string, interpolate_uint16_t] __INTERPOLATE_uint16_t
__INTERPOLATE_uint16_t["floor"]  = &__interpolate_floor_uint16_t
__INTERPOLATE_uint16_t["ceil"]   = &__interpolate_ceil_uint16_t
__INTERPOLATE_uint16_t["nn"]     = &__interpolate_nn_uint16_t
__INTERPOLATE_uint16_t["linear"] = &__interpolate_linear_uint16_t
__INTERPOLATE_uint16_t["error"]  = &__interpolate_keys_only_uint16_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef uint32_t ( *interpolate_uint32_t)(node_ptr, node_ptr, object, node_ptr, 
                   uint32_t, int32_t* )
ctypedef uint32_t (*itermode_search_uint32_t)(__TreeSeries_uint32_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef uint32_t __interpolate_floor_uint32_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, uint32_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_uint32_t(node_1)

    return extrapolate


cdef uint32_t __interpolate_ceil_uint32_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, uint32_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_uint32_t(node_2)

    return extrapolate


cdef uint32_t __interpolate_nn_uint32_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, uint32_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_uint32_t(node_2)

        return __deref_value_ptr_uint32_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_uint32_t(node_2)

    return __deref_value_ptr_uint32_t(node_1)


cdef uint32_t __interpolate_linear_uint32_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, uint32_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef uint32_t tan
    cdef uint32_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_uint32_t(node_1)

        return value + tan*(__deref_value_ptr_uint32_t(node_2) - value)

    return extrapolate


cdef uint32_t __interpolate_keys_only_uint32_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, uint32_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_uint32_t(node_1)

    error[0] = INT_KEY_ERROR

    return <uint32_t>0xdeadbeef 


cdef unordered_map[string, interpolate_uint32_t] __INTERPOLATE_uint32_t
__INTERPOLATE_uint32_t["floor"]  = &__interpolate_floor_uint32_t
__INTERPOLATE_uint32_t["ceil"]   = &__interpolate_ceil_uint32_t
__INTERPOLATE_uint32_t["nn"]     = &__interpolate_nn_uint32_t
__INTERPOLATE_uint32_t["linear"] = &__interpolate_linear_uint32_t
__INTERPOLATE_uint32_t["error"]  = &__interpolate_keys_only_uint32_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef uint64_t ( *interpolate_uint64_t)(node_ptr, node_ptr, object, node_ptr, 
                   uint64_t, int32_t* )
ctypedef uint64_t (*itermode_search_uint64_t)(__TreeSeries_uint64_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef uint64_t __interpolate_floor_uint64_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, uint64_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_uint64_t(node_1)

    return extrapolate


cdef uint64_t __interpolate_ceil_uint64_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, uint64_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_uint64_t(node_2)

    return extrapolate


cdef uint64_t __interpolate_nn_uint64_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, uint64_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_uint64_t(node_2)

        return __deref_value_ptr_uint64_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_uint64_t(node_2)

    return __deref_value_ptr_uint64_t(node_1)


cdef uint64_t __interpolate_linear_uint64_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, uint64_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef uint64_t tan
    cdef uint64_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_uint64_t(node_1)

        return value + tan*(__deref_value_ptr_uint64_t(node_2) - value)

    return extrapolate


cdef uint64_t __interpolate_keys_only_uint64_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, uint64_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_uint64_t(node_1)

    error[0] = INT_KEY_ERROR

    return <uint64_t>0xdeadbeef 


cdef unordered_map[string, interpolate_uint64_t] __INTERPOLATE_uint64_t
__INTERPOLATE_uint64_t["floor"]  = &__interpolate_floor_uint64_t
__INTERPOLATE_uint64_t["ceil"]   = &__interpolate_ceil_uint64_t
__INTERPOLATE_uint64_t["nn"]     = &__interpolate_nn_uint64_t
__INTERPOLATE_uint64_t["linear"] = &__interpolate_linear_uint64_t
__INTERPOLATE_uint64_t["error"]  = &__interpolate_keys_only_uint64_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef uint96_t ( *interpolate_uint96_t)(node_ptr, node_ptr, object, node_ptr, 
                   uint96_t, int32_t* )
ctypedef uint96_t (*itermode_search_uint96_t)(__TreeSeries_uint96_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef uint96_t __interpolate_floor_uint96_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, uint96_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_uint96_t(node_1)

    return extrapolate


cdef uint96_t __interpolate_ceil_uint96_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, uint96_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_uint96_t(node_2)

    return extrapolate


cdef uint96_t __interpolate_nn_uint96_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, uint96_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_uint96_t(node_2)

        return __deref_value_ptr_uint96_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_uint96_t(node_2)

    return __deref_value_ptr_uint96_t(node_1)


cdef uint96_t __interpolate_linear_uint96_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, uint96_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef uint96_t tan
    cdef uint96_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_uint96_t(node_1)

        return value + tan*(__deref_value_ptr_uint96_t(node_2) - value)

    return extrapolate


cdef uint96_t __interpolate_keys_only_uint96_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, uint96_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_uint96_t(node_1)

    error[0] = INT_KEY_ERROR

    return <uint96_t>0xdeadbeef 


cdef unordered_map[string, interpolate_uint96_t] __INTERPOLATE_uint96_t
__INTERPOLATE_uint96_t["floor"]  = &__interpolate_floor_uint96_t
__INTERPOLATE_uint96_t["ceil"]   = &__interpolate_ceil_uint96_t
__INTERPOLATE_uint96_t["nn"]     = &__interpolate_nn_uint96_t
__INTERPOLATE_uint96_t["linear"] = &__interpolate_linear_uint96_t
__INTERPOLATE_uint96_t["error"]  = &__interpolate_keys_only_uint96_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef uint128_t ( *interpolate_uint128_t)(node_ptr, node_ptr, object, node_ptr, 
                   uint128_t, int32_t* )
ctypedef uint128_t (*itermode_search_uint128_t)(__TreeSeries_uint128_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef uint128_t __interpolate_floor_uint128_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, uint128_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_uint128_t(node_1)

    return extrapolate


cdef uint128_t __interpolate_ceil_uint128_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, uint128_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_uint128_t(node_2)

    return extrapolate


cdef uint128_t __interpolate_nn_uint128_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, uint128_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_uint128_t(node_2)

        return __deref_value_ptr_uint128_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_uint128_t(node_2)

    return __deref_value_ptr_uint128_t(node_1)


cdef uint128_t __interpolate_linear_uint128_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, uint128_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef uint128_t tan
    cdef uint128_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_uint128_t(node_1)

        return value + tan*(__deref_value_ptr_uint128_t(node_2) - value)

    return extrapolate


cdef uint128_t __interpolate_keys_only_uint128_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, uint128_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_uint128_t(node_1)

    error[0] = INT_KEY_ERROR

    return <uint128_t>0xdeadbeef 


cdef unordered_map[string, interpolate_uint128_t] __INTERPOLATE_uint128_t
__INTERPOLATE_uint128_t["floor"]  = &__interpolate_floor_uint128_t
__INTERPOLATE_uint128_t["ceil"]   = &__interpolate_ceil_uint128_t
__INTERPOLATE_uint128_t["nn"]     = &__interpolate_nn_uint128_t
__INTERPOLATE_uint128_t["linear"] = &__interpolate_linear_uint128_t
__INTERPOLATE_uint128_t["error"]  = &__interpolate_keys_only_uint128_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef int8_t ( *interpolate_int8_t)(node_ptr, node_ptr, object, node_ptr, 
                   int8_t, int32_t* )
ctypedef int8_t (*itermode_search_int8_t)(__TreeSeries_int8_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef int8_t __interpolate_floor_int8_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, int8_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_int8_t(node_1)

    return extrapolate


cdef int8_t __interpolate_ceil_int8_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, int8_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_int8_t(node_2)

    return extrapolate


cdef int8_t __interpolate_nn_int8_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, int8_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_int8_t(node_2)

        return __deref_value_ptr_int8_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_int8_t(node_2)

    return __deref_value_ptr_int8_t(node_1)


cdef int8_t __interpolate_linear_int8_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, int8_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef int8_t tan
    cdef int8_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_int8_t(node_1)

        return value + tan*(__deref_value_ptr_int8_t(node_2) - value)

    return extrapolate


cdef int8_t __interpolate_keys_only_int8_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, int8_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_int8_t(node_1)

    error[0] = INT_KEY_ERROR

    return <int8_t>0xdeadbeef 


cdef unordered_map[string, interpolate_int8_t] __INTERPOLATE_int8_t
__INTERPOLATE_int8_t["floor"]  = &__interpolate_floor_int8_t
__INTERPOLATE_int8_t["ceil"]   = &__interpolate_ceil_int8_t
__INTERPOLATE_int8_t["nn"]     = &__interpolate_nn_int8_t
__INTERPOLATE_int8_t["linear"] = &__interpolate_linear_int8_t
__INTERPOLATE_int8_t["error"]  = &__interpolate_keys_only_int8_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef int16_t ( *interpolate_int16_t)(node_ptr, node_ptr, object, node_ptr, 
                   int16_t, int32_t* )
ctypedef int16_t (*itermode_search_int16_t)(__TreeSeries_int16_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef int16_t __interpolate_floor_int16_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, int16_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_int16_t(node_1)

    return extrapolate


cdef int16_t __interpolate_ceil_int16_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, int16_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_int16_t(node_2)

    return extrapolate


cdef int16_t __interpolate_nn_int16_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, int16_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_int16_t(node_2)

        return __deref_value_ptr_int16_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_int16_t(node_2)

    return __deref_value_ptr_int16_t(node_1)


cdef int16_t __interpolate_linear_int16_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, int16_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef int16_t tan
    cdef int16_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_int16_t(node_1)

        return value + tan*(__deref_value_ptr_int16_t(node_2) - value)

    return extrapolate


cdef int16_t __interpolate_keys_only_int16_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, int16_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_int16_t(node_1)

    error[0] = INT_KEY_ERROR

    return <int16_t>0xdeadbeef 


cdef unordered_map[string, interpolate_int16_t] __INTERPOLATE_int16_t
__INTERPOLATE_int16_t["floor"]  = &__interpolate_floor_int16_t
__INTERPOLATE_int16_t["ceil"]   = &__interpolate_ceil_int16_t
__INTERPOLATE_int16_t["nn"]     = &__interpolate_nn_int16_t
__INTERPOLATE_int16_t["linear"] = &__interpolate_linear_int16_t
__INTERPOLATE_int16_t["error"]  = &__interpolate_keys_only_int16_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef int32_t ( *interpolate_int32_t)(node_ptr, node_ptr, object, node_ptr, 
                   int32_t, int32_t* )
ctypedef int32_t (*itermode_search_int32_t)(__TreeSeries_int32_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef int32_t __interpolate_floor_int32_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, int32_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_int32_t(node_1)

    return extrapolate


cdef int32_t __interpolate_ceil_int32_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, int32_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_int32_t(node_2)

    return extrapolate


cdef int32_t __interpolate_nn_int32_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, int32_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_int32_t(node_2)

        return __deref_value_ptr_int32_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_int32_t(node_2)

    return __deref_value_ptr_int32_t(node_1)


cdef int32_t __interpolate_linear_int32_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, int32_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef int32_t tan
    cdef int32_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_int32_t(node_1)

        return value + tan*(__deref_value_ptr_int32_t(node_2) - value)

    return extrapolate


cdef int32_t __interpolate_keys_only_int32_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, int32_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_int32_t(node_1)

    error[0] = INT_KEY_ERROR

    return <int32_t>0xdeadbeef 


cdef unordered_map[string, interpolate_int32_t] __INTERPOLATE_int32_t
__INTERPOLATE_int32_t["floor"]  = &__interpolate_floor_int32_t
__INTERPOLATE_int32_t["ceil"]   = &__interpolate_ceil_int32_t
__INTERPOLATE_int32_t["nn"]     = &__interpolate_nn_int32_t
__INTERPOLATE_int32_t["linear"] = &__interpolate_linear_int32_t
__INTERPOLATE_int32_t["error"]  = &__interpolate_keys_only_int32_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef int64_t ( *interpolate_int64_t)(node_ptr, node_ptr, object, node_ptr, 
                   int64_t, int32_t* )
ctypedef int64_t (*itermode_search_int64_t)(__TreeSeries_int64_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef int64_t __interpolate_floor_int64_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, int64_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_int64_t(node_1)

    return extrapolate


cdef int64_t __interpolate_ceil_int64_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, int64_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_int64_t(node_2)

    return extrapolate


cdef int64_t __interpolate_nn_int64_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, int64_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_int64_t(node_2)

        return __deref_value_ptr_int64_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_int64_t(node_2)

    return __deref_value_ptr_int64_t(node_1)


cdef int64_t __interpolate_linear_int64_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, int64_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef int64_t tan
    cdef int64_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_int64_t(node_1)

        return value + tan*(__deref_value_ptr_int64_t(node_2) - value)

    return extrapolate


cdef int64_t __interpolate_keys_only_int64_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, int64_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_int64_t(node_1)

    error[0] = INT_KEY_ERROR

    return <int64_t>0xdeadbeef 


cdef unordered_map[string, interpolate_int64_t] __INTERPOLATE_int64_t
__INTERPOLATE_int64_t["floor"]  = &__interpolate_floor_int64_t
__INTERPOLATE_int64_t["ceil"]   = &__interpolate_ceil_int64_t
__INTERPOLATE_int64_t["nn"]     = &__interpolate_nn_int64_t
__INTERPOLATE_int64_t["linear"] = &__interpolate_linear_int64_t
__INTERPOLATE_int64_t["error"]  = &__interpolate_keys_only_int64_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef int96_t ( *interpolate_int96_t)(node_ptr, node_ptr, object, node_ptr, 
                   int96_t, int32_t* )
ctypedef int96_t (*itermode_search_int96_t)(__TreeSeries_int96_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef int96_t __interpolate_floor_int96_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, int96_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_int96_t(node_1)

    return extrapolate


cdef int96_t __interpolate_ceil_int96_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, int96_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_int96_t(node_2)

    return extrapolate


cdef int96_t __interpolate_nn_int96_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, int96_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_int96_t(node_2)

        return __deref_value_ptr_int96_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_int96_t(node_2)

    return __deref_value_ptr_int96_t(node_1)


cdef int96_t __interpolate_linear_int96_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, int96_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef int96_t tan
    cdef int96_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_int96_t(node_1)

        return value + tan*(__deref_value_ptr_int96_t(node_2) - value)

    return extrapolate


cdef int96_t __interpolate_keys_only_int96_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, int96_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_int96_t(node_1)

    error[0] = INT_KEY_ERROR

    return <int96_t>0xdeadbeef 


cdef unordered_map[string, interpolate_int96_t] __INTERPOLATE_int96_t
__INTERPOLATE_int96_t["floor"]  = &__interpolate_floor_int96_t
__INTERPOLATE_int96_t["ceil"]   = &__interpolate_ceil_int96_t
__INTERPOLATE_int96_t["nn"]     = &__interpolate_nn_int96_t
__INTERPOLATE_int96_t["linear"] = &__interpolate_linear_int96_t
__INTERPOLATE_int96_t["error"]  = &__interpolate_keys_only_int96_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef int128_t ( *interpolate_int128_t)(node_ptr, node_ptr, object, node_ptr, 
                   int128_t, int32_t* )
ctypedef int128_t (*itermode_search_int128_t)(__TreeSeries_int128_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef int128_t __interpolate_floor_int128_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, int128_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_int128_t(node_1)

    return extrapolate


cdef int128_t __interpolate_ceil_int128_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, int128_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_int128_t(node_2)

    return extrapolate


cdef int128_t __interpolate_nn_int128_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, int128_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_int128_t(node_2)

        return __deref_value_ptr_int128_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_int128_t(node_2)

    return __deref_value_ptr_int128_t(node_1)


cdef int128_t __interpolate_linear_int128_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, int128_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef int128_t tan
    cdef int128_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_int128_t(node_1)

        return value + tan*(__deref_value_ptr_int128_t(node_2) - value)

    return extrapolate


cdef int128_t __interpolate_keys_only_int128_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, int128_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_int128_t(node_1)

    error[0] = INT_KEY_ERROR

    return <int128_t>0xdeadbeef 


cdef unordered_map[string, interpolate_int128_t] __INTERPOLATE_int128_t
__INTERPOLATE_int128_t["floor"]  = &__interpolate_floor_int128_t
__INTERPOLATE_int128_t["ceil"]   = &__interpolate_ceil_int128_t
__INTERPOLATE_int128_t["nn"]     = &__interpolate_nn_int128_t
__INTERPOLATE_int128_t["linear"] = &__interpolate_linear_int128_t
__INTERPOLATE_int128_t["error"]  = &__interpolate_keys_only_int128_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef float32_t ( *interpolate_float32_t)(node_ptr, node_ptr, object, node_ptr, 
                   float32_t, int32_t* )
ctypedef float32_t (*itermode_search_float32_t)(__TreeSeries_float32_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef float32_t __interpolate_floor_float32_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, float32_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_float32_t(node_1)

    return extrapolate


cdef float32_t __interpolate_ceil_float32_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, float32_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_float32_t(node_2)

    return extrapolate


cdef float32_t __interpolate_nn_float32_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, float32_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_float32_t(node_2)

        return __deref_value_ptr_float32_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_float32_t(node_2)

    return __deref_value_ptr_float32_t(node_1)


cdef float32_t __interpolate_linear_float32_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, float32_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef float32_t tan
    cdef float32_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_float32_t(node_1)

        return value + tan*(__deref_value_ptr_float32_t(node_2) - value)

    return extrapolate


cdef float32_t __interpolate_keys_only_float32_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, float32_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_float32_t(node_1)

    error[0] = INT_KEY_ERROR

    return <float32_t>0xdeadbeef 


cdef unordered_map[string, interpolate_float32_t] __INTERPOLATE_float32_t
__INTERPOLATE_float32_t["floor"]  = &__interpolate_floor_float32_t
__INTERPOLATE_float32_t["ceil"]   = &__interpolate_ceil_float32_t
__INTERPOLATE_float32_t["nn"]     = &__interpolate_nn_float32_t
__INTERPOLATE_float32_t["linear"] = &__interpolate_linear_float32_t
__INTERPOLATE_float32_t["error"]  = &__interpolate_keys_only_float32_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef float64_t ( *interpolate_float64_t)(node_ptr, node_ptr, object, node_ptr, 
                   float64_t, int32_t* )
ctypedef float64_t (*itermode_search_float64_t)(__TreeSeries_float64_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef float64_t __interpolate_floor_float64_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, float64_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_float64_t(node_1)

    return extrapolate


cdef float64_t __interpolate_ceil_float64_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, float64_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_float64_t(node_2)

    return extrapolate


cdef float64_t __interpolate_nn_float64_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, float64_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_float64_t(node_2)

        return __deref_value_ptr_float64_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_float64_t(node_2)

    return __deref_value_ptr_float64_t(node_1)


cdef float64_t __interpolate_linear_float64_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, float64_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef float64_t tan
    cdef float64_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_float64_t(node_1)

        return value + tan*(__deref_value_ptr_float64_t(node_2) - value)

    return extrapolate


cdef float64_t __interpolate_keys_only_float64_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, float64_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_float64_t(node_1)

    error[0] = INT_KEY_ERROR

    return <float64_t>0xdeadbeef 


cdef unordered_map[string, interpolate_float64_t] __INTERPOLATE_float64_t
__INTERPOLATE_float64_t["floor"]  = &__interpolate_floor_float64_t
__INTERPOLATE_float64_t["ceil"]   = &__interpolate_ceil_float64_t
__INTERPOLATE_float64_t["nn"]     = &__interpolate_nn_float64_t
__INTERPOLATE_float64_t["linear"] = &__interpolate_linear_float64_t
__INTERPOLATE_float64_t["error"]  = &__interpolate_keys_only_float64_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef float80_t ( *interpolate_float80_t)(node_ptr, node_ptr, object, node_ptr, 
                   float80_t, int32_t* )
ctypedef float80_t (*itermode_search_float80_t)(__TreeSeries_float80_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef float80_t __interpolate_floor_float80_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, float80_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_float80_t(node_1)

    return extrapolate


cdef float80_t __interpolate_ceil_float80_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, float80_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_float80_t(node_2)

    return extrapolate


cdef float80_t __interpolate_nn_float80_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, float80_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_float80_t(node_2)

        return __deref_value_ptr_float80_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_float80_t(node_2)

    return __deref_value_ptr_float80_t(node_1)


cdef float80_t __interpolate_linear_float80_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, float80_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef float80_t tan
    cdef float80_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_float80_t(node_1)

        return value + tan*(__deref_value_ptr_float80_t(node_2) - value)

    return extrapolate


cdef float80_t __interpolate_keys_only_float80_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, float80_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_float80_t(node_1)

    error[0] = INT_KEY_ERROR

    return <float80_t>0xdeadbeef 


cdef unordered_map[string, interpolate_float80_t] __INTERPOLATE_float80_t
__INTERPOLATE_float80_t["floor"]  = &__interpolate_floor_float80_t
__INTERPOLATE_float80_t["ceil"]   = &__interpolate_ceil_float80_t
__INTERPOLATE_float80_t["nn"]     = &__interpolate_nn_float80_t
__INTERPOLATE_float80_t["linear"] = &__interpolate_linear_float80_t
__INTERPOLATE_float80_t["error"]  = &__interpolate_keys_only_float80_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef float96_t ( *interpolate_float96_t)(node_ptr, node_ptr, object, node_ptr, 
                   float96_t, int32_t* )
ctypedef float96_t (*itermode_search_float96_t)(__TreeSeries_float96_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef float96_t __interpolate_floor_float96_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, float96_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_float96_t(node_1)

    return extrapolate


cdef float96_t __interpolate_ceil_float96_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, float96_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_float96_t(node_2)

    return extrapolate


cdef float96_t __interpolate_nn_float96_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, float96_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_float96_t(node_2)

        return __deref_value_ptr_float96_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_float96_t(node_2)

    return __deref_value_ptr_float96_t(node_1)


cdef float96_t __interpolate_linear_float96_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, float96_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef float96_t tan
    cdef float96_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_float96_t(node_1)

        return value + tan*(__deref_value_ptr_float96_t(node_2) - value)

    return extrapolate


cdef float96_t __interpolate_keys_only_float96_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, float96_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_float96_t(node_1)

    error[0] = INT_KEY_ERROR

    return <float96_t>0xdeadbeef 


cdef unordered_map[string, interpolate_float96_t] __INTERPOLATE_float96_t
__INTERPOLATE_float96_t["floor"]  = &__interpolate_floor_float96_t
__INTERPOLATE_float96_t["ceil"]   = &__interpolate_ceil_float96_t
__INTERPOLATE_float96_t["nn"]     = &__interpolate_nn_float96_t
__INTERPOLATE_float96_t["linear"] = &__interpolate_linear_float96_t
__INTERPOLATE_float96_t["error"]  = &__interpolate_keys_only_float96_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef float128_t ( *interpolate_float128_t)(node_ptr, node_ptr, object, node_ptr, 
                   float128_t, int32_t* )
ctypedef float128_t (*itermode_search_float128_t)(__TreeSeries_float128_t, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef float128_t __interpolate_floor_float128_t( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, float128_t extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_float128_t(node_1)

    return extrapolate


cdef float128_t __interpolate_ceil_float128_t( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, float128_t extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_float128_t(node_2)

    return extrapolate


cdef float128_t __interpolate_nn_float128_t( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, float128_t extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_float128_t(node_2)

        return __deref_value_ptr_float128_t(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_float128_t(node_2)

    return __deref_value_ptr_float128_t(node_1)


cdef float128_t __interpolate_linear_float128_t( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, float128_t extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef float128_t tan
    cdef float128_t value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_float128_t(node_1)

        return value + tan*(__deref_value_ptr_float128_t(node_2) - value)

    return extrapolate


cdef float128_t __interpolate_keys_only_float128_t( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, float128_t extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_float128_t(node_1)

    error[0] = INT_KEY_ERROR

    return <float128_t>0xdeadbeef 


cdef unordered_map[string, interpolate_float128_t] __INTERPOLATE_float128_t
__INTERPOLATE_float128_t["floor"]  = &__interpolate_floor_float128_t
__INTERPOLATE_float128_t["ceil"]   = &__interpolate_ceil_float128_t
__INTERPOLATE_float128_t["nn"]     = &__interpolate_nn_float128_t
__INTERPOLATE_float128_t["linear"] = &__interpolate_linear_float128_t
__INTERPOLATE_float128_t["error"]  = &__interpolate_keys_only_float128_t
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Basics interpolation implementation.
#--------------------------------------------------------------------------------------------
ctypedef object ( *interpolate_object)(node_ptr, node_ptr, object, node_ptr, 
                   object, int32_t* )
ctypedef object (*itermode_search_object)(__TreeSeries_object, object, int32_t*)



# Interpolation for node wich key in [node_1->key, node_2->key]
cdef object __interpolate_floor_object( node_ptr node_1, node_ptr node_2, key, 
                                          node_ptr link, object extrapolate,
                                          int32_t* error ):
    
    if node_1 != link:
        return __deref_value_ptr_object(node_1)

    return extrapolate


cdef object __interpolate_ceil_object( node_ptr node_1, node_ptr node_2, key, 
                                         node_ptr link, object extrapolate,
                                         int32_t* error ):

    if node_2 != link:
        return __deref_value_ptr_object(node_2)

    return extrapolate


cdef object __interpolate_nn_object( node_ptr node_1, node_ptr node_2, key, 
                                       node_ptr link, object extrapolate,
                                       int32_t* error ):
    
    cdef object time_1
    cdef object time_2

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data

        if (time_2 - key) <= (key - time_1):
            return __deref_value_ptr_object(node_2)

        return __deref_value_ptr_object(node_1)

    elif (node_1 == link):
        return __deref_value_ptr_object(node_2)

    return __deref_value_ptr_object(node_1)


cdef object __interpolate_linear_object( node_ptr node_1, node_ptr node_2, key, 
                                           node_ptr link, object extrapolate,
                                           int32_t* error ):
    
    cdef object time_1
    cdef object time_2
    cdef object tan
    cdef object value

    if (node_1 != link) and (node_2 != link):

        time_1 = <object>deref(node_1).key.data
        time_2 = <object>deref(node_2).key.data
        tan = (key - time_1)/(time_2 - time_1)
        value = __deref_value_ptr_object(node_1)

        return value + tan*(__deref_value_ptr_object(node_2) - value)

    return extrapolate


cdef object __interpolate_keys_only_object( node_ptr node_1, node_ptr node_2, key, 
                                              node_ptr link, object extrapolate,
                                              int32_t* error ):
    
    if node_1 != link:

        if <object>deref(node_1).key.data == key:
            return __deref_value_ptr_object(node_1)

    error[0] = INT_KEY_ERROR

    return <object>0xdeadbeef 


cdef unordered_map[string, interpolate_object] __INTERPOLATE_object
__INTERPOLATE_object["floor"]  = &__interpolate_floor_object
__INTERPOLATE_object["ceil"]   = &__interpolate_ceil_object
__INTERPOLATE_object["nn"]     = &__interpolate_nn_object
__INTERPOLATE_object["linear"] = &__interpolate_linear_object
__INTERPOLATE_object["error"]  = &__interpolate_keys_only_object
