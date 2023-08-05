#include <gxx/math/util.h>
//#include <stdint.h>

//extern float veryquick_rsqrt( float number );
//extern float quick_rsqrt( float number );

union float_long
{
	long i;
	float y;
};

float veryquick_rsqrt( float number )
{
	float x2;
	union float_long u;
	const float threehalfs = 1.5F;

	x2 = number * 0.5F;
	u.y  = number;
	//i  = 0x5f3759df - ( i >> 1 );               // what the fuck?
	u.i  = 0x5F375A86 - ( u.i >> 1 );               // what the fuck?
	u.y  = u.y * ( threehalfs - ( x2 * u.y * u.y ) );   // 1st iteration
	//u.y  = u.y * ( threehalfs - ( x2 * u.y * u.y ) );   // 2nd iteration, this can be removed

	return u.y;
}

float quick_rsqrt( float number )
{
	float x2;//, y;
	union float_long u;
	const float threehalfs = 1.5F;

	x2 = number * 0.5F;
	u.y  = number;
	//i  = 0x5f3759df - ( i >> 1 );               // what the fuck?
	u.i  = 0x5F375A86 - ( u.i >> 1 );               // what the fuck?
	u.y  = u.y * ( threehalfs - ( x2 * u.y * u.y ) );   // 1st iteration
	u.y  = u.y * ( threehalfs - ( x2 * u.y * u.y ) );   // 2nd iteration, this can be removed

	return u.y;
}
