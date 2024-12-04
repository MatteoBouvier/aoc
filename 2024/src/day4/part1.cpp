#include <iostream>
#include <ostream>
#include <print>
#include <string>
#include <vector>

struct Position {
    int line_nb;
    int line_pos;
};

const std::string XMAS = "XMAS";

int main() {
    std::vector<std::string> lines = {};
    std::vector<Position> X_pos = {};
    int count = 0;

    int line_nb = 0;
    for (std::string line; std::getline(std::cin, line);) {
        // scan line to get X char positions
        for (int i{}; i < line.size(); i++) {
            if (line[i] == 'X') {
                X_pos.emplace_back(Position(line_nb, i));
            }
        }

        lines.emplace_back(line);
        line_nb++;
    }

    const int height = lines.size();
    const int width = lines[0].size();

    for (auto [x, y] : X_pos) {
        std::string line = lines[x];

        // horizontal --> scan
        if (line.substr(y, 4) == "XMAS") {
            count++;
        }

        // horizontal <-- scan
        if (y >= 3 and line.substr(y - 3, 4) == "SAMX") {
            count++;
        }

        // vertical v scan
        if (x <= height - 4) {
            bool is_match = true;
            for (int offset = 1; offset < 4; offset++) {
                if (lines[x + offset][y] != XMAS[offset]) {
                    is_match = false;
                    break;
                }
            }

            if (is_match) {
                count++;
            }
        }

        // vertical ^ scan
        if (x >= 3) {
            bool is_match = true;
            for (int offset = 1; offset < 4; offset++) {
                if (lines[x - offset][y] != XMAS[offset]) {
                    is_match = false;
                    break;
                }
            }

            if (is_match) {
                count++;
            }
        }

        // diagonal >v scan
        if (x <= height - 4 and y <= width - 4) {
            bool is_match = true;
            for (int offset = 1; offset < 4; offset++) {
                if (lines[x + offset][y + offset] != XMAS[offset]) {
                    is_match = false;
                    break;
                }
            }

            if (is_match) {
                count++;
            }
        }

        // diagonal <v scan
        if (x <= height - 4 and y >= 3) {
            bool is_match = true;
            for (int offset = 1; offset < 4; offset++) {
                if (lines[x + offset][y - offset] != XMAS[offset]) {
                    is_match = false;
                    break;
                }
            }

            if (is_match) {
                count++;
            }
        }

        // diagonal <v scan
        if (x >= 3 and y <= width - 4) {
            bool is_match = true;
            for (int offset = 1; offset < 4; offset++) {
                if (lines[x - offset][y + offset] != XMAS[offset]) {
                    is_match = false;
                    break;
                }
            }

            if (is_match) {
                count++;
            }
        }

        // diagonal <^ scan
        if (x >= 3 and y >= 3) {
            bool is_match = true;
            for (int offset = 1; offset < 4; offset++) {
                if (lines[x - offset][y - offset] != XMAS[offset]) {
                    is_match = false;
                    break;
                }
            }

            if (is_match) {
                count++;
            }
        }
    }

    std::cout << count << std::endl;

    return 0;
}
