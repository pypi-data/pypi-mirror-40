# threedvector Package

threedvector is a package providing common methods for working with 3D vectors in both Spherical and Cartesian coordinates.

Vectors are stored in Spherical format but can be created in both Spherical and Cartesian formats.

## Methods

### _to_spherical([x, y, z])
Returns a Vector opject based on `[x, y, z]` cartesian cooridates.

### _to_cartesian()_
Returns a list in the form of `[x, y, z]` representing the corresponding Cartesian coordinates for a vector.

### _is_same()_
Compares the length as well as angles theta and phi to determine equality.  This is different to '=' which only checks for equality of the vector length.

### _dot(s_vector)_
Returns the resultant scalar dot product of a vector with `s_vector`.

### _cross(s_vector)_
Returns  `Vector` resulting from the cross product of a vector with `s_vector`.

### _angle(s_vector)_
Returns the in-plane angle between a vector and `s_vector`.

### _magnitude()_
Returns the length of a vector.

### _unit()_
Returns the corresponding unit vector of a vector.

### _addition_ and _subtraction_
Returns resulting Vector.  Normal addition and subtraction is done through cartesian addition and subtraction operations.

### _multplication_
Multiplication is implemented as scalar multiplication only.  For dot and cross products the corresponding methods should be used.

### _comparison_
All comparison operators returns comparison with length of vectors only.

## Atributes

### _radius_
Returns the length of a vector

### _theta_
Returns the angle theta of a vector

### _phi_
Returns the ancle phi of a vector