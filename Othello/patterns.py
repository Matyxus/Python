import move_generator
move_gen = move_generator.MoveGenerator()
row_patterns = []
col_patterns = []
diag_patterns = []
diag2_pattern = []
row_1 = 0xFF00000000000000
col_1 = 0x8080808080808080
# Rows and cols.
for i in range(8):
	row_patterns.append(row_1 >> 8*i)
	col_patterns.append(col_1 >> i)
# Left diagonals.
start = 1 << 7
for i in range(7):
	start = (((start >> 1) << 9) | (start >> 1))
	diag_patterns.append(start)
start = 1 << 56
for i in range(6):
	start = (((start << 1) >> 9) | (start << 1))
	diag_patterns.append(start)
# Right diagonals.
start = 1 << 63
for i in range(7):
	start = ((start >> 8) | (start >> 1))
	diag2_pattern.append(start)
start = 1
for i in range(6):
	start = ((start << 8) | (start << 1))
	diag2_pattern.append(start)
# Center 16.
center = (1 << 18) | (1 << 19) | (1 << 20) | (1 << 21)
center |= (center << 8)
center |= (center << 8)
center |= (center << 8)
# Edges, outer_edges, corners
edges = col_patterns[0] |  col_patterns[-1] | row_patterns[0] | row_patterns[-1]
inner_edges = col_patterns[1] |  col_patterns[-2] | row_patterns[1] | row_patterns[-2]
inner_edges ^= (inner_edges & edges)
corners = 1 | (1 << 7) | (1 << 56) | (1 << 63)
corners_alone = [1, (1 << 7), (1 << 56), (1 << 63)]
corners_adjacent = [((1 << 1) | (1 << 8)),  ((1 << 15) | (1 << 6)),  ((1 << 57) | (1 << 48)), ((1 << 62) | (1 << 55))]
corners_and_adjacent = corners | sum(corners_adjacent)
if __name__ == '__main__':
	for row, col in zip(row_patterns, col_patterns):
		move_gen.print_board(row | col)

