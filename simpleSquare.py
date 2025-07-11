from pyembroidery import EmbPattern, write_pes, STITCH

# Create a new embroidery pattern
pattern = EmbPattern()

# Define a square path with simple running stitches (in mm)
square_points = [
    (0, 0),
    (40, 0),
    (40, 40),
    (0, 40),
    (0, 0)
]

# Add the points as simple running stitches
for x, y in square_points:
    pattern.add_stitch_absolute(STITCH, x, y)

# End the pattern
pattern.end()

# Save to a .PES file
write_pes(pattern, "simple_square.pes")

print("simple_square.pes created!")
