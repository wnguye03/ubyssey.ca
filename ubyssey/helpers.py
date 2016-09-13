from dispatch.apps.content.models import Article

class ArticleHelper(object):

    @staticmethod
    def get_frontpage(reading_times=None, section=None, section_id=None, sections=[], exclude=[], limit=7, is_published=True):

        if is_published:
            is_published = 1
        else:
            is_published = 0

        if reading_times is None:
            reading_times = {
                'morning_start': '9:00:00',
                'midday_start': '11:00:00',
                'midday_end': '16:00:00',
                'evening_start': '16:00:00',
            }

        context = {
            'section': section,
            'section_id': section_id,
            'excluded': ",".join(map(str, exclude)),
            'sections': ",".join(sections),
            'limit': limit,
            'is_published': is_published
        }

        context.update(reading_times)

        query = """
        SELECT *,
            TIMESTAMPDIFF(SECOND, published_at, NOW()) as age,
            CASE reading_time
                 WHEN 'morning' THEN IF( CURTIME() < %(morning_start)s, 1, 0 )
                 WHEN 'midday'  THEN IF( CURTIME() >= %(midday_start)s AND CURTIME() < %(midday_end)s, 1, 0 )
                 WHEN 'evening' THEN IF( CURTIME() >= %(evening_start)s, 1, 0 )
                 ELSE 0.5
            END as reading
            FROM content_article
        """

        query_where = """
            WHERE head = 1 AND
            is_published = %(is_published)s AND
            parent_id NOT IN (%(excluded)s)
        """

        if section is not None:
            query += """
                INNER JOIN content_section on content_article.section_id = content_section.id AND content_section.slug = %(section)s
            """
        elif section_id is not None:
            query_where += " AND section_id = %(section_id)s "
        elif sections:
            query += """
                INNER JOIN content_section on content_article.section_id = content_section.id AND FIND_IN_SET(content_section.slug, %(sections)s)
            """

        query += query_where + """
            ORDER BY reading DESC, ( age * ( 1 / ( 4 * importance ) ) ) ASC
            LIMIT %(limit)s
        """

        return Article.objects.raw(query, context)
