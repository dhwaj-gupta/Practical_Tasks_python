from collections import defaultdict

def count_characters(s):
    char_count = defaultdict(int)
    for char in s:
        char_count[char] += 1
    return char_count

if __name__ == "__main__":
    s = input("Enter a string: ")
    char_count = count_characters(s)
    for char, count in char_count.items():
        print(f"{char}:{count}", end="")
        if char != list(char_count.keys())[-1]:
            print(", ", end="")
    print()

