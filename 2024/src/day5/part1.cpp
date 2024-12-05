#include <cassert>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <print>
#include <ranges>
#include <string>
#include <sys/types.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>

#include "./utils.h"

int main(int argc, char *argv[]) {
    std::unordered_map<uint, std::unordered_set<uint>> page_order{};
    std::vector<std::vector<uint>> updates{};
    uint total = 0;

    bool is_update = false;
    for (std::string line; getline(std::cin, line);) {
        if (line == "") {
            is_update = true;
            continue;
        }

        if (is_update) {
            updates.emplace_back(as_vector(line));

        } else {
            size_t index_pipe = line.find('|');
            assert(index_pipe != std::string::npos);

            const uint a = stoi(line.substr(0, index_pipe));
            const uint b = stoi(line.substr(index_pipe + 1));

            page_order.try_emplace(a, std::unordered_set<uint>());
            page_order[a].insert(b);
        }
    }

    auto is_valid_pair = [&page_order](uint a, uint b) {
        return page_order[a].contains(b);
    };

    for (auto update : updates) {
        bool is_valid = true;
        for (auto [a, b] : update | std::ranges::views::pairwise) {
            if (not is_valid_pair(a, b)) {
                is_valid = false;
                break;
            }
        }

        if (is_valid) {
            const size_t middle = std::floor(update.size() / 2);
            total += update[middle];
        }
    }

    std::cout << total << std::endl;

    return 0;
}
