import {Product } from "./product";
import { Supplier } from "./supplier";


export interface ProductSupplier {
    product: Product;
    supplier: Supplier;
    price: number;
    leadTime: number;
}
