#pragma once

#include <stdint.h>

template <typename S> struct fnv_internal;
template <typename S> struct fnv1;
template <typename S> struct fnv1a;

template <> struct fnv_internal<uint64_t>
{
	constexpr static uint64_t default_offset_basis = 0x811C9DC5;
	constexpr static uint64_t prime                = 0x01000193;
};

template <> struct fnv1<uint64_t> : public fnv_internal<uint64_t>
{
	constexpr static inline uint64_t hash(char const*const aString, const uint64_t val = default_offset_basis)
	{
		return (aString[0] == '\0') ? val : hash( &aString[1], ( val * prime ) ^ uint64_t(aString[0]) );
	}
};

template <> struct fnv1a<uint64_t> : public fnv_internal<uint64_t>
{
	constexpr static inline uint64_t hash(char const*const aString, const uint64_t val = default_offset_basis)
	{
		return (aString[0] == '\0') ? val : hash( &aString[1], ( val ^ uint64_t(aString[0]) ) * prime);
	}
};