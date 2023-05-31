import pandas as pd


df = pd.read_csv("uploads/transactions_1.csv")

outliers = []


def find_outliers_by_status(frame: pd.DataFrame,
                            status: str,
                            threshold: int) -> pd.Series:
    
    transactions_by_status = frame[frame['status'] == status]['count']

    max_deviation = (transactions_by_status.mean()
                    + threshold*transactions_by_status.std())
    
    min_deviation = (transactions_by_status.mean()
                    - threshold*transactions_by_status.std())

    outliers = frame[(frame['count'] < min_deviation)
                   | (frame['count'] > max_deviation)]
    
    outliers_by_status = outliers[outliers['status'] == status]

    return outliers_by_status


def make_alerts(status: str) -> None:
    outliers_found = find_outliers_by_status(df, status, 3)

    for _, column in outliers_found.iterrows():
        time = column["time"]
        count = column['count']

        outlier = {
            'time': time,
            'status': status,
            'count': count,
        }

        outliers.append(outlier)
        print(f"Alert: {status} transactions are above normal at {time}")


make_alerts('reversed')

def create_report(data: list) -> None:
    with open('data/outliers_report.txt', 'w') as report:
        for anomaly in data:
            time = anomaly['time']
            status = anomaly['status']
            count = anomaly['count']
            report.write(
                f'Anomalies detect at {time}\n'
                f'Status: {status}\n'
                f'Amount of transactions per minute: {count}\n'
                f'\n'
            )

create_report(outliers)
