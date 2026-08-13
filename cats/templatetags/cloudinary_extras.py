from django import template

register = template.Library()


@register.filter
def cld_optimize(url):
    """Inserts Cloudinary's automatic format + quality transformation
    (f_auto,q_auto) into a Cloudinary delivery URL.

    f_auto - Cloudinary serves whichever image format the visitor's
             browser supports best (WebP/AVIF where possible, falling
             back to JPEG/PNG otherwise), with no duplicate files and
             no manual conversion needed.
    q_auto - Cloudinary picks the lowest quality setting that doesn't
             produce a visible difference, tuned per image.

    Safe no-op on any URL that isn't a Cloudinary "/upload/" delivery
    URL, so it can be applied without checking the source first.
    """
    if not url or '/upload/' not in url:
        return url
    return url.replace('/upload/', '/upload/f_auto,q_auto/', 1)
