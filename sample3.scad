include <json_exporter.scad>

/*
    Sample OpenSCAD script for a simple cabinet with drilling information,
    exporting to JSON.
*/

// Define the dimensions of the cabinet
width = 600;
height = 800;
depth = 400;
thickness = 18;

// Create the cabinet data
panels = [
    ["Left", [0, 0, 0], [thickness, height, depth], [
        [[thickness / 2, 50, 0], 5, 10],
        [[thickness / 2, 50, depth], 5, 10]
    ]],
    ["Right", [width - thickness, 0, 0], [thickness, height, depth], [
        [[width - thickness / 2, 50, 0], 5, 10],
        [[width - thickness / 2, 50, depth], 5, 10]
    ]],
    ["Top", [thickness, height - thickness, 0], [width - 2 * thickness, thickness, depth], [
        [[width/2, height, 200], 8, 12]
    ]],
    ["Bottom", [thickness, 0, 0], [width - 2 * thickness, thickness, depth], [
        [[width/2, 0, 200], 8, 12]
    ]],
    ["Back", [thickness, thickness, depth - thickness], [width - 2 * thickness, height - 2 * thickness, thickness], []]
];

// Export the data to JSON
echo("{\"elements\": [{\"name\": \"Cabinet\", \"panels\": [ ");
for (p = panels) {
    panel_json(p[0], p[1][0], p[1][1], p[1][2], p[2][0], p[2][1], p[2][2], p[3]);
    if (p != panels[len(panels)-1]) {
        echo(",");
    }
}
echo("]}]}");

// Render the cabinet for visualization
for (p = panels) {
    translate(p[1])
    cube(p[2]);
    for (drill = p[3]) {
        translate(drill[0])
        cylinder(h = drill[2], d = drill[1], $fn = 20);
    }
}
