#
# utiliy methods for creating workspace files - which needs SeriesId and Orientation
#
import sys
import logging
logger = logging.getLogger(__file__)
import subprocess
import ast

def get_series_dict(dcm_file):
    cmd_list = f'c3d -dicom-series-list {dcm_file}'.split(' ')
    logger.info(str(cmd_list))
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = str(out.decode("utf-8"))
    err = str(err.decode("utf-8"))
    if len(err)>0:
        raise ValueError(err)
    lines = out.split("\n")
    mydict = {k:v for k,v in zip(lines[0].split('\t'), lines[1].split("\t") )}
    logger.info(str(mydict))

    # {'SeriesNumber': '2 ', 'Dimensions': '512x512x123', 'NumImages': '123', 
    # 'SeriesDescription': '', 'SeriesID': '1.2.123'}
    return mydict

def get_series_info(dcm_file):
    series_dict = get_series_dict(dcm_file)
    cmd_list = f'c3d -dicom-series-read {dcm_file} {series_dict["SeriesID"]} -info'.split(' ')
    logger.info(str(cmd_list))
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = str(out.decode("utf-8"))
    err = str(err.decode("utf-8"))
    if len(err)>0:
        raise ValueError(err)
    lines = out.split("\n")
    dim_str,bb_str,vox_str,range_str,orientation_str=[x.strip(" ").split("=")[-1].strip(" ") for x in lines[0].split(";")]
    min_point_str,max_point_str = bb_str.strip("{}").split(",")
    min_point = ast.literal_eval(min_point_str.strip(' ').replace(' ',','))
    max_point = ast.literal_eval(max_point_str.strip(' ').replace(' ',','))
    dimension,voxel_size,intensity_range = (ast.literal_eval(x) for x in [dim_str,vox_str,range_str])
    # sample output:
    # dimension,voxel_size,intensity_range,orient_str,min_point,max_point
    # ([512, 512, 123], [0.6875, 0.6875, 0.123], [-1024, 2035], 'RAI', [-176.656, -335.656, -1083.9], [175.344, 16.3438, -719.878])
    return series_dict,dimension,voxel_size,intensity_range,orientation_str,min_point,max_point

def create_empty_image(dcm_file,output_file,backgound_int=0):
    series_dict,dimension,voxel_size,intensity_range,orient_str,min_point,max_point = get_series_info(dcm_file)
    dimension_str = f'{dimension[0]}x{dimension[1]}x{dimension[2]}'
    voxel_str = f'{voxel_size[0]}x{voxel_size[1]}x{voxel_size[2]}mm'
    origin_str = f'{min_point[0]}x{min_point[1]}x{min_point[2]}mm'
    cmd_list = f'c3d -background {backgound_int} -create {dimension_str} {voxel_str} -origin {origin_str} -o {output_file}'.split(' ')
    logger.info(str(cmd_list))
    process = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    out = str(out.decode("utf-8"))
    err = str(err.decode("utf-8"))
    if len(err)>0:
        raise ValueError(err)

if __name__ == "__main__":
    dcm_file = sys.argv[1]
    out_file = sys.argv[2]
    print('get_series_info')
    print(get_series_info(dcm_file))
    print('create_blank_nifi')
    create_empty_image(dcm_file,out_file)


