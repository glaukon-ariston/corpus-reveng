/*
    Sample OpenSCAD script for a simple cabinet with drilling information.
*/

// Define a list of colors for the panels
colors = [
    "LightBlue",
    "LightGreen",
    "LightCoral",
    "LightSalmon",
    "LightSteelBlue",
    "Khaki"
];

// Define the dimensions of the cabinet
width = 600;
height = 800;
depth = 400;
thickness = 18;

// Module to create a panel
module panel(name, x, y, z, w, h, d, color_index) {
    color(colors[color_index]) {
        translate([x, y, z])
        cube([w, h, d]);
    }
    echo(str("PANEL:", name, ",", w, ",", h, ",", d, ",", x, ",", y, ",", z));
}

// Module to create a drill hole
module drill_hole(x, y, z, diameter, depth) {
    color("red") {
        translate([x, y, z])
        cylinder(h = depth, d = diameter, $fn = 20);
    }
    echo(str("DRILL:", x, ",", y, ",", z, ",", diameter, ",", depth));
}

// Create the cabinet
// Left panel
panel("Left", 0, 0, 0, thickness, height, depth, 0);
drill_hole(thickness / 2, 50, 50, 5, 10);
drill_hole(thickness / 2, 50, 150, 5, 10);

// Right panel
panel("Right", width - thickness, 0, 0, thickness, height, depth, 1);
drill_hole(width - thickness / 2, 50, 50, 5, 10);
drill_hole(width - thickness / 2, 50, 150, 5, 10);

// Top panel
panel("Top", thickness, height - thickness, 0, width - 2 * thickness, thickness, depth, 2);

// Bottom panel
panel("Bottom", thickness, 0, 0, width - 2 * thickness, thickness, depth, 3);

// Back panel
panel("Back", thickness, thickness, depth - thickness, width - 2 * thickness, height - 2 * thickness, thickness, 4);
