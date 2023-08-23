import { mock_product_suppliers, mock_suppliers } from "../app/mock_data/mock_data";
import { ProductSupplier } from "../models/product-supplier";
import { Supplier } from "../models/supplier";
import { SupplierClientInterface } from "./api/supplier-client-interface";

export class SupplierClientMock implements SupplierClientInterface {


    getAllSuppliers(): Supplier[] {
        return mock_suppliers;
    }
}
