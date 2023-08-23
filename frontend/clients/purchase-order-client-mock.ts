import { mock_purchase_orders } from "../app/mock_data/mock_data";
import { Product } from "../models/product";
import { PurchaseOrder } from "../models/purchase-order";
import { PurchaseOrderClientInterface } from "./api/purchase-order-client-interface";

export class PurchaseOrderClientMock implements PurchaseOrderClientInterface {
    getAllPurchaseOrders(): PurchaseOrder[] {
        return mock_purchase_orders;
    }
    getProductPurchaseOrders(product: Product): PurchaseOrder[] {
        return mock_purchase_orders.filter(po => po.orderPositions.some(op => op.product.id === product.id));
    }
}
