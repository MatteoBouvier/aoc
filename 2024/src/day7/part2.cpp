#include <cmath>
#include <cstddef>
#include <cstdint>
#include <generator>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

void load_values(std::vector<uint64_t> &test_values,
                 std::vector<std::vector<uint64_t>> &numbers) {
    for (std::string line; getline(std::cin, line);) {
        uint colon_pos = line.find(':');
        test_values.emplace_back(stoull(line.substr(0, colon_pos)));
        std::vector<uint64_t> number_values = {};

        line = line.substr(colon_pos + 2);
        while (line.size()) {
            size_t space_pos = line.find(' ');
            number_values.emplace_back(stoull(line.substr(0, space_pos)));

            if (space_pos == std::string::npos) {
                break;
            }
            line = line.substr(space_pos + 1);
        }

        numbers.push_back(number_values);
    }
}

uint64_t equation(const uint64_t test_value,
                  const std::vector<uint64_t> &numbers) {
    uint mask;
    std::vector<uint> combs;
    combs.reserve(numbers.size() - 1);

    bool found_equation = false;
    for (uint comb = 0; comb < pow(3, numbers.size()); comb++) {
        for (uint i = 0; i < numbers.size() - 1; i++) {
            combs[i] = comb % (uint)pow(3, i + 1) / pow(3, i);
        }

        uint64_t total = numbers[0];
        for (uint i = 0; i < numbers.size() - 1; i++) {
            switch (combs[i]) {
            case 0:
                total += numbers[i + 1];
                break;

            case 1:
                total *= numbers[i + 1];
                break;

            case 2:
                total = stoull(std::to_string(total) +
                               std::to_string(numbers[i + 1]));
                break;

            default:
                throw std::invalid_argument("");
            }
        }

        if (total == test_value) {
            found_equation = true;
            break;
        }
    }

    if (found_equation) {
        return test_value;
    }

    return 0;
}

uint64_t
get_total_equations(const std::vector<uint64_t> &test_values,
                    const std::vector<std::vector<uint64_t>> &numbers) {
    uint64_t total = 0;

    for (auto [test_value, numbs] :
         std::ranges::views::zip(test_values, numbers)) {
        total += equation(test_value, numbs);
    }

    return total;
}

int main(int argc, char *argv[]) {
    std::vector<uint64_t> test_values{};
    std::vector<std::vector<uint64_t>> numbers{};

    load_values(test_values, numbers);

    uint64_t total = get_total_equations(test_values, numbers);
    std::cout << total << std::endl;

    return 0;
}
