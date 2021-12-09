import nussl

# import file
dummy_signal = nussl.AudioSignal()


# separate stems
ft2d = nussl.separation.primitive.FT2D(dummy_signal)


# save stems