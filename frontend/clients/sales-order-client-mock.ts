import { mock_sales_orders } from "../app/mock_data/mock_data";
import { SalesOrder } from "../models/sales-order";
import { SalesOrderClientInterface } from "./api/sales-order-client-interface";

export class SalesOrderClientMock implements SalesOrderClientInterface {

    getAllSalesOrders(): SalesOrder[] {
        return mock_sales_orders;
    }

    getProductSalesOrders(productId: String): SalesOrder[] {
        return mock_sales_orders.filter(so => so.orderPositions.some(op => op.product.id === productId));
    }
}
