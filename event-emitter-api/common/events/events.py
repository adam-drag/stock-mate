from enum import Enum, auto


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


class EventStatus(Enum):
    Pending = auto()
    Failed = auto()
    Processed = auto()
