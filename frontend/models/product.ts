export interface Product {
    id?: string;
    name: string;
    minimumStockLevel: number;
    maximumStockLevel: number;
}


export interface ProductStock {
    product: Product;
    price: number;
    batch: string;
    quantity: number;
    deliveryDate: Date;
}

export interface ProductStatistic {
    product: Product;
    totalQuantity: number;
    totalValue: number;
}
