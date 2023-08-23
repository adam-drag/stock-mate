import { Product } from "./product";

export interface OrderPosition {
    id: string;
    product: Product;
    price: number;
    quantityOrdered: number;
    quantityReceived: number;
    deliveryDate: Date;
}
