import parser
import pathfinder

if __name__ == '__main__':
    parser.parse_data("test_data/test_task_data.csv")
    print('Cheapest:')
    for path in pathfinder.find_cheapest():
        pathfinder.reconstruct_path(path)

    print('Shortest:')
    for path in pathfinder.find_fastest():
        pathfinder.reconstruct_path(path)
