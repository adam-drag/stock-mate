import { Card, Metric, Text, Flex, BadgeDelta } from '@tremor/react';

interface DashboardSummaryCardParams {
    item: any,
    dataFormatter: any
}

export default function DashboardSummaryCard({ item, dataFormatter }: DashboardSummaryCardParams) {
    return (
        <Card key={item.title}>
            <Flex alignItems="start">
                <Text>{item.title}</Text>
                <BadgeDelta
            deltaType="moderateIncrease"
            isIncreasePositive={true}
            size="xs"
        >
            +12.3%
        </BadgeDelta>
            </Flex>
            <Flex
                className="space-x-3 truncate"
                justifyContent="start"
                alignItems="baseline"
            >
                <Metric>{dataFormatter(item.metric)}</Metric>
                {item.subtitle ? <Text className="truncate">{item.subtitle}</Text> : null}
            </Flex>
        </Card>
    )
}