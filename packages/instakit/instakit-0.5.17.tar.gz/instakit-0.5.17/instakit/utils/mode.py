 #!/usr/bin/env python
# encoding: utf-8

from __future__ import print_function

import contextlib
import numpy
import os
import types

from PIL import Image, ImageMode
from enum import Enum, auto, unique

junkdrawer = types.SimpleNamespace()
junkdrawer.imode = lambda image: ImageMode.getmode(image.mode)

def split_abbreviations(s):
    """ Split a string into a tuple of its unique constituents,
        based on its internal capitalization -- to wit:
        
        >>> split_abbreviations('RGB')
        ('R', 'G', 'B')
        >>> split_abbreviations('CMYK')
        ('C', 'M', 'Y', 'K')
        >>> split_abbreviations('YCbCr')
        ('Y', 'Cb', 'Cr')
        >>> split_abbreviations('sRGB')
        ('R', 'G', 'B')
        >>> split_abbreviations('XYZZ')
        ('X', 'Y', 'Z')
        
        If you still find this function inscrutable,
        have a look here: https://gist.github.com/4027079
    """
    abbreviations = []
    current_token = ''
    for char in s:
        if current_token is '':
            current_token += char
        elif char.islower():
            current_token += char
        else:
            if not current_token.islower():
                if current_token not in abbreviations:
                    abbreviations.append(current_token)
            current_token = ''
            current_token += char
    if current_token is not '':
        if current_token not in abbreviations:
            abbreviations.append(current_token)
    return tuple(abbreviations)


ImageMode.getmode('RGB') # one call must be made to getmode()
                         # to properly initialize ImageMode._modes:

junkdrawer.modes = ImageMode._modes
junkdrawer.types = Image._MODE_CONV

image_mode_strings = tuple(junkdrawer.modes.keys())
dtypes_for_modes = { k : v[0] for k, v in junkdrawer.types.items() }


class ModeAncestor(Enum):
    """
    Valid ImageMode mode strings:
    ('1',    'L',     'I',     'F',     'P',
     'RGB',  'RGBX',  'RGBA',  'CMYK',  'YCbCr',
     'LAB',  'HSV',   'RGBa',  'LA',    'La',
     'PA',   'I;16',  'I;16L', 'I;16B') """
    
    def _generate_next_value_(name,
                              start,
                              count,
                              last_values):
        return ImageMode.getmode(
               image_mode_strings[count])
    
    @classmethod
    def _missing_(cls, value):
        try:
            return cls(ImageMode.getmode(
                       image_mode_strings[value]))
        except (IndexError, TypeError):
            pass
        return super(ModeAncestor, cls)._missing_(value)
    
    @classmethod
    def is_mode(cls, instance):
        return type(instance) in cls.__mro__


class ModeContext(contextlib.AbstractContextManager):
    
    """ An ad-hoc mutable named-tuple-ish context-manager class,
        for keeping track of an image while temporarily converting
        it to a specified mode within the managed context block.
        
        Loosely based on the following Code Review posting:
        • https://codereview.stackexchange.com/q/173045/6293
    """
    
    __slots__ = ('initial_image',
                         'image',
                 'original_mode',
                          'mode')
    
    def __init__(self, image, mode):
        assert Image.isImageType(image)
        assert Mode.is_mode(mode)
        label = getattr(image, 'filename', None) \
            and os.path.basename(getattr(image, 'filename', None)) \
            or str(image)
        print("ModeContext.__init__: configured with image: %s" % label)
        self.initial_image = image
        self.image = None
        self.original_mode = Mode.of(image)
        self.mode = mode
    
    def __repr__(self):
        return type(self).__name__ + repr(tuple(self))
    
    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)
    
    def __getitem__(self, idx):
        return getattr(self, self.__slots__[idx])
    
    def __len__(self):
        return len(self.__slots__)
    
    def __enter__(self):
        initial_image = getattr(self, 'initial_image', None)
        mode = getattr(self, 'mode', None)
        if initial_image is not None and mode is not None:
            print("ModeContext.__enter__: converting %s to %s" % (Mode.of(initial_image), mode))
            image = mode.process(initial_image)
            setattr(self, 'image', image)
        return self
    
    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        image = getattr(self, 'image', None)
        original_mode = getattr(self, 'original_mode', None)
        if image is not None and original_mode is not None:
            print("ModeContext.__exit__: converting %s to %s" % (Mode.of(image), original_mode))
            initial_image = original_mode.process(image)
        setattr(self, 'initial_image', initial_image)
        return exc_type is None


@unique
class Mode(ModeAncestor):
    
    """ An enumeration class wrapping ImageMode.ModeDescriptor. """
    
    # N.B. this'll have to be manually updated,
    # whenever PIL.ImageMode gets a change pushed.
    
    MONO    = auto() # formerly ‘1’
    L       = auto()
    I       = auto()
    F       = auto()
    P       = auto()
    
    RGB     = auto()
    RGBX    = auto()
    RGBA    = auto()
    CMYK    = auto()
    YCbCr   = auto()
    
    LAB     = auto()
    HSV     = auto()
    RGBa    = auto()
    LA      = auto()
    La      = auto()
    
    PA      = auto()
    I16     = auto() # formerly ‘I;16’
    I16L    = auto() # formerly ‘I;16L’
    I16B    = auto() # formerly ‘I;16B’
    
    @classmethod
    def of(cls, image):
        for mode in cls:
            if mode.check(image):
                return mode
        raise ValueError("Image has unknown mode %s" % image.mode)
    
    @classmethod
    def for_string(cls, string):
        for mode in cls:
            if mode.to_string() == string:
                return mode
        raise ValueError("for_string(): unknown mode %s" % string)
    
    def to_string(self):
        return str(self.value)
    
    def __str__(self):
        return self.to_string()
    
    def __bytes__(self):
        return bytes(self.to_string(), encoding="UTF-8")
    
    def __call__(self, image):
        return ModeContext(image, self)
    
    def dtype_code(self):
        return dtypes_for_modes.get(self.to_string(), None) or \
                                    self.basetype.dtype_code()
    
    @property
    def bands(self):
        return self.value.bands
    
    @property
    def band_count(self):
        return len(self.value.bands)
    
    @property
    def basemode(self):
        return type(self).for_string(self.value.basemode)
    
    @property
    def basetype(self):
        return type(self).for_string(self.value.basetype)
    
    @property
    def dtype(self):
        return numpy.dtype(self.dtype_code())
    
    @property
    def label(self):
        return str(self) == self.name \
                        and self.name \
                        or "%s (%s)" % (self, self.name)
    
    def check(self, image):
        return junkdrawer.imode(image) is self.value
    
    def merge(self, *channels):
        return Image.merge(self.to_string(), channels)
    
    def process(self, image):
        if self.check(image):
            return image
        return image.convert(self.to_string())
    
    def new(self, size, color=0):
        return Image.new(self.to_string(), size, color=color)
    
    def open(self, fileish):
        return self.process(Image.open(fileish))
    
    def frombytes(self, size, data, decoder_name='raw', *args):
        return Image.frombytes(self.to_string(),
                               size, data, decoder_name,
                              *args)


def test():
    
    print("«KNOWN IMAGE MODES»")
    print()
    
    for m in Mode:
        print("• %10s\t ∞%5s/%s : %s » %s" % (m.label,
                                              m.basemode,
                                              m.basetype,
                                              m.dtype_code(),
                                              m.dtype))
    
    print()
    
    print("«TESTING: split_abbreviations()»")
    
    assert split_abbreviations('RGB') == ('R', 'G', 'B')
    assert split_abbreviations('CMYK') == ('C', 'M', 'Y', 'K')
    assert split_abbreviations('YCbCr') == ('Y', 'Cb', 'Cr')
    assert split_abbreviations('sRGB') == ('R', 'G', 'B')
    assert split_abbreviations('XYZ') == ('X', 'Y', 'Z')
    
    print("«SUCCESS»")
    
    # print(list(Mode))
    # print()
    
    assert Mode(10) == Mode.LAB
    
    print()
    
    print("«TESTING: CONTEXT-MANAGED IMAGE MODES»")
    print()
    from instakit.utils import static
    
    image_paths = list(map(
        lambda image_file: static.path('img', image_file),
            static.listfiles('img')))
    image_inputs = list(map(
        lambda image_path: Mode.RGB.open(image_path),
            image_paths))
    
    for image in image_inputs:
        with Mode.L(image) as grayscale:
            assert Mode.of(grayscale.image) is Mode.L
            print(grayscale.image)
            grayscale.image = Mode.MONO.process(grayscale.image)
        print()
    
    print("«SUCCESS»")
    print()

if __name__ == '__main__':
    test()