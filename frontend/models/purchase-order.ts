import { OrderPosition } from "./order-position";
import { Supplier } from "./supplier";

export interface PurchaseOrder {
    id:String;
    supplier: Supplier;
    orderPositions: OrderPosition[];
    creationDate: Date;
}
