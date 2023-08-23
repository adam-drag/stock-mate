'use client';
import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { Container } from '../services/container';
import { Product } from '../models/product';
import { SalesOrder } from '../models/sales-order';

interface AppContextInterface {
  products: Array<Product>,
  fetchProducts: Function
}

const emptyContext: AppContextInterface = {
  products: [],
  fetchProducts: () => { }
}

export const AppContext = createContext(emptyContext);


export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [products, setProducts] = useState<Array<Product>>([]);
  const [salesOrders, setSalesOrders] = useState<Array<SalesOrder>>([]);

  const fetchProducts = async () => {
    const products = Container.getProductService().getProducts();
    setProducts(products);
  };

  // const fetchOrders = async () => {
  //   const products = Container.getSalesOrderService()
  //   setProducts(products);
  // };

  const contextValue = {
    products,
    fetchProducts,
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

