import { Card, Metric, Text, Flex, Title, BarList } from '@tremor/react';

interface DashboardBarListCardParams {
    item: any,
    dataFormatter: any
}

export interface BarListRecord {
    name: string;
    value: number;
}

export default function DasboardBarListCard({ item, dataFormatter }: DashboardBarListCardParams) {
    return (<Card key={item.category}>
        <Title>{item.title}</Title>
        
        <Flex
            className="space-x-2"
            justifyContent="start"
            alignItems="baseline"
        >
            <Metric>{dataFormatter(item.stat)}</Metric>
            <Text>{item.subtitle}</Text>
        </Flex>
        <Flex className="mt-6">
            <Text>{item.firstColumnHeader}</Text>
            <Text className="text-right">{item.secondColumnHeader}</Text>
        </Flex>
        <BarList
            className="mt-2"
            data={item.data}
            valueFormatter={dataFormatter}
        />
    </Card>)
}
