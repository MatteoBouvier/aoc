#pragma once

#include <string>
#include <sys/types.h>
#include <vector>

std::vector<uint> as_vector(std::string line);

template <class T> bool contains(std::vector<T> vec, T value) {
    return std::ranges::find(vec.begin(), vec.end(), value) != vec.end();
}
