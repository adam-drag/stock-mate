'use client';
import { Card, Grid, TextInput, Text, Bold, Flex, Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Dropdown, DropdownItem, Button } from "@tremor/react";
import { useEffect, useState } from "react";
import { Container } from "../../../services/container";
import { SupplierService } from "../../../services/supplier-service";
import { ProductService } from "../../../services/product-service";
import { Product } from "../../../models/product";
import { Supplier } from "../../../models/supplier";
import { ProductSupplier } from "../../../models/product-supplier";
import { ProductSupplierService } from "../../../services/product-supplier-service";

const suppliersService: SupplierService = Container.getSupplierService();
const productService: ProductService = Container.getProductService();
const productSupplierService: ProductSupplierService = Container.getProductSupplierService();

export interface AddProductProps {
    closeModalCallback: React.MouseEventHandler<HTMLButtonElement>;
    product?: Product;
}

interface ProductSupplierRecord {
    supplier: Supplier;
    product?: Product;
    price: number;
    leadTime: number;
}



export default function ProductDataModal(props: AddProductProps) {
    const { product } = props;
    const [productName, setProductName] = useState(product ? product.name : "");
    const [supplierName, setSupplierName] = useState(""); // TODO change to list of suppliers
    const [price, setPrice] = useState(""); // TODO change to price per supplier
    const [productSupplierRecords, setProductSupplierRecords] = useState<Array<ProductSupplierRecord>>
        (product && product.id ? productSupplierService.getProductSuppliers(product.id) : []);
    const [allSuppliers, setAllSuppliers] = useState<Supplier[]>([]);
    const [supplierOptions, setSupplierOptions] = useState<Array<string>>([])
    const [leadTime, setLeadTime] = useState<string>("");
    const [minStockLevel, setMinStockLevel] = useState<string>("");
    const [maxStockLevel, setMaxStockLevel] = useState<string>("");

    const [isProductNameError, setIsProductNameError] = useState(false);
    const [isMinStockLevelError, setIsMinStockLevelError] = useState(false);
    const [isMaxStockLevelError, setIsMaxStockLevelError] = useState(false);
    const [isSupplierError, setIsSupplierError] = useState(false);
    const [isPriceError, setIsPriceError] = useState(false);
    const [productNameErrorMsg, setProductNameErrorMsg] = useState("");
    const [minStockLevelErrorMsg, setMinStockLevelErrorMsg] = useState("");
    const [maxStockLevelErrorMsg, setMaxStockLevelErrorMsg] = useState("");
    const [supplierErrorMsg, setSupplierErrorMsg] = useState("");
    const [priceErrorMsg, setPriceErrorMsg] = useState("");


    useEffect(() => {
        const newAllSuppliers = suppliersService.getAllSuppliers();
        const filteredSuppliers = newAllSuppliers.filter(ns => productSupplierRecords.findIndex(psr => psr && psr.supplier && psr.supplier.id === ns.id) === -1);
        const newSupplierOptions = filteredSuppliers.map(supplier => supplier.name);
        setAllSuppliers(newAllSuppliers);
        setSupplierOptions(newSupplierOptions);
    }, [productSupplierRecords]);

    useEffect(() => {
        console.log("Called");
        const newAllSuppliers = suppliersService.getAllSuppliers();
        const filteredSuppliers = newAllSuppliers.filter(ns => productSupplierRecords.findIndex(psr => psr && psr.supplier && psr.supplier.id === ns.id) === -1);
        const newSupplierOptions = filteredSuppliers.map(supplier => supplier.name);
        setAllSuppliers(newAllSuppliers)
        setSupplierOptions(newSupplierOptions);
    }, [])


    const handleProductNameChange = (event: any) => {
        setProductName(event.target.value);
        if (isProductNameError) {
            validateProductName(event.target.value);
        }
    };

    const handleMinStockLevelChange = (event: any) => {
        if (isMinStockLevelError) {
            validateMinStockLevel(event.target.value);
        }
        setMinStockLevel(event.target.value);
    };

    const handleMaxStockLevelChange = (event: any) => {
        if (isMinStockLevelError) {
            validateMinStockLevel(event.target.value);
        }
        setMaxStockLevel(event.target.value);
    };

    const handleSupplierChange = (selectedSupplierName: string) => {
        if (isSupplierError) {
            validateSupplier(selectedSupplierName);
        }
        setSupplierName(selectedSupplierName);
    };

    const handlePriceChange = (event: any) => {
        if (isPriceError) {
            validatePrice(event.target.value);
        }
        setPrice(event.target.value);
    };

    const isNumber = (value: string): boolean => {
        return !isNaN(Number(value));
    };

    const validateProductName = (productName: string) => {
        setIsProductNameError(false);
        if (productName.length < 3) {
            setIsProductNameError(true);
            setProductNameErrorMsg("Product name must have at least 3 characters")
            return false;
        }
        if (!productName.match(/^[a-zA-Z0-9 ]+$/)) {
            setIsProductNameError(true);
            setProductNameErrorMsg("Product must be alhpanumeric");
            return false;
        }
        return true;
    }

    const validateMinStockLevel = (minStockLevel: string) => {
        setIsMinStockLevelError(false);
        if (!isNumber(minStockLevel)) {
            setIsMinStockLevelError(true);
            setMinStockLevelErrorMsg("Minimum stock level must be a number")
            return false;
        }
        return true;
    }
    const validateMaxStockLevel = (maxStockLevel: string) => {
        setIsMaxStockLevelError(false);
        if (!isNumber(maxStockLevel)) {
            setIsMaxStockLevelError(true);
            setMaxStockLevelErrorMsg("Maximum stock level must be a number")
            return false;
        }
        return true;
    }

    const validatePrice = (price: string) => {
        setIsPriceError(false);
        if (!isNumber(price)) {
            setIsPriceError(true);
            setPriceErrorMsg("Price must be a number")
            return false;
        }
        if (!price) {
            setIsPriceError(true);
            setPriceErrorMsg("Price is required")
            return false;
        }
        return true;
    }


    const validateLeadTime = (leadTime: string) => {
        setIsPriceError(false);
        if (!isNumber(leadTime)) {
            setIsPriceError(true);
            setPriceErrorMsg("Price must be a number")
            return false;
        }
        if (!leadTime) {
            setIsPriceError(true);
            setPriceErrorMsg("Price is required")
            return false;
        }
        return true;
    }


    const validateSupplier = (supplier: string) => {
        setIsSupplierError(false);
        if (allSuppliers.filter(sup => sup.name === supplier).length === 0) {
            setIsSupplierError(true);
            setSupplierErrorMsg("Provide a correct supplier from the list")
            return false;
        }
        return true;
    }

    const validateSubmitInputs = () => {
        const isProductNameValid = validateProductName(productName);
        const isMinStockLevelvalid = validateMinStockLevel(minStockLevel);
        const isMaxStockLevelvalid = validateMaxStockLevel(maxStockLevel);
        return isProductNameValid && isMinStockLevelvalid && isMaxStockLevelvalid;
    }

    const handleSubmit = (event: any) => {
        event.preventDefault();

        if (validateSubmitInputs()) {
            const newProduct: Product = {
                ...product, ...{
                    name: productName,
                    maximumStockLevel: Number.parseFloat(maxStockLevel),
                    minimumStockLevel: Number.parseFloat(minStockLevel)
                }
            }


            productService.upsertProduct(newProduct);
            const productSuppliers: ProductSupplier[] = productSupplierRecords.map(psr => ({
                ...psr, ...{ product: newProduct }
            }))
            productSupplierService.upsertProductSuppliers(productSuppliers);

            props.closeModalCallback(event);
        }
    };

    const handleAddSupplier = (event: any) => {
        if (validateSupplier(supplierName) && validatePrice(price) && validateLeadTime(leadTime)) {
            const selectedSupplier: Supplier = allSuppliers.filter(s => s.name === supplierName)[0]
            const productSupplierRecord: ProductSupplierRecord = {
                supplier: selectedSupplier,
                product: undefined,
                price: parseFloat(price),
                leadTime: 3
            }
            const newSuppliers = [...productSupplierRecords, productSupplierRecord]
            setProductSupplierRecords(newSuppliers);
            setSupplierName("");
            setPrice("")
        }
    };

    const removeProductSuppierRecord = (removedPsr: ProductSupplierRecord) => {
        const filteredPcrs = productSupplierRecords
            .filter(psr => psr && psr.supplier &&
                removedPsr && removedPsr.supplier &&
                psr.supplier.id !== removedPsr.supplier.id)
        setProductSupplierRecords(filteredPcrs);
    }

    return (
        <div className="fixed z-10 inset-0 overflow-y-auto">
            <div className="flex items-center justify-center min-h-screen px-4">
                {/* <div className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"></div> */}
                <div className="bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all  sm:w-8/12">
                    <div>
                        <h3 className="text-lg leading-6 font-medium text-gray-900">{product ? 'Modify Product' : 'Add Product'}</h3>
                    </div>
                    <div className="mt-6">
                        <Card>
                            <Grid numColsMd={2} numColsLg={2} className="mt-9 gap-8 flex justify-center items-center">
                                <div className="flex justify-center items-center">
                                    <Text><Bold>Product name</Bold></Text>
                                    <TextInput defaultValue={productName} error={isProductNameError}
                                        onChange={handleProductNameChange} className="w-1/3" placeholder="Name..." />

                                </div>
                                <div className="flex justify-center items-center">
                                    <Text className="w-1/3"><Bold>Minimum stock level</Bold></Text>
                                    <TextInput defaultValue={'placeholder'} error={isMinStockLevelError} onChange={handleMinStockLevelChange}
                                        className="w-1/3" />
                                </div>
                                <div className="flex justify-center items-center">
                                    <Text className="w-1/3"><Bold>Maximum stock level</Bold></Text>
                                    <TextInput defaultValue={'placeholder'} error={isMaxStockLevelError} onChange={handleMaxStockLevelChange}
                                        className="w-1/3" />
                                </div>

                            </Grid>
                            <div className="mt-6">
                                <Grid numColsMd={1} numColsLg={4} className="mt-9">
                                    <div className="flex justify-center items-center">
                                        {/* <div className="flex justify-left">
                                            <Text className="w-1/2"><Bold>Supplier</Bold></Text>
                                        </div> */}
                                        <Dropdown
                                            className="w-3/4"
                                            onValueChange={handleSupplierChange}
                                            placeholder="Supplier"
                                        >
                                            {supplierOptions.map(s => (<DropdownItem key={s} value={s} text={s} />))}
                                        </Dropdown>
                                    </div>
                                    <div className="flex justify-center items-center">
                                        <div className="flex justify-center items-center">
                                            <Text className="w-1/2"><Bold>Price</Bold></Text>
                                        </div>
                                        <div className="flex justify-center items-center">
                                            <TextInput value={price} error={isPriceError} onChange={handlePriceChange} className="w-1/2" placeholder="Price..." />
                                        </div>
                                    </div>
                                    <div className="flex justify-center items-center">
                                        <div className="flex justify-center items-center">
                                            <Text className="w-1/2"><Bold>Lead Time</Bold></Text>
                                        </div>
                                        <div className="flex justify-center items-center">
                                            <TextInput value={price} error={isPriceError} onChange={handlePriceChange} className="w-1/2" placeholder="Lead time..." />
                                        </div>
                                    </div>
                                    <div className="flex justify-center items-center">
                                        <button
                                            onClick={handleAddSupplier}
                                            className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-blue-500 
                                        hover:bg-blue-600 border border-transparent rounded-md focus:outline-none focus-visible:ring-2
                                         focus-visible:ring-offset-2 focus-visible:ring-blue-500 w-1/4 ml-12"
                                        >
                                            Add
                                        </button>
                                    </div>
                                </Grid>
                                {productSupplierRecords.length > 0 && <Flex className="mt-8">
                                    <Table className='w-full'>
                                        <TableHead>
                                            <TableRow className="px-4 py-2 border font-bold text-mid">
                                                <TableHeaderCell className="w-1/8">Supplier id</TableHeaderCell>
                                                <TableHeaderCell>Supplier name</TableHeaderCell>
                                                <TableHeaderCell>Price</TableHeaderCell>
                                                <TableHeaderCell>Lead time</TableHeaderCell>
                                                <TableHeaderCell>Delete</TableHeaderCell>
                                            </TableRow>
                                        </TableHead>
                                        <TableBody>
                                            {productSupplierRecords.map(psr => (
                                                <TableRow key={psr!.supplier!.id}>
                                                    <TableCell className="w-1/8">
                                                        <Text>{psr.supplier!.id}</Text>
                                                    </TableCell>
                                                    <TableCell>
                                                        <Text>{psr.supplier!.name}</Text>
                                                    </TableCell>
                                                    <TableCell>
                                                        <Text>{psr.price}</Text>
                                                    </TableCell>
                                                    <TableCell>
                                                        <Text>{psr.leadTime}</Text>
                                                    </TableCell>
                                                    <TableCell className="fill-blue-500 w-1/8">
                                                        <svg
                                                            onClick={() => removeProductSuppierRecord(psr)}
                                                            className="h-8 w-8 text-blue-500 hover:fill-red-500 hover:text-black-900 cursor-pointer"
                                                            fill="none"
                                                            viewBox="0 0 24 24"
                                                            stroke="currentColor"
                                                        >
                                                            <path
                                                                stroke-linecap="round"
                                                                stroke-linejoin="round"
                                                                stroke-width="2"
                                                                d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                                                            />
                                                        </svg>


                                                    </TableCell>
                                                </TableRow>
                                            ))}
                                        </TableBody>
                                    </Table>
                                </Flex>}
                            </div>
                        </Card>
                    </div>
                    {isProductNameError && <Text color='red' className="flex justify-center items-center mt-4">{productNameErrorMsg}</Text>}
                    {isMinStockLevelError && <Text color='red' className="flex justify-center items-center mt-4">{minStockLevelErrorMsg}</Text>}
                    {isSupplierError && <Text color='red' className="flex justify-center items-center mt-4">{supplierErrorMsg}</Text>}
                    {isPriceError && <Text color='red' className="flex justify-center items-center mt-4">{priceErrorMsg}</Text>}

                    <div className="flex justify-center items-center mt-4">
                        <button
                            onClick={handleSubmit}
                            className="inline-flex justify-center px-4 py-2 text-sm font-medium text-white bg-blue-500
                             hover:bg-blue-600 border border-transparent rounded-md focus:outline-none focus-visible:ring-2
                              focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                        >
                            Submit
                        </button>
                        <button
                            onClick={props.closeModalCallback}
                            className="inline-flex justify-center px-4 py-2 ml-2 text-sm font-medium text-gray-700 bg-gray-200 hover:bg-gray-300 border border-transparent rounded-md focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
                        >
                            Cancel
                        </button>
                    </div>

                </div>
            </div>
        </div>
    )
}