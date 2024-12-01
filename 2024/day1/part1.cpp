#include <cstddef>
#include <iostream>
#include <print>
#include <ranges>
#include <set>
#include <stdexcept>
#include <string>

#include "utils.h"

/* read input from stdin */
int main() {

  std::multiset<int> set1, set2;

  for (std::string line; std::getline(std::cin, line);) {
    auto splits = split(line, ' ');

    if (splits.size() != 2) {
      throw std::length_error("Expected 2 values per line");
    }

    set1.insert(splits[0]);
    set2.insert(splits[1]);
  }

  auto distance = [](const int &a, const int &b) { return std::abs(a - b); };
  auto view = std::views::zip_transform(distance, set1, set2);

  size_t total = 0;
  for (auto e : view) {
    total += e;
  }

  std::cout << total << std::endl;

  return 0;
}
