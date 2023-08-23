'use client';
import { useState } from 'react';
import {
  Table,
  TableHead,
  TableRow,
  TableHeaderCell,
  TableBody,
  TableCell,
  Text,
  Grid,
  Flex,
  Button
} from '@tremor/react';
import { Product } from '../../models/product';
import ReactPaginate from 'react-paginate';
import Link from 'next/link';

export default function ProductsTable({ products }: { products: Product[] }) {
  const [pageNumber, setPageNumber] = useState(0);
  const productsPerPage = 5;
  const pagesVisited = pageNumber * productsPerPage;

  const displayProducts = products
    .slice(pagesVisited, pagesVisited + productsPerPage)
    .map((product) => (
      <TableRow key={product.id}>
        <TableCell>{product.id}</TableCell>
        <TableCell>
          <Text>{product.name}</Text>
        </TableCell>
        <TableCell>
          <Text>{product.minimumStockLevel}</Text>
        </TableCell>
        <TableCell>
          <Text>{product.maximumStockLevel}</Text>
        </TableCell>
        <TableCell>
          <Text>{"placeholder"}</Text>
        </TableCell>
        <TableCell>
          <Link href= {`/product/${product.id}`}>
            <Button size="xs" variant="secondary" color="gray">
              See details
            </Button>

          </Link>
        </TableCell>
      </TableRow>
    ));

  const pageCount = Math.ceil(products.length / productsPerPage);

  const changePage = ({ selected }: { selected: number }) => {
    setPageNumber(selected);
  };

  return (
    // <>
    <Grid numColsLg={0} className="mt-1 gap-y-10 gap-x-14">
      <Flex>
        <Table className='w-full'>
          <TableHead>
            <TableRow className="px-4 py-2 border font-bold text-mid">
              <TableHeaderCell>Id</TableHeaderCell>
              <TableHeaderCell>Name</TableHeaderCell>
              <TableHeaderCell>Minimum stock level</TableHeaderCell>
              <TableHeaderCell>Maximum stock level</TableHeaderCell>
              <TableHeaderCell>Placeholder</TableHeaderCell>
              <TableHeaderCell>Link</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>{displayProducts}</TableBody>
        </Table>
      </Flex>
      <Flex>
        <ReactPaginate
          previousLabel={'Previous'}
          nextLabel={'Next'}
          pageCount={pageCount}
          onPageChange={changePage}
          containerClassName={'pagination flex justify-center mt-4'}
          previousLinkClassName={'px-3 py-1 rounded-md bg-gray-200 text-gray-700 hover:bg-gray-300 mr-2'}
          nextLinkClassName={'px-3 py-1 rounded-md bg-gray-200 text-gray-700 hover:bg-gray-300 ml-2'}
          disabledClassName={'opacity-50 cursor-not-allowed'}
          activeClassName={'bg-gray-400 text-white rounded-md px-2'}
        />

      </Flex>
    </Grid>
  );
}
