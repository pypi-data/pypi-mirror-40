"""
Handles writing process output into a pyramid of GeoTIFF files.

output configuration parameters
-------------------------------

mandatory
~~~~~~~~~

bands: integer
    number of output bands to be written
path: string
    output directory
dtype: string
    numpy datatype

optional
~~~~~~~~

tiled: bool
    internal TIFF tiling (default: True)
blockxsize: integer
    internal tile width (default: 256)
blockysize:
    internal tile height (default: 256)
nodata: integer or float
    nodata value used for writing
compress: string
    compression method (default: lzw): lzw, jpeg, packbits, deflate, CCITTRLE,
    CCITTFAX3, CCITTFAX4, lzma
"""

import logging
import os
import numpy as np
import numpy.ma as ma
import warnings

from mapchete.config import validate_values
from mapchete.formats import base
from mapchete.io import makedirs, get_boto3_bucket
from mapchete.io.raster import (
    write_raster_window, prepare_array, memory_file, read_raster_no_crs
)
from mapchete.tile import BufferedTile


logger = logging.getLogger(__name__)
METADATA = {
    "driver_name": "GTiff",
    "data_type": "raster",
    "mode": "rw"
}
GTIFF_DEFAULT_PROFILE = {
    "blockysize": 256,
    "blockxsize": 256,
    "tiled": True,
    "dtype": "uint8",
    "compress": "lzw",
    "interleave": "band",
    "nodata": 0
}


class OutputData(base.OutputData):
    """
    Template class handling process output data.

    Parameters
    ----------
    output_params : dictionary
        output parameters from Mapchete file

    Attributes
    ----------
    path : string
        path to output directory
    file_extension : string
        file extension for output files (.tif)
    output_params : dictionary
        output parameters from Mapchete file
    nodata : integer or float
        nodata value used when writing GeoTIFFs
    pixelbuffer : integer
        buffer around output tiles
    pyramid : ``tilematrix.TilePyramid``
        output ``TilePyramid``
    crs : ``rasterio.crs.CRS``
        object describing the process coordinate reference system
    srid : string
        spatial reference ID of CRS (e.g. "{'init': 'epsg:4326'}")
    """

    METADATA = METADATA

    def __init__(self, output_params, **kwargs):
        """Initialize."""
        super(OutputData, self).__init__(output_params)
        self.path = output_params["path"]
        self.file_extension = ".tif"
        self.output_params = output_params
        self.nodata = output_params.get("nodata", GTIFF_DEFAULT_PROFILE["nodata"])
        self._bucket = self.path.split("/")[2] if self.path.startswith("s3://") else None

    def read(self, output_tile):
        """
        Read existing process output.

        Parameters
        ----------
        output_tile : ``BufferedTile``
            must be member of output ``TilePyramid``

        Returns
        -------
        NumPy array
        """
        try:
            return read_raster_no_crs(self.get_path(output_tile))
        except FileNotFoundError:
            return self.empty(output_tile)

    def write(self, process_tile, data):
        """
        Write data from process tiles into GeoTIFF file(s).

        Parameters
        ----------
        process_tile : ``BufferedTile``
            must be member of process ``TilePyramid``
        """
        if (
            isinstance(data, tuple) and
            len(data) == 2 and
            isinstance(data[1], dict)
        ):
            data, tags = data
        else:
            tags = {}
        data = prepare_array(
            data,
            masked=True,
            nodata=self.nodata,
            dtype=self.profile(process_tile)["dtype"]
        )

        if data.mask.all():
            logger.debug("data empty, nothing to write")
        else:
            # in case of S3 output, create an boto3 resource
            bucket_resource = get_boto3_bucket(self._bucket) if self._bucket else None

            # Convert from process_tile to output_tiles and write
            for tile in self.pyramid.intersecting(process_tile):
                out_path = self.get_path(tile)
                self.prepare_path(tile)
                out_tile = BufferedTile(tile, self.pixelbuffer)
                write_raster_window(
                    in_tile=process_tile,
                    in_data=data,
                    out_profile=self.profile(out_tile),
                    out_tile=out_tile,
                    out_path=out_path,
                    tags=tags,
                    bucket_resource=bucket_resource
                )

    def is_valid_with_config(self, config):
        """
        Check if output format is valid with other process parameters.

        Parameters
        ----------
        config : dictionary
            output configuration parameters

        Returns
        -------
        is_valid : bool
        """
        return validate_values(
            config, [
                ("bands", int),
                ("path", str),
                ("dtype", str)]
        )

    def get_path(self, tile):
        """
        Determine target file path.

        Parameters
        ----------
        tile : ``BufferedTile``
            must be member of output ``TilePyramid``

        Returns
        -------
        path : string
        """
        return os.path.join(*[
            self.path,
            str(tile.zoom),
            str(tile.row),
            str(tile.col) + self.file_extension
        ])

    def prepare_path(self, tile):
        """
        Create directory and subdirectory if necessary.

        Parameters
        ----------
        tile : ``BufferedTile``
            must be member of output ``TilePyramid``
        """
        makedirs(os.path.dirname(self.get_path(tile)))

    def profile(self, tile=None):
        """
        Create a metadata dictionary for rasterio.

        Parameters
        ----------
        tile : ``BufferedTile``

        Returns
        -------
        metadata : dictionary
            output profile dictionary used for rasterio.
        """
        dst_metadata = GTIFF_DEFAULT_PROFILE
        dst_metadata.pop("transform", None)
        dst_metadata.update(
            count=self.output_params["bands"],
            dtype=self.output_params["dtype"],
            driver="GTiff"
        )
        if tile is not None:
            dst_metadata.update(
                crs=tile.crs, width=tile.width, height=tile.height,
                affine=tile.affine)
        else:
            for k in ["crs", "width", "height", "affine"]:
                dst_metadata.pop(k, None)
        if "nodata" in self.output_params:
            dst_metadata.update(nodata=self.output_params["nodata"])
        try:
            if "compression" in self.output_params:
                warnings.warn(
                    "use 'compress' instead of 'compression'", DeprecationWarning
                )
                dst_metadata.update(compress=self.output_params["compression"])
            else:
                dst_metadata.update(compress=self.output_params["compress"])
            dst_metadata.update(predictor=self.output_params["predictor"])
        except KeyError:
            pass
        return dst_metadata

    def empty(self, process_tile):
        """
        Return empty data.

        Parameters
        ----------
        process_tile : ``BufferedTile``
            must be member of process ``TilePyramid``

        Returns
        -------
        empty data : array
            empty array with data type provided in output profile
        """
        profile = self.profile(process_tile)
        return ma.masked_array(
            data=np.full(
                (profile["count"], ) + process_tile.shape, profile["nodata"],
                dtype=profile["dtype"]),
            mask=True
        )

    def for_web(self, data):
        """
        Convert data to web output (raster only).

        Parameters
        ----------
        data : array

        Returns
        -------
        web data : array
        """
        return memory_file(
            prepare_array(
                data, masked=True, nodata=self.nodata, dtype=self.profile()["dtype"]
            ),
            self.profile()
        ), "image/tiff"

    def open(self, tile, process, **kwargs):
        """
        Open process output as input for other process.

        Parameters
        ----------
        tile : ``Tile``
        process : ``MapcheteProcess``
        kwargs : keyword arguments
        """
        return InputTile(tile, process, kwargs.get("resampling", None))


class InputTile(base.InputTile):
    """
    Target Tile representation of input data.

    Parameters
    ----------
    tile : ``Tile``
    process : ``MapcheteProcess``
    resampling : string
        rasterio resampling method

    Attributes
    ----------
    tile : ``Tile``
    process : ``MapcheteProcess``
    resampling : string
        rasterio resampling method
    pixelbuffer : integer
    """

    def __init__(self, tile, process, resampling):
        """Initialize."""
        self.tile = tile
        self.process = process
        self.pixelbuffer = None
        self.resampling = resampling

    def read(self, indexes=None):
        """
        Read reprojected & resampled input data.

        Parameters
        ----------
        indexes : integer or list
            band number or list of band numbers

        Returns
        -------
        data : array
        """
        band_indexes = self._get_band_indexes(indexes)
        arr = self.process.get_raw_output(self.tile)
        if len(band_indexes) == 1:
            return arr[band_indexes[0] - 1]
        else:
            return ma.concatenate([
                ma.expand_dims(arr[i - 1], 0) for i in band_indexes
            ])

    def is_empty(self, indexes=None):
        """
        Check if there is data within this tile.

        Returns
        -------
        is empty : bool
        """
        # empty if tile does not intersect with file bounding box
        return not self.tile.bbox.intersects(self.process.config.area_at_zoom())

    def _get_band_indexes(self, indexes=None):
        """Return valid band indexes."""
        if indexes:
            if isinstance(indexes, list):
                return indexes
            else:
                return [indexes]
        else:
            return range(1, self.process.config.output.profile(self.tile)["count"] + 1)

    def __enter__(self):
        """Enable context manager."""
        return self

    def __exit__(self, t, v, tb):
        """Clear cache on close."""
        pass
