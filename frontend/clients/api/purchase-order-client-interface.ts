import { Product } from "../../models/product";
import { PurchaseOrder } from "../../models/purchase-order";

export interface PurchaseOrderClientInterface {
    getAllPurchaseOrders(): Array<PurchaseOrder>;
    getProductPurchaseOrders(product: Product): Array<PurchaseOrder>;
}
