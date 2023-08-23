import { ProductSupplier } from "./product-supplier";

export interface Supplier {
    id: string;
    name: string;
    productSuppliers?: Array<ProductSupplier>;
}
