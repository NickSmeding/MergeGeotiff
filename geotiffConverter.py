import glob
import subprocess

from osgeo import gdal
from osgeo import osr
import os

class Geotiff:
    # function convert_image_to_tif
    #   Parameters:
    #   image_src = image file that needs to be converted
    #   llat = latitude of the left-top corner of the image
    #   llong = longitude of the left-top corner of the image
    #   rlat = latitude of the right-bottom corner of the image
    #   rlong = longitude of the right-bottom corner of the image

    #used to create icon .tiff
    #commented out the parts that need the database
    def convertIconToTif(self,image, llat, llong, rlat, rlong):

        #marker = Markers.query.filter_by(id=23).first()

        #   Open the Image Size
        image = 'C://Users//nicks//programming//server//core//endpoints//..//icons//horse2.png'
        ds = gdal.Open(image)

        new_file = os.path.splitext(image)[0]

        #   Convert image to a Tif file
        translateoptions = gdal.TranslateOptions(rgbExpand='RGBA', format='GTiff')
        translate = gdal.Translate(new_file + '.tif', ds, options=translateoptions)

        #Top left x-coordinate, Pixel width, Row rotation (mostly zero), Top left y-coordinate, Column rotation (mostly zero), Pixel height (Negative value for a north-up image)
        #hardcoded
        #geotransform = (marker.long - 0.0009, 30.0000000000000000e-07, 0, marker.lat - 0.0028, 0, -30.0000000000000000e-07)

        #   Specify coords to new image
        # translate.SetGeoTransform(geotransform)
        srs = osr.SpatialReference()  # establish encoding
        srs.ImportFromEPSG(4326)  # WGS84 lat/long = 4326

        #   Export coords to file
        translate.SetProjection(srs.ExportToWkt())

        #   Write to disk (Without this image  wont save
        translate.FlushCache()
        translate = None
        self.mergeTiff()

    #the part that needs work and doesnt work as intended
    def mergeTiff(self):
        demList = glob.glob(os.path.dirname(os.path.abspath(__file__)) + "//tiffs//*.tif")
        print(demList)

        VRToptions = gdal.BuildVRTOptions()
        vrt = gdal.BuildVRT(os.path.dirname(os.path.abspath(__file__)) + "//merged.vrt", demList, options=VRToptions)
        translateOptions = gdal.TranslateOptions()
        gdal.Translate(os.path.dirname(os.path.abspath(__file__)) + "//mergedDEM.tif", vrt, options=translateOptions)
        vrt = None

        #also tried calling the cmd directly, same as the library does.
        #cmd = "gdal_merge.py -ps 10 -10 -o mergedDEM.tif"
        #subprocess.call(cmd.split()+demList)