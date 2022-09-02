from django.apps import AppConfig


class SectionConfig(AppConfig):
    name = 'section'

    def ready(self) -> None:
        import section.sectionable.signals
        return super().ready()