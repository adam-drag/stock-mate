import { PurchaseOrderClientInterface } from "../clients/api/purchase-order-client-interface";
import { Product } from "../models/product";
import { PurchaseOrder } from "../models/purchase-order";

export class PurchaseOrderService {
    constructor(private readonly purchaseOrderClient: PurchaseOrderClientInterface) { }
    getProductOrders(product: Product): Array<PurchaseOrder> {
        return this.purchaseOrderClient.getProductPurchaseOrders(product);
    }
}
