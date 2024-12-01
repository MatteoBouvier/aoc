#include <string>
#include <vector>

#include "utils.h"

std::vector<int> split(const std::string &s, const char c) {
  std::vector<int> splits;
  size_t offset = 0;
  size_t pos = s.find(c, offset);

  while (pos != std::string::npos) {
    splits.push_back(stoi(s.substr(offset, pos)));

    // move pos to next non-space character
    while (s[pos] == ' ') {
      pos++;
    }
    offset = pos;
    pos = s.find(c, offset);
  }

  splits.push_back(stoi(s.substr(offset, pos)));

  return splits;
}
