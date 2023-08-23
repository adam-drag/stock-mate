import { mock_product_stock } from "../app/mock_data/mock_data";
import { ProductClientInterface } from "../clients/api/product-client-interface";
import { ProductClientMock } from "../clients/product-client-mock";
import {  Product, ProductStatistic } from "../models/product";

export class ProductService {

    constructor(private readonly productClient: ProductClientInterface) { }

    getProducts(): Array<Product> {
        return this.productClient.getAllProducts();
    }

    getProductTotalQuantity(productId:string): number {
        return mock_product_stock.filter(ps=>ps.product.id === productId).reduce((acc, ps) => acc + ps.quantity, 0);
    }

    getProductTotalValue(productId:string): number {
        return mock_product_stock.filter(ps=>ps.product.id === productId).reduce((acc, ps) => acc + ps.price * ps.quantity, 0);
    }

    getTotalValue() {
        return mock_product_stock.reduce((acc, ps) => acc + ps.price * ps.quantity, 0);
    }

    getTotalQuantity() {
        return mock_product_stock.reduce((acc, ps) => acc + ps.quantity, 0);
    }

    upsertProduct(product:Product):void {
        // this.productClient.upsertProduct(product);
    }

    getTopProductsByQty():Array<ProductStatistic>{
        const pc :ProductClientInterface = new ProductClientMock();
        return pc.getTopNProductsByQuantity(3);
    }

    getTopProductsByVal():Array<ProductStatistic>{
        const pc :ProductClientInterface = new ProductClientMock();
        return pc.getTopNProductsByValue(3);
    }
}
