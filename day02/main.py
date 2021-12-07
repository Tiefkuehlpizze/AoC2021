def part1():
    def sum_commands(command, commands): return sum(
        map(lambda args: args[1], filter(lambda c: c[0] == command, commands)))

    with open('input') as f:
        raw_commands = [(command[0], int(command[1])) for command in map(str.split, f.readlines())]
    movement_forward = sum_commands('forward', raw_commands)
    movement_up = sum_commands('up', raw_commands)
    movement_down = sum_commands('down', raw_commands)

    final_depth = movement_down - movement_up
    print(final_depth * movement_forward)


def part2():
    with open('input') as f:
        raw_commands = [(command[0], int(command[1])) for command in map(str.split, f.readlines())]
    aim = depth = pos_x = 0
    for command, value in raw_commands:
        if command == 'forward':
            pos_x += value
            depth += aim * value
        elif command == 'down':
            aim += value
        elif command == 'up':
            aim -= value
    print(depth * pos_x)


if __name__ == '__main__':
    part1()
    part2()
