'use client';

import { Card, Title, DonutChart } from "@tremor/react";
import { IssueStat } from "../../models/issue-stat";


export default function DashboardDonatCard({issueStats}:{issueStats:Array<IssueStat>}) {
  return (
    <Card className="max-w-lg">
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <DonutChart
          className="mt-6"
          data={issueStats}
          category='quantity'
          showLabel={true}
          id="severity"
          index="severity"
          variant='donut'
          colors={["red", "orange", "yellow"]}
          label="Issues"
        />
      </div>
    </Card>
  );
}
