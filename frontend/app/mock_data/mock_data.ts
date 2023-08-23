import { Customer } from "../../models/customer";
import { Product, ProductStock } from "../../models/product";
import { ProductSupplier } from "../../models/product-supplier";
import { PurchaseOrder } from "../../models/purchase-order";
import { SalesOrder } from "../../models/sales-order";
import { Supplier } from "../../models/supplier";


export const mock_suppliers: Array<Supplier> = [
    {
        id: "sup_01",
        name: "Apple",
    },
    {
        id: "sup_02",
        name: "JB-HIFI",
    }
]

export const mock_products: Array<Product> = [
    {
        id: "SKU_001",
        name: "iPhone 14",
        maximumStockLevel: 100,
        minimumStockLevel: 10
    },
    {
        id: "SKU_002",
        name: "iPhone 14 PRO",
        maximumStockLevel: 100,
        minimumStockLevel: 10
    },
    {
        id: "SKU_003",
        name: "MacBook AIR M2",
        maximumStockLevel: 100,
        minimumStockLevel: 10
    },
    {
        id: "SKU_004",
        name: "MacBook M2",
        maximumStockLevel: 100,
        minimumStockLevel: 10
    },
    {
        id: "SKU_005",
        name: "MacBook PRO M2",
        maximumStockLevel: 100,
        minimumStockLevel: 10
    },
]

export const mock_product_suppliers: Array<ProductSupplier> = [
    {
        product: mock_products[0],
        supplier: mock_suppliers[0],
        price: 1300,
        leadTime: 3
    },
    {
        product: mock_products[0],
        supplier: mock_suppliers[1],
        price: 1500,
        leadTime: 1
    },
    {
        product: mock_products[1],
        supplier: mock_suppliers[0],
        price: 1600,
        leadTime: 3
    },
    {
        product: mock_products[2],
        supplier: mock_suppliers[0],
        price: 1800,
        leadTime: 3
    },
    {
        product: mock_products[3],
        supplier: mock_suppliers[0],
        price: 2100,
        leadTime: 3
    },
    {
        product: mock_products[4],
        supplier: mock_suppliers[0],
        price: 3000,
        leadTime: 3
    },
    {
        product: mock_products[2],
        supplier: mock_suppliers[1],
        price: 1500,
        leadTime: 8
    },
    {
        product: mock_products[3],
        supplier: mock_suppliers[1],
        price: 1900,
        leadTime: 8
    },
    {
        product: mock_products[4],
        supplier: mock_suppliers[1],
        price: 28,
        leadTime: 8
    },
]

export const mock_purchase_orders: PurchaseOrder[] = [
    {
        id: "po_01",
        supplier: mock_suppliers[0],
        orderPositions: [
            {
                id: "op_1",
                product: mock_products[0],
                price: 1300,
                deliveryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
                quantityOrdered: 3,
                quantityReceived: 0
            },
            {
                id: "op_2",
                product: mock_products[1],
                price: 1600,
                deliveryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
                quantityOrdered: 1,
                quantityReceived: 0
            },
            {
                id: "op_3",
                product: mock_products[2],
                price: 1800,
                deliveryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
                quantityOrdered: 1,
                quantityReceived: 0
            },
            {
                id: "op_4",
                product: mock_products[3],
                price: 2100,
                deliveryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
                quantityOrdered: 1,
                quantityReceived: 0
            },
            {
                id: "op_5",
                product: mock_products[4],
                price: 3000,
                deliveryDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
                quantityOrdered: 1,
                quantityReceived: 0
            },
        ],
        creationDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    },
    {
        id: "po_02",
        supplier: mock_suppliers[1],
        orderPositions: [
            {
                id: "op_1",
                product: mock_products[0],
                price: 1300,
                deliveryDate: new Date(Date.now() + 8 * 24 * 60 * 60 * 1000),
                quantityOrdered: 1,
                quantityReceived: 0
            },
        ],
        creationDate: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000)
    }
];

export const customers: Array<Customer> = [
    {
        id: "cus_1",
        name: 'Company XYZ',
        address: "Brisbane",
    },
]

const weekInMs = 7 * 24 * 60 * 60 * 1000;

export const mock_sales_orders: Array<SalesOrder> =
    [
        {
            id: "so_1",
            creationDate: new Date(Date.now() - weekInMs),
            orderPositions: [{
                deliveryDate: new Date(Date.now() + weekInMs),
                id: "op_1",
                product: mock_products[0],
                quantityOrdered: 1,
                quantityReceived: 0,
                price: 1300
            }],
            customer: customers[0]
        },
    ]

let batchId = 0;
export const mock_product_stock: Array<ProductStock> = [

]

for (let i = 0; i < 100; i++) {
    const supId = i % mock_suppliers.length;
    const prodId = i % mock_products.length
    const price = mock_product_suppliers
        .filter(ps => ps.product.id === mock_products[prodId].id && ps.supplier.id === mock_suppliers[supId].id)
        .map(ps => (ps.price))[0];
    if (price) {
        mock_product_stock.push({
            product: mock_products[prodId],
            price: price,
            batch: `2023/06/${batchId++}`,
            quantity: Math.round(Math.random() * 10),
            deliveryDate: new Date
        });
    }

}
