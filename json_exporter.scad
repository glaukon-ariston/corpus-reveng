/*
    OpenSCAD JSON Exporter
*/

// Function to create a JSON object for a vector
function V(v) = str("{\"X\": ", v[0], ", \"Y\": ", v[1], ", \"Z\": ", v[2], "}");

// Function to create a JSON object for a panel
module panel_json(name, x, y, z, w, h, d, drills) {
    echo(str("{\n",
        "\"name\": \"", name, "\",\n",
        "\"position\": ", V([x, y, z]), ",\n",
        "\"dimensions\": {\"Width\": ", w, ", \"Height\": ", h, ", \"Thickness\": ", d, "},\n",
        "\"drills\": [\n",
        for (drill = drills) 
            str("    {\"position\": ", V(drill[0]), ", \"diameter\": ", drill[1], ", \"depth\": ", drill[2], "}", if(drill == drills[len(drills)-1]) "" else ","),
        "\n]\n}"));
}
