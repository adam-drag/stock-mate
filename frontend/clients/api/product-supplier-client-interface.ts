import { ProductSupplier } from "../../models/product-supplier";

export interface ProductSupplierClientInterface {
    getAllProductSuppliers(): Array<ProductSupplier>;
    getProductSuppliersByProductId(productId: string): Array<ProductSupplier>;
    upsertProductSuppliers(productSupplier: ProductSupplier[]): ProductSupplier[];
}
