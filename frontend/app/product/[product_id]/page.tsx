
'use client';
import { Card, Title, Text, Tab, TabList, Grid, Button } from "@tremor/react";

import { useContext, useEffect, useState } from "react";
import UsageChartCard from "./usage-chart-card";
import { AppContext } from "../../../store/app_provider";
import { Product } from "../../../models/product";
import TableCard, { TableCardColumnMapping } from "../../cards/table-card";
import { PurchaseOrderService } from "../../../services/purchase-order-service";
import { Container } from "../../../services/container";
import { PurchaseOrder } from "../../../models/purchase-order";
import moment from "moment";
import { SalesOrder } from "../../../models/sales-order";
import { SalesOrderService } from "../../../services/sales-order-service";
import { Supplier } from "../../../models/supplier";
import { SupplierService } from "../../../services/supplier-service";
import { IssueService } from "../../../services/issue-service";
import { Issue } from "../../../models/issue";
import ProductDataModal from "../product-modal/page";
import { ProductService } from "../../../services/product-service";
import { ProductSupplier } from "../../../models/product-supplier";
import { ProductSupplierService } from "../../../services/product-supplier-service";


const purchaseOrderService: PurchaseOrderService = Container.getPurchaseOrderService()
const salesOrderService: SalesOrderService = Container.getSalesOrderService();
const productService: ProductService = Container.getProductService();
const supplierService: SupplierService = Container.getSupplierService();
const issueService: IssueService = Container.getIssueService();
const productSupplierService: ProductSupplierService = Container.getProductSupplierService();

interface PurchaseOrderTableRecord {
    id: String;
    deliveryDate: String;
    creationDate: String;
    quantityOrdered: number;
    quantityReceived: number;
    supplierName: String;
}

interface SalesOrderTableRecord {
    id: String;
    deliveryDate: String;
    quantityOrdered: number;
    quantityReceived: number;
    name: String;
}

interface ProductSupplierTableRecord {
    id: String;
    name: String;
    price: number;
    leadTime: number;
}

const purchaseOrderColumnMappings: Array<TableCardColumnMapping> = [
    { columnKey: 'id', columnName: 'Order Id' },
    { columnKey: 'quantityOrdered', columnName: 'Ordered' },
    { columnKey: 'quantityReceived', columnName: 'Received' },
    { columnKey: 'supplierName', columnName: 'Supplier Name' },
    { columnKey: 'creationDate', columnName: 'Created at' },
    { columnKey: 'deliveryDate', columnName: 'Delivery Date' },
]

const salesOrderColumnMappings: Array<TableCardColumnMapping> = [
    { columnKey: 'id', columnName: 'Order Id' },
    { columnKey: 'quantityOrdered', columnName: 'Ordered' },
    { columnKey: 'quantityReceived', columnName: 'Received' },
    { columnKey: 'name', columnName: 'Customer Name' },
    { columnKey: 'deliveryDate', columnName: 'Delivery Date' },
]

const issueColumnMappings: Array<TableCardColumnMapping> = [
    { columnKey: 'id', columnName: 'Issue Id' },
    { columnKey: 'severity', columnName: 'Severity' },
]

const suppliersColumnMappings: Array<TableCardColumnMapping> = [
    { columnKey: 'id', columnName: 'Supplier Id' },
    { columnKey: 'name', columnName: 'Name' },
    { columnKey: 'price', columnName: 'Price' },
    { columnKey: 'leadTime', columnName: 'Lead Time' },
]



export default function ProductPage({ params }: { params: { product_id: string } }) {
    const [selectedView, setSelectedView] = useState("1");

    const { products, fetchProducts } = useContext(AppContext);
    const [product, setProduct] = useState<Product>();
    const [purchaseOrders, setPurchaseOrders] = useState<Array<PurchaseOrder>>([])
    const [purchaseOrderTableRecords, setPurchaseOrderTableRecords] = useState<Array<PurchaseOrderTableRecord>>([]);
    const [salesOrders, setSalesOrders] = useState<Array<SalesOrder>>([]);
    const [salesOrderTableRecords, setSalesOrderTableRecords] = useState<Array<SalesOrderTableRecord>>([]);
    const [productSuppliersRecords, setProductSuppliersRecords] = useState<Array<ProductSupplierTableRecord>>([]);
    const [productSuppliers, setProductSuppliers] = useState<Array<ProductSupplier>>([]);
    const [issues, setIssues] = useState<Array<Issue>>([]);
    const [totalQty, setTotalQty] = useState<number>(0);
    const [totalValue, setTotalValue] = useState<number>(0);

    useEffect(() => {
        fetchProducts();
    }, []);

    useEffect(() => {
        const product = products.filter(prod => prod.id === params.product_id)[0];
        setProduct(product);

    }, [products]);

    useEffect(() => {
        if (product && product.id) {
            const purchaseOrders = purchaseOrderService.getProductOrders(product);
            const salesOrders = salesOrderService.getProductOrders(product);
            const productSuppliers = product && product.id ? productSupplierService.getProductSuppliers(product.id) : [];
            const issues = issueService.getProductIssues(product);
            setPurchaseOrders(purchaseOrders);
            setSalesOrders(salesOrders);
            setProductSuppliers(productSuppliers);
            setProductSuppliersRecords(productSuppliers.map(ps => ({ leadTime: ps.leadTime, id: ps.supplier.id, name: ps.supplier.name, price: ps.price })));
            setIssues(issues);
            setTotalQty(productService.getProductTotalQuantity(product.id));
            setTotalValue(productService.getProductTotalValue(product.id));
        }

    }, [product])

    // useEffect(() => {
    //     const suppliers = product ? product.productSuppliers ? product.productSuppliers.map(ps => ps.supplier) : [] : [];
    //     setSuppliers(suppliers);
    // }, [product?.productSuppliers])

    useEffect(() => {
        const poRecords: Array<PurchaseOrderTableRecord> = [];
        purchaseOrders.forEach(currentPo => {
            const currentPoTableRecords = currentPo.orderPositions
                .filter(op => product && op.product.id === product.id)
                .map(pos => {
                    return {
                        id: currentPo.id,
                        deliveryDate: moment(pos.deliveryDate).format('YYYY-MM-DD'),
                        creationDate: moment(currentPo.creationDate).format('YYYY-MM-DD'),
                        quantityOrdered: pos.quantityOrdered,
                        quantityReceived: pos.quantityReceived,
                        supplierName: currentPo.supplier.name
                    }
                })
            poRecords.push(...currentPoTableRecords)
        })

        setPurchaseOrderTableRecords(poRecords)
    }, [purchaseOrders])


    useEffect(() => {
        const soRecords: Array<SalesOrderTableRecord> = [];
        salesOrders.forEach(currentSo => {
            const currentPoTableRecords: Array<SalesOrderTableRecord> = currentSo.orderPositions.map(pos => {
                return {
                    id: currentSo.id,
                    deliveryDate: moment(pos.deliveryDate).format('YYYY-MM-DD'),
                    quantityOrdered: pos.quantityOrdered,
                    quantityReceived: pos.quantityReceived,
                    name: currentSo.customer.name
                }
            })
            soRecords.push(...currentPoTableRecords)
        })

        setSalesOrderTableRecords(soRecords)
    }, [salesOrders])
    const [isOpen, setIsOpen] = useState(false);
    const openModal = () => {
        setIsOpen(true);
    };

    const closeModal = () => {
        fetchProducts();
        setIsOpen(false);
    };

    return (
        <main className="p-4 md:p-10 mx-auto max-w-7xl">
            <TabList
                defaultValue="1"
                onValueChange={(value) => setSelectedView(value)}
            >
                <Tab value="1" text="Page 1" />
                <Tab value="2" text="Page 2" />
            </TabList>

            {selectedView === "1" ? (
                <>
                    <div className="mt-6">
                        <Card>
                            {isOpen && (<ProductDataModal closeModalCallback={closeModal} product={product} />)}
                            <div className="flex justify-between items-center">
                                <Title>Product Details</Title>
                                <Button onClick={openModal} size="xs">Edit product</Button>
                            </div>
                            <Grid numColsMd={1} numColsLg={4} className="mt-9">
                                <div className="flex justify-center">
                                    <p>Name: {product?.name}</p>
                                </div>
                                <div className="flex justify-center">
                                    <p>Quantity: {totalQty}</p>
                                </div>
                                <div className="flex justify-center">
                                    <p>Value: {totalValue}</p>
                                </div>

                                <div className="flex justify-center">
                                    <p>Suppliers: {productSuppliers && productSuppliers.length}</p>
                                </div>
                            </Grid>
                            <Grid numColsMd={1} numColsLg={2} className="mt-9 gap-4">

                                <UsageChartCard />
                                <UsageChartCard />

                            </Grid>
                            <Grid numColsMd={1} numColsLg={2} className="mt-9 gap-4">
                                <TableCard
                                    title={'Suppliers'}
                                    recordsPerPage={4}
                                    data={productSuppliersRecords}
                                    columnsMappings={suppliersColumnMappings} />
                                <TableCard
                                    title={'Issues'}
                                    recordsPerPage={4}
                                    data={issues}
                                    columnsMappings={issueColumnMappings} />
                            </Grid>

                            <Grid numColsMd={1} numColsLg={1} className="mt-9 gap-4">
                                <TableCard
                                    title={'Purchase Orders'}
                                    recordsPerPage={4}
                                    data={purchaseOrderTableRecords}
                                    columnsMappings={purchaseOrderColumnMappings} />
                                <TableCard
                                    title={'Sales Orders'}
                                    recordsPerPage={4}
                                    data={salesOrderTableRecords}
                                    columnsMappings={salesOrderColumnMappings} />

                            </Grid>

                        </Card>
                    </div>
                </>
            ) : (
                <div className="mt-6">
                    <Card>
                        <div className="h-96" />
                    </Card>
                </div>
            )}
        </main>
    );
}


