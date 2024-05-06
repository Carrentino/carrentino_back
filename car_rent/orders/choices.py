from core.types import Choices


class ORDER_STATUSES(Choices):
    UNDER_CONSIDERATION = 'UC'
    ACCEPTED = 'AD'
    IN_PROGRESS = 'IP'
    CANCELED = 'CD'
    REJECTED = 'RD'
    FINISHED = 'FD'

    CHOICES = (
        (UNDER_CONSIDERATION, "На рассмотрении"),
        (ACCEPTED, "Одобрен"),
        (IN_PROGRESS, "Выполняется"),
        (CANCELED, "Отменен"),
        (REJECTED, "Отклонен"),
        (FINISHED, "Завершен")
    )
