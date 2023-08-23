import { Customer } from "./customer";
import { OrderPosition } from "./order-position";


export interface SalesOrder {
    id:String;
    customer: Customer;
    orderPositions: Array<OrderPosition>;
    creationDate: Date;
}
