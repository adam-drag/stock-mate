import { IssueService } from "./issue-service"
import { PurchaseOrderService } from "./purchase-order-service";
import { ProductService } from "./product-service"
import { SupplierService } from "./supplier-service";
import { SalesOrderService } from "./sales-order-service";
import { ProductClientMock } from "../clients/product-client-mock";
import { SupplierClientMock } from "../clients/supplier-client-mock";
import { PurchaseOrderClientMock } from "../clients/purchase-order-client-mock";
import { SalesOrderClientMock } from "../clients/sales-order-client-mock";
import { ProductSupplier } from "../models/product-supplier";
import { ProductSupplierService } from "./product-supplier-service";
import { ProductSupplierClientMock } from "../clients/product-suppliers-client-mock";

export class Container {

    public static instance = new Container()

    private readonly productService: ProductService;
    private readonly issueService: IssueService;
    private readonly purchaseOrderService: PurchaseOrderService;
    private readonly supplierService: SupplierService;
    private readonly salesOrderService: SalesOrderService;
    private readonly productSupplierService: ProductSupplierService

    private constructor() {
        this.productService = new ProductService(new ProductClientMock());
        this.issueService = new IssueService();
        this.supplierService = new SupplierService(new SupplierClientMock());
        this.purchaseOrderService = new PurchaseOrderService( new PurchaseOrderClientMock());
        this.salesOrderService = new SalesOrderService(new SalesOrderClientMock());
        this.productSupplierService = new ProductSupplierService(new ProductSupplierClientMock());
    }

    public static getProductService(): ProductService {
        return this.instance.productService;
    }

    public static getIssueService(): IssueService {
        return this.instance.issueService;
    }

    public static getPurchaseOrderService(): PurchaseOrderService {
        return this.instance.purchaseOrderService;
    }

    public static getSupplierService(): SupplierService {
        return this.instance.supplierService;
    }
    
    public static getSalesOrderService(): SalesOrderService {
        return this.instance.salesOrderService;
    }

    public static getProductSupplierService(): ProductSupplierService {
        return this.instance.productSupplierService;
    }
}
