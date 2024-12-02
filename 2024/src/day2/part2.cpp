#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <ostream>
#include <ranges>
#include <stdexcept>
#include <string>
#include <sys/types.h>
#include <vector>

#include "../print.h"

enum class Variation { decreasing, unsure, increasing };

/* Analyze levels, expects at least 2 levels separated by spaces */
bool is_safe(const std::string &levels) {
    std::vector<int> ilevels;
    size_t pos = 0, prev = 0;

    while (pos != std::string::npos) {
        pos = levels.find(' ', prev);
        ilevels.emplace_back(stoi(levels.substr(prev, pos)));
        prev = pos + 1;
    }

    std::adjacent_difference(ilevels.begin(), ilevels.end(), ilevels.begin());

    Variation is_increasing = Variation::unsure;
    int first_inc = -1, first_dec = -1, invalid_index = -1;

    for (int i = 1; i < ilevels.size(); ++i) {

        if (ilevels[i] > 0) {
            if (first_inc == -1) {
                first_inc = i;

                continue;
            }

            if (is_increasing == Variation::unsure) {
                is_increasing = Variation::increasing;
                continue;
            }

            if (is_increasing == Variation::decreasing) {
                if (invalid_index == -1) {
                    invalid_index = i;
                } else {
                    return false;
                }
            }

        } else if (ilevels[i] < 0) {
            if (first_dec == -1) {
                first_dec = i;

                continue;
            }

            if (is_increasing == Variation::unsure) {
                is_increasing = Variation::decreasing;
                continue;
            }

            if (is_increasing == Variation::increasing) {
                if (invalid_index == -1) {
                    invalid_index = i;
                } else {
                    return false;
                }
            }
        } else {
            // no variation
            if (invalid_index == -1) {
                invalid_index = i;
            } else {
                return false;
            }
        }
    }

    switch (is_increasing) {
    case Variation::unsure:
        throw std::logic_error("unsure");
        break;

    case Variation::increasing:
        if (first_dec != -1) {
            if (invalid_index == -1) {
                invalid_index = first_dec;
            } else {
                return false;
            }
        }
        break;

    case Variation::decreasing:
        if (first_inc != -1) {
            if (invalid_index == -1) {
                invalid_index = first_inc;
            } else {
                return false;
            }
        }
        break;
    }

    if (invalid_index != -1) {
        ilevels.erase(ilevels.begin() + invalid_index);
    }

    auto differences = ilevels | std::views::drop(1);

    if (std::any_of(differences.begin(), differences.end(), [](int e) {
            e = std::abs(e);
            return e < 1 or e > 3;
        })) {
        return false;
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
