# Haas `.PGM` File Splitter

This Python 3 utility splits Haas CNC `.PGM` files into individual program files, one per `O-word` program, and separates any MDI code into its own file.

## 🔧 Features

- Removes `%` characters (line-based)
- Preserves blank lines and formatting
- Extracts everything **before the first `O-word`** into `MDI.nc`
- Splits each program starting with `Oxxxxxx` into a separate `.nc` file
- Supports optional **inline comments** or **next-line comments** for program naming:
  - `O1234 (Finishing)` → `O1234_Finishing.nc`
  - `O1234` followed by `(Finishing)` → `O1234_Finishing.nc`

## 📂 Output Example

Given:

```gcode
%
G91 G28 Z0
T1 M06
G90

O1001
(Roughing)
G0 X0 Y0
M30

O1002 (Finishing)
G0 X1 Y1
M30
%

