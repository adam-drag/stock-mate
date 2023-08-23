import { SalesOrder } from "../../models/sales-order";

export interface SalesOrderClientInterface {
    getAllSalesOrders(): Array<SalesOrder>;
    getProductSalesOrders(productId: String): Array<SalesOrder>;
}