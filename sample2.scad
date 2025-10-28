/*
    More complex OpenSCAD script for a cabinet with drilling information.
*/

// Define the dimensions of the cabinet
width = 600;
height = 800;
depth = 400;
thickness = 18;

// Module to create a panel
module panel(name, x, y, z, w, h, d) {
    translate([x, y, z])
    cube([w, h, d]);
    echo(str("PANEL:", name, ",", w, ",", h, ",", d, ",", x, ",", y, ",", z));
}

// Module to create a drill hole
module drill_hole(x, y, z, diameter, depth) {
    translate([x, y, z])
    cylinder(h = depth, d = diameter, $fn = 20);
    echo(str("DRILL:", x, ",", y, ",", z, ",", diameter, ",", depth));
}

// Create the cabinet
// Left panel
panel("Left", 0, 0, 0, thickness, height, depth);
// Drill on the front face
drill_hole(thickness / 2, 50, 0, 5, 10);
// Drill on the back face
drill_hole(thickness / 2, 50, depth, 5, 10);

// Right panel
panel("Right", width - thickness, 0, 0, thickness, height, depth);
// Drill on the front face
drill_hole(width - thickness / 2, 50, 0, 5, 10);
// Drill on the back face
drill_hole(width - thickness / 2, 50, depth, 5, 10);

// Top panel
panel("Top", thickness, height - thickness, 0, width - 2 * thickness, thickness, depth);
// Drill on the top face
drill_hole(width/2, height, 200, 8, 12);

// Bottom panel
panel("Bottom", thickness, 0, 0, width - 2 * thickness, thickness, depth);
// Drill on the bottom face
drill_hole(width/2, 0, 200, 8, 12);

// Back panel
panel("Back", thickness, thickness, depth - thickness, width - 2 * thickness, height - 2 * thickness, thickness);
