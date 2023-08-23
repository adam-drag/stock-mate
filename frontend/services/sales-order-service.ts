import { SalesOrderClientInterface } from "../clients/api/sales-order-client-interface";
import { OrderPosition } from "../models/order-position";
import { Product } from "../models/product";
import { SalesOrder } from "../models/sales-order";


export class SalesOrderService {

    constructor(private readonly salesOrderClient: SalesOrderClientInterface) { }
    getProductOrders(product: Product): Array<SalesOrder> {
        return this.salesOrderClient.getProductSalesOrders(product.id);
    }
}
