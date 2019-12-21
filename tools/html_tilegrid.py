#!/usr/bin/env python3
"""
Convert the tile grid for a given family and device to HTML format
"""
import sys, re
import argparse
import database
import tiles as tilelib

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('family', type=str,
                    help="FPGA family (e.g. LIFCL)")
parser.add_argument('device', type=str,
                    help="FPGA device (e.g. LIFCL-40)")
parser.add_argument('outfile', type=argparse.FileType('w'),
                    help="output HTML file")


def get_colour(ttype):
    colour = "#FFFFFF"
    if "TAP" in ttype:
        colour = "#DDDDDD"
    elif ttype.startswith("SYSIO"):
        colour = "#88FF88"
    elif "PLL" in ttype or "DPHY" in ttype or "CDR" in ttype or "PCIE" in ttype or "EFB" in ttype or "PMU" in ttype or "ADC" in ttype:
        colour = "#88FFFF"
    elif ttype.startswith("CIB"):
        colour = "#FF8888"
    elif ttype.startswith("PLC"):
        colour = "#8888FF"
    elif ttype.startswith("DUMMY"):
        colour = "#FFFFFF"
    elif ttype.startswith("MIB_EBR") or ttype.startswith("EBR_") or ttype.startswith("LRAM"):
        colour = "#FF88FF"
    elif "DSP" in ttype or ttype == "ALU":
        colour = "#FFFF88"
    else:
        colour = "#888888"
    return colour


def main(argv):
    args = parser.parse_args(argv[1:])
    tilegrid = database.get_tilegrid(args.family, args.device)["tiles"]
    device_info = database.get_devices()["families"][args.family]["devices"][args.device]

    max_row = device_info["max_row"]
    max_col = device_info["max_col"]

    tiles = []
    for i in range(max_row + 1):
        row = []
        for j in range(max_col + 1):
            row.append([])
        tiles.append(row)

    for identifier, data in sorted(tilegrid.items()):
        name = identifier.split(":")[0]
        row, col = tilelib.pos_from_name(name)
        colour = get_colour(data["tiletype"])
        tiles[row][col].append((name, data["tiletype"], colour))

    f = args.outfile
    print(
        """<html>
            <head><title>{} Tiles</title></head>
            <body>
            <h1>{} Tilegrid</h1>
            <table style='font-size: 8pt; border: 2px solid black; text-align: center'>
        """.format(args.device, args.device), file=f)
    for trow in tiles:
        print("<tr>", file=f)
        row_max_height = 0
        for tloc in trow:
            row_max_height = max(row_max_height, len(tloc))
        row_height = max(75, 30 * row_max_height)
        for tloc in trow:
            print("<td style='border: 2px solid black; height: {}px'>".format(row_height), file=f)
            for tile in tloc:
                print(
                    "<div style='height: {}%; background-color: {}'><em>{}</em><br/><strong><a href='../tilehtml/{}.html' style='color: black'>{}</a></strong></div>".format(
                        100 / len(tloc), tile[2], tile[0], tile[1], tile[1]), file=f)
            print("</td>", file=f)
        print("</tr>", file=f)
    print("</table></body></html>", file=f)


if __name__ == "__main__":
    main(sys.argv)