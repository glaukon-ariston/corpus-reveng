/*
    More complex OpenSCAD script for a cabinet with drilling information.
*/

// Transparency
part_alpha = 0.4;

// Define a list of colors for the panels
colors = [
    [0.68, 0.85, 0.90], // LightBlue
    [0.56, 0.93, 0.56], // LightGreen
    [0.94, 0.50, 0.50], // LightCoral
    [1.00, 0.63, 0.48], // LightSalmon
    [0.69, 0.77, 0.87], // LightSteelBlue
    [0.94, 0.90, 0.55]  // Khaki
];

// Define the dimensions of the cabinet
width = 600;
height = 800;
depth = 400;
thickness = 18;

// Module to create a panel
module panel(name, x, y, z, w, h, d, color_index, material, banding_front="", banding_back="", banding_left="", banding_right="") {
    color(concat(colors[color_index], [part_alpha])) {
        translate([x, y, z])
        cube([w, h, d]);
    }
    echo(str("PANEL:", name, ",", w, ",", h, ",", d, ",", x, ",", y, ",", z, ",", material, ",", banding_front, ",", banding_back, ",", banding_left, ",", banding_right));
}

// Module to create a drill hole
module drill_hole(x, y, z, diameter, depth, normal) {
    color("red") {
        translate([x, y, z])
        cylinder(h = depth, d = diameter, $fn = 20);
    }
    echo(str("DRILL:", x, ",", y, ",", z, ",", diameter, ",", depth, ",", normal[0], ",", normal[1], ",", normal[2]));
}

// Create the cabinet
// Left panel
panel("Left", 0, 0, 0, thickness, height, depth, 0, "EGGER_ELGRAD_RP_F486_ST76", "EGGER_ELGRAD_ABS_U999_ST2", "", "", "");
// Drill on the front face
drill_hole(thickness / 2, 50, 0, 5, 10, [0, 0, -1]);
// Drill on the back face
drill_hole(thickness / 2, 50, depth, 5, 10, [0, 0, 1]);

// Right panel
panel("Right", width - thickness, 0, 0, thickness, height, depth, 1, "EGGER_ELGRAD_RP_F486_ST76", "EGGER_ELGRAD_ABS_U999_ST2", "", "", "");
// Drill on the front face
drill_hole(width - thickness / 2, 50, 0, 5, 10, [0, 0, -1]);
// Drill on the back face
drill_hole(width - thickness / 2, 50, depth, 5, 10, [0, 0, 1]);

// Top panel
panel("Top", thickness, height - thickness, 0, width - 2 * thickness, thickness, depth, 2, "EGGER_ELGRAD_RP_F486_ST76", "EGGER_ELGRAD_ABS_U999_ST2", "", "", "");
// Drill on the top face
drill_hole(width/2, height, 200, 8, 12, [0, 1, 0]);

// Bottom panel
panel("Bottom", thickness, 0, 0, width - 2 * thickness, thickness, depth, 3, "EGGER_ELGRAD_RP_F486_ST76", "EGGER_ELGRAD_ABS_U999_ST2", "", "", "");
// Drill on the bottom face
drill_hole(width/2, 0, 200, 8, 12, [0, -1, 0]);

// Back panel
panel("Back", thickness, thickness, depth - thickness, width - 2 * thickness, height - 2 * thickness, thickness, 4, "EGGER_ELGRAD_RP_F486_ST76", "EGGER_ELGRAD_ABS_U999_ST2", "", "", "");
