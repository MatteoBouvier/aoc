#include <string>
#include <sys/types.h>
#include <vector>

#include "./utils.h"

std::vector<uint> as_vector(std::string line) {
    std::vector<uint> numbers{};

    while (line.size()) {
        size_t index_comma = line.find(',');

        numbers.push_back(stoi(line.substr(0, index_comma)));

        if (index_comma == std::string::npos) {
            break;
        }
        line = line.substr(index_comma + 1);
    }

    return numbers;
}
