#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef uint8_t (*arithmetic_uint8_t)(uint8_t, uint8_t)
ctypedef __TreeSeries_uint8_t (*arithmetic_type_uint8_t)( __TreeSeries_uint8_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_uint8_t )


cdef inline uint8_t __add_uint8_t(uint8_t a, uint8_t b):

    return a + b


cdef inline uint8_t __sub_uint8_t(uint8_t a, uint8_t b):

    return a - b


cdef inline uint8_t __mul_uint8_t(uint8_t a, uint8_t b):

    return a * b


cdef inline uint8_t __div_uint8_t(uint8_t a, uint8_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef uint16_t (*arithmetic_uint16_t)(uint16_t, uint16_t)
ctypedef __TreeSeries_uint16_t (*arithmetic_type_uint16_t)( __TreeSeries_uint16_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_uint16_t )


cdef inline uint16_t __add_uint16_t(uint16_t a, uint16_t b):

    return a + b


cdef inline uint16_t __sub_uint16_t(uint16_t a, uint16_t b):

    return a - b


cdef inline uint16_t __mul_uint16_t(uint16_t a, uint16_t b):

    return a * b


cdef inline uint16_t __div_uint16_t(uint16_t a, uint16_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef uint32_t (*arithmetic_uint32_t)(uint32_t, uint32_t)
ctypedef __TreeSeries_uint32_t (*arithmetic_type_uint32_t)( __TreeSeries_uint32_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_uint32_t )


cdef inline uint32_t __add_uint32_t(uint32_t a, uint32_t b):

    return a + b


cdef inline uint32_t __sub_uint32_t(uint32_t a, uint32_t b):

    return a - b


cdef inline uint32_t __mul_uint32_t(uint32_t a, uint32_t b):

    return a * b


cdef inline uint32_t __div_uint32_t(uint32_t a, uint32_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef uint64_t (*arithmetic_uint64_t)(uint64_t, uint64_t)
ctypedef __TreeSeries_uint64_t (*arithmetic_type_uint64_t)( __TreeSeries_uint64_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_uint64_t )


cdef inline uint64_t __add_uint64_t(uint64_t a, uint64_t b):

    return a + b


cdef inline uint64_t __sub_uint64_t(uint64_t a, uint64_t b):

    return a - b


cdef inline uint64_t __mul_uint64_t(uint64_t a, uint64_t b):

    return a * b


cdef inline uint64_t __div_uint64_t(uint64_t a, uint64_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef uint96_t (*arithmetic_uint96_t)(uint96_t, uint96_t)
ctypedef __TreeSeries_uint96_t (*arithmetic_type_uint96_t)( __TreeSeries_uint96_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_uint96_t )


cdef inline uint96_t __add_uint96_t(uint96_t a, uint96_t b):

    return a + b


cdef inline uint96_t __sub_uint96_t(uint96_t a, uint96_t b):

    return a - b


cdef inline uint96_t __mul_uint96_t(uint96_t a, uint96_t b):

    return a * b


cdef inline uint96_t __div_uint96_t(uint96_t a, uint96_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef uint128_t (*arithmetic_uint128_t)(uint128_t, uint128_t)
ctypedef __TreeSeries_uint128_t (*arithmetic_type_uint128_t)( __TreeSeries_uint128_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_uint128_t )


cdef inline uint128_t __add_uint128_t(uint128_t a, uint128_t b):

    return a + b


cdef inline uint128_t __sub_uint128_t(uint128_t a, uint128_t b):

    return a - b


cdef inline uint128_t __mul_uint128_t(uint128_t a, uint128_t b):

    return a * b


cdef inline uint128_t __div_uint128_t(uint128_t a, uint128_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef int8_t (*arithmetic_int8_t)(int8_t, int8_t)
ctypedef __TreeSeries_int8_t (*arithmetic_type_int8_t)( __TreeSeries_int8_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_int8_t )


cdef inline int8_t __add_int8_t(int8_t a, int8_t b):

    return a + b


cdef inline int8_t __sub_int8_t(int8_t a, int8_t b):

    return a - b


cdef inline int8_t __mul_int8_t(int8_t a, int8_t b):

    return a * b


cdef inline int8_t __div_int8_t(int8_t a, int8_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef int16_t (*arithmetic_int16_t)(int16_t, int16_t)
ctypedef __TreeSeries_int16_t (*arithmetic_type_int16_t)( __TreeSeries_int16_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_int16_t )


cdef inline int16_t __add_int16_t(int16_t a, int16_t b):

    return a + b


cdef inline int16_t __sub_int16_t(int16_t a, int16_t b):

    return a - b


cdef inline int16_t __mul_int16_t(int16_t a, int16_t b):

    return a * b


cdef inline int16_t __div_int16_t(int16_t a, int16_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef int32_t (*arithmetic_int32_t)(int32_t, int32_t)
ctypedef __TreeSeries_int32_t (*arithmetic_type_int32_t)( __TreeSeries_int32_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_int32_t )


cdef inline int32_t __add_int32_t(int32_t a, int32_t b):

    return a + b


cdef inline int32_t __sub_int32_t(int32_t a, int32_t b):

    return a - b


cdef inline int32_t __mul_int32_t(int32_t a, int32_t b):

    return a * b


cdef inline int32_t __div_int32_t(int32_t a, int32_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef int64_t (*arithmetic_int64_t)(int64_t, int64_t)
ctypedef __TreeSeries_int64_t (*arithmetic_type_int64_t)( __TreeSeries_int64_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_int64_t )


cdef inline int64_t __add_int64_t(int64_t a, int64_t b):

    return a + b


cdef inline int64_t __sub_int64_t(int64_t a, int64_t b):

    return a - b


cdef inline int64_t __mul_int64_t(int64_t a, int64_t b):

    return a * b


cdef inline int64_t __div_int64_t(int64_t a, int64_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef int96_t (*arithmetic_int96_t)(int96_t, int96_t)
ctypedef __TreeSeries_int96_t (*arithmetic_type_int96_t)( __TreeSeries_int96_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_int96_t )


cdef inline int96_t __add_int96_t(int96_t a, int96_t b):

    return a + b


cdef inline int96_t __sub_int96_t(int96_t a, int96_t b):

    return a - b


cdef inline int96_t __mul_int96_t(int96_t a, int96_t b):

    return a * b


cdef inline int96_t __div_int96_t(int96_t a, int96_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef int128_t (*arithmetic_int128_t)(int128_t, int128_t)
ctypedef __TreeSeries_int128_t (*arithmetic_type_int128_t)( __TreeSeries_int128_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_int128_t )


cdef inline int128_t __add_int128_t(int128_t a, int128_t b):

    return a + b


cdef inline int128_t __sub_int128_t(int128_t a, int128_t b):

    return a - b


cdef inline int128_t __mul_int128_t(int128_t a, int128_t b):

    return a * b


cdef inline int128_t __div_int128_t(int128_t a, int128_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef float32_t (*arithmetic_float32_t)(float32_t, float32_t)
ctypedef __TreeSeries_float32_t (*arithmetic_type_float32_t)( __TreeSeries_float32_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_float32_t )


cdef inline float32_t __add_float32_t(float32_t a, float32_t b):

    return a + b


cdef inline float32_t __sub_float32_t(float32_t a, float32_t b):

    return a - b


cdef inline float32_t __mul_float32_t(float32_t a, float32_t b):

    return a * b


cdef inline float32_t __div_float32_t(float32_t a, float32_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef float64_t (*arithmetic_float64_t)(float64_t, float64_t)
ctypedef __TreeSeries_float64_t (*arithmetic_type_float64_t)( __TreeSeries_float64_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_float64_t )


cdef inline float64_t __add_float64_t(float64_t a, float64_t b):

    return a + b


cdef inline float64_t __sub_float64_t(float64_t a, float64_t b):

    return a - b


cdef inline float64_t __mul_float64_t(float64_t a, float64_t b):

    return a * b


cdef inline float64_t __div_float64_t(float64_t a, float64_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef float80_t (*arithmetic_float80_t)(float80_t, float80_t)
ctypedef __TreeSeries_float80_t (*arithmetic_type_float80_t)( __TreeSeries_float80_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_float80_t )


cdef inline float80_t __add_float80_t(float80_t a, float80_t b):

    return a + b


cdef inline float80_t __sub_float80_t(float80_t a, float80_t b):

    return a - b


cdef inline float80_t __mul_float80_t(float80_t a, float80_t b):

    return a * b


cdef inline float80_t __div_float80_t(float80_t a, float80_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef float96_t (*arithmetic_float96_t)(float96_t, float96_t)
ctypedef __TreeSeries_float96_t (*arithmetic_type_float96_t)( __TreeSeries_float96_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_float96_t )


cdef inline float96_t __add_float96_t(float96_t a, float96_t b):

    return a + b


cdef inline float96_t __sub_float96_t(float96_t a, float96_t b):

    return a - b


cdef inline float96_t __mul_float96_t(float96_t a, float96_t b):

    return a * b


cdef inline float96_t __div_float96_t(float96_t a, float96_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef float128_t (*arithmetic_float128_t)(float128_t, float128_t)
ctypedef __TreeSeries_float128_t (*arithmetic_type_float128_t)( __TreeSeries_float128_t, 
													      __BaseTreeSeries, 
                                                          arithmetic_float128_t )


cdef inline float128_t __add_float128_t(float128_t a, float128_t b):

    return a + b


cdef inline float128_t __sub_float128_t(float128_t a, float128_t b):

    return a - b


cdef inline float128_t __mul_float128_t(float128_t a, float128_t b):

    return a * b


cdef inline float128_t __div_float128_t(float128_t a, float128_t b):

    return a / b
#
#  Created by Soldoskikh Kirill.
#  Copyright © 2018 Intuition. All rights reserved.
#

#--------------------------------------------------------------------------------------------
# Arithmetic helpers
#--------------------------------------------------------------------------------------------
ctypedef object (*arithmetic_object)(object, object)
ctypedef __TreeSeries_object (*arithmetic_type_object)( __TreeSeries_object, 
													      __BaseTreeSeries, 
                                                          arithmetic_object )


cdef inline object __add_object(object a, object b):

    return a + b


cdef inline object __sub_object(object a, object b):

    return a - b


cdef inline object __mul_object(object a, object b):

    return a * b


cdef inline object __div_object(object a, object b):

    return a / b
