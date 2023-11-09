import os


class EventConfig:
    def __init__(self, name, topic_arn=None, subject=None):
        self.name = name
        self.topic_arn = topic_arn if topic_arn else os.environ.get(f"{name}_TOPIC_ARN")
        self.subject = subject if subject else

    def __str__(self):
        return self.name


class EventType(Enum):
    NewPurchaseOrderScheduled = auto()
    NewPurchaseOrderPersisted = auto()

    NewSalesOrderScheduled = auto()
    NewSalesOrderPersisted = auto()

    NewDeliveryScheduled = auto()
    NewDeliveryPersisted = auto()

    NewDispatchRequested = auto()
    RequestedDispatchSucceeded = auto()
    RequestedDispatchFailed = auto()

    UsageUpdateScheduled = auto()
    UsageUpdatePersisted = auto()

    NewProductScheduled = auto()
    NewProductPersisted = auto()

    NewSupplierScheduled = auto()
    NewSupplierPersisted = auto()

    NewCustomerScheduled = auto()
    NewCustomerPersisted = auto()
