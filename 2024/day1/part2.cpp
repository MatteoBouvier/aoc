#include <iostream>
#include <stdexcept>
#include <string>
#include <sys/types.h>
#include <unordered_map>
#include <vector>

#include "utils.h"

/* read input from stdin */
int main() {

  std::vector<int> left;
  std::unordered_map<int, int> right_counts;

  for (std::string line; std::getline(std::cin, line);) {
    auto splits = split(line, ' ');

    if (splits.size() != 2) {
      throw std::length_error("Expected 2 values per line");
    }

    left.emplace_back(splits[0]);
    ++right_counts[splits[1]];
  }

  /*print_map(right_counts);*/

  uint score = 0;
  for (auto l : left) {
    score += l * right_counts[l];
  }

  std::cout << score << std::endl;

  return 0;
}
