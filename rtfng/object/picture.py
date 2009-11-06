from binascii import hexlify

from rtfng.document.base import RawCode


class Image( RawCode ) :

    #  Need to add in the width and height in twips as it crashes
    #  word xp with these values.  Still working out the most
    #  efficient way of getting these values.
    # \picscalex100\picscaley100\piccropl0\piccropr0\piccropt0\piccropb0
    # picwgoal900\pichgoal281

    PNG_LIB = 'pngblip'
    JPG_LIB = 'jpegblip'
    PICT_TYPES = { 'png' : PNG_LIB,
                   'jpg' : JPG_LIB }

    def __init__( self, file_name, **kwargs ) :

        # Try to import PIL.
        try:
            from PIL import Image
        except:
            raise Exception('Unable to import PIL Image library')

        # Calculate size of image.
        image = Image.open(file_name)
        self.width, self.height = image.size

        # Generate header codes.
        pict_type = self.PICT_TYPES[ file_name[ -3 : ].lower() ]
        codes = [ pict_type,
                  'picwgoal%s' % (self.width  * 20),
                  'pichgoal%s' % (self.height * 20) ]
        for kwarg, code, default in [ ( 'scale_x',     'scalex', '100' ),
                                      ( 'scale_y',     'scaley', '100' ),
                                      ( 'crop_left',   'cropl',    '0' ),
                                      ( 'crop_right',  'cropr',    '0' ),
                                      ( 'crop_top',    'cropt',    '0' ),
                                      ( 'crop_bottom', 'cropb',    '0' ) ] :
            codes.append( 'pic%s%s' % ( code, kwargs.pop( kwarg, default ) ) )


        # Reset back to the start of the file to get all of it and now
        # turn it into hex.
        # I tried using image.getdata() below but it relies on having libjpeg installed.
        fin = file( file_name, 'rb' )
        fin.seek( 0, 0 )
        data = []
        image = hexlify( fin.read() )
        for i in range( 0, len( image ), 128 ) :
            data.append( image[ i : i + 128 ] )

        data = r'{\pict{\%s}%s}' % ( '\\'.join( codes ), '\n'.join( data ) )
        RawCode.__init__( self, data )

    def ToRawCode( self, var_name ) :
        return '%s = RawCode( """%s""" )' % ( var_name, self.Data )

