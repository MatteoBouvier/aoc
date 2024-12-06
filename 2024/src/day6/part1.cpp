#include <array>
#include <cassert>
#include <iostream>
#include <string>
#include <sys/types.h>

#define MAP_SIZE 130

enum class Tile { empty, obstacle, visited };
enum class Direction { up, down, left, right };

class MapError : public std::exception {
public:
    MapError(std::string const &message) throw() : message(message) {}

    virtual const char *what() const throw() { return message.c_str(); }

private:
    std::string message;
};

class Map {
public:
    Map()
        : m_array{}, m_row_init(0), m_position({-1, -1}),
          m_direction(Direction::up), m_nb_visited(0) {};

    Tile at(const uint x, const uint y) { return m_array[x * MAP_SIZE + y]; }

    void set_at(const uint x, const uint y, Tile value) {
        m_array[x * MAP_SIZE + y] = value;
    }

    void set_visited(const uint x, const uint y) {
        switch (m_array[x * MAP_SIZE + y]) {
        case Tile::obstacle:
            throw MapError("Tried visiting an obstacle");
            break;

        case Tile::empty:
            m_array[x * MAP_SIZE + y] = Tile::visited;
            m_nb_visited++;
            break;

        case Tile::visited:
            break;
        }
    }

    void set_row(std::string line) {
        for (uint i = 0; i < line.size(); i++) {
            switch (line[i]) {
            case '.':
                set_at(m_row_init, i, Tile::empty);
                break;
            case '#':
                set_at(m_row_init, i, Tile::obstacle);
                break;
            case '^':
                m_position = {m_row_init, i};
                set_visited(m_row_init, i);
                break;
            }
        }

        m_row_init++;
    }

    bool try_visit(const uint x, const uint y) {
        if (at(x, y) == Tile::obstacle) {
            return false;
        }

        set_visited(x, y);
        return true;
    }

    void visit_all() {
        bool exited_map = false;

        while (not exited_map) {
            switch (m_direction) {
            case Direction::down:
                if (m_position.first == MAP_SIZE - 1) {
                    exited_map = true;
                    break;
                }

                if (try_visit(m_position.first + 1, m_position.second)) {
                    m_position.first++;
                } else {
                    m_direction = Direction::left;
                }

                break;

            case Direction::up:
                if (m_position.first == 0) {
                    exited_map = true;
                    break;
                }

                if (try_visit(m_position.first - 1, m_position.second)) {
                    m_position.first--;
                } else {
                    m_direction = Direction::right;
                }

                break;

            case Direction::right:
                if (m_position.second == MAP_SIZE - 1) {
                    exited_map = true;
                    break;
                }

                if (try_visit(m_position.first, m_position.second + 1)) {
                    m_position.second++;
                } else {
                    m_direction = Direction::down;
                }

                break;

            case Direction::left:
                if (m_position.second == 0) {
                    exited_map = true;
                    break;
                }

                if (try_visit(m_position.first, m_position.second - 1)) {
                    m_position.second--;
                } else {
                    m_direction = Direction::up;
                }

                break;
            }
        }
    }

    void print() {
        char tile;

        for (int x = 0; x < MAP_SIZE; x++) {
            for (int y = 0; y < MAP_SIZE; y++) {
                switch (at(x, y)) {
                case Tile::empty:
                    tile = '.';
                    break;

                case Tile::obstacle:
                    tile = '#';
                    break;

                case Tile::visited:
                    tile = 'X';
                    break;
                }

                std::cout << tile;
            }

            std::cout << std::endl;
        }
    }

    uint count_visited() { return m_nb_visited; }

private:
    std::array<Tile, MAP_SIZE * MAP_SIZE> m_array;
    uint m_row_init;
    std::pair<int, int> m_position;
    Direction m_direction;
    uint m_nb_visited;
};

int main(int argc, char *argv[]) {
    Map map{};

    for (std::string line; getline(std::cin, line);) {
        map.set_row(line);
    }

    map.visit_all();
    map.print();

    std::cout << map.count_visited() << std::endl;

    return 0;
}
