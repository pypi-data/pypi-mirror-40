#include <gxx/io/ostream.h>
#include <gxx/io/spec.h>

#include <gxx/panic.h>

ssize_t gxx::io::ostream::format_print(float num, gxx::buffer opts)
{
	gxx::io::float_spec spec(opts);
	return format_print(num, spec);
}

ssize_t gxx::io::ostream::format_print(float num, const gxx::io::float_spec& spec)
{
	char body[32];
	if (spec.width > 32) panic("fprint");
	ftoa(num, body, 5);
	return format_print(body, strlen(body), spec);
}

ssize_t gxx::io::ostream::format_print(double num, gxx::buffer opts)
{
	gxx::io::float_spec spec(opts);
	return format_print(num, spec);
}

ssize_t gxx::io::ostream::format_print(double num, const gxx::io::float_spec& spec)
{
	char body[32];
	if (spec.width > 32) panic("fprint");
	ftoa(num, body, 5);
	return format_print(body, strlen(body), spec);
}

ssize_t gxx::io::ostream::format_print(int32_t num, gxx::buffer opts)
{
	gxx::io::integer_spec spec(opts);
	return format_print(num, spec);
}

ssize_t gxx::io::ostream::format_print(int32_t num, const gxx::io::integer_spec& spec)
{
	char body[32];
	if (spec.width > 32) panic("fprint");
	i32toa(num, body, 10);
	return format_print(body, strlen(body), spec);
}

ssize_t gxx::io::ostream::format_print(const char* str, gxx::buffer opts)
{
	gxx::io::text_spec spec(opts);
	return format_print(str, strlen(str), spec);
}

ssize_t gxx::io::ostream::format_print(const char* body_, size_t bodylen, gxx::buffer opts)
{
	return format_print(body_, bodylen, text_spec(opts));
}

ssize_t gxx::io::ostream::format_print(const char* body_, size_t bodylen, const gxx::io::basic_spec& spec)
{
	/*char body[32];
	memcpy(body, body_, bodylen > 32 ? 32 : bodylen);*/

	int ret = 0;

	//if (spec.width > 32) panic("fprint");

	int pre_fill_len = 0;
	char post_fill_len = 0;

	/*if (spec.tcase == text_case::upper)
	{
		for (unsigned int i = 0; i < bodylen; ++i)
		{
			body[i] = toupper(body[i]);
		}
	}*/

	if (spec.tcase == text_case::lower)
	{
		PANIC_TRACED();
	}

	int difflen = spec.width - bodylen;

	if (difflen > 0)
	{
		switch (spec.align)
		{
			case alignment::left:
				post_fill_len = difflen;
				break;

			case alignment::right:
				pre_fill_len = difflen;
				break;

			case alignment::center:
				pre_fill_len = difflen / 2;
				post_fill_len = difflen / 2;

				if (difflen % 2) pre_fill_len++;

				break;
		}
	}

	if (pre_fill_len)
	{
		ret += fill(spec.fill, pre_fill_len);
	}

	ret += write(body_, bodylen);

	if (post_fill_len)
	{
		ret += fill(spec.fill, post_fill_len);
	}

	return ret;
}