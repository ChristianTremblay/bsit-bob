import sys

lines = sys.stdin.readlines()

chunks = []
while lines:
    blank_line_index = lines.index("\n")
    chunks.append(lines[0 : blank_line_index + 1])
    lines = lines[blank_line_index + 1 :]

print("".join(chunks[0][:-1]))
del chunks[0]

chunks.sort()
for chunk in chunks:
    print("".join(chunk[:-1]))
