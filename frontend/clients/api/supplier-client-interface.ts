import { Supplier } from "../../models/supplier";

export interface SupplierClientInterface {

    getAllSuppliers(): Array<Supplier>;
}