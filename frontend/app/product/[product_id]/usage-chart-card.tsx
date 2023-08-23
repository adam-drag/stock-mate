'use client';

import { Card, Title, Text, LineChart, TabList, Tab } from "@tremor/react";

import { useState } from "react";
import { startOfYear, subDays } from "date-fns";

const data = [
    {
        Date: "04.05.2021",
        Price: 113.05,
        Volume: 21400410,
    },
    {
        Date: "05.05.2021",
        Price: 113,
        Volume: 29707270,
    },
    {
        Date: "17.11.2022",
        Price: 95.32,
        Volume: 45187420,
    },
];

const dataFormatter = (number: number) =>
    `$ ${Intl.NumberFormat("us").format(number).toString()}`;

export default function UsageChartCard() {
    const [selectedPeriod, setSelectedPeriod] = useState("Max");

    const getDate = (dateString: string) => {
        const [day, month, year] = dateString.split(".").map(Number);
        return new Date(year, month - 1, day);
    };

    const filterData = (startDate: Date, endDate: Date) =>
        data.filter((item) => {
            const currentDate = getDate(item.Date);
            return currentDate >= startDate && currentDate <= endDate;
        });

    // const getFilteredData = (period: string) => {
    //     const lastAvailableDate = getDate(data[data.length - 1].Date);
    //     switch (period) {
    //         case "1M": {
    //             const periodStartDate = subDays(lastAvailableDate, 30);
    //             return filterData(periodStartDate, lastAvailableDate);
    //         }
    //         case "2M": {
    //             const periodStartDate = subDays(lastAvailableDate, 60);
    //             return filterData(periodStartDate, lastAvailableDate);
    //         }
    //         case "6M": {
    //             const periodStartDate = subDays(lastAvailableDate, 180);
    //             return filterData(periodStartDate, lastAvailableDate);
    //         }
    //         case "YTD": {
    //             const periodStartDate = startOfYear(lastAvailableDate);
    //             return filterData(periodStartDate, lastAvailableDate);
    //         }
    //         default:
    //             return data;
    //     }
    // };
    const data2 = [];
    for (let i = 0; i < 12; i++) {
        data2.push({
            week:i+1,
            qty:100+Math.random()*200
        })
        
    }
    return (
        <Card>
            {/* <Title>Share Price</Title>
            <Text>Daily share price of a fictive company</Text> */}
            {/* <TabList
                defaultValue={selectedPeriod}
                onValueChange={(value) => setSelectedPeriod(value)}
                className="text-xs"
            >
                <Tab value="1M" text="1M"  className="tab-label"/>
                <Tab value="2M" text="2M" />
                <Tab value="6M" text="6M" />
                <Tab value="YTD" text="YTD" />
                <Tab value="Max" text="Max" />
            </TabList> */}

            <LineChart
                className="h-40 mt-8"
                data={data2}
                index="week"
                categories={["qty"]}
                colors={["blue"]}
                valueFormatter={dataFormatter}
                showLegend={false}
                yAxisWidth={48}
            />
        </Card>
    );
}