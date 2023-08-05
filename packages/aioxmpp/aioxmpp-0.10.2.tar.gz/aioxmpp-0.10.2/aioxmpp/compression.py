import asyncio
import zlib

import aioxmpp.xso as xso

from . import protocol, nonza


class CompressionFilter(protocol.StreamFilter):
    def __init__(self, level=-1, unsafe_mode=False):
        super().__init__()
        self._flush_mode = (
            zlib.Z_SYNC_FLUSH
            if unsafe_mode else
            zlib.Z_FULL_FLUSH
        )
        self._compressor = zlib.compressobj(level)
        self._decompressor = zlib.decompressobj()

    def filter_received(self, data: bytes) -> bytes:
        return self._decompressor.decompress(data)

    def filter_sending(self, data: bytes) -> bytes:
        return self._compressor.compress(data)

    def flush_sending(self) -> bytes:
        return self._compressor.flush(zlib.Z_FULL_FLUSH)


class CompressionMethod(xso.XSO):
    TAG = ("http://jabber.org/features/compress", "method")

    name = xso.Text()

    def __init__(self, name):
        super().__init__()
        self.name = name


class CompressionMethodType(xso.AbstractElementType):
    @classmethod
    def get_xso_types(self):
        return [CompressionMethod]

    def pack(self, v):
        return CompressionMethod(v)

    def unpack(self, obj):
        return obj.name


@nonza.StreamFeatures.as_feature_class
class CompressionFeature(xso.XSO):
    TAG = ("http://jabber.org/features/compress", "compression")

    methods = xso.ChildValueList(
        type_=CompressionMethodType(),
    )


class CompressionRequest(xso.XSO):
    TAG = ("http://jabber.org/protocol/compress", "compress")

    method = xso.ChildText(
        ("http://jabber.org/protocol/compress", "method"),
    )

    def __init__(self, method):
        super().__init__()
        self.method = method


class CompressionSuccess(xso.XSO):
    TAG = ("http://jabber.org/protocol/compress", "compressed")

    SUCCESS = True


class CompressionFailure(xso.XSO):
    TAG = ("http://jabber.org/protocol/compress", "failure")

    SUCCESS = False


@asyncio.coroutine
def negotiate_compression(xmlstream, negotiation_timeout, features):
    # return features

    xmlstream._logger.debug("trying to negotiate compression")
    try:
        compression_feature = features[CompressionFeature]
    except KeyError:
        xmlstream._logger.debug("compression is not offered")
        return features

    xmlstream._logger.debug("compression methods: %s",
                            compression_feature.methods)

    if "zlib+full_flush" not in compression_feature.methods:
        return features

    response = yield from protocol.send_and_wait_for(
        xmlstream,
        [
            CompressionRequest("zlib+full_flush"),
        ],
        [
            CompressionFailure,
            CompressionSuccess,
        ]
    )

    if not response.SUCCESS:
        return features

    xmlstream.add_filter(CompressionFilter(unsafe_mode=True))

    return (yield from protocol.reset_stream_and_get_features(xmlstream))
