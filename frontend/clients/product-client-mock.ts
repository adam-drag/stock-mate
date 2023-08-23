import { mock_product_stock, mock_products } from "../app/mock_data/mock_data";
import { Product, ProductStatistic } from "../models/product";
import { ProductClientInterface } from "./api/product-client-interface";

export class ProductClientMock implements ProductClientInterface {

    private id = 5;

    getAllProducts(): Product[] {
        return mock_products;
    }

    upsertProduct(product: Product): void {
        throw new Error("Method not implemented.");
        // const productInDb = mock_products2.filter(prod => prod.id === product.id)[0]
        // debugger;

        // if (productInDb) {
        //     productInDb.name = product.name;
        //     productInDb.price = product.price;
        //     productInDb.quantity = product.quantity;
        //     productInDb.productSuppliers = product.productSuppliers;
        // } else {
        //     product.id = "SKU_00" + ++this.id;
        //     product.value = product.quantity * product.price;
        //     mock_products.push(product);
        // }
    }

    getProductStatistics(): ProductStatistic[] {
        const productsStatistics: Array<ProductStatistic> = mock_products.map(prod => ({ product: prod, totalQuantity: 0, totalValue: 0 }));
        debugger;
        mock_product_stock.forEach(productBatch => {
            const ps: ProductStatistic = productsStatistics.filter(ps => ps.product.id === productBatch.product.id)[0]
            ps.totalQuantity += productBatch.quantity;
            ps.totalValue += productBatch.price * productBatch.quantity;
        }
        )
        return productsStatistics;
    }

    getTopNProductsByQuantity(n: number): ProductStatistic[] {
        const productsStatistics: Array<ProductStatistic> = this.getProductStatistics();
        return productsStatistics.sort((ps1, ps2) => ps2.totalQuantity - ps1.totalQuantity).splice(0, n);
    }

    getTopNProductsByValue(n: number): ProductStatistic[] {
        const productsStatistics: Array<ProductStatistic> = this.getProductStatistics();
        return productsStatistics.sort((ps1, ps2) => ps2.totalValue - ps1.totalValue).splice(0, n);
    }
}
