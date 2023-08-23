import { mock_product_suppliers } from "../app/mock_data/mock_data";
import { ProductSupplier } from "../models/product-supplier";
import { ProductSupplierClientInterface } from "./api/product-supplier-client-interface";

export class ProductSupplierClientMock implements ProductSupplierClientInterface {

    getAllProductSuppliers(): ProductSupplier[] {
        return mock_product_suppliers;
    }

    getProductSuppliersByProductId(productId: string): ProductSupplier[] {
        return mock_product_suppliers.filter(ps => ps.product.id === productId);
    }

    upsertProductSuppliers(productSuppliers: ProductSupplier[]): ProductSupplier[] {
        // Zmienic, przekazac product.id i [supplier.id] do serwisu plus reszta danych z ProductSupplier
        productSuppliers.forEach(ps => {
            const existingProductSupplier = mock_product_suppliers
                .find(mps => mps.product.id === ps.product.id && mps.supplier.id === ps.supplier.id);
            if (existingProductSupplier) {
                existingProductSupplier.price = ps.price;
                existingProductSupplier.leadTime = ps.leadTime;
            } else {
                mock_product_suppliers.push(ps);
            }
        });
        console.log("new product suppliers", mock_product_suppliers);
        return mock_product_suppliers;
    }
}
