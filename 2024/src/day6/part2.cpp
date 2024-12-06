#include <array>
#include <cassert>
#include <iostream>
#include <print>
#include <string>
#include <sys/types.h>

#define MAP_SIZE 130

enum class TileKind { empty, obstacle, visited };
enum class Direction { none, up, down, left, right };

struct Position {
    uint x, y;
};

struct Tile {
    TileKind kind;
    Direction direction;
};

struct Visit {
    bool hit_wall, found_cycle;
};

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
        : m_array{}, m_row_init(0), m_position({0, 0}),
          m_direction(Direction::up) {};

    Tile at(const std::array<Tile, MAP_SIZE * MAP_SIZE> &array, const uint x,
            const uint y) {
        return array[x * MAP_SIZE + y];
    }

    void set_at(std::array<Tile, MAP_SIZE * MAP_SIZE> &array, const uint x,
                const uint y, Tile value) {
        array[x * MAP_SIZE + y] = value;
    }

    void set_visited(std::array<Tile, MAP_SIZE * MAP_SIZE> &array, const uint x,
                     const uint y, Direction direction) {
        switch (array[x * MAP_SIZE + y].kind) {
        case TileKind::obstacle:
            throw MapError("Tried visiting an obstacle");
            break;

        case TileKind::empty:
            array[x * MAP_SIZE + y] = Tile(TileKind::visited, direction);
            break;

        case TileKind::visited:
            break;
        }
    }

    void set_row(std::string line) {
        for (uint i = 0; i < line.size(); i++) {
            switch (line[i]) {
            case '.':
                set_at(m_array, m_row_init, i,
                       Tile(TileKind::empty, Direction::none));
                break;

            case '#':
                set_at(m_array, m_row_init, i,
                       Tile(TileKind::obstacle, Direction::none));
                break;

            case '^':
                m_position = {m_row_init, i};
                m_array[m_row_init * MAP_SIZE + i] =
                    Tile(TileKind::visited, Direction::up);
                break;
            }
        }

        m_row_init++;
    }

    Visit try_visit(std::array<Tile, MAP_SIZE * MAP_SIZE> &array, const uint x,
                    const uint y, Direction direction) {
        Tile tile = at(array, x, y);

        if (tile.kind == TileKind::obstacle) {
            return Visit(true, false);
        } else if (tile.kind == TileKind::visited and
                   tile.direction == direction) {
            return Visit(false, true);
        }

        set_visited(array, x, y, direction);
        return Visit(false, false);
    }

    bool check_cycle(Position new_obstacle) {
        bool exited_map = false;
        bool found_cycle = false;
        Visit visit;
        Position position = m_position;
        Direction direction = m_direction;
        std::array<Tile, MAP_SIZE * MAP_SIZE> array;
        for (uint i = 0; i < array.size(); i++) {
            array[i] = Tile(m_array[i].kind, m_array[i].direction);
        }

        if (new_obstacle.x == m_position.x and new_obstacle.y == m_position.y) {
            return false;
        }

        if (at(array, new_obstacle.x, new_obstacle.y).kind ==
            TileKind::obstacle) {
            return false;
        }

        set_at(array, new_obstacle.x, new_obstacle.y,
               Tile(TileKind::obstacle, Direction::none));

        while (not exited_map and not found_cycle) {
            switch (direction) {
            case Direction::down:
                if (position.x == MAP_SIZE - 1) {
                    exited_map = true;
                    break;
                }

                visit = try_visit(array, position.x + 1, position.y,
                                  Direction::down);

                if (visit.found_cycle) {
                    found_cycle = true;
                    break;
                }

                if (visit.hit_wall) {
                    direction = Direction::left;
                } else {
                    position.x++;
                }

                break;

            case Direction::up:
                if (position.x == 0) {
                    exited_map = true;
                    break;
                }

                visit =
                    try_visit(array, position.x - 1, position.y, Direction::up);

                if (visit.found_cycle) {
                    found_cycle = true;
                    break;
                }

                if (visit.hit_wall) {
                    direction = Direction::right;
                } else {
                    position.x--;
                }

                break;

            case Direction::right:
                if (position.y == MAP_SIZE - 1) {
                    exited_map = true;
                    break;
                }

                visit = try_visit(array, position.x, position.y + 1,
                                  Direction::right);

                if (visit.found_cycle) {
                    found_cycle = true;
                    break;
                }

                if (visit.hit_wall) {
                    direction = Direction::down;
                } else {
                    position.y++;
                }

                break;

            case Direction::left:
                if (position.y == 0) {
                    exited_map = true;
                    break;
                }

                visit = try_visit(array, position.x, position.y - 1,
                                  Direction::left);

                if (visit.found_cycle) {
                    found_cycle = true;
                    break;
                }

                if (visit.hit_wall) {
                    direction = Direction::up;
                } else {
                    position.y--;
                }

                break;

            case Direction::none:
                throw MapError("No direction");
                break;
            }
        }

        return found_cycle;
    }

    void print(const std::array<Tile, MAP_SIZE * MAP_SIZE> &array) {
        char tile;

        for (int x = 0; x < MAP_SIZE; x++) {
            for (int y = 0; y < MAP_SIZE; y++) {
                switch (at(array, x, y).kind) {
                case TileKind::empty:
                    tile = '.';
                    break;

                case TileKind::obstacle:
                    tile = '#';
                    break;

                case TileKind::visited:
                    tile = 'X';
                    break;
                }

                std::cout << tile;
            }

            std::cout << std::endl;
        }
    }

public:
    std::array<Tile, MAP_SIZE * MAP_SIZE> m_array;

private:
    uint m_row_init;
    Position m_position;
    Direction m_direction;
};

int main(int argc, char *argv[]) {
    Map map{};
    uint nb_cycles = 0;

    for (std::string line; getline(std::cin, line);) {
        map.set_row(line);
    }

    map.print(map.m_array);

    for (uint x = 0; x < MAP_SIZE; x++) {
        for (uint y = 0; y < MAP_SIZE; y++) {
            if (map.check_cycle(Position(x, y))) {
                std::println("({}, {})", x, y);
                nb_cycles++;
            }
        }
    }

    std::cout << nb_cycles << std::endl;

    return 0;
}
