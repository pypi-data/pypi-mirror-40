# threedvector Package

threedvector is a package providing common methods for working with 3D vectors in both Spherical and Cartesian coordinates.

Vectors are stored in Spherical format but can be created in both Spherical and Cartesian formats.

## Methods

### ___init__(radius_x=0, theta_y=0, phi_z=0, coords="spherical")_
Default Vector creation is in the Spherical coordinate system where `coords` is set to "spherical".  `radius_x` represents the length of the vector, `theta_y` the polar angle, theta and `phi_z` the azimuthal angle, phi.  

A Vector can be created using Cartesian coordinates with `coords` set to "cartesian" instead of "spherical".  In this case `radius_x` represents the `x` coordinate, `theta_y` the `y` coordinate and `phi_z` the `z` coordinate.

### _cartesian()_
Returns a `list` in the form of `[x, y, z]` representing the corresponding Cartesian coordinates of a vector.

### _is_same(s_vector)_
Compares the length as well as angles theta and phi of vector with `s_vector` to determine equality.  This is different to '=' which only checks for equality of the vector length.

### _dot(s_vector)_
Returns a `float` as the resultant dot product of a vector with `s_vector`.

### _cross(s_vector)_
Returns the `Vector` object resulting from the cross product of a vector with `s_vector`.

### _angle(s_vector)_
Returns a `float` as the in-plane angle in degrees between a vector and `s_vector`.

### _unit()_
Returns a `Vector` object as the corresponding unit vector of a vector.

### _magnitude()_
Returns a `float` as the length of a vector

### _theta()_
Returns a `float` as the polar angle theta of a vector in degrees

### _phi()_
Returns a `float` as the azimuthal angle phi of a vector in degrees

### _set_magnitude(magnitude)_
Sets the length of a vector to `magnitude` as 

### _set_theta(theta)_
Sets the polar angle, theta, of a vector to `theta` in degrees

### _set_phi(phi)_
Sets the azimuthal angle, phi, of a vector to `phi` in 

### _copy()
Returns a `Vector` object representing a copy of the `self`

### _addition_ and _subtraction_
Returns resulting `Vector` object.  Normal addition and subtraction are done through Cartesian addition and subtraction operations.

### _multiplication_
Multiplication is implemented as scalar multiplication only.  For dot and cross products, the corresponding methods should be used.

### _comparison_
All comparison operators return comparison with length of vectors only.
