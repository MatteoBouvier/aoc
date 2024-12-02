#pragma once

#include <iostream>
#include <ranges>
#include <set>
#include <unordered_map>
#include <vector>

template <class T> void print_vec(std::vector<T> vec) {
    std::cout << "Vector[";

    for (auto e : vec | std::views::take(vec.size() - 1)) {
        std::cout << e << ", ";
    }

    std::cout << vec[vec.size() - 1] << ']' << std::endl;
}

template <class T> void print_set(std::multiset<T> set) {
    std::cout << "Set{";

    for (auto e : set | std::views::take(set.size() - 1)) {
        std::cout << e << ", ";
    }

    std::cout << set[set.size() - 1] << '}' << std::endl;
}

template <class K, class V> void print_map(std::unordered_map<K, V> map) {
    std::cout << "Map{\n";

    for (auto e : map) {
        std::cout << e.first << " = " << e.second << "\n";
    }

    std::cout << "}" << std::endl;
}
