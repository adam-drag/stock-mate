import { SupplierClientInterface } from "../clients/api/supplier-client-interface";
import {Product } from "../models/product";
import { ProductSupplier } from "../models/product-supplier";
import { Supplier } from "../models/supplier";

export class SupplierService {

    constructor(private readonly supplierClient: SupplierClientInterface) { }

    getAllSuppliers(): Array<Supplier> {
        return this.supplierClient.getAllSuppliers()
    }
}
