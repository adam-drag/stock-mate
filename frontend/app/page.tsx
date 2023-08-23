import { Grid } from '@tremor/react';
import { IssueStat } from '../models/issue-stat';
import { ProductStatistic } from '../models/product';
import { Container } from '../services/container';
import { IssueService } from '../services/issue-service';
import { ProductService } from '../services/product-service';
import DashboardSummaryCard from './cards/dashboard-summary-card';
import DasboardBarListCard, { BarListRecord } from './cards/dashboard-bar-list-card';
import DashboardIssueDonutChart from './cards/dashboard-issue-donut-chart';

const dataFormatter = (number: number) =>
  Intl.NumberFormat('us').format(number).toString();

const productService: ProductService = Container.getProductService()
const issueService: IssueService = Container.getIssueService()

export default function DashboardPage() {
  const productsTotalValue = productService.getTotalValue()
  const productsTotalQuantity = productService.getTotalQuantity()
  const topProductsByQuantity: Array<ProductStatistic> = productService.getTopProductsByQty()
  const topProductsByValue: Array<ProductStatistic> = productService.getTopProductsByVal()
  const issueStats: Array<IssueStat> = issueService.getIssuesSummary()

  const topProductsByQtyCardData = {
    title: "Top products by quantity",
    subtitle: "Total quantity",
    firstColumnHeader: 'Products',
    secondColumnHeader: 'Quantity',
    stat: topProductsByQuantity.reduce((total, current) => total + current.totalQuantity, 0),
    data: mapProductsByQuantityToBarList(topProductsByQuantity)
  }

  const topProductsByValueCardData = {
    title: "Top products by value",
    subtitle: "Total value",
    firstColumnHeader: 'Products',
    secondColumnHeader: 'Value',
    stat: topProductsByValue.reduce((total, current) => total + current.totalValue, 0),
    data: mapProductsByValueToBarList(topProductsByValue)
  }
  const numberOfIssues = issueStats.reduce((total, current) => total + current.quantity, 0)
  return (
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Grid className="gap-6" numColsSm={2} numColsLg={3}>
        <DashboardSummaryCard item={{ title: "Products quantity", metric: productsTotalQuantity }} dataFormatter={dataFormatter} />
        <DashboardSummaryCard item={{ title: "Products value", metric: productsTotalValue }} dataFormatter={dataFormatter} />
        <DashboardSummaryCard item={{ title: "Number of issues", metric: numberOfIssues }} dataFormatter={dataFormatter} />
      </Grid>
      <Grid className="mt-8 gap-6" numColsSm={2} numColsLg={3}>
        <DasboardBarListCard item={topProductsByQtyCardData} dataFormatter={dataFormatter} />
        <DasboardBarListCard item={topProductsByValueCardData} dataFormatter={dataFormatter} />
        <DashboardIssueDonutChart issueStats={issueStats} />
      </Grid>
      {productService.getTopProductsByQty().map(p => (<p>{JSON.stringify(p)}</p>))}
      <br></br>
      {productService.getTopProductsByVal().map(p => (<p>{JSON.stringify(p)}</p>))}
    </main>
  );
}


const mapProductsByQuantityToBarList = (productStatistics: Array<ProductStatistic>): Array<BarListRecord> =>
  productStatistics.map(ps => ({ name: ps.product.name, value: ps.totalQuantity }))

const mapProductsByValueToBarList = (productStatistics: Array<ProductStatistic>): Array<BarListRecord> =>
  productStatistics.map(ps => ({ name: ps.product.name, value: ps.totalValue }))

const mapIssueSummaryToBarListData = (issueStats: Array<IssueStat>): Array<BarListRecord> =>
  issueStats.map(issueStat => ({ name: issueStat.severity, value: issueStat.quantity }))