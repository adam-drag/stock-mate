'use client';
import { useState } from 'react';
import {
  Table,
  TableHead,
  TableRow,
  TableHeaderCell,
  TableBody,
  TableCell,
  Grid,
  Flex,
  Card,
  Title,
} from '@tremor/react';
import ReactPaginate from 'react-paginate';

export interface TableCardColumnMapping {
  columnName: string;
  columnKey: string;
}

export interface TableCardPropsInterface {
  data: Array<any>;
  columnsMappings: Array<TableCardColumnMapping>;
  recordsPerPage: number,
  title: String
}

export default function TableCard(tableCardProps: TableCardPropsInterface) {
  const [pageNumber, setPageNumber] = useState(0);
  const recordsPerPage = tableCardProps.recordsPerPage;
  const pagesVisited = pageNumber * recordsPerPage;

  const displayData = tableCardProps.data
    .slice(pagesVisited, pagesVisited + recordsPerPage)
    .map((element) => (
      <TableRow key={element.id}>
        {tableCardProps.columnsMappings.map(mapping => (<TableCell key={element[mapping.columnKey]}>{element[mapping.columnKey]}</TableCell>))}
      </TableRow>
    ));

  const displayColumnHeaders = tableCardProps.columnsMappings
    .map(mapping => (<TableHeaderCell key={mapping.columnName}>{mapping.columnName}</TableHeaderCell>))

  const pageCount = Math.ceil(tableCardProps.data.length / recordsPerPage);

  const changePage = ({ selected }: { selected: number }) => {
    setPageNumber(selected);
  };

  return (
    <Card>
      <Title>{tableCardProps.title}</Title>
      <Grid numColsLg={0} className="mt-1 gap-y-10 gap-x-14">
        <Flex>
          <Table className='w-full'>
            <TableHead>
              <TableRow className="px-4 py-2 border font-bold text-mid">
                {displayColumnHeaders}
              </TableRow>
            </TableHead>
            <TableBody>{displayData}</TableBody>
          </Table>
        </Flex>
        {pageCount > 1 && <Flex>
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
        </Flex>}
      </Grid>
    </Card>
  );
}
