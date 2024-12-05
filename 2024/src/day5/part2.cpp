#include <algorithm>
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

bool is_valid_pair(
    std::unordered_map<uint, std::unordered_set<uint>> &page_order, uint a,
    uint b) {
    return page_order[a].contains(b);
};

void reorder(std::vector<uint> &update,
             std::unordered_map<uint, std::unordered_set<uint>> &page_order,
             uint start = 0) {
    for (int i = start; i < update.size() - 1; i++) {
        if (not is_valid_pair(page_order, update[i], update[i + 1])) {
            std::iter_swap(update.begin() + i, update.begin() + i + 1);
            reorder(update, page_order, start = std::max(0, i - 1));
            break;
        }
    }
}

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

    for (auto update : updates) {
        bool is_valid = true;
        for (auto [a, b] : update | std::ranges::views::pairwise) {
            if (not is_valid_pair(page_order, a, b)) {
                is_valid = false;
                break;
            }
        }

        if (not is_valid) {
            reorder(update, page_order);

            const size_t middle = std::floor(update.size() / 2);
            total += update[middle];
        }
    }

    std::cout << total << std::endl;

    return 0;
}
