'use client';
import { Card, Title, Button } from '@tremor/react';
import ProductsTable from './table';
import { useContext, useEffect, useState } from 'react';
import { AppContext } from '../../store/app_provider';
import ProductDataModal from '../product/product-modal/page';

export const dynamic = 'force-dynamic';


export default function ProductsPage() {
  const { products, fetchProducts } = useContext(AppContext);

  useEffect(() => {
    fetchProducts();
  }, []);

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
      <div className="flex justify-between items-center">
        <Title>Products</Title>
        <Button onClick={openModal} size="xs">Add product</Button>
      </div>
      <Card className="mt-6">
        {isOpen && (<ProductDataModal closeModalCallback={closeModal} />)}
        {/* @ts-expect-error Server Component */}
        <ProductsTable products={products} />
      </Card>
    </main>
  );
}
