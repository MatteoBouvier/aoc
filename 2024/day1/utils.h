#include <iostream>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>

#pragma once

std::vector<int> split(const std::string &s, const char c);

template <class T> void print_set(std::multiset<T> set) {
  std::cout << "Set{";

  for (auto e : set) {
    std::cout << e << ", ";
  }

  std::cout << '}' << std::endl;
}
template <class K, class V> void print_map(std::unordered_map<K, V> map) {
  std::cout << "Map{\n";

  for (auto e : map) {
    std::cout << e.first << " = " << e.second << "\n";
  }

  std::cout << "}" << std::endl;
}
