#include <cstdlib>
#include <iostream>
#include <string>
#include <sys/types.h>

/* Analyze levels, expects at least 2 levels separated by spaces */
bool is_safe(const std::string &levels) {
    int level_a, level_b;
    size_t pos = 0, prev = 0;

    pos = levels.find(' ', 0);
    level_a = stoi(levels.substr(0, pos));
    prev = pos + 1;

    pos = levels.find(' ', prev);
    level_b = stoi(levels.substr(prev, pos));
    prev = pos + 1;

    bool increasing = (level_b - level_a) > 0;
    auto valid_variation = [increasing](int a, int b) {
        return increasing ? (b - a) > 0 : (b - a) < 0;
    };
    auto valid_difference = [](int a, int b) {
        int difference = std::abs(b - a);
        return difference >= 1 and difference <= 3;
    };
    auto valid_level_pair = [&](int a, int b) {
        return valid_variation(a, b) and valid_difference(a, b);
    };

    if (not valid_level_pair(level_a, level_b)) {
        return false;
    }

    while (pos != std::string::npos) {
        level_a = level_b;

        pos = levels.find(' ', prev);
        level_b = stoi(levels.substr(prev, pos));
        prev = pos + 1;

        if (not valid_level_pair(level_a, level_b)) {
            return false;
        }
    }

    return true;
}

int main() {
    uint counter = 0;

    for (std::string line; std::getline(std::cin, line);) {
        if (is_safe(line)) {
            counter++;
        }
    }

    std::cout << counter << std::endl;

    return 0;
}
