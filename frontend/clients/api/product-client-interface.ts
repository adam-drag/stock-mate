import {Product, ProductStatistic } from "../../models/product";

export interface ProductClientInterface {
    getAllProducts():Array<Product>;

    upsertProduct(product:Product):void;

    getTopNProductsByQuantity(n: number): Array<ProductStatistic>;
    
    getTopNProductsByValue(n: number): ProductStatistic[];
}