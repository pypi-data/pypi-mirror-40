from webtypes import validators
from webtypes.codecs import BaseCodec
from webtypes.parse import parse_yaml

APISTAR_CONFIG = validators.Object(
    properties=[
        ('schema', validators.Object(
            properties=[
                ('path', validators.String()),
                ('format', validators.String(enum=['openapi', 'swagger'])),
            ],
            additional_properties=False,
            required=['path', 'format']
        )),
        ('docs', validators.Object(
            properties=[
                ('theme', validators.String(enum=['webtypes', 'redoc', 'swaggerui'])),
            ],
            additional_properties=False,
        ))
    ],
    additional_properties=False,
    required=['schema'],
)


class ConfigCodec(BaseCodec):
    media_type = 'application/x-yaml'
    format = 'webtypes'

    def decode(self, content, **options):
        return parse_yaml(content, validator=APISTAR_CONFIG)
