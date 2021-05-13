from wagtail.core import blocks
from wagtail.embeds import blocks as embed_blocks

class VideoBlock(blocks.StructBlock):
    video_embed = embed_blocks.EmbedBlock(
        null=False,
        blank=False,
    )
    tile = blocks.CharBlock()
    caption = blocks.CharBlock()
    credit = blocks.CharBlock()