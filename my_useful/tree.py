from pathlib import Path
import sys

# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dir_path: Path, prefix: str='', count=0, max_count=3):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """    
    if count >= max_count:
        return
    contents = list(dir_path.iterdir())
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space 
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension, count=count+1, max_count=max_count)

if __name__ == '__main__':
    print(sys.argv[1])
    for line in tree(Path(sys.argv[1]), max_count=int(sys.argv[2])):
        print(line)
