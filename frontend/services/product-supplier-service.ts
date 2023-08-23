import { ProductSupplierClientInterface } from "../clients/api/product-supplier-client-interface";
import { ProductSupplier } from "../models/product-supplier";

export class ProductSupplierService {
    constructor(private productSupplierClient: ProductSupplierClientInterface) {
        this.productSupplierClient = productSupplierClient;
    }
    getProductSuppliers(productId: string): ProductSupplier[] {
        return this.productSupplierClient.getProductSuppliersByProductId(productId);
    }
    getAllProductSuppliers(): ProductSupplier[] {
        return this.productSupplierClient.getAllProductSuppliers();
    }

    upsertProductSuppliers(productSuppliers: ProductSupplier[]): ProductSupplier[] {
        return this.productSupplierClient.upsertProductSuppliers(productSuppliers);
    }
}
