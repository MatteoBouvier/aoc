#include <cstdio>
#include <iostream>
#include <string>
#include <vector>

struct Position {
    int x, y;
};

int main() {
    std::vector<std::string> lines = {};
    std::vector<Position> A_pos = {};
    int count = 0;

    int line_nb = 0;
    for (std::string line; getline(std::cin, line);) {
        if (line_nb >= 1) {
            for (int i = 1; i < line.size() - 1; i++) {
                if (line[i] == 'A') {
                    A_pos.emplace_back(Position(line_nb, i));
                }
            }
        }

        lines.emplace_back(line);

        line_nb++;
    }

    for (auto [x, y] : A_pos) {
        if (x == line_nb - 1) {
            continue;
        }

        char top_left = lines[x - 1][y - 1];
        char top_right = lines[x - 1][y + 1];
        char bottom_left = lines[x + 1][y - 1];
        char bottom_right = lines[x + 1][y + 1];

        if (((top_left == 'M' and bottom_right == 'S') or
             (top_left == 'S' and bottom_right == 'M')) and
            ((top_right == 'M' and bottom_left == 'S') or
             (top_right == 'S' and bottom_left == 'M'))) {
            count++;
        }
    }

    std::cout << count << std::endl;

    return 0;
}
