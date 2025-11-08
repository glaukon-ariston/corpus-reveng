
import re

def parse_krivulje_data(data_string):
    points = []
    
    # Remove the outer quotes and split by comma
    data_string = data_string.strip()[1:-1]
    parts = data_string.split(',')
    
    point_data = {}
    
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            # Remove quotes from value if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            if key == '"PTOCKA':
                if point_data:
                    points.append(point_data)
                point_data = {}
            
            if key == '"PTX':
                point_data['x'] = float(value.strip('"'))
            elif key == '"PTZ':
                point_data['z'] = float(value.strip('"'))

    if point_data:
        points.append(point_data)

    return points

# Example usage:
data = '"0","G","CUSYSMODE=0","CUSTYPE=0","CUSSPSEG=10","CUSSPNULA=0","CUSSPSTART=0","CUSSPEND=360","CUSYROT=1","CUSSPHERE=0","INFDEF=0","CLR=0","CLG=0","CLB=0","CLA=204","INFSPOV=-1","INFSPOV=0","INFSMAIN=-1","INFSALL=0","INFDONE=1","CUSVARS=","CURVE=-1","CNNAME=c","CNOPEN=0","USEDINTES=1","CREATOR=0","PTOCKA=0","PTSTYLE=0","PTANMODE=0","PTSEGCOUNT=10","PTX=0","PTZ=0","PTDEPTH=0","PTS=0","PTCLEN=0","PTOCKA=1","PTSTYLE=0","PTANMODE=0","PTSEGCOUNT=10","PTX=2.6159999370575","PTZ=0","PTDEPTH=0","PTS=2","PTCLEN=0","PTOCKA=2","PTSTYLE=0","PTANMODE=0","PTSEGCOUNT=10","PTX=2.6159999370575","PTZ=0.699999928474426","PTDEPTH=0","PTS=4","PTCLEN=0","PTOCKA=3","PTSTYLE=0","PTANMODE=0","PTSEGCOUNT=10","PTX=0","PTZ=0.699999928474426","PTDEPTH=0","PTS=6","PTCLEN=0","CMODE=2","CCENTARMODE=0","CNCNCMANUAL=0",'
points = parse_krivulje_data(data)
print(points)
