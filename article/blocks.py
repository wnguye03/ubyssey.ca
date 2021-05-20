from wagtail.core import blocks
from wagtail.embeds import blocks as embed_blocks

class OneOffVideoBlock(blocks.StructBlock):
    video_embed = embed_blocks.EmbedBlock(
        null=False,
        blank=False,
    )
    title = blocks.CharBlock()
    caption = blocks.CharBlock()
    credit = blocks.CharBlock()